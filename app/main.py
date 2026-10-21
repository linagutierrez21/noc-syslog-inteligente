from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from app.database import get_db_connection, init_db

app = FastAPI(title="NOC Syslog Inteligente", version="0.2.0")

templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    conn = get_db_connection()
    devices = conn.execute("SELECT * FROM devices").fetchall()
    events = conn.execute("SELECT * FROM syslog_events ORDER BY id DESC LIMIT 10").fetchall()
    # Traemos solo los incidentes que NO estén resueltos para mantener dinámico el dashboard
    incidents = conn.execute("SELECT * FROM incidents WHERE status != 'Resuelto'").fetchall()
    conn.close()
    
    return templates.TemplateResponse(
        request, 
        "index.html", 
        {
            "devices": devices,
            "events": events,
            "incidents": incidents
        }
    )

@app.post("/devices/add")
def add_device(name: str = Form(...), ip: str = Form(...), brand: str = Form(...), 
               model: str = Form(...), version: str = Form(...), location: str = Form(...), status: str = Form(...)):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO devices (name, ip, brand, model, version, location, status, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (name, ip, brand, model, version, location, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)

@app.post("/syslog/simulate")
def simulate_syslog(device_ip: str = Form(...), facility: int = Form(...), severity: int = Form(...), message: str = Form(...)):
    conn = get_db_connection()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn.execute(
        "INSERT INTO syslog_events (timestamp, device_ip, facility, severity, message, simulated) VALUES (?, ?, ?, ?, ?, 1)",
        (timestamp, device_ip, facility, severity, message)
    )
    
    # Si la severidad es crítica (0, 1 o 2), crea un incidente con estado inicial "Registrado"
    if severity in [0, 1, 2]:
        conn.execute(
            "INSERT INTO incidents (title, description, severity, status, notes, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (
                f"Alerta Crítica en IP {device_ip}",
                message,
                severity,
                "Registrado",
                "Sin documentación inicial.",
                timestamp
            )
        )
        
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)

@app.post("/incidents/update/{incident_id}")
def update_incident(incident_id: int, status: str = Form(...), notes: str = Form(...)):
    conn = get_db_connection()
    conn.execute(
        "UPDATE incidents SET status = ?, notes = ? WHERE id = ?",
        (status, notes, incident_id)
    )
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)

@app.post("/console/run", response_class=HTMLResponse)
def run_console_command(request: Request, command: str = Form(...)):
    allowed_commands = ["show version", "show interfaces", "show ip route", "show log"]
    blocked_patterns = ["configure terminal", "write erase", "rm -rf", "shutdown", "delete"]
    
    result = ""
    status_cmd = "PERMITIDO"
    
    if any(blocked in command.lower() for blocked in blocked_patterns):
        status_cmd = "BLOQUEADO"
        result = f"ACCESO DENEGADO: El comando '{command}' está prohibido por la política de seguridad y defensa ante agentes IA."
    elif command.lower() in allowed_commands:
        result = f"Ejecución exitosa para el comando de solo lectura: '{command}'. (Simulado OK)"
    else:
        status_cmd = "DESCONOCIDO"
        result = f"Comando no reconocido en la lista de solo lectura: '{command}'."
        
    conn = get_db_connection()
    devices = conn.execute("SELECT * FROM devices").fetchall()
    events = conn.execute("SELECT * FROM syslog_events ORDER BY id DESC LIMIT 10").fetchall()
    incidents = conn.execute("SELECT * FROM incidents WHERE status != 'Resuelto'").fetchall()
    conn.close()

    return templates.TemplateResponse(
        request, 
        "index.html", 
        {
            "devices": devices,
            "events": events,
            "incidents": incidents,
            "console_result": result,
            "console_status": status_cmd,
            "last_command": command
        }
    )