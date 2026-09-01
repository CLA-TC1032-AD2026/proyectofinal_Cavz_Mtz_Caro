def ejecutar_lmc(memoria, entradas):
    """memoria: lista de 100 enteros de 3 dígitos (instrucciones/datos codificados).
    entradas: cola de valores para INP.
    Regresa la lista de valores enviados por OUT."""
    memoria = list(memoria)
    entradas = list(entradas    )
    pc = 0
    acumulador = 0
    salidas = []



    pila = []
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
        elif instruccion == 999: 
            if not pila: 
                raise ValueError("No hay nada en pila")
            pc = pila.pop()
        elif opcode == 5:                    # LDA
            acumulador = memoria[direccion]
        elif opcode == 4: 
            pila.append(pc)
            pc = direccion
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


def leertxt(archivo):
    memoria = [0] * 100

    with open(archivo) as file:
        for linea in file:
            partes = linea.strip().split(',')

            direccion = int(partes[0])
            instruccion = int(partes[1])

            memoria[direccion] = instruccion

    return memoria

if __name__ == "__main__":
#    prueba3 = leertxt('programa3.txt')
 #   print(ejecutar_lmc(prueba3, [5,6]))
  #  prueba2 = leertxt('programa2.txt')
   # print(ejecutar_lmc(prueba2, [5,6]))
    prueba1 = leertxt('programa1.txt')
    print(ejecutar_lmc(prueba1, [5,6]))

   # pruebarec = leertxt('recr.txt')
    #print(ejecutar_lmc(pruebarec, [5,6]))
