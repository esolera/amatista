# ReadMe
** **
## Archivos
* **Codificador.py:** Es el es codificador que pone solo 1 bit por ventana. Su ejecución genera un archivo pruebasss.wav el cual contiene el audio con los ecos. En su código se generan los metadatos de manera aleatoria y se guardan el archivos meta.csv

* **Decodificador.py:** Es la implementación del decodificador que que sirve para los archivo de audio codificacidos con solo un bit por ventana. Su ejecución lee un archivo preubasss.wav, metadatos.csv. Este último archivo contiene los metadatos originales.

* **Codificador_Multiple.py:** Este codificador funciona igual que el codificador.py, con la diferencia que es capaz de codificar  2 bits por ventana.

* **Decodificador_Multiple.py:** Este decodificador funciona igual que el decodificador.py con la diferencia que es capaz de decodificar 2 bits por ventana.

* **Codificador_correción.py:** Este codificador funciona igual que el codificador.py, con la diferencia que es capaz de agregar bits para la detección y correción de errores por medio del algoritmo hamming.

* **Decodificador_Multiple.py:** Este decodificador funciona igual que el decodificador.py con la diferencia que puede detectar errores por medio del algoritmo hamming.

* **run.py**: Este es un script de python que corre todas las canciones ejecutando al **codificador.py** y luego al **decodificador.py** variando parámetros de tamaño de vetana y amplitud. Simula 5 con los mismo parámetros, luego calcula el promedio de datos recuperados de manera correcta y los va graficando. Las graficas las guarda en la carpeta Resultados.

* **run_multiples.py**: Este script realiza lo mismo que **run.py**, pero ejecutando a **Codificador_Multiple.py** y **Decodificador_Multiple.py**. Las graficas generadas las guarda en  la carpeta Resultados_Multiple.

* **run_Correcion.py**: Este script realiza lo mismo que **run.py**, pero ejecutando a **Codificador_corrección.py** y **Decodificador_corrección.py**. Las graficas generadas las guarda en  la carpeta Resultados_Multiple.

** **
## Ejecucion Codificador.py o Codificacion_correcion.py
Los script tiene como entradas:

* La cancion a ejecutar la cual debe ser de 8 bits.
* Los retrasos de los ecos que se ingresan en ms, no pueden ser menores a 1.
* Las amplitudes de los ecos, los cuales si pueden ser menores a 1.
* El tamaño de la ventana que se ingresa en ms.

```
python3 Codificador.py Cancion retraso1 restraso0 amplitud1 amplitud0 ventana_size
```

Un ejemplo de ejecución es :
```
python3 Codificador.py Canciones/Californication.wav 3 8 0.1 0.1 10
```

```
python3 Codificacion_correcion.py Canciones/Californication.wav 3 8 0.1 0.1 10

```
Su ejecución deberia generar el archivo pruebasss.wav

** **
## Ejecución de Decodificación.py o Decodificador_correcion.py

Este script tiene como entradas:

* El archivo que se desea decodifcar.
* Los retrasos de los ecos que se ingresan en ms, no pueden ser menores que 1.
* El tamaño de la ventana que se ingresa en ms.

```
python3 Decodificador.py archivo.wav restraso1 restraso0 ventana_size
```
Un codigo de ejemplo es :

```
python3 Decodificador.py pruebasss.wav 3 8 10
```

```
python3 Decodificador_correcion.py pruebasss.wav 3 8 10

```
** **

## Ejecucion de Codificador_Multiple
* Su unica diferencia con los anteriores es que necesita que se le ingresen 4 retardos de eco y  amplitudes de eco.

```
python3 Codificador_Multiple.py Cancion.wav retraso0 restraso1 restraso2 restraso3 amplitud0 amplitud1 ventana_size
```
Un ejemplo de su ejecución es :
```
python3 Codificador_Multiple.py Canciones/Californication.wav 1 3 5 7 0.1 0.1 10
```
## Ejecucion de Decodificador_Multiple

* Su unica diferencia con los decodificadores anteriores es que se le indiquen los 4 retraso posibles en ves de 2.

```
python3 Deodificador_multiple.py Cancion.wav retraso0 restraso1 restraso2 restraso3 ventana_size
```
Un ejemplo de su ejecución es :
```
python3 Deodificador_multiple.py pruebasss.wav 1 3 5 7 50

```
** **
## Ejecución de todos los run.py.

* Tiene solo un parametro de entrada que indica cuantas veces se decea correr una simulación con los mismo parametros. Esto en otras palabras sirve para indicar de cuantos datos quiere el promedio. La ejecución de este script tarda bastante pues corre todas las canciones.

```
run.py cantidad
```
