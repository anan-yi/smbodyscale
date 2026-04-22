import serial
import serial.tools.list_ports
import threading
import time
from typing import Callable, Optional
import struct


class STM32Service:
    """STM32 串口通信服务"""
    
    # 通信协议帧格式
    FRAME_HEAD = 0xAA
    FRAME_TAIL = 0x55
    
    def __init__(self, port: str = "COM3", baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
        self.serial: Optional[serial.Serial] = None
        self.is_connected = False
        self.is_running = False
        
        # 数据回调
        self.on_data_received: Optional[Callable[[dict], None]] = None
        self.on_connection_change: Optional[Callable[[bool], None]] = None
        
        # 接收线程
        self._thread: Optional[threading.Thread] = None
        self._buffer = bytearray()
        
    def list_available_ports(self) -> list[dict]:
        """列出可用串口"""
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append({
                "device": port.device,
                "description": port.description,
                "hwid": port.hwid
            })
        return ports
    
    def connect(self) -> bool:
        """连接STM32"""
        try:
            print(f"🔌 尝试连接串口 {self.port} @ {self.baudrate}bps...")
            
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
            
            self.is_connected = True
            self.is_running = True
            
            # 启动接收线程
            self._thread = threading.Thread(target=self._read_loop, daemon=True)
            self._thread.start()
            
            print(f"✅ 串口连接成功: {self.port}")
            
            if self.on_connection_change:
                self.on_connection_change(True)
                
            return True
            
        except serial.SerialException as e:
            print(f"❌ 串口连接失败: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self):
        """断开连接"""
        self.is_running = False
        self.is_connected = False
        
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1)
        
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("🔌 串口已断开")
        
        if self.on_connection_change:
            self.on_connection_change(False)
    
    def _read_loop(self):
        """后台读取线程"""
        while self.is_running:
            if not self.serial or not self.serial.is_open:
                time.sleep(0.1)
                continue
            
            try:
                # 读取可用数据
                if self.serial.in_waiting > 0:
                    data = self.serial.read(self.serial.in_waiting)
                    self._buffer.extend(data)
                    self._parse_buffer()
                else:
                    time.sleep(0.01)  # 10ms轮询
                    
            except serial.SerialException as e:
                print(f"❌ 串口读取错误: {e}")
                self.is_connected = False
                if self.on_connection_change:
                    self.on_connection_change(False)
                break
    
    def _parse_buffer(self):
        """解析数据缓冲区"""
        while len(self._buffer) >= 6:  # 最小帧长度
            # 查找帧头
            try:
                head_idx = self._buffer.index(self.FRAME_HEAD)
            except ValueError:
                self._buffer.clear()  # 没有帧头，清空
                return
            
            # 检查是否有足够长度
            if len(self._buffer) < head_idx + 6:
                return
            
            # 查找帧尾
            tail_found = False
            for i in range(head_idx + 2, min(head_idx + 20, len(self._buffer))):
                if self._buffer[i] == self.FRAME_TAIL:
                    frame = self._buffer[head_idx:i+1]
                    self._buffer = self._buffer[i+1:]
                    self._process_frame(frame)
                    tail_found = True
                    break
            
            if not tail_found:
                # 丢弃错误帧头
                self._buffer = self._buffer[head_idx+1:]
    
    def _process_frame(self, frame: bytearray):
        """处理完整数据帧"""
        if len(frame) < 6:
            return
        
        cmd = frame[2]
        data_bytes = frame[3:-2]  # 去掉头、命令、尾
        
        result = {}
        
        if cmd == 0x01:  # 体重数据
            if len(data_bytes) >= 2:
                weight_raw = struct.unpack('>H', bytes(data_bytes[0:2]))[0]
                result = {
                    "type": "weight",
                    "weight": weight_raw / 10.0,  # 0.1kg精度
                    "timestamp": time.time()
                }
                
        elif cmd == 0x02:  # 体脂数据
            if len(data_bytes) >= 6:
                result = {
                    "type": "body_composition",
                    "body_fat_percent": data_bytes[0] / 10.0,
                    "muscle_percent": data_bytes[1] / 10.0,
                    "water_percent": data_bytes[2] / 10.0,
                    "bone_mass": data_bytes[3] / 100.0,
                    "bmr": struct.unpack('>H', bytes(data_bytes[4:6]))[0],
                    "timestamp": time.time()
                }
        
        if result and self.on_data_received:
            print(f"📨 收到数据: {result}")
            self.on_data_received(result)
    
    def send_command(self, cmd: int):
        """发送命令到STM32"""
        if not self.is_connected or not self.serial:
            print("⚠️ 串口未连接")
            return False
        
        # 构建命令帧: [HEAD] [LEN=1] [CMD] [CHECKSUM] [TAIL]
        frame = bytes([self.FRAME_HEAD, 0x01, cmd, cmd, self.FRAME_TAIL])
        
        try:
            self.serial.write(frame)
            print(f"📤 发送命令: 0x{cmd:02X}")
            return True
        except serial.SerialException as e:
            print(f"❌ 发送失败: {e}")
            return False
    
    def start_measurement(self):
        """开始测量"""
        return self.send_command(0x10)
    
    def get_status(self) -> dict:
        """获取连接状态"""
        return {
            "connected": self.is_connected,
            "port": self.port,
            "baudrate": self.baudrate,
            "buffer_size": len(self._buffer)
        }


# 单例实例
stm32_service = STM32Service()