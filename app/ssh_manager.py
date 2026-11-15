from datetime import datetime
from app.database import get_db_connection

def registrar_auditoria(username: str, host_ip: str, command: str, status: str, output: str):
    """Registra cada intento de comando SSH en la bitácora de auditoría de la BD."""
    conn = get_db_connection()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "INSERT INTO ssh_audit_logs (username, host_ip, command, status, output, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (username, host_ip, command, status, output, timestamp)
    )
    conn.commit()
    conn.close()

def procesar_comando_ssh(username: str, role: str, host_ip: str, command: str):
    """
    Evalúa el comando según el rol del usuario y las políticas de seguridad:
    - Bloquea comandos destructivos.
    - Exige aprobación o restringe comandos de configuración según el rol.
    - Permite comandos de solo lectura de forma directa.
    """
    command_lower = command.lower().strip()
    
    # Patrones prohibidos por seguridad y defensa ante agentes IA
    blocked_patterns = ["write erase", "rm -rf", "shutdown now", "format", "reload"]
    # Comandos sensibles (cambios de configuración)
    sensitive_patterns = ["configure terminal", "interface", "ip address", "no shutdown", "snmp-server"]

    if any(p in command_lower for p in blocked_patterns):
        status = "BLOQUEADO"
        output = f"ACCESO DENEGADO: El comando '{command}' viola la política estricta de seguridad del NOC."
    elif any(p in command_lower for p in sensitive_patterns):
        if role != "Administrador":
            status = "RECHAZADO"
            output = f"ACCESO DENEGADO: El usuario '{username}' (Rol: {role}) no tiene privilegios de Administrador para ejecutar cambios."
        else:
            status = "PENDIENTE"
            output = f"Comando de cambio registrado. En espera de aprobación humana por un supervisor."
    else:
        # Comandos seguros de solo lectura permitidos
        status = "APROBADO"
        output = f"Ejecución SSH exitosa en el host {host_ip}: Salida simulada para '{command}' [OK]."

    # Guardar en la bitácora de auditoría
    registrar_auditoria(username, host_ip, command, status, output)
    return {"status": status, "output": output}