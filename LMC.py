def ejecutar_lmc(memoria: list, entradas: list) -> list:
    """memoria: lista de 100 enteros de 3 dígitos (instrucciones/datos codificados).
    entradas: cola de valores para INP.
    Regresa la lista de valores enviados por OUT."""
    memoria = list(memoria)
    pc = 0
    acumulador = 0
    salidas = []
    entradas = list(entradas)
    while True:
        instruccion = memoria[pc]
        opcode = instruccion // 100
        direccion = instruccion % 100
        pc += 1
        if instruccion == 0:                 # HLT
            break
        elif instruccion == 901:             # INP
            acumulador = entradas.pop(0)
        elif instruccion == 902:             # OUT
            salidas.append(acumulador)
        elif opcode == 5:                    # LDA
            acumulador = memoria[direccion]
        elif opcode == 3:                    # STA
            memoria[direccion] = acumulador
        elif opcode == 1:                    # ADD: se mantiene el módulo (overflow real de 3 dígitos)
            acumulador = (acumulador + memoria[direccion]) % 1000
        elif opcode == 2:                    # SUB: sin módulo, para que el signo quede disponible para BRP
            acumulador = acumulador - memoria[direccion]
        elif opcode == 6:                    # BRA
            pc = direccion
        elif opcode == 7:                    # BRZ
            if acumulador == 0:
                pc = direccion
        elif opcode == 8:                    # BRP
            if acumulador >= 0:
                pc = direccion
        else:
            raise ValueError(f"Opcode desconocido: {instruccion}")
    return salidas

lista = [0] * 100
lista[0] = 901
lista[1] = 399
lista[2] = 901
lista[3] = 199
lista[4] = 902

print("Salida generada por el programa LMC:", ejecutar_lmc(lista, [4, 1]))

def cargar_memoria_desde_archivo(nombre_archivo: str) -> list:
    # Carga un programa en un arreglo de memoria de 100 posiciones.
    memoria = [0] * 100 # Definir 100 ceros.
    with open(nombre_archivo, "r") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea:
                posicion, instruccion = map(int, linea.split(","))
                memoria[posicion] = instruccion
    return memoria # Se utilizará en la siguiente función.

def ejecutar_lmc_con_subrutinas(memoria: list, entradas: list) -> list:
    pc = 0
    acumulador = 0
    salidas = []
    entradas = list(entradas)
    pila_retorno = []  # Pila (Stack) para manejar llamadas y retornos de subrutinas

    while True:
        instruccion = memoria[pc]
        opcode = instruccion // 100
        direccion = instruccion % 100
        pc += 1

        if instruccion == 0:                  # HLT: Detener
            break
        elif instruccion == 901:              # INP: Entrar dato
            acumulador = entradas.pop(0)
        elif instruccion == 902:              # OUT: Salida de dato
            salidas.append(acumulador)
        elif opcode == 5:                     # LDA: Cargar memoria en acumulador
            acumulador = memoria[direccion]
        elif opcode == 3:                     # STA: Guardar acumulador en memoria
            memoria[direccion] = acumulador
        elif opcode == 1:                     # ADD: Sumar con módulo 1000
            acumulador = (acumulador + memoria[direccion]) % 1000
        elif opcode == 2:                     # SUB: Restar (conserva el signo para BRP)
            acumulador = acumulador - memoria[direccion]
        elif opcode == 6:                     # BRA: Salto incondicional
            pc = direccion
        elif opcode == 7:                     # BRZ: Salto si es cero
            if acumulador == 0:
                pc = direccion
        elif opcode == 8:                     # BRP: Salto si es positivo o cero
            if acumulador >= 0:
                pc = direccion
        elif opcode == 4:                     # CALL dir: Llamada a subrutina
            pila_retorno.append(pc)           # Apila la dirección de regreso
            pc = direccion                    # Salta a la subrutina
        elif instruccion == 999:              # RET: Retorno de subrutina
            pc = pila_retorno.pop()           # Desapila la dirección de regreso
        else:
            raise ValueError(f"Opcode desconocido: {instruccion} en la dirección {pc-1}")

    return salidas

# --- Prueba del programa ---
if __name__ == "__main__":
    # 1. Carga del programa desde el archivo .txt
    memoria_programa = cargar_memoria_desde_archivo("programa4.txt")
    
    # 2. Dos entradas de prueba (por ejemplo: 7 y 5)
    resultado = ejecutar_lmc_con_subrutinas(memoria_programa, entradas=[7, 5])
    
    print("Salidas generadas por el programa con subrutinas LMC:", resultado)
