# ⚔ PALADEX

Aplicación de escritorio para la gestión de torneos, campeones, mazos y usuarios del juego **Paladins**. Desarrollada en Python con PyQt5 y conexión a base de datos MySQL mediante JDBC.

---

## 👥 Equipo

| Alumno | Responsabilidad |
|---|---|
| Óscar Collantes Peñalba | Arquitectura MVC, Login/Registro, Home con buscador, Panel Info, Sidebar, integración general |
| Raúl Iglesias Valdueza | Creación de mazos, Mis Mazos, Perfil de usuario, Torneos, DAOs de Mazo y Torneo |
| Hugo Díez Hernaez | Panel de Administración, Panel de Moderación |

---

## 🗂 Estructura del proyecto

```
Proyecto/
├── main.py                        ← Punto de entrada
├── Paladex.sql                    ← Script de base de datos
├── lib/
│   └── mysql-connector-j-9.7.0.jar
├── src/
│   ├── controlador/
│   │   ├── ControladorPrincipal.py
│   │   ├── ControladorHome.py
│   │   ├── ControladorAdmin.py
│   │   └── ControladorModerador.py
│   ├── modelo/
│   │   ├── Logica.py
│   │   ├── LogicaHome.py
│   │   ├── LogicaAdmin.py
│   │   ├── LogicaModerador.py
│   │   ├── conexion/
│   │   │   └── Conexion.py
│   │   ├── dao/
│   │   │   ├── UsersDaoJBDC.py
│   │   │   ├── CampeonDaoJBDC.py
│   │   │   ├── CartaDaoJBDC.py
│   │   │   ├── MazoDaoJBDC.py
│   │   │   ├── MazoDAO.py
│   │   │   ├── TorneoDaoJBDC.py
│   │   │   ├── ModeradoDaoJBDC.py
│   │   │   └── SeccionDaoJBDC.py
│   │   └── vo/
│   │       ├── UsuarioVo.py
│   │       ├── LoginVO.py
│   │       ├── CampeonVo.py
│   │       ├── CartaVo.py
│   │       ├── MazoVo.py
│   │       ├── TorneoVo.py
│   │       └── HabilidadVo.py
│   └── vista/
│       ├── Login.py
│       ├── VistaHome.py
│       ├── VistaAdmin.py
│       ├── VistaModerador.py
│       ├── VistaMazo.py
│       ├── VistaMisMazos.py
│       ├── VistaPerfil.py
│       ├── VistaTorneos.py
│       └── Ui/
│           ├── VistaLogReg.ui
│           ├── Home.ui
│           ├── menu_admin.ui
│           ├── menu_moderador.ui
│           ├── crear_mazo.ui
│           ├── mis_mazos.ui
│           ├── perfil.ui
│           └── torneos.ui
```

---

## ⚙️ Requisitos

- Python 3.10 o superior
- Java JDK instalado (necesario para jaydebeapi)
- MySQL 8.0 o superior

### Dependencias Python

```bash
pip install PyQt5 jaydebeapi
```

---

## 🗄️ Base de datos

El fichero `Paladex.sql` está incluido en la raíz de `Proyecto/` e incluye toda la estructura y datos necesarios para crear la base de datos. Impórtalo con:

```bash
mysql -u root -p < Paladex.sql
```

O desde **MySQL Workbench**: `Server → Data Import → Import from Self-Contained File`.

La base de datos incluye:
- 58 campeones con sus habilidades y cartas
- 174 mazos oficiales
- Usuarios de prueba con distintos roles
- 1 torneo de ejemplo

### Configuración de conexión

Edita `src/modelo/conexion/Conexion.py` con tus datos:

```python
def __init__(self, host='localhost', database='paladex', user='User', password='1234'):
```

---

## ▶️ Ejecución

> ⚠️ **El programa debe ejecutarse siempre desde la carpeta `Proyecto/`**, de lo contrario las rutas a los archivos `.ui` y al driver JDBC no se resolverán correctamente.

```bash
cd Paladex/Proyecto
python main.py
```

---

## 👤 Usuarios de prueba

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | `admin123` | Administrador |
| `ModLaura` | `mod12345` | Moderador |
| `HugoMt` | `user1234` | Creador de Mazos |
| `MiguelT` | `user1234` | Usuario Lector |

---

## 🏗️ Arquitectura y patrones

- **MVC** — Vista (PyQt5 + .ui), Controlador, Lógica y DAO completamente separados
- **DAO** — Un DAO por entidad de base de datos
- **VO** — Objetos de transferencia de datos entre capas

---

## 🔐 Sistema de roles

| ID | Rol | Acceso |
|---|---|---|
| 0 | Administrador | Panel admin: gestión de usuarios y logs |
| 1 | Moderador | Panel moderador: auditoría de mazos y torneos |
| 2 | Creador de Mazos | Crear y gestionar mazos propios (requiere ≥100 XP) |
| 3 | Usuario Lector | Búsqueda y consulta, inscripción en torneos |

---

## 📋 Funcionalidades principales

- Login y registro con validaciones
- Buscador con filtros por Campeones, Cartas, Mazos y Torneos
- Panel de información con Novedades, Mapas y Modos de Juego (desde BD)
- Creación de mazos con validaciones (nivel total 15, máx. nivel 5 por carta, sin repetidas)
- Perfil de usuario con XP, nivel y estadísticas de torneos
- Inscripción en torneos con alias
- Sistema de logs de moderación (`modera_mazo`)
- Ocultación de mazos (soft delete) por moderadores
- Ascenso automático a Creador de Mazos al superar 100 XP