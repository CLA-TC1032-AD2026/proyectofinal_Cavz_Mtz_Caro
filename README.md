# Ensamblador e Intérprete Little Man Computer (LMC)

Este proyecto implementa un **ensamblador de dos pasadas** y un **intérprete para Little Man Computer (LMC)**. Permite escribir programas utilizando mnemónicos y etiquetas, convertirlos a código máquina y ejecutarlos mediante una simulación de una máquina LMC con 100 casillas de memoria.

## Requisitos

- Python 3
- Los archivos del ensamblador y del intérprete deben encontrarse en el mismo directorio.
- El intérprete debe estar disponible como:

```text
ejecutar_lmc.py
```

El ensamblador lo importa mediante:

```python
import ejecutar_lmc as lm
```

## Formato de entrada

Los programas fuente se escriben en archivos de texto, por ejemplo:

```text
programa1.txt
```

Cada línea puede tener uno de los siguientes formatos:

```text
MNEMONICO
MNEMONICO ETIQUETA
ETIQUETA MNEMONICO
ETIQUETA DAT VALOR
```

También se permiten comentarios utilizando `//` o `#`:

```text
INP          // Leer primer número
STA NUM1     # Guardar valor
```

Las líneas vacías son ignoradas.

## Instrucciones soportadas

| Instrucción | Código | Descripción |
|---|---:|---|
| `INP` | `901` | Lee un valor de entrada y lo guarda en el acumulador. |
| `OUT` | `902` | Envía el contenido del acumulador a la salida. |
| `HLT` | `000` | Finaliza la ejecución. |
| `LDA` | `5xx` | Carga en el acumulador el valor almacenado en `xx`. |
| `STA` | `3xx` | Guarda el acumulador en la dirección `xx`. |
| `ADD` | `1xx` | Suma al acumulador el contenido de `xx`. |
| `SUB` | `2xx` | Resta al acumulador el contenido de `xx`. |
| `BRA` | `6xx` | Salta incondicionalmente a `xx`. |
| `BRZ` | `7xx` | Salta a `xx` si el acumulador es cero. |
| `BRP` | `8xx` | Salta a `xx` si el acumulador es mayor o igual a cero. |
| `CALL` | `4xx` | Llama a una subrutina y guarda la dirección de retorno. |
| `RET` | `999` | Retorna de una subrutina. |
| `DAT` | — | Reserva una casilla de memoria con un valor inicial entre `0` y `999`. |

Las instrucciones `LDA`, `STA`, `ADD`, `SUB`, `BRA`, `BRZ`, `BRP` y `CALL` utilizan **etiquetas como operandos**.

Por ejemplo:

```text
BRA INICIO
NUM DAT 10
INICIO LDA NUM
```

## Ejecución

El bloque principal del ensamblador está configurado para ensamblar y ejecutar tres programas:

```text
programa1.txt
programa2.txt
programa3.txt
```

Para ejecutar el proyecto:

```bash
python proyecto_final.py
```

El ensamblador genera automáticamente archivos de código máquina:

```text
solucion1.txt
solucion2.txt
solucion3.txt
```

Posteriormente, estos archivos son cargados por el intérprete mediante `leertxt()` y ejecutados con `ejecutar_lmc()`.

Por ejemplo:

```python
ensamblar("programa1.txt", "solucion1.txt")

programa = lm.leertxt("solucion1.txt")
resultado = lm.ejecutar_lmc(programa, [5, 6])

print("El resultado del programa 1 es:", resultado)
```

En este caso, la lista:

```python
[5, 6]
```

representa los valores que serán consumidos por las instrucciones `INP` durante la ejecución.

## Formato del código máquina

El ensamblador genera un archivo con las **100 casillas de memoria de LMC**, numeradas desde `00` hasta `99`.

El formato de cada línea es:

```text
DIRECCION    INSTRUCCION
```

Por ejemplo:

```text
00    901
01    306
02    901
03    106
04    902
05    000
06    000
```

Las posiciones de memoria que no forman parte del programa se inicializan automáticamente en `000`.

## Validaciones

El ensamblador detecta, entre otros, los siguientes errores:

- Mnemónicos desconocidos.
- Etiquetas duplicadas.
- Etiquetas utilizadas pero no definidas.
- Instrucciones sin el operando requerido.
- Operandos proporcionados a instrucciones que no los aceptan.
- Valores `DAT` fuera del rango `0–999`.
- Programas que excedan las 100 casillas de memoria disponibles.

Los errores se reportan indicando, cuando corresponde, el número de línea donde fueron encontrados.

## Funcionamiento del ensamblador

El ensamblado se realiza en dos etapas:

1. **Primera pasada:** elimina comentarios, identifica las etiquetas y construye la tabla de símbolos con sus respectivas direcciones de memoria.
2. **Segunda pasada:** resuelve las etiquetas, traduce los mnemónicos a código máquina y genera la memoria final de 100 posiciones.

Este enfoque permite utilizar etiquetas simbólicas antes o después del lugar donde son referenciadas dentro del programa.

## Ejemplo completo

Crea un archivo llamado `programa1.txt` con el siguiente contenido:

```text
// Programa de ejemplo: lee dos números y muestra su suma

INP
STA NUM1
INP
ADD NUM1
OUT
HLT

NUM1 DAT 0
```

Después, ejecuta el ensamblador:

```bash
python proyecto_final.py
```

El programa ensamblará `programa1.txt`, generará `solucion1.txt` y ejecutará el código máquina usando las entradas definidas en el bloque principal del archivo Python.
