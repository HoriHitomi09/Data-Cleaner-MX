import pandas as pd
from pathlib import Path

# Detectar valores faltantes
def detectar_faltantes(df):

    faltantes = df.isna().sum()

    print("|\nREPORTE DE VALORES FALTANTES")
    print("============================")

    print(faltantes)

    if faltantes.sum() == 0:
        print("No hay valores faltantes.")
    else:
        print("Hay valores faltantes.")

# Detectar valores duplicados
def detectar_duplicados(df):

    duplicados = df.duplicated().sum()

    print("\nREPORTE DE VALORES DUPLICADOS")
    print("============================")

    print("Registro de duplicados", duplicados)

# Detectar valores negativos
def detectar_valores_negativos(df):

    print("\nREPORTE DE VALORES NEGATIVOS")
    print("============================")

    for columna in ["Price", "Stock"]:

        negativos = df[df[columna] < 0]

        if len(negativos) == 0:
            print(f"No hay valores negativos es {columna}.")
        else:
            print(f"Se encontraron {len(negativos)} valores negativos en {columna}.")
            print(negativos)

# Eliminar valores duplicados
def eliminar_duplicados(df):

    registros_originales = len(df)

    df_clean = df.drop_duplicates()

    duplicados_eliminados = registros_originales - len(df_clean)

    print("\nLimpieza de duplicados")
    print("============================")

    print("Registros originales:", registros_originales)
    print("Registros después de la limpieza:", len(df_clean))
    print("Duplicados eliminados:", duplicados_eliminados)
    print("============================")

    return df_clean, duplicados_eliminados

# Rangos de precios y stock
def rango_general_stock_precios(df):

    print("\nRANGO DE PRECIOS Y STOCK")
    print("============================")

    print("Rango de precios:")
    print("Mínimo:", df["Price"].min())
    print("Máximo:", df["Price"].max())

    print("\nRango de stock:")
    print("Mínimo:", df["Stock"].min())
    print("Máximo:", df["Stock"].max())

#Rango permitido de precios y stock
rangos_permitidos = {
    "Price": {
        "min": 1,
        "max": 50000
    },
    "Stock": {
        "min": 0,
        "max": 10000
    }
}

# validar rangos
def validar_rangos(df, rangos_permitidos):

    for columna, limites in rangos_permitidos.items():
        
        min_valor = limites["min"]
        max_valor = limites["max"]

        valores_fuera_rango = (df[columna] < min_valor) | (df[columna] > max_valor)

        if valores_fuera_rango.any():
            print(f"\nValores fuera del rango permitido en {columna}:")
            print(df.loc[valores_fuera_rango, columna])

# Correccíon de rangos
def corregir_rangos(df, rangos_permitidos):

    df = df.copy()

    total_corregidos = 0
    total_invalidos = 0
    total_sustituidos = 0

    for columna, limites in rangos_permitidos.items():

        min_valor = limites["min"]
        max_valor = limites["max"]

        valores_negativos = df[columna] < 0

        df.loc[valores_negativos, columna] = (
            df.loc[valores_negativos, columna].abs()
        )

        valores_recuperados = (
            valores_negativos &
            (df[columna] >= min_valor) &
            (df[columna] <= max_valor)
        )

        total_corregidos += valores_recuperados.sum()
        
        valores_invalidos = (
            (df[columna] < min_valor) |
            (df[columna] > max_valor)
        )

        total_invalidos += valores_invalidos.sum()

        total_sustituidos += valores_invalidos.sum()

        df.loc[valores_invalidos, columna] = float("nan")

    print("\nReporte de correcciones")
    print("============================")
    print("Valores negativos recuperados:", total_corregidos)
    print("Valores que continuan fuera de rango:", total_invalidos)
    print("Valores sustituidos por Nan:", total_sustituidos)

    return df, total_corregidos, total_sustituidos

