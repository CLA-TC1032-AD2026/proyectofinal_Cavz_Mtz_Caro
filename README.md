# LMC: Ensamblador e Intérprete

Este proyecto implementa un ensamblador de **Little Man Computer (LMC)** y un intérprete capaz de ejecutar el código máquina generado.

## Archivos

- `ensamblador.py`: traduce un programa LMC escrito con mnemónicos a código máquina.
- `ejecutar_lmc.py`: carga y ejecuta el código máquina.
- `programa1.txt`: programa fuente de entrada.
- `solucion.txt`: archivo generado por el ensamblador.

## Formato de entrada del ensamblador

Cada línea puede contener una etiqueta opcional, un mnemónico y, cuando corresponda, un operando.

```text
INP
STA N1
INP
ADD N1
OUT
HLT
N1 DAT 000
```

Se aceptan los mnemónicos:

`INP`, `OUT`, `HLT`, `DAT`, `LDA`, `STA`, `ADD`, `SUB`, `BRA`, `BRZ`, `BRP`, `CALL` y `RET`.

Los comentarios pueden comenzar con `#` o `//`. Los valores de `DAT` deben estar entre `0` y `999`.

## Ejecutar el ensamblador

El programa principal ensambla `programa1.txt` y genera `solucion.txt`:

```bash
python ensamblador.py
```

La función también puede usarse desde Python:

```python
from ensamblador import ensamblar

ensamblar("programa1.txt", "solucion.txt")
```

## Ejecutar el intérprete

El intérprete espera una memoria de 100 casillas y una lista de valores de entrada para las instrucciones `INP`.

```python
from ejecutar_lmc import leertxt, ejecutar_lmc

memoria = leertxt("solucion.txt")
salidas = ejecutar_lmc(memoria, [7, 8])

print(salidas)
```

El archivo de código máquina debe tener una dirección y una instrucción por línea:

```text
00 901
01 306
02 901
03 106
04 902
05 000
06 000
```

`ejecutar_lmc()` regresa una lista con todos los valores producidos por instrucciones `OUT`.
