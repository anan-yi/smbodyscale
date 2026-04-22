from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime

from ..models.schemas import MeasurementData, AnalysisRequest, AnalysisResponse
from ..services.stm32_service import stm32_service
from ..services.gemini_service import gemini_service as ai_service
from ..services.calculator import calculate_all_metrics
from ..services.database import init_db, save_measurement, get_all_measurements, get_latest_measurement, get_measurement_by_id

router = APIRouter(prefix="/api", tags=["measurement"])

# 存储最新测量数据
latest_data: Optional[MeasurementData] = None
connected_clients: list[WebSocket] = []


@router.get("/status")
async def get_status():
    """获取系统状态"""
    return {
        "stm32": stm32_service.get_status(),
        "latest_data": latest_data.dict() if latest_data else None
    }


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_health(request: AnalysisRequest):
    """分析健康数据并保存到数据库"""
    
    # 计算指标
    metrics = calculate_all_metrics(
        request.measurement.model_dump(),
        request.user.model_dump()
    )
    
    # 调用AI分析
    ai_result = await ai_service.analyze_health(
        request.measurement.model_dump(),
        request.user.model_dump(),
        metrics
    )
    
    # 保存到数据库
    save_measurement(
        weight=request.measurement.weight,
        body_fat_percent=request.measurement.body_fat_percent,
        muscle_percent=request.measurement.muscle_percent,
        water_percent=request.measurement.water_percent,
        bone_mass=request.measurement.bone_mass,
        bmr=request.measurement.bmr,
        age=request.user.age,
        gender=request.user.gender,
        height=request.user.height,
        bmi=metrics.get("bmi")
    )
    
    return AnalysisResponse(
        metrics=metrics,
        ai_result=ai_result,
        raw_data=request,
        analysis_time=datetime.now().isoformat()
    )


@router.get("/history")
async def get_history(limit: int = 30):
    """获取历史测量记录"""
    records = get_all_measurements(limit)
    return {
        "records": records,
        "count": len(records)
    }


@router.get("/latest")
async def get_latest():
    """获取最新测量记录"""
    record = get_latest_measurement()
    if record:
        return record
    return {"message": "暂无数据"}


@router.get("/measurement/{measurement_id}")
async def get_measurement(measurement_id: int):
    """根据ID获取单条记录"""
    record = get_measurement_by_id(measurement_id)
    if record:
        return record
    raise HTTPException(status_code=404, detail="记录不存在")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 实时数据推送"""
    await websocket.accept()
    connected_clients.append(websocket)
    
    await websocket.send_json({
        "event": "connected",
        "data": {"status": stm32_service.is_connected}
    })
    
    try:
        while True:
            message = await websocket.receive_text()
            data = __import__('json').loads(message)
            action = data.get("action")
            
            if action == "start_measurement":
                if stm32_service.is_connected:
                    stm32_service.start_measurement()
                    await websocket.send_json({
                        "event": "status",
                        "data": {"measuring": True}
                    })
                else:
                    await websocket.send_json({
                        "event": "error",
                        "data": "STM32未连接"
                    })
                    
            elif action == "connect_stm32":
                success = stm32_service.connect()
                await websocket.send_json({
                    "event": "connection_status",
                    "data": {"connected": success}
                })
                
            elif action == "disconnect_stm32":
                stm32_service.disconnect()
                await websocket.send_json({
                    "event": "connection_status",
                    "data": {"connected": False}
                })
                
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
    except Exception as e:
        print(f"WebSocket错误: {e}")
        if websocket in connected_clients:
            connected_clients.remove(websocket)


def broadcast_to_clients(message: dict):
    """广播消息到所有WebSocket客户端"""
    import asyncio
    
    async def send():
        disconnected = []
        for client in connected_clients:
            try:
                await client.send_json(message)
            except:
                disconnected.append(client)
        
        for client in disconnected:
            connected_clients.remove(client)
    
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(send())
    except:
        pass


def on_stm32_data(data: dict):
    """STM32数据接收回调"""
    global latest_data
    
    print(f"📨 STM32数据: {data}")
    
    if data.get("type") == "weight":
        if latest_data is None:
            latest_data = MeasurementData(weight=data["weight"])
        else:
            latest_data.weight = data["weight"]
            
    elif data.get("type") == "body_composition":
        if latest_data is None:
            latest_data = MeasurementData(
                weight=0,
                body_fat_percent=data.get("body_fat_percent"),
                muscle_percent=data.get("muscle_percent"),
                water_percent=data.get("water_percent"),
                bone_mass=data.get("bone_mass"),
                bmr=data.get("bmr")
            )
        else:
            latest_data.body_fat_percent = data.get("body_fat_percent")
            latest_data.muscle_percent = data.get("muscle_percent")
            latest_data.water_percent = data.get("water_percent")
            latest_data.bone_mass = data.get("bone_mass")
            latest_data.bmr = data.get("bmr")
    
    broadcast_to_clients({
        "event": "new_measurement",
        "data": data
    })


def on_connection_change(connected: bool):
    """连接状态变化回调"""
    broadcast_to_clients({
        "event": "connection_status",
        "data": {"connected": connected}
    })


stm32_service.on_data_received = on_stm32_data
stm32_service.on_connection_change = on_connection_change