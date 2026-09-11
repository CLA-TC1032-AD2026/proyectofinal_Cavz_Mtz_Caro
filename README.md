Este proyecto implementa un ensamblador de dos pasadas y un intérprete para el modelo pedagógico Little Man Computer (LMC), permitiendo escribir código en lenguaje ensamblador con mnemónicos y etiquetas, traducirlo a código máquina y ejecutarlo de manera automatizada.

Características Principales
Ensamblador de dos pasadas: Soporta el uso de etiquetas simbólicas, manejo de comentarios y directivas de almacenamiento (DAT).

Intérprete completo de LMC: Simula la memoria de 100 casillas (00 a 99), el acumulador, la pila para subrutinas y el flujo de ejecución estándar.

Manejo de errores detallado: Valida mnemónicos desconocidos, etiquetas duplicadas o no definidas, desbordamientos de memoria y falta de parámetros.

Instrucciones Soportadas
INP (901): Lee un valor de la entrada estándar y lo carga en el acumulador.

OUT (902): Envía el valor actual del acumulador a la salida.

HLT (000): Detiene la ejecución del programa.

LDA (5xx): Carga en el acumulador el valor de la casilla xx.

STA (3xx): Almacena el valor del acumulador en la casilla xx.

ADD (1xx): Suma el valor de la casilla xx al acumulador.

SUB (2xx): Resta el valor de la casilla xx al acumulador.

BRA (6xx): Salto incondicional a la casilla xx.

BRZ (7xx): Salto condicional a xx si el acumulador es cero.

BRP (8xx): Salto condicional a xx si el acumulador es mayor o igual a cero.

CALL (4xx): Llama a una subrutina en la dirección xx (guarda retorno en pila).

RET (999): Retorna de una subrutina usando la dirección almacenada en la pila.

DAT (Variable): Reserva una casilla de memoria con un valor inicial.

Estructura del Código
Intérprete (ejecutar_lmc y leertxt): Interpreta el archivo de código máquina generado y ejecuta la simulación de la máquina LMC paso a paso.

Ensamblador (primera_pasada y segunda_pasada):

Primera pasada: Construye la tabla de símbolos (etiquetas y direcciones) y limpia comentarios.

Segunda pasada: Traduce los mnemónicos a códigos numéricos y valida la integridad sintáctica.

Bloque Principal (main): Ejemplo listo para ensamblar y ejecutar archivos fuente de prueba (programa1.txt, programa2.txt, etc.).

Ejemplo de Uso
Crea un archivo de texto llamado programa1.txt con el siguiente contenido:

// Programa de ejemplo: Lee dos números y los suma
INP
STA NUM1
INP
ADD NUM1
OUT
HLT
NUM1 DAT 0

Ejecuta el script principal para ensamblar y probar el programa:

python tu_script.py
