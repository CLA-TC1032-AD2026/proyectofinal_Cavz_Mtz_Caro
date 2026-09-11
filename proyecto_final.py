import ejecutar_lmc as lm
# Diccionario de mnemónicos
mnemonicos = { 
    "INP": 901,
    "OUT": 902,
    "HLT": 0,
    "DAT": 0,
    "LDA": 5, # 5 + N1
    "STA": 3,
    "ADD": 1,
    "SUB": 2,
    "BRA": 6,
    "BRZ": 7,
    "BRP": 8,
    "CALL": 4,
    "RET": 999
}

sin_operando = {"INP", "OUT", "HLT", "RET"}
con_operando = {"LDA", "STA", "ADD", "SUB", "BRA", "BRZ", "BRP", "CALL"}

def limpiar_linea(linea):
    # Elimina comentarios que empiecen con // o #.
    linea = linea.split("//")[0]
    linea = linea.split("#")[0]
    return linea.strip() # Quita espacios al inicio y al final.
    
def primera_pasada(archivo_entrada):
    # Primera pasada:
    # Lee el archivo, detecta etiquetas y construye la tabla de símbolos.
    # También guarda las instrucciones limpias para traducirlas después.
    simbolos = {}
    instrucciones = []
    direccion = 0

    with open(archivo_entrada) as file:
        for numero_linea, linea in enumerate(file, start=1): # Enumerar (mailboxes).
            linea = limpiar_linea(linea)

            if linea == "": # Continuar si la línea está vacía.
                continue
            
            partes = linea.split() # Separa la línea en partes: etiqueta, mnemónico y operando.
        
            # Caso 1: la línea empieza directamente con un mnemónico.
            # Ejemplo: STA N1
            if partes[0] in mnemonicos: 
                mnemonico = partes[0]
                operando = partes[1] if len(partes) > 1 else None
            # Caso 2: la línea empieza con una etiqueta.
                # Ejemplo: N1 DAT 000
            else:
                etiqueta = partes[0]
    
                if len(partes) < 2:
                    raise ValueError(f"Falta mnemonico despues de la etiqueta en linea {numero_linea}: {etiqueta}")
        
                mnemonico = partes[1]
                operando = partes[2] if len(partes) > 2 else None
    
                if etiqueta in simbolos: # Detecta etiquetas repetidas.
                    raise ValueError(f"Etiqueta duplicada en linea {numero_linea}: {etiqueta}")
    
                simbolos[etiqueta] = direccion # Guarda la dirección donde aparece la etiqueta.

            if mnemonico not in mnemonicos: # Valida que el mnemónico sí exista.
                raise ValueError(f"Mnemonico desconocido en linea {numero_linea}: {mnemonico}")

            instrucciones.append((direccion, mnemonico, operando, numero_linea)) # Guarda la instrucción procesada para la segunda pasada.
            direccion += 1 # Avanza a la siguiente casilla de memoria.

            if direccion > 100:
                raise ValueError("El programa excede las 100 casillas disponibles")

    return simbolos, instrucciones

def segunda_pasada(simbolos, instrucciones):
    # Segunda pasada:
    # Traduce las instrucciones a código máquina usando la tabla de símbolos.
    memoria = [0] * 100

    for direccion, mnemonico, operando, numero_linea in instrucciones:
        # Instrucciones como INP, OUT, HLT y RET ya tienen código completo.
        if mnemonico in sin_operando:
            if operando is not None:
                raise ValueError(f"{mnemonico} no debe tener operando en linea {numero_linea}")

            memoria[direccion] = int(mnemonicos[mnemonico])
        # Instrucciones como STA N1 o BRP POS necesitan una etiqueta.
        elif mnemonico in con_operando:
            if operando is None:
                raise ValueError(f"Falta operando para {mnemonico} en linea {numero_linea}")
            # Verifica que la etiqueta usada como operando exista.
            if operando not in simbolos:
                raise ValueError(f"Etiqueta no definida en linea {numero_linea}: {operando}")

            direccion_operando = simbolos[operando] # Obtiene la dirección real de la etiqueta.
            # Forma el código final: opcode * 100 + dirección.
            # Ejemplo: STA N1, si N1 está en 06 -> 3 * 100 + 6 = 306.
            memoria[direccion] = int(mnemonicos[mnemonico]) * 100 + direccion_operando

        # DAT reserva una casilla de memoria con un valor.
        elif mnemonico == "DAT":
            if operando is None:
                memoria[direccion] = 0
            else:
                try:
                    memoria[direccion] = int(operando)
                except ValueError:
                    raise ValueError(f"Valor invalido para DAT en linea {numero_linea}: {operando}")

                if memoria[direccion] < 0 or memoria[direccion] > 999: # Valida que el valor quepa en una casilla LMC.
                    raise ValueError(f"DAT fuera de rango en linea {numero_linea}: {memoria[direccion]}")

    return memoria

def guardar_memoria(memoria, archivo_salida):
    # Guarda las 100 casillas en el formato que espera el intérprete.
    with open(archivo_salida, "w") as file:
        for direccion, instruccion in enumerate(memoria):
            file.write(f"{direccion:02d}    {instruccion:03d}\n")


def ensamblar(archivo_entrada, archivo_salida="solucion.txt"):
    # Coordina todo el proceso de ensamblado.
    simbolos, instrucciones = primera_pasada(archivo_entrada)
    memoria = segunda_pasada(simbolos, instrucciones)
    guardar_memoria(memoria, archivo_salida)
    return memoria

if __name__ == "__main__":
    try:
        # Programa 1
        ensamblar("programa1.txt", "solucion1.txt")
        pe = lm.leertxt("solucion1.txt")
        print("El resultado del programa 1 es:", lm.ejecutar_lmc(pe, [5, 6]))

        # Programa 2
        ensamblar("programa2.txt", "solucion2.txt")
        pe = lm.leertxt("solucion2.txt")
        print("El resultado del programa 2 es:", lm.ejecutar_lmc(pe, [5, 6]))

        # Programa 3
        ensamblar("programa3.txt", "solucion3.txt")
        pe = lm.leertxt("solucion3.txt")
        print("El resultado del programa 3 es:", lm.ejecutar_lmc(pe, [5]))

        # Programa 4
        ensamblar("programa4.txt", "solucion4.txt")
        pe = lm.leertxt("solucion4.txt")
        print("El resultado del programa 4 es:", lm.ejecutar_lmc(pe, [9, 4]))

        # Programa error
        ensamblar("programa_error.txt", "solucion_error.txt")
        pe = lm.leertxt("solucion_error.txt")
        print("El resultado del programa error es:", lm.ejecutar_lmc(pe, [9, 4]))
        
    except ValueError as error:
        print("Error:", error)