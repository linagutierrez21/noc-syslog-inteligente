# 🛡️ NOC Syslog Inteligente (MVP v0.2.0)

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-0.158.1-005571?style=for-the-badge&logo=fastapi">
  <img src="https://img.shields.io/badge/Python-3.15-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white">
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white">
  <img src="https://img.shields.io/badge/Status-MVP%20Completado-success?style=for-the-badge">
</p>

> **Asignatura:** Administración y Gestión de Redes  
> **Evaluación:** MVP - Corte 2 (Versión 0.2.0)  
> **Descripción:** Centro de Operaciones de Red (NOC) inteligente para la gestión de infraestructura, recepción/simulación de eventos Syslog (severidades 0–7) y consola de comandos segura con políticas de defensa ante agentes de IA.

---

## 📑 Tabla de Contenidos
1. [Arquitectura del Sistema](#-arquitectura-del-sistema)
2. [Características Principales (Corte 2)](#-características-principales-corte-2)
3. [Estructura del Proyecto](#-estructura-del-proyecto)
4. [Guía de Instalación y Despliegue](#-guía-de-instalación-y-despliegue)
5. [Endpoints y Funcionalidades](#-endpoints-y-funcionalidades)
6. [Políticas de Seguridad y Consola](#-políticas-de-seguridad-y-consola)

---

## 🏛️ Arquitectura del Sistema
El proyecto está desarrollado bajo un patrón arquitectónico moderno desacoplado por capas:
* **Capa Backend:** FastAPI (Python), manejando peticiones asíncronas, enrutamiento web y lógica de validación.
* **Capa de Datos:** SQLite con conexión optimizada mediante `sqlite3` y gestión relacional de tablas para dispositivos, eventos e incidentes.
* **Capa Frontend:** Jinja2 Templates combinados con **Bootstrap 5** y componentes interactivos responsivos adaptados al estándar de un NOC corporativo.

---

## 🚀 Características Principales (Corte 2)

* **Inventario Editable de Dispositivos:** Permite registrar, listar y consultar equipos de red (nombre, IP, marca, modelo, versión de firmware y ubicación física).
* **Simulador y Receptor Syslog (Severidades 0–7):** Módulo dinámico para simular y clasificar eventos de red en tiempo real según los niveles estándar de Syslog (desde Emergencia `0` hasta Debug `7`).
* **Consola de Red Simulada:** Interfaz estilo terminal oscura con control estricto de comandos de solo lectura y bloqueo automático de acciones destructivas o inyecciones de agentes de IA no autorizados.

---

## 📂 Estructura del Proyecto

```text
noc-syslog-inteligente/
│
├── app/
│   ├── __init__.py
│   ├── database.py         # Conexión y esquemas SQLite
│   ├── main.py             # Servidor FastAPI y Endpoints
│   └── templates/
│       └── index.html      # Dashboard visual y consola interactiva
│
├── venv/                   # Entorno virtual de Python
├── noc_syslog.db           # Base de datos SQLite local
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación oficial del MVP