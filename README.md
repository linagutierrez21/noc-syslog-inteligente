# NOC Syslog Inteligente - Proyecto Corte 2

¡Hola! Este es el repositorio para mi proyecto de la materia **Administración y Gestión de Redes**. Aquí implementé un prototipo (MVP v0.2.0) de un Centro de Operaciones de Red (NOC) enfocado en la gestión de dispositivos, recepción de mensajes Syslog y una consola simulada.

---

## 🚀 ¿Qué hace este proyecto?

En este segundo corte desarrollé las siguientes funcionalidades:

1. **Inventario de Dispositivos:** Permite registrar y listar equipos de red (Routers, Switches, Firewalls) con su nombre, dirección IP, marca, modelo, versión de firmware y ubicación.
2. **Recepción y Simulador Syslog:** Un módulo donde se pueden enviar y almacenar eventos de red clasificados por su nivel de severidad (del 0 al 7, desde emergencia hasta depuración).
3. **Consola de Comandos Simulada:** Una interfaz tipo terminal interactiva para ejecutar comandos de lectura (como `show version` o `show ip route`). Incluye una regla de seguridad que bloquea comandos peligrosos o destructivos (como `configure terminal` o `shutdown`).
4. **Dashboard:** Una vista general con contadores en tiempo real de los dispositivos e incidentes registrados.

---

## 🛠️ Tecnologías que utilicé

* **Backend:** Python 3.15 con FastAPI
* **Servidor Web:** Uvicorn
* **Base de Datos:** SQLite3 (base de datos local en archivo `.db`)
* **Frontend:** HTML, Jinja2 Templates y Bootstrap 5 (con Bootstrap Icons)

---

## 📂 Estructura de carpetas

```text
noc-syslog-inteligente/
├── app/
│   ├── database.py       # Script de conexión e inicialización de las tablas en SQLite
│   ├── main.py           # Código de FastAPI con los endpoints y la lógica
│   └── templates/
│       └── index.html    # Interfaz visual del dashboard y formularios
├── requirements.txt      # Librerías necesarias para correr el proyecto
└── README.md             # Documentación del repositorio