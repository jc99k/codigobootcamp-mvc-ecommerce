# Ejemplo MVC E-Commerce

- Lenguaje: Python 3.9
- Base de Datos: Postgres 17+
- Funcionalidades:
  - Users
  - Products
  - Cart
  - (WIP) Orders

## Pasos para ejecutar en Windows (CMD)

1. **Clonar el repositorio**

```cmd
git clone https://github.com/jc99k/codigobootcamp-mvc-ecommerce.git
cd codigobootcamp-mvc-ecommerce
```


2. **Crear y activar el entorno virtual (Python 3.9)**

```cmd
py -3 -m venv .venv
call .venv\Scripts\activate.bat
```

3. **Actualizar pip e instalar dependencias**

```cmd
python -m pip install -U pip
pip install -r requirements.txt
```

4. **Crear un archivo ".env" en la raíz del proyecto**

Debe tener los siguientes contenidos, reemplazando los valores entre comillas por los valores a utilizar.
  - **DB_NAME**: Nombre de la Base de Datos (ej: "ecommerce")
  - **DB_USER**: Usuario de la Base de Datos
  - **DB_PASS**: Contraseña de la Base de Datos
  - **DB_HOST**: Hostname o IP de la Base de Datos (ej: "localhost")
  - **DB_PORT**: Puerto de la Base de Datos (ej: "5432")

Archivo ejemplo:
```
DB_NAME="ecommerce"
DB_USER="my_username"
DB_PASS="my_password"
DB_HOST="localhost"
DB_PORT="5432"
```

5. **Preparar Base de Datos PostgreSQL**

**IMPORTANTE:** _Utilizar los mismos valores del archivo .env_

- Ingresar a Postgres via `psql`

- Si la Base de Datos no existe:
```sql
CREATE DATABASE ecommerce;
```
- Finalmente:
```sql
CREATE USER my_username WITH PASSWORD 'my_password';
GRANT ALL PRIVILEGES ON DATABASE ecommerce TO my_username;
```

6. **Inicializar la base de datos**

```cmd
if not exist instance mkdir instance
python setup_db.py
```

7. **Ejecutar la aplicación**

```cmd
python run.py
```

Abre [http://localhost:5000](http://localhost:5000) en tu navegador.

---

> **Nota:**  
> Si `py -3` no funciona, prueba con `py -3.12` o simplemente `python`, según tu instalación.  
> Estos pasos están preparados para ejecutarse en el Símbolo del sistema (cmd.exe), no en PowerShell.

Si tienes algún error, comparte el mensaje exacto para ayudarte a corregirlo.