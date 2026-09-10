import LMC as lm

mmnemico = {"INP":"901","OUT":"902","LDA":"5","STA":"3","ADD":"1","SUB":"2","BRA":"6","BRZ":"7","BRP":"8","HLT":"000","DAT":"000"}


not_need_dir = ["INP","OUT","HLT","DAT"]
need_dir = ["LDA","STA","ADD","SUB","BRA","BRZ","BRP"]
def lmc(memoria,linea):
    file = open("solucion.txt","w")

    for i in range(0,100):
        if len(memoria)-1<i:
            file.write(str(i)+ "    " + "000" + "\n")
        else:
                if (mmnemico[memoria[i]]) in need_dir:
                    temp = linea.pop()
                    file.write(str(i)+ "    " + str(mmnemico[str(memoria[i])]) + str(temp) +"    " + str(memoria[i]) + "\n")
                else:
                    file.write(str(i)+ "    " + str(mmnemico[str(memoria[i])]) +"    " + str(memoria[i]) + "\n")

def leertxt1(archivo):
    instruccion = ""
    memoria = list([])
    count = 0
    with open(archivo) as file:
        for linea in file:
            linea = linea.replace(" ","",5)
            partes = linea.strip().split(' ')
            instruccion = str(partes[0])
            if len(partes) > 2:
                instruccion = str(partes[1])
            count +=1
            memoria.append(instruccion)
    return memoria

temp = list([88,88])
t = leertxt1("programa1.txt")
lmc(t, temp)
pe = lm.leertxt("solucion.txt")

print(lm.ejecutar_lmc(pe,[7,8]))