# Proceso general de lipieza de datos
def limpiar_datos(df):

    registros_originales = len(df)

    print("\nIniciando Limpieza")
    print("============================")

    # Detectar valores faltantes
    detectar_faltantes(df)
    # Detectar valores duplicados
    detectar_duplicados(df)
    # Detectar precios negativos
    detectar_valores_negativos(df)
    # Mostrar rangos de precios y stock
    rango_general_stock_precios(df)
    # Validar los rangos
    validar_rangos(df, rangos_permitidos)
    # Eliminar valores duplicados
    df_clean, duplicados_eliminados = eliminar_duplicados(df)
    # Corregir rangos
    df_clean, total_corregidos, total_sustituidos = corregir_rangos(
        df_clean, rangos_permitidos
    )
    #Contar valores faltantes finales
    faltantes_finales = df_clean.isna().sum().sum()
    registros_finales = len(df_clean)

    print("\nLimpieza finalizada")

    detectar_faltantes(df_clean)

    return df_clean, {
        "registros_originales": registros_originales,
        "registros_finales": registros_finales,
        "duplicados_eliminados": duplicados_eliminados,
        "valores_recuperados": total_corregidos,
        "valores_sustituidos": total_sustituidos,
        "faltantes_finales": faltantes_finales
    }

# Mostrar resumen general de limpieza
def mostrar_resumen(reporte):

    print("\n============================")
    print("     RESUMEN DEL DATA CLEANER MX")
    print("============================")

    print("Registros originales:", reporte["registros_originales"])
    print("Registros finales:", reporte["registros_finales"])

    print("\nRESULTADOS DE LIMPIEZA")
    print("============================")

    print("Duplicados eliminados:", reporte["duplicados_eliminados"])
    print("Valores negativos recuperados:", reporte["valores_recuperados"])
    print("Valores sustituidos por Nan:", reporte["valores_sustituidos"])
    print("Valores faltantes finales:", reporte["faltantes_finales"])

    if reporte["faltantes_finales"] > 0:
        print("\nEstado: Limpieza finalizada con observaciones")
    else:
        print("\nEstado: Limpieza completa")

    print("============================")

# Validar tipos de datos
def validar_tipos_datos(df):

    columnas_numericas = ["Price", "Stock"]

    for columna in columnas_numericas:

        valores_no_numericos = pd.to_numeric(
            df[columna], errors="coerce"
        ).isna() & df[columna].notna()

        if valores_no_numericos.any():

            print(f"\nERROR: La columna {columna} contiene datos no numericos.")

            print(df.loc[valores_no_numericos, columna])

            return False

    print("Validacion de tipos de datos correcta.")

    return True

# Validar columnas del archivo CSV
def validar_columnas(df):

    columnas_requeridas = ["Product", "Price", "Stock"]

    columnas_faltantes = [
        columna for columna in columnas_requeridas
        if columna not in df.columns
    ]

    if columnas_faltantes:
        print("\nERROR: El archivo no contiene todas las columnas necesarias.")
        print("Columnas faltantes:", columnas_faltantes)

        return False
    
    print("Validacion de columnas correcta.")

    return True

# Carga de archivo CSV
def cargar_csv(ruta_archivo):

    try:

        df = pd.read_csv(ruta_archivo)

        if not validar_columnas(df):
            return None

        if not validar_tipos_datos(df):
            return None

        print("\nArchivo CSV cargado correctamente")
        print("Registros:", len(df))

        return df

    except FileNotFoundError:
        print("\nERROR: No se encontro el archivo CSV.")

    except pd.errors.EmptyDataError:
        print("\nERROR: El archivo CSV esta vacio.")

    except pd.errors.ParserError:
        print("\nERROR: No se pudo interpretar el archivo CSV. ")

    except Exception as e:
        print("\nERROR inesperado.", e)

    return None

# Archivo CSV limpio
def exportar_csv(df, ruta_salida):

    df.to_csv(ruta_salida, index=False)

    print("\nArchivo CSV exportado correctamente.")
    print("Ubicacion:", ruta_salida)

# Ejecución del programa
BASE_DIR = Path(__file__).resolve().parent

ruta_csv = BASE_DIR / "inventario en VSC.csv"

df = cargar_csv(ruta_csv)

if df is not None:

    print("\nDatos originales")
    print(df)

    df_clean, reporte = limpiar_datos(df)
    
    mostrar_resumen(reporte)

    print("\nResultado final")
    print(df_clean)

    ruta_salida = BASE_DIR / "inventario en VSC_LIMPIO.csv"

    exportar_csv(df_clean, ruta_salida)