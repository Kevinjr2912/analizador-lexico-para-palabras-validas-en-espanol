# Analizador Léxico para Palabras Válidas en Español (Diccionario)
Programa que simule la primera fase del análisis léxico para un idioma
natural (español), utilizando una base de datos de palabras válidas y reglas específicas para
identificar, clasificar y manejar errores en un texto de entrada.

## Creando entornos
Si trabajas con una versión superior a Python 3, la creación de los entornos se hace de la siguiente manera. En terminal ejecutamos el siguiente comando.

```bash
python -m venv env
```

Por buenas practicas los entornos debemos nombrarlos como env. Si bien es cierto podemos definir el nombre que deseemos, te recomiendo siempre seguir una convención.

Una vez el entorno haya sido creado, lo siguiente será activarlo. La activación depende completamente del sistema operativo. Aquí los comandos que necesitas.

* Unix
```bash
source env/bin/activate
```

* Windows
```bash
env\Scripts\activate
```

Para desactivar el entorno, independientemente de tu sistema operativo, debes ejecutar el comando deactivate en consola.

Una vez con el entorno activado, ya seremos capaces de instalar todo lo que nuestro proyecto necesite. Las instalaciones ya no se harán a nivel sistema, si no ahora a nivel entorno.

Por lo tanto, si queremos ejecutar nuestro proyecto siempre debemos tener nuestro entorno activado.

En caso requieras conocer que dependencias y en que versión se han instalado en el entorno te recomiendo hacer uso del siguiente comando.

```bash
pip freeze
```

Por lo tanto, siempre es una excelente idea crear un archivo llamado requirements.txt en el cual almacenaremos el listado de todas las dependencias.

Será a través de este archivo con el cual podremos generar nuevamente nuestro entorno. Garantizando así que el entorno sea portable.

Para crear el archivo ejecutamos el comando.

```bash
pip freeze > requirements.txt
```

Una vez tengamos este archivo, ya podremos generar nuevamente el entorno en cualquier parte o en cualquier sistema operativo que deseemos. Basta con ejecutar el comando.

```bash
pip install -r requirements.txt
```