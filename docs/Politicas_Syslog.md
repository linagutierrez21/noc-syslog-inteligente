# 📜 Políticas de Clasificación Syslog, Escalamiento y Control de Acceso SSH
**Proyecto:** NOC Syslog Inteligente (`v1.0.0`)  
**Alcance:** Infraestructura de Red, Operaciones NOC y Ciberseguridad

---

## 1. Clasificación de Severidades Syslog (Estándar RFC 5424)
Todo evento recibido en el servidor NOC se clasifica según su impacto operativo y determina la acción automatizada correspondiente:

| Nivel | Nombre RFC | Descripción Operativa | Acción Automatizada del Sistema | Tiempo de Respuesta (SLA) |
| :--- | :--- | :--- | :--- | :--- |
| **0** | **Emergency** | Sistema inutilizable / Caída total de core. | Crea Incidente Crítico + **Alerta SMTP Gmail Inmediata** | < 5 minutos |
| **1** | **Alert** | Acción inmediata requerida (ej. caída de sesión BGP). | Crea Incidente Crítico + **Alerta SMTP Gmail Inmediata** | < 10 minutos |
| **2** | **Critical** | Condiciones críticas de hardware o enlace troncal. | Crea Incidente Crítico + **Alerta SMTP Gmail Inmediata** | < 15 minutos |
| **3** | **Error** | Errores no críticos que requieren revisión. | Registro en base de datos (`syslog_events`). | < 1 hora |
| **4** | **Warning** | Advertencias de umbral o degradación leve. | Registro en base de datos (`syslog_events`). | < 4 horas |
| **5** | **Notice** | Condiciones normales pero significativas. | Registro histórico para auditoría. | Rutinario |
| **6** | **Informational** | Mensajes informativos operativos. | Registro histórico para auditoría. | Rutinario |
| **7** | **Debug** | Mensajes de depuración técnica. | Registro en laboratorio / pruebas. | Bajo demanda |

---

## 2. Política de Escalamiento y Notificación Automatizada
* **Disparador Crítico:** Cualquier mensaje Syslog con `severity <= 2` dispara de forma automática la creación de un ticket en estado `Registrado` dentro del módulo de Gestión de Incidentes.
* **Notificación Out-of-Band:** El módulo `app/mailer.py` establece una conexión cifrada TLS (`STARTTLS` puerto `587`) contra `smtp.gmail.com` utilizando credenciales aisladas en `.env` para alertar al ingeniero de turno.
* **Cierre del Ciclo de Vida:** Ningún incidente crítico desaparece del panel principal hasta que un operador documente la causa raíz en el campo de notas y cambie su estado a `Resuelto`.

---

## 3. Matriz de Control de Acceso Basado en Roles (RBAC) - Gestor SSH
Para prevenir modificaciones accidentales o ejecución de comandos destructivos (tanto por error humano como por agentes automatizados), el módulo `app/ssh_manager.py` aplica las siguientes reglas estrictas:

* **Rol `Operador` (Solo Lectura):**
  * **Permitido (`APROBADO`):** Comandos de diagnóstico y consulta (`show version`, `show interfaces`, `show ip route`, `show log`).
  * **Restringido (`RECHAZADO`):** Cualquier intento de entrar a modo configuración (`configure terminal`, `interface`, `ip address`, `no shutdown`) es denegado automáticamente y registrado en la bitácora.
* **Rol `Administrador` (Privilegios Altos):**
  * **Control Humano (`PENDIENTE`):** Los cambios de configuración quedan registrados bajo supervisión para validación humana antes de aplicarse en producción.
* **Comandos Prohibidos Globalmente (`BLOQUEADO`):**
  * Patrones destructivos como `write erase`, `rm -rf`, `shutdown now`, `format` o `reload` son bloqueados sin excepción para todos los roles.

---

## 4. Trazabilidad y Auditoría
Cada interacción en el Gestor SSH queda almacenada de forma inmutable en la tabla `ssh_audit_logs` con marca de tiempo (`timestamp`), usuario, rol, IP destino, comando enviado, estado resultante y mensaje del sistema.