import pandas as pd
import re

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

def main():
    palabras_validas = leer_CSV(r'/Users/kev29.06/Documents/Kevin/C7/Lenguajes y automátas/Project-1/palabras_espanol.csv', ',') 

    tokens = analizar_texto(palabras_validas=palabras_validas, texto_entrada='El perro corrio 3 veses acia la kasa. ¿tenemos computadoras?')

    print(tokens)

if __name__ == '__main__':
    main()

