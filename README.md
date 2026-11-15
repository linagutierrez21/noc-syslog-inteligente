# 🛡️ NOC Syslog Inteligente (`v1.0.0`)

![Version](https://img.shields.io/badge/version-v1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10+-yellow.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?logo=fastapi&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3.svg?logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57.svg?logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/Estado-Corte%203%20Finalizado-success.svg)

Aplicación web para un Centro de Operaciones de Red (NOC): registra eventos Syslog clasificados por severidad, crea incidentes y envía alertas por correo cuando un evento es crítico, y evalúa comandos SSH según el rol del usuario dejando cada intento en una bitácora de auditoría.

* **Institución:** Fundación Universitaria Compensar
* **Asignatura:** Administración y Gestión de Redes
* **Entrega:** Corte 3 — Versión `v1.0.0`
* **Autora:** Lina Valentina Gutierrez Macana
* **Docente:** Ing. John Harold Pérez Calderón
* **Repositorio:** [github.com/linagutierrez21/noc-syslog-inteligente](https://github.com/linagutierrez21/noc-syslog-inteligente)

> **⚠️ Aviso de Entorno Simulado:** Todos los datos, direcciones IP, comandos ejecutados y dispositivos de este proyecto son **simulados**. La aplicación no se conecta ni altera equipos reales de producción.

---

## 📑 Tabla de Contenido
1. [Propósito](#-propósito)
2. [Arquitectura y Flujo](#-arquitectura-y-flujo)
3. [Funciones Principales](#-funciones-principales)
4. [Tecnologías](#-tecnologías)
5. [Estructura del Proyecto](#-estructura-del-proyecto)
6. [Modelo de Datos](#-modelo-de-datos)
7. [Requisitos](#-requisitos)
8. [Instalación y Configuración](#-instalación-y-configuración)
9. [Ejecución y Uso](#-ejecución-y-uso)
10. [Pruebas Funcionales y Evidencias](#-pruebas-funcionales-y-evidencias)
11. [Seguridad y Control de IA](#-seguridad-y-control-de-ia)
12. [Limitaciones Conocidas](#-limitaciones-conocidas)
13. [Control de Versiones](#-control-de-versiones)
14. [Documentación Adicional](#-documentación-adicional)

---

## 🎯 Propósito

En una red empresarial los equipos generan mensajes Syslog todo el tiempo y la mayoría son informativos. El riesgo está en que un evento grave llegue mezclado con cientos de mensajes de rutina y nadie lo vea a tiempo. Un segundo riesgo es que cualquier persona, o un agente de IA, con acceso por SSH ejecute comandos de configuración sin control ni registro.

**NOC Syslog Inteligente** atiende ambos problemas:
* **Clasificación y Escalamiento:** Categoriza los eventos por severidad (estándar RFC 5424) y escala únicamente los críticos (`0`, `1` y `2`).
* **Control SSH y Trazabilidad:** Decide en el servidor si un comando SSH se aprueba, se rechaza, se bloquea o queda pendiente de aprobación humana, registrando cada intento de forma inmutable.

---

## 🏗️ Arquitectura y Flujo

```text
┌────────────────────────────┐      ┌─────────────────────────────────────────┐
│   Simulador / Dashboard    │ ───▶ │          Backend (FastAPI)              │
│   (HTML5 + Bootstrap 5)    │      │                                         │
└────────────────────────────┘      │  1. Clasificador RFC 5424 (main.py)     │
                                    │     ├─ Sev 0-2 ──▶ SMTP Gmail (STARTTLS)│
                                    │     └─ Sev 0-7 ──▶ Registro SQLite3     │
                                    │                                         │
                                    │  2. Validador RBAC (ssh_manager.py)     │
                                    │     └─ Evalúa Rol ──▶ ssh_audit_logs    │
                                    └─────────────────────────────────────────┘
⚙️ Funciones Principales
Función	Descripción
Inventario de dispositivos	Registro de equipos con nombre, IP, marca, modelo, versión, ubicación y estado.
Simulador de eventos Syslog	Registro de eventos con IP de origen, facility (0 a 23), severidad (0 a 7) y mensaje.
Filtro por severidad	La tabla de eventos se puede filtrar dinámicamente por nivel (0 a 7).
Incidentes automáticos	Un evento de severidad 0, 1 o 2 crea un incidente en estado Registrado.
Alerta por correo	El mismo evento crítico envía un correo automático por SMTP (Gmail) con cifrado STARTTLS.
Ciclo de vida de incidentes	Gestión de estados Registrado, En Proceso y Resuelto, con notas de diagnóstico.
Gestor SSH con roles	Evalúa el comando según el rol (Operador o Administrador) y devuelve una salida simulada.
Bitácora de auditoría	Cada intento del gestor SSH se guarda en la tabla ssh_audit_logs.
Consola de solo lectura	Acepta únicamente comandos de consulta y bloquea los de configuración.
Severidades RFC 5424 y Acción del Sistema
Nivel	Nombre	Acción Automatizada
0	Emergency	Crea incidente + Alerta por correo
1	Alert	Crea incidente + Alerta por correo
2	Critical	Crea incidente + Alerta por correo
3	Error	Registro en base de datos
4	Warning	Registro en base de datos
5	Notice	Registro en base de datos
6	Informational	Registro en base de datos
7	Debug	Registro en base de datos
Resultados Posibles en el Gestor SSH
Estado	Cuándo aplica
BLOQUEADO	Comandos destructivos (write erase, rm -rf, shutdown now, format, reload), para cualquier rol.
RECHAZADO	Comandos de configuración (configure terminal, interface, ip address, no shutdown, snmp-server) enviados por un Operador.
PENDIENTE	Los mismos comandos de configuración enviados por un Administrador; quedan a la espera de aprobación humana.
APROBADO	Cualquier otro comando; se trata como consulta de diagnóstico.
💻 Tecnologías
Backend: Python 3.10 o superior, FastAPI, Uvicorn.

Base de datos: SQLite3 (noc_syslog_v2.db).

Interfaz: Plantillas Jinja2, Bootstrap 5 y Bootstrap Icons.

Correo: smtplib y email.message (biblioteca estándar) con python-dotenv para el aislamiento de credenciales.

📂 Estructura del Proyecto
Plaintext
noc-syslog-inteligente/
├── app/
│   ├── main.py            # Rutas y controladores principales de la aplicación
│   ├── database.py        # Conexión y creación de tablas en SQLite3
│   ├── mailer.py          # Envío de alertas críticas por correo SMTP
│   ├── ssh_manager.py     # Evaluación de comandos por rol y auditoría
│   └── templates/
│       └── index.html     # Dashboard principal
├── docs/
│   ├── evidencias/        # Capturas de validación funcional
│   ├── Manual_Operacion.md
│   └── Politicas_Syslog.md
├── .gitignore             # Exclusión de entorno virtual, base de datos y .env
├── README.md
└── requirements.txt
Nota: El archivo .env no hace parte del repositorio; se crea localmente en cada equipo.

🗄️ Modelo de Datos
Tabla	Campos
devices	id, name, ip, brand, model, version, location, status, updated_at
syslog_events	id, timestamp, device_ip, facility, severity, message, simulated
incidents	id, title, description, severity, status, notes, created_at
ssh_audit_logs	id, username, host_ip, command, status, output, timestamp
📋 Requisitos
Sistema operativo Windows 10/11, Linux o macOS.

Python 3.10 o superior y Git instalados.

Salida a internet por el puerto TCP 587 (para el envío de correos SMTP).

Cuenta de Gmail con verificación en dos pasos activa y una contraseña de aplicación.

🚀 Instalación y Configuración
1. Clonar el repositorio y crear entorno virtual
Bash
git clone [https://github.com/linagutierrez21/noc-syslog-inteligente.git](https://github.com/linagutierrez21/noc-syslog-inteligente.git)
cd noc-syslog-inteligente

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\activate

# Linux o macOS
python3 -m venv venv
source venv/bin/activate
2. Instalar dependencias
Bash
pip install -r requirements.txt
pip install python-multipart
(Nota: python-multipart es necesario para que FastAPI procese los formularios HTML; si ya está en requirements.txt, el segundo comando no es necesario).

3. Configurar variables de entorno (.env)
Crea un archivo llamado .env en la raíz del proyecto con las siguientes variables:

Fragmento de código
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=tu_correo@gmail.com
SENDER_PASSWORD=tu_contraseña_de_aplicacion
ALERT_RECIPIENT=correo_que_recibe_las_alertas@gmail.com
Variable	Uso
SMTP_SERVER	Servidor SMTP (por defecto smtp.gmail.com).
SMTP_PORT	Puerto SMTP (por defecto 587).
SENDER_EMAIL	Cuenta de Gmail que envía la alerta.
SENDER_PASSWORD	Contraseña de aplicación generada en Google (no la contraseña normal).
ALERT_RECIPIENT	Destinatario de la alerta. Si se omite, se usa SENDER_EMAIL.
Si las credenciales no están configuradas, la aplicación sigue funcionando: registra el evento y el incidente en la base de datos, y muestra un aviso en la terminal indicando que no se envió el correo.

▶️ Ejecución y Uso
Con el entorno virtual activo, inicia el servidor desde la raíz del proyecto:

Bash
python -m uvicorn app.main:app --reload
Abre tu navegador en: http://127.0.0.1:8000 (Para detener el servidor, presiona Ctrl + C en la terminal).

Flujo de Operación en el Dashboard
Inventario: En "Registrar Nuevo Dispositivo", completa los campos y pulsa Guardar Dispositivo.

Simular un evento: En "Simulador y Recepción de Mensajes Syslog", ingresa IP, facility, severidad y mensaje, y pulsa Simular.

Filtrar eventos: En "Filtrar por severidad", elige un nivel (0 a 7) y pulsa Filtrar.

Gestionar incidentes: En "Gestión de Incidentes Críticos Activos", actualiza el estado (Registrado, En Proceso, Resuelto), redacta una nota y pulsa Guardar y Actualizar. Los incidentes en estado Resuelto desaparecen del panel activo.

Evaluar comandos SSH: En "Gestor SSH", indica usuario, rol, IP del host y comando para registrar su evaluación en la bitácora.

Consola de solo lectura: Acepta comandos de diagnóstico (show version, show interfaces, show ip route, show log).

🧪 Pruebas Funcionales y Evidencias
#	Prueba	Procedimiento	Resultado Esperado
1	Alerta por correo	Simular evento con IP 192.168.1.100, facility 16, severidad 1 y mensaje %SYS-1-CRITICAL: BGP peer down on interface TenGigE0/0/0/1.	Crea un incidente en estado Registrado y envía el correo de alerta.
2	Control por roles	En el gestor SSH, enviar configure terminal con rol Operador.	La bitácora registra el intento con estado RECHAZADO.
3	Filtro por severidad	Con eventos de distintos niveles registrados, filtrar por Nivel 1.	La tabla muestra únicamente los eventos de nivel 1.
4	Consola solo lectura	Enviar show ip route y posteriormente shutdown.	El primero queda PERMITIDO y el segundo BLOQUEADO.
Evidencias Capturadas (v1.0.0)
Notificación SMTP recibida ante evento crítico: docs/evidencias/Notificación Correo.png

Auditoría SSH bloqueando comando privilegiado: docs/evidencias/Gestion SSH.png

🔒 Seguridad y Control de IA
Credenciales fuera del repositorio: El archivo .env está excluido en .gitignore. No se publican contraseñas, tokens ni claves.

Protocolo ante exposición accidental: Si una credencial llega a publicarse por error en un commit, se revoca inmediatamente desde la cuenta de Google y se genera una nueva, purgándola del control de versiones.

Control de acceso por roles: La decisión sobre cada comando se ejecuta estrictamente en el servidor (ssh_manager.py), nunca en el cliente.

Aprobación humana: Ningún cambio de configuración se aplica automáticamente; incluso con rol Administrador queda marcado como PENDIENTE.

Auditoría inmutable: Cada intento en el gestor SSH queda registrado con usuario, host, comando, estado, salida y marca de tiempo.

Logs como texto plano: El mensaje Syslog se almacena y renderiza como texto; ninguna parte del código lo evalúa ni ejecuta.

Correo cifrado: La comunicación SMTP negocia cifrado STARTTLS antes de autenticarse.

⚠️ Limitaciones Conocidas
Los eventos se generan desde el formulario de simulación; no existe un listener UDP en el puerto 514 para recibir tramas de hardware real.

El gestor SSH devuelve salidas simuladas y no abre sesiones reales contra equipos de red.

No hay módulo de autenticación con inicio de sesión; el usuario y el rol se seleccionan en el formulario.

El gestor SSH opera mediante listas de bloqueo; cualquier comando fuera de dichas listas se aprueba como consulta.

El estado PENDIENTE se registra en bitácora, pero falta una vista dedicada para que un supervisor apruebe o rechace manualmente.

Las notificaciones se envían únicamente por correo electrónico (no incluye integración con Telegram).

El filtrado de eventos funciona exclusivamente por severidad (no filtra por rango de fechas, marca ni equipo).

Las configuraciones Syslog para Cisco, Fortinet y Huawei están documentadas en los manuales, sin verificación en emuladores (como GNS3/EVE-NG) ni hardware físico.

🌿 Control de Versiones
main: Rama estable con el código validado.

develop: Rama de desarrollo e integración de nuevas características.

Release oficial: Etiquetado como v1.0.0 para la entrega del Corte 3.

Corte	Alcance y Entregables
Corte 2	Backend en FastAPI, base de datos SQLite, dashboard, inventario, simulador de eventos y ciclo de vida de incidentes.
Corte 3 (v1.0.0)	Alerta por correo SMTP, gestor SSH con roles y auditoría, filtro por severidad, documentación normativa y blindaje de .gitignore.
📖 Documentación Adicional
docs/Politicas_Syslog.md: Clasificación de severidades RFC 5424, escalamiento y matriz de control de acceso SSH.

docs/Manual_Operacion.md: Guía detallada de instalación, operación diaria y validación funcional.

Proyecto académico desarrollado para la asignatura Administración y Gestión de Redes — Fundación Universitaria Compensar (2026).


### Para actualizarlo en tu GitHub:
1. Pega este contenido en tu `README.md` y guarda (`Ctrl + S`).
2. En tu terminal ejecuta:
   ```bash
   git add README.md
   git commit -m "Docs: Mejorar formato y estructura completa del README.md v1.0.0"
   git push origin main
