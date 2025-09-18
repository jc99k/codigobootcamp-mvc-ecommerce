# Ejemplo MVC E-Commerce

- Lenguaje: Python 3.9
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

4. **Inicializar la base de datos**

```cmd
if not exist instance mkdir instance
python setup_db.py
```

5. **Ejecutar la aplicación**

```cmd
python run.py
```

Abre [http://localhost:5000](http://localhost:5000) en tu navegador.

---

> **Nota:**  
> Si `py -3` no funciona, prueba con `py -3.12` o simplemente `python`, según tu instalación.  
> Estos pasos están preparados para ejecutarse en el Símbolo del sistema (cmd.exe), no en PowerShell.

Si tienes algún error, comparte el mensaje exacto para ayudarte a corregirlo.