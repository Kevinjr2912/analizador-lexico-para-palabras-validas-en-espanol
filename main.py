import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Expresiones regulares
ER_PALABRA_BASICA=r"^[a-zñáéíóúü]+$"
ER_PUNTUACION=r"^[.,;:¿?!¡()]+$"
ER_DIGITO=r"^[0-9]+$"

def leer_CSV(ruta_archivo, separador):
    # Cargar el archivo CSV con el separador personalizado en un DataFrame
    df = pd.read_csv(ruta_archivo, delimiter=separador, usecols=['Frecuencia','Alfabético'])

    # Estructura de datos para almacenar las palabras válidas (HASH)
    diccionario_palabras_validas = set()

    # Extraer la columna 'Frecuencia' y 'Alfabético' y convertirla en un conjunto para eliminar duplicados
    diccionario_palabras_validas.update(df['Frecuencia'].dropna())
    diccionario_palabras_validas.update(df['Alfabético'].dropna())
    
    # Regresar la lista de palabras válidas
    return diccionario_palabras_validas

def tokenizar(texto_entrada):
    # Tokenizar el texto en palabras y signos de puntuación
    palabras_entrantes = re.findall(r"\w+|[^\w\s]", texto_entrada)
    
    # Convertir todas las palabras a minúsculas para comparación uniforme
    palabras_entrantes = [token.lower() for token in palabras_entrantes] 

    return palabras_entrantes  


def analizar_texto(palabras_validas, texto_entrada):

    formato = {
        'PALABRA_VALIDA_ESPANOL': [],
        'PUNTUACION': [],
        'DIGITO': [],
        'ERROR_ORTOGRAFICO': [],
    }
    
    palabras_entrantes = tokenizar(texto_entrada=texto_entrada)
   
    for palabra in palabras_entrantes:
         # PASO A (Diccionario): Si el lexema existe en el DiccionarioPalabrasValidas, se clasifica como "PALABRA_VALIDA"
        if palabra in palabras_validas:
            formato['PALABRA_VALIDA_ESPANOL'].append(palabra)
            continue
            
        # Paso B (Regla de Puntuación): Si el lexema coincide con ER_PUNTUACION: Clasificar como PUNTUACION.
        if re.search(ER_PUNTUACION, palabra):
            formato['PUNTUACION'].append(palabra)
            continue
        
        # Paso C (Regla de Dígito): Si el lexema coincide con ER_DIGITO: Clasificar como DIGITO.
        if re.search(ER_DIGITO, palabra):
            formato['DIGITO'].append(palabra)
            continue
            
        # Paso D (Error Léxico): Si no coincide con ninguno de los anteriores: Clasificar como ERROR_ORTOGRAFICO.
        formato['ERROR_ORTOGRAFICO'].append(palabra)
            
    return formato

#TKINTER
def interfaz():
    print("interfaz papu")

    root = tk.Tk()
    root.title("Analizador Léxico")
    root.geometry("750x600")
    root.resizable(False, False)

    # cariables de 
    ruta_csv = tk.StringVar()
    texto_cargado = tk.StringVar()

    # donde carga el csv
    def cargar_csv():
        ruta = filedialog.askopenfilename(
            title="Seleccionar diccionario CSV",
            filetypes=[("Archivos CSV", "*.csv")]
        )
        if ruta:
            try:
                ruta_csv.set(ruta)
                messagebox.showinfo("CSV cargado", "Diccionario cargado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo CSV:\n{e}")

    tk.Label(root, text="Cargar diccionario CSV:").pack(pady=3)
    tk.Button(root, text="Seleccionar CSV", command=cargar_csv, width=20).pack(pady=5)

    # carga el txttttttt
    def cargar_archivo_txt():
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo TXT a analizar",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        if ruta:
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read()
                    texto_cargado.set(contenido)
                messagebox.showinfo("TXT cargado", "Texto cargado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo TXT:\n{e}")

    tk.Label(root, text="Cargar archivo TXT para análisis:").pack(pady=3)
    tk.Button(root, text="Seleccionar TXT", command=cargar_archivo_txt, width=20).pack(pady=5)

    # el resultaooooo
    tk.Label(root, text="Resultado de tokens (TOKEN - LEXEMA):").pack(pady=5)
    salida_texto = scrolledtext.ScrolledText(root, width=90, height=22)
    salida_texto.pack()

    # tablaaaaaa
    def convertir_a_tabla(diccionario_tokens, texto_original):
        tabla = []
        tokens_ordenados = tokenizar(texto_original)

        for palabra in tokens_ordenados:
            if palabra in diccionario_tokens["PALABRA_VALIDA_ESPANOL"]:
                tabla.append(("PALABRA_VALIDA_ESPANOL", palabra))
            elif palabra in diccionario_tokens["PUNTUACION"]:
                tabla.append(("PUNTUACION", palabra))
            elif palabra in diccionario_tokens["DIGITO"]:
                tabla.append(("DIGITO", palabra))
            else:
                tabla.append(("ERROR_ORTOGRAFICO", palabra))

        return tabla

    # analizar
    def ejecutar_analisis():
        if ruta_csv.get() == "":
            messagebox.showwarning("Falta el CSV", "Primero carga el archivo CSV del diccionario.")
            return

        if texto_cargado.get().strip() == "":
            messagebox.showwarning("Falta el TXT", "Primero carga un archivo TXT.")
            return

        # carga el diccion
        palabras_validas = leer_CSV(ruta_csv.get(), ",")

        # analiza txt
        resultado_diccionario = analizar_texto(palabras_validas, texto_cargado.get())

        salida_texto.delete("1.0", tk.END)

        salida_texto.insert(tk.END, "TOKEN".ljust(28) + "LEXEMA\n")
        salida_texto.insert(tk.END, "-" * 60 + "\n")

        tabla = convertir_a_tabla(resultado_diccionario, texto_cargado.get())

        for token, lexema in tabla:
            salida_texto.insert(tk.END, f"{token.ljust(28)}{lexema}\n")

    tk.Button(root, text="Analizar archivo", command=ejecutar_analisis, width=20).pack(pady=10)

    root.mainloop()


def main():
    palabras_validas = leer_CSV(r'/Users/Andre/Documentos/1TareasUp/7moCuatri/Automatas/analizador-lexico-para-palabras-validas-en-espanol/palabras_espanol.csv', ',') 

    tokens = analizar_texto(palabras_validas=palabras_validas, texto_entrada='El perro corrio 3 veses acia la kasa. ¿tenemos computadoras?')

    print(tokens)

if __name__ == '__main__':
    main()
    interfaz()


