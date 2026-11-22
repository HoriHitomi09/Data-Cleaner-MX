Data Cleaner MX

Herramienta desarrollada en Python para la limpieza y validación de archivos CSV, enfocada en la gestión de datos de inventario.

Descripción

Data Cleaner MX permite identificar y corregir problemas comunes en conjuntos de datos, como valores faltantes, registros duplicados y valores numéricos fuera de los rangos permitidos.

El programa utiliza Pandas para procesar la información y generar un nuevo archivo CSV con los datos resultantes de la limpieza.

Objetivo

Facilitar la limpieza y validación de datos de inventario mediante un proceso automatizado, reduciendo errores y mejorando la calidad de la información.

Funcionalidades

Carga de archivos CSV.

Validación de columnas requeridas.

Validación de tipos de datos.

Detección de valores faltantes.

Detección y eliminación de registros duplicados.

Detección de valores negativos.

Validación de rangos numéricos.

Recuperación de valores negativos cuando es posible.

Sustitución por valores faltantes (NaN) cuando los datos están fuera de los rangos permitidos.

Generación de un reporte con los resultados de la limpieza.

Exportación de los datos procesados a un nuevo archivo CSV.

Manejo de errores durante la carga del archivo.

Tecnologías utilizadas

Python

Pandas

Pathlib

Requisitos

Python instalado.

Biblioteca Pandas.

Instalación

Instala Pandas desde la terminal:

pip install pandas

Uso

Coloca el archivo CSV en la carpeta del proyecto.

Asegúrate de que tenga las columnas Product, Price y Stock.

Utiliza el nombre inventario en VSC.csv.

Abre la terminal en la carpeta del proyecto.

Ejecuta el programa:

python "inventario en VSC.py"

El programa realizará las validaciones, procesará los datos y generará un archivo llamado inventario en VSC_LIMPIO.csv en la misma carpeta del proyecto.

Ejemplo de datos

Archivo original

| Product |   Price   | Stock |
|---------|-----------|-------|
| Laptop  |   12000   |   5   |
|  Mouse  | -89743563 |  -10  |
|Keyboard |    500    |   8   |
| Monitor |   3500    |   4   |
|  Mouse  |    250    |  10   |

Resultado esperado

| Product | Price | Stock |
|---------|-------|-------|
| Laptop  | 12000 |   5   |
|  Mouse  |  NaN  |  10   |
|Keyboard |  500  |   8   |
| Monitor | 3500  |   4   |
|  Mouse  |  250  |  10   |

En este ejemplo:

El valor negativo de Stock se recupera porque su valor absoluto está dentro del rango permitido.

El valor de Price se sustituye por NaN porque continúa fuera del rango permitido después de intentar recuperarlo.

Los registros duplicados se eliminan cuando existen.

Rangos permitidos

Actualmente, el programa utiliza los siguientes rangos:

| Columna | Mínimo | Máximo |
|---------|--------|--------|
|  Price  |    1   | 50000  |
|  Stock  |    0   | 10000  |

Estos valores pueden modificarse en la configuración del código.

Manejo de errores

El programa contempla situaciones como:

Archivo CSV inexistente.

Archivo CSV vacío.

Errores de lectura o formato.

Columnas requeridas faltantes.

Tipos de datos no válidos.

Estado del proyecto

Versión 1.0 — Versión funcional inicial.

Proyecto desarrollado como práctica de programación y procesamiento de datos con Python y Pandas.

Autor

Luis Elias Avalos Tinoco

Proyecto personal: Data Cleaner MX.