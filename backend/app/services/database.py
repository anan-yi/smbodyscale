import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "measurements.db")

# 确保数据目录存在
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            weight REAL NOT NULL,
            body_fat_percent REAL,
            muscle_percent REAL,
            water_percent REAL,
            bone_mass REAL,
            bmr INTEGER,
            age INTEGER,
            gender TEXT,
            height REAL,
            bmi REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ 数据库初始化完成")


def save_measurement(
    weight: float,
    body_fat_percent: Optional[float] = None,
    muscle_percent: Optional[float] = None,
    water_percent: Optional[float] = None,
    bone_mass: Optional[float] = None,
    bmr: Optional[int] = None,
    age: Optional[int] = None,
    gender: Optional[str] = None,
    height: Optional[float] = None,
    bmi: Optional[float] = None
) -> int:
    """保存测量记录"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO measurements 
        (weight, body_fat_percent, muscle_percent, water_percent, bone_mass, bmr, age, gender, height, bmi)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        weight, body_fat_percent, muscle_percent, water_percent,
        bone_mass, bmr, age, gender, height, bmi
    ))
    
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"💾 记录已保存，ID: {record_id}")
    return record_id


def get_all_measurements(limit: int = 100) -> List[Dict]:
    """获取所有历史记录"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM measurements 
        ORDER BY created_at DESC 
        LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_latest_measurement() -> Optional[Dict]:
    """获取最新一条记录"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM measurements 
        ORDER BY created_at DESC 
        LIMIT 1
    """)
    
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None


def get_measurement_by_id(measurement_id: int) -> Optional[Dict]:
    """根据ID获取记录"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM measurements WHERE id = ?", (measurement_id,))
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None