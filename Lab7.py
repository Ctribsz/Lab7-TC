import time

def descomponer_producciones(gramatica):
    """
    Descompone las producciones con múltiples símbolos en el lado derecho para cumplir con la CNF.
    :param gramatica: Diccionario que representa la gramática.
    :return: Gramática con producciones binarias.
    """
    nueva_gramatica = {}
    contador_auxiliar = 1

    for no_terminal, producciones in gramatica.items():
        nueva_gramatica[no_terminal] = []

        for produccion in producciones:
            while len(produccion) > 2:
                nuevo_no_terminal = f"X{contador_auxiliar}"
                contador_auxiliar += 1

                nueva_gramatica[nuevo_no_terminal] = [[produccion[0], produccion[1]]]
                produccion = [nuevo_no_terminal] + produccion[2:]

            nueva_gramatica[no_terminal].append(produccion)

    return nueva_gramatica

def eliminar_epsilon(gramatica):
    """
    Elimina las producciones epsilon de la gramática.
    :param gramatica: Diccionario que representa las producciones de la gramática.
    :return: Gramática sin producciones epsilon.
    """
    # Identificar no terminales que producen epsilon
    generadores_epsilon = set()
    for no_terminal, producciones in gramatica.items():
        for produccion in producciones:
            if produccion == ['ε']:
                generadores_epsilon.add(no_terminal)

    # Remover producciones epsilon directas
    for no_terminal in generadores_epsilon:
        gramatica[no_terminal] = [prod for prod in gramatica[no_terminal] if prod != ['ε']]

    for no_terminal, producciones in list(gramatica.items()):
        nuevas_producciones = set()
        for produccion in producciones:
            combinaciones = [produccion]
            for simbolo in produccion:
                if simbolo in generadores_epsilon:
                    nuevas_combinaciones = []
                    for comb in combinaciones:
                        nueva_comb = [s for s in comb if s != simbolo]
                        nuevas_combinaciones.append(comb)
                        if nueva_comb:
                            nuevas_combinaciones.append(nueva_comb)
                    combinaciones = nuevas_combinaciones
            nuevas_producciones.update(tuple(comb) for comb in combinaciones if comb)

        gramatica[no_terminal].extend(list(nuevas_producciones))

    for no_terminal, producciones in gramatica.items():
        gramatica[no_terminal] = [list(prod) for prod in set(tuple(p) for p in producciones)]

    return gramatica

def eliminar_unarias(gramatica):
    """
    Elimina las producciones unitarias de la gramática.
    :param gramatica: Diccionario que representa las producciones de la gramática.
    :return: Gramática sin producciones unitarias.
    """
    nueva_gramatica = {nt: [] for nt in gramatica}

    for no_terminal, producciones in gramatica.items():
        no_unitarias = [prod for prod in producciones if len(prod) != 1 or prod[0] not in gramatica]
        nueva_gramatica[no_terminal].extend(no_unitarias)

        unitarias = [prod[0] for prod in producciones if len(prod) == 1 and prod[0] in gramatica]
        while unitarias:
            unidad = unitarias.pop()
            for prod in gramatica[unidad]:
                if len(prod) != 1 or prod[0] not in gramatica:
                    if prod not in nueva_gramatica[no_terminal]:
                        nueva_gramatica[no_terminal].append(prod)
                elif prod[0] not in unitarias:
                    unitarias.append(prod[0])

    return nueva_gramatica

def gr_reader(file_path):
    gramatica = {}
    simbolo_inicial = None

    with open(file_path, 'r') as file:
        for linea in file:
            linea = linea.strip()

            # Aquí nos encargamos de separar la parte izquierda de la derecha
            # La parte de la producción y del símbolo que la produce
            if "->" in linea:
                no_terminal, producciones = linea.split("->")
                no_terminal = no_terminal.strip()
                producciones = producciones.strip().split("|")

                # Si es la primera vez que vemos un no terminal, lo usamos como símbolo inicial
                if simbolo_inicial is None:
                    simbolo_inicial = no_terminal

                if no_terminal not in gramatica:
                    gramatica[no_terminal] = [prod.strip().split() for prod in producciones]
                else:
                    gramatica[no_terminal].extend([prod.strip().split() for prod in producciones])

    print("\nGramática leída:")
    for nt, prods in gramatica.items():
        for prod in prods:
            print(f"{nt} -> {' '.join(prod)}")

    return gramatica, simbolo_inicial

def print_g (gramatica):
    for no_terminal, producciones in gramatica.items():
        producciones_formateadas = " | ".join(" ".join(prod) for prod in producciones)
        print(f"{no_terminal} -> {producciones_formateadas}")
        


file_path = "Gramatica2.txt"
gramatica, simbolo_inicial = gr_reader(file_path)

start_time = time.time()

print("\nEliminando producciones epsilon...")
gramatica = eliminar_epsilon(gramatica)
print_g(gramatica)

print("\nEliminando producciones unitarias...")
gramatica = eliminar_unarias(gramatica)
print_g(gramatica)
