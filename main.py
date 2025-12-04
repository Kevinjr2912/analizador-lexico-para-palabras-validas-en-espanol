import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Expresiones regulares
ER_PALABRA_BASICA=r"^[a-zñáéíóúü]+$"
ER_PUNTUACION=r"^[.,;:¿?!¡]+$"
ER_DIGITO=r"^[0-9]+$"

def leer_CSV(ruta_archivo, separador):
    # Cargar el archivo CSV con el separador personalizado en un DataFrame
    df = pd.read_csv(ruta_archivo, delimiter=separador, usecols=['Frecuencia','Alfabético'])

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
    RUTA_CSV = r"/Users/Andre/Documentos/1TareasUp/7moCuatri/Automatas/analizador-lexico-para-palabras-validas-en-espanol/palabras_espanol.csv"
    palabras_validas = leer_CSV(RUTA_CSV, ",")

# donde se hace la ventanaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa 
    root = tk.Tk()
    root.title("Analizador Léxico ")
    root.geometry("720x550")
    root.resizable(False, False)
    print("TOKEN".ljust(25), "LEXEMA")
    print("-" * 50)

    tk.Label(root, text="Ingrese el texto a analizar:").pack(pady=5)

    entrada_texto = scrolledtext.ScrolledText(root, width=80, height=8)
    entrada_texto.pack()

    tk.Label(root, text="Resultado de tokens (Token - Lexema):").pack(pady=5)
    salida_texto = scrolledtext.ScrolledText(root, width=80, height=15)
    salida_texto.pack()

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


#boton 
    def ejecutar_analisis():
        texto = entrada_texto.get("1.0", tk.END).strip()

        if texto == "":
            messagebox.showwarning("Escriba un texto para analizar.")
            return

        resultado_diccionario = analizar_texto(palabras_validas, texto)

# limpiar 
        salida_texto.delete("1.0", tk.END)

# encabezado
        salida_texto.insert(tk.END, "TOKEN".ljust(28) + "LEXEMA\n")
        salida_texto.insert(tk.END, "-" * 50 + "\n")

        tabla = convertir_a_tabla(resultado_diccionario, texto)

        for token, lexema in tabla:
            salida_texto.insert(tk.END, f"{token.ljust(28)}{lexema}\n")



    tk.Button(root, text="Analizar texto", command=ejecutar_analisis, width=20).pack(pady=10)

    root.mainloop()

def main():
    palabras_validas = leer_CSV(r'/Users/Andre/Documentos/1TareasUp/7moCuatri/Automatas/analizador-lexico-para-palabras-validas-en-espanol/palabras_espanol.csv', ',') 

    tokens = analizar_texto(palabras_validas=palabras_validas, texto_entrada='El perro corrio 3 veses acia la kasa. ¿tenemos computadoras?')

    print(tokens)

if __name__ == '__main__':
    main()
    interfaz()


