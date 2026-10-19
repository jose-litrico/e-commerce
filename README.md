# E-Commerce API

API REST de e-commerce construida con **Django** y **Django REST Framework**.  
Permite gestionar productos, categorías, usuarios y pedidos de forma sencilla y escalable.

---

## Características

- Gestión de productos con imágenes (Pillow)
- Categorías y filtrado de productos
- Autenticación de usuarios
- Carrito de compras y pedidos
- API RESTful documentada
- Configuración mediante variables de entorno

---

## Stack tecnológico

| Tecnología              | Versión   |
|-------------------------|-----------|
| Python                  | 3.12+     |
| Django                  | 6.1.2     |
| Django REST Framework   | 3.18.2    |
| Pillow                  | 12.3.0    |
| python-dotenv           | 1.2.4     |

---

## Requisitos previos

- Python 3.12 o superior
- pip
- (Opcional) Virtualenv / venv

---

## Instalación

1. **Clonar el repositorio**

```bash
git clone <url-del-repositorio>
cd <nombre-del-proyecto>
```

2. **Crear y activar entorno virtual**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**

Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. **Aplicar migraciones**

```bash
python manage.py migrate
```

6. **Crear superusuario (opcional)**

```bash
python manage.py createsuperuser
```

7. **Ejecutar el servidor**

```bash
python manage.py runserver
```

La API estará disponible en: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Estructura del proyecto

```
├── config/                 # Configuración del proyecto (settings, urls, wsgi)
├── apps/
│   ├── products/           # Productos y categorías
│   ├── users/              # Usuarios y autenticación
│   ├── orders/             # Pedidos y carrito
│   └── ...
├── media/                  # Archivos subidos (imágenes de productos)
├── static/                 # Archivos estáticos
├── .env                    # Variables de entorno (no subir a git)
├── manage.py
├── requirements.txt
└── README.md
```

> **Nota:** Ajusta esta estructura según la organización real de tu código.

---

## Endpoints principales

| Método | Endpoint                  | Descripción                     |
|--------|---------------------------|---------------------------------|
| GET    | `/api/products/`          | Listar productos                |
| POST   | `/api/products/`          | Crear producto                  |
| GET    | `/api/products/{id}/`     | Detalle de un producto          |
| GET    | `/api/categories/`        | Listar categorías               |
| POST   | `/api/auth/login/`        | Iniciar sesión                  |
| POST   | `/api/orders/`            | Crear pedido                    |

> Estos endpoints son orientativos. Actualízalos según tu implementación real.

---

## Variables de entorno

| Variable       | Descripción                          | Ejemplo                  |
|----------------|--------------------------------------|--------------------------|
| `SECRET_KEY`   | Clave secreta de Django              | `django-insecure-...`    |
| `DEBUG`        | Modo debug                           | `True` / `False`         |
| `ALLOWED_HOSTS`| Hosts permitidos                     | `localhost,127.0.0.1`    |

---

## Desarrollo

```bash
# Ejecutar tests
python manage.py test

# Crear migraciones después de modificar modelos
python manage.py makemigrations
python manage.py migrate
```

---

## Licencia

Este proyecto es de uso personal / educativo.  
Si deseas publicar el código, añade aquí la licencia correspondiente (MIT, Apache 2.0, etc.).
```