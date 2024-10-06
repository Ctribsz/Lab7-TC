import re

def cargar_gramatica(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            lineas = archivo.readlines()
        return [linea.strip() for linea in lineas if linea.strip()]
    except FileNotFoundError:
        print(f"Error: El archivo {nombre_archivo} no fue encontrado.")
        return []

def validar_produccion(produccion):
    regex = r"[A-Z]\s*->\s*([A-Za-z0-9]+(\|[A-Za-z0-9]+)*)"
    return re.match(regex, produccion)

def procesar_gramatica(gramatica):
    producciones = {}
    for linea in gramatica:
        partes = linea.split("->")
        no_terminal = partes[0].strip()
        reglas = [regla.strip() for regla in partes[1].split("|")]
        producciones[no_terminal] = reglas
    return producciones

def encontrar_anulables(producciones):
    anulables = set()
    for no_terminal, reglas in producciones.items():
        for regla in reglas:
            if regla == 'e': 
                anulables.add(no_terminal)
    return anulables

def generar_producciones_sin_anulables(regla, anulables):
    if not any(simbolo in anulables for simbolo in regla):
        return {regla}
    
    nuevas_producciones = set()
    for i, simbolo in enumerate(regla):
        if simbolo in anulables:
            nueva = regla[:i] + regla[i+1:]
            if nueva:
                nuevas_producciones.add(nueva)
    return nuevas_producciones

def eliminar_producciones_e(producciones):
    anulables = encontrar_anulables(producciones)
    print(f"Símbolos anulables encontrados: {anulables}")
    
    nuevas_producciones = {}
    for no_terminal, reglas in producciones.items():
        nuevas_reglas = set(reglas)  
        for regla in reglas:
            if any(simbolo in anulables for simbolo in regla):
                nuevas_reglas.update(generar_producciones_sin_anulables(regla, anulables))
        
        nuevas_reglas.discard('e')
        nuevas_producciones[no_terminal] = list(nuevas_reglas)
    
    return nuevas_producciones

def mostrar_producciones(producciones):
    print("\nProducciones actuales:")
    for no_terminal, reglas in producciones.items():
        print(f"{no_terminal} -> {' | '.join(reglas)}")

def main():
    archivo1 = 'Gramatica1.txt'
    archivo2 = 'Gramatica2.txt'

    gramaticas = [cargar_gramatica(archivo1), cargar_gramatica(archivo2)]
    
    for gramatica in gramaticas:
        for produccion in gramatica:
            if not validar_produccion(produccion):
                print(f"Producción inválida: {produccion}")
                return
        
        producciones = procesar_gramatica(gramatica)
        print("\nGramática cargada:")
        mostrar_producciones(producciones)
        
        producciones_sin_epsilon = eliminar_producciones_e(producciones)
        
        print("\nGramática sin producciones-e:")
        mostrar_producciones(producciones_sin_epsilon)

if __name__ == '__main__':
    main()