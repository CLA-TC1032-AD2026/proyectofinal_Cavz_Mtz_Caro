# Ensamblador para LMC 
*Proyecto final oficial del curso, 20% de la calificación. Equipos de 2-3 estudiantes.*

## Objetivo

Construir, en Python, un ensamblador de dos pasadas para el LMC que traduzca el pseudo-ensamblador con etiquetas (mnemónicos + etiquetas simbólicas) a código máquina numérico de 3 dígitos por casilla, y conectarlo con un intérprete LMC (el de la Sesión 5, extendido con subrutinas) para ejecutar el programa de principio a fin: código fuente en ensamblador, ensamblado, ejecución, salida.

## Alcance funcional (requisitos mínimos)

1. **Entrada**: un archivo de texto con el programa fuente, un mnemónico (y su etiqueta/operando si aplica) por línea, con soporte para etiquetas al inicio de línea, comentarios (todo lo que sigue a `//` o `#` en una línea se ignora), y líneas en blanco.

2. **Mnemónicos soportados**: `INP`, `OUT`, `LDA`, `STA`, `ADD`, `SUB`, `BRA`, `BRZ`, `BRP`, `HLT`, `DAT`, y opcionalmente `CALL`/`RET` (la extensión de subrutinas de la Sesión 5).

3. **Dos pasadas**: en la primera, el ensamblador recorre el programa asignando a cada línea una dirección de memoria (0, 1, 2, ...) y construye una tabla de símbolos (etiqueta → dirección); en la segunda, traduce cada línea a su código numérico de 3 dígitos, resolviendo las etiquetas usadas como operando contra la tabla de símbolos de la primera pasada. Esto es lo que permite usar una etiqueta antes de que se defina más adelante en el programa (como `BRA FIN` cuando `FIN` aparece varias líneas después).

4. **Salida**: una lista o archivo con 100 casillas (direcciones 00-99), en el mismo formato que `programa1.txt`/`programa2.txt` (`dirección,instrucción`), rellenando con `000` las direcciones no usadas.

5. **Ejecución**: el ensamblador debe conectar su salida directamente con un intérprete LMC (pueden reutilizar y extender el de la Sesión 5) para correr el programa con entradas dadas y mostrar la salida.

6. **Manejo de errores**: el ensamblador debe detectar y reportar con un mensaje claro (no simplemente fallar con un traceback de Python) al menos: mnemónico desconocido, etiqueta usada como operando que nunca fue definida, etiqueta definida dos veces, y programa que excede las 100 casillas disponibles.

## Extensiones opcionales (para subir de nivel)

- Ensamblar y ejecutar correctamente un programa con subrutinas anidadas (`CALL`/`RET`).
- Una interfaz de línea de comandos con manejo de argumentos, por ejemplo `python ensamblador.py programa.asm --run --input 7,5`
- Alguna mejora adicional a los requerimientos mínimos

## Entregables

1. Código fuente del ensamblador y del intérprete, en un repositorio o carpeta compartida.
2. Al menos 3 programas de prueba en pseudo-ensamblador (por ejemplo: suma de dos números, diferencia positiva, mayor de dos números) con sus resultados esperados documentados.
3. Un `README.md` breve que explique cómo ejecutar el ensamblador y el intérprete, y el formato de entrada esperado.
4. Un reporte corto (1-2 páginas) que describa las decisiones de diseño (por ejemplo, cómo manejaron las dos pasadas), los errores encontrados durante el desarrollo y cómo los resolvieron, y qué extensiones opcionales implementaron, si aplica.
5. Una demostración en vivo (5 minutos) ensamblando y ejecutando un programa que el profesor proponga en el momento, como prueba de que el ensamblador funciona de verdad y no solo con los casos ya probados de antemano.

## Rúbrica (100 puntos, 20% de la calificación final)

| Rubro | Puntos | Criterio |
|---|---|---|
| Traducción correcta de mnemónicos a código numérico | 25 | Cada mnemónico soportado se traduce al opcode y formato correctos |
| Resolución de etiquetas (dos pasadas) | 20 | Etiquetas definidas antes o después de su uso se resuelven correctamente; se detectan etiquetas no definidas o duplicadas |
| Integración con el intérprete (ejecución de principio a fin) | 20 | El programa ensamblado se ejecuta correctamente con al menos 3 casos de prueba distintos |
| Manejo de errores | 10 | Los errores del punto 6 del alcance se detectan y se reportan con un mensaje claro, no con un traceback crudo |
| Documentación (README + reporte) | 10 | Instrucciones claras de uso; el reporte explica decisiones de diseño, no solo que "funcionó" |
| Demostración en vivo con un programa nuevo | 15 | El ensamblador funciona con un programa que el equipo no había probado antes |

## Fechas

- **Sesión 7**: equipos confirmados y propuesta de una página (qué mnemónicos soportarán, cómo manejarán la tabla de símbolos).
- **Sesión 8**: avance funcional, al menos las dos pasadas del ensamblador trabajando, aunque todavía no esté conectado al intérprete.
- **Sesión 10**: entrega final y demostración en vivo.

## Programas de ejemplo para probar el ensamblador

Sirven como casos de prueba mínimos: el primero no usa saltos ni etiquetas hacia adelante; el segundo sí, y por eso es un buen caso para confirmar que las dos pasadas funcionan de verdad (la etiqueta `POS` se usa en `BRP POS` antes de que el ensamblador la haya visto definida).

### Programa de ejemplo 1: suma de dos números

Código fuente:

```
        INP
        STA N1
        INP
        ADD N1
        OUT
        HLT
N1      DAT 000
```

Ensamblado esperado (dirección, código numérico, mnemónico):

| Dirección | Código | Mnemónico |
|---|---|---|
| 00 | 901 | INP |
| 01 | 306 | STA N1 |
| 02 | 901 | INP |
| 03 | 106 | ADD N1 |
| 04 | 902 | OUT |
| 05 | 000 | HLT |
| 06 | 000 | N1 DAT 000 |

Casos de prueba verificados: (7,5) → 12; (3,9) → 12; (0,0) → 0; (50,49) → 99.

### Programa de ejemplo 2: diferencia positiva

El mismo programa que se trabaja a mano en la Sesión 4 (`SUB` + `BRP`), ahora con etiquetas para que el ensamblador resuelva las direcciones. Nótese que `POS` se usa como operando en la línea `BRP POS` antes de aparecer definida como etiqueta más abajo: es el caso que obliga a que el ensamblador funcione en dos pasadas y no en una sola.

Código fuente:

```
        INP
        STA A
        INP
        STA B
        SUB A
        BRP POS
        LDA A
        SUB B
POS     OUT
        HLT
A       DAT 000
B       DAT 000
```

Ensamblado esperado (dirección, código numérico, mnemónico):

| Dirección | Código | Mnemónico |
|---|---|---|
| 00 | 901 | INP |
| 01 | 310 | STA A |
| 02 | 901 | INP |
| 03 | 311 | STA B |
| 04 | 210 | SUB A |
| 05 | 808 | BRP POS |
| 06 | 510 | LDA A |
| 07 | 211 | SUB B |
| 08 | 902 | POS OUT |
| 09 | 000 | HLT |
| 10 | 000 | A DAT 000 |
| 11 | 000 | B DAT 000 |

Casos de prueba verificados: A=7,B=5 → 2; A=3,B=9 → 6; A=5,B=5 → 0; A=0,B=0 → 0; A=99,B=1 → 98.
