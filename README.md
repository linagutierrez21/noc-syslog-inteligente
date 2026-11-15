# 🛡️ NOC Syslog Inteligente (v1.0.0)

Sistema integral de gestión de redes, ciberseguridad, monitoreo de eventos Syslog, alertas automatizadas vía SMTP (Gmail) y control de acceso SSH con bitácora de auditoría.

---

## 🚀 Características Principales (Corte 3)
* **Monitoreo y Simulación Syslog (RFC 5424):** Recepción y registro de eventos de red con clasificación por severidades (0 a 7).
* **Alertas Críticas Automatizadas (SMTP Gmail):** Envío automático de correos electrónicos a administradores ante eventos críticos (Severidad 0, 1 y 2) utilizando autenticación segura por Contraseña de Aplicación.
* **Inventario Editable de Dispositivos:** Gestión completa de equipos de red (routers, switches, firewalls) con atributos de marca, modelo, IP y estado en tiempo real.
* **Gestor SSH Backend con Roles y Auditoría:** 
  * Control de acceso diferenciado por roles (*Operador* de solo lectura vs. *Administrador* con permisos sensibles).
  * Mecanismo de evaluación de comandos y bitácora de auditoría almacenada en base de datos SQLite (`ssh_audit_logs`).
* **Ciberseguridad y Buenas Prácticas:** Protección de secretos y credenciales mediante variables de entorno (`.env`) excluidas estrictamente en `.gitignore`.

---

## 🛠️ Tecnologías Utilizadas
* **Backend:** Python 3.10+, FastAPI, Uvicorn.
* **Base de Datos:** SQLite3 con consultas optimizadas y control de esquemas relacionales.
* **Frontend:** Jinja2 Templates, Bootstrap 5, Bootstrap Icons.
* **Alertas:** Protocolo SMTP seguro (`smtplib`, `email.message`, `python-dotenv`).

---

## 📦 Instalación y Configuración Local

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/noc-syslog-inteligente.git](https://github.com/tu-usuario/noc-syslog-inteligente.git)
   cd noc-syslog-inteligente