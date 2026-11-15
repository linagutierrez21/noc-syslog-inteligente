from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from app.database import get_db_connection, init_db
from app.mailer import enviar_alerta_correo
from app.ssh_manager import procesar_comando_ssh

app = FastAPI(title="NOC Syslog Inteligente", version="1.0.0")

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
    
    # Traemos los últimos registros de auditoría SSH (Fase 2 - Corte 3)
    audit_logs = conn.execute("SELECT * FROM ssh_audit_logs ORDER BY id DESC LIMIT 10").fetchall()
    
    conn.close()
    
    return templates.TemplateResponse(
        request, 
        "index.html", 
        {
            "devices": devices,
            "events": events,
            "incidents": incidents,
            "audit_logs": audit_logs
        }
    )

@app.post("/devices/add")
def add_device(
    name: str = Form(...), 
    ip: str = Form(...), 
    brand: str = Form(...), 
    model: str = Form(...), 
    version: str = Form(...), 
    location: str = Form(...), 
    status: str = Form(...)
):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO devices (name, ip, brand, model, version, location, status, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (name, ip, brand, model, version, location, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)

@app.post("/syslog/simulate")
def simulate_syslog(
    device_ip: str = Form(...), 
    facility: int = Form(...), 
    severity: int = Form(...), 
    message: str = Form(...)
):
    conn = get_db_connection()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn.execute(
        "INSERT INTO syslog_events (timestamp, device_ip, facility, severity, message, simulated) VALUES (?, ?, ?, ?, ?, 1)",
        (timestamp, device_ip, facility, severity, message)
    )
    
    # Si la severidad es crítica (0, 1 o 2), crea un incidente y dispara la alerta por correo (Gmail)
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
        
        # Envío de alerta crítica por correo electrónico (Gmail SMTP)
        asunto_correo = f"🚨 ALERTA NOC CRÍTICA: Severidad Nivel {severity}"
        cuerpo_correo = (
            f"Se ha detectado un evento crítico en la infraestructura de red.\n\n"
            f"• Dispositivo IP: {device_ip}\n"
            f"• Nivel de Severidad: {severity}\n"
            f"• Mensaje Syslog: {message}\n"
            f"• Fecha/Hora: {timestamp}\n"
            f"• Estado: Registrado en el sistema NOC (v1.0.0)\n\n"
            f"Por favor ingrese al dashboard del NOC para gestionar y resolver el caso."
        )
        enviar_alerta_correo(asunto_correo, cuerpo_correo)
        
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
    audit_logs = conn.execute("SELECT * FROM ssh_audit_logs ORDER BY id DESC LIMIT 10").fetchall()
    conn.close()

    return templates.TemplateResponse(
        request, 
        "index.html", 
        {
            "devices": devices,
            "events": events,
            "incidents": incidents,
            "audit_logs": audit_logs,
            "console_result": result,
            "console_status": status_cmd,
            "last_command": command
        }
    )

@app.post("/ssh/execute")
def execute_ssh_command(
    username: str = Form(...),
    role: str = Form(...),
    host_ip: str = Form(...),
    command: str = Form(...)
):
    """Ejecuta o evalúa un comando SSH simulado con control de roles y auditoría (Fase 2)."""
    procesar_comando_ssh(username, role, host_ip, command)
    return RedirectResponse(url="/", status_code=303)