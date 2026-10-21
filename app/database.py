import sqlite3
from datetime import datetime

DB_NAME = "noc_syslog.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabla de Inventario de Dispositivos (Requisito Corte 2)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ip TEXT NOT NULL,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            version TEXT NOT NULL,
            location TEXT NOT NULL,
            status TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    
    # Tabla de Mensajes Syslog (Clasificación de 0 a 7)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS syslog_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            device_ip TEXT NOT NULL,
            facility INTEGER NOT NULL,
            severity INTEGER NOT NULL,
            message TEXT NOT NULL,
            simulated BOOLEAN DEFAULT 1
        )
    """)
    
    # Tabla de Incidentes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            severity INTEGER NOT NULL,
            status TEXT NOT NULL,
            assigned_to TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada correctamente.")