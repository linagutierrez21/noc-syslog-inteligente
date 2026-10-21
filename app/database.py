import sqlite3

def get_db_connection():
    conn = sqlite3.connect("noc_syslog_v2.db") # <-- Cambiamos el nombre aquí
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    
    # Tabla de Dispositivos
    conn.execute('''
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
    ''')
    
    # Tabla de Eventos Syslog
    conn.execute('''
        CREATE TABLE IF NOT EXISTS syslog_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            device_ip TEXT NOT NULL,
            facility INTEGER NOT NULL,
            severity INTEGER NOT NULL,
            message TEXT NOT NULL,
            simulated INTEGER DEFAULT 1
        )
    ''')
    
    # Tabla de Incidentes (con soporte para notas de diagnóstico/solución)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            severity INTEGER NOT NULL,
            status TEXT DEFAULT 'Registrado',
            notes TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()