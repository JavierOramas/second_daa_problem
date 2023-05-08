# El Triángulo
### Integrantes
- Javier A. Oramas López
- Eduardo García Maleta

## Descripción del problema

## Solución Fuerza Bruta
La solución de fuerza bruta se basa en generar todas las posibles subcadenas válidas dadas la condición definida en el problema, seleccionar las 4 melodías que no colisionan entre ellas y que maximizan el total de notas utilizadas.

Para esta solución se iteran por todas las posibles melodías validas y por cada melodía seleccionada se prueban todas las posibles combinaciones con las otras 3. Dando como resultado un algoritmo con una complejidad de O(n^4).

## Solución Utilizando Flujo Máximo, Costo Mínimo
Para esta solución se modela el Problema como un grafo, donde cada nota es un nodo del grafo, la arista {i} - {j} existe si i,j cumplen con la condición, y además i < j, dado que no se puede colocar una nota que aparece más adelante en la lista antes que una anterior.
Por lo antes mencionado, podemos asegurar que G (el grafo que se está construyendo) es un DAG.

Como G es un DAG, no existen ciclos con costo negativo. 
Cada arista tendrá un costo de -1, y, modelando como grafo de flujo, una capacidad máxima de 1. de esta manera garantizamos que una vez que una nota sea tomada por una melodía, ninguna otra tomará esa nota.

Para resolver el problema, realizamos una re-implementación del algoritmo y correspondientes demostraciónes propuestas por el usuario de codeforces '-is-this-fft' en el [blogpost](https://codeforces.com/blog/entry/104960) referente al algoritmo de Dinitz. en dicho post se proveen demostraciones que serán omitidas aquí.

El grafo se termina de construir creando cuatro vertederos que recibirán el costo de cada una de las 4 melodías y estos a su vez se conectan a un vertedero final que recive los costos de las 4 melodías.

Como las aristas se crearon con un costo de -1, el mínimo costo del algoritmo, será -1 * cantidad de notas utilizadas, por tanto, tomando el valor absoluto de dicho resultado, se obtiene el máximo costo de las melodías.

## Generación de Casos de Prueba
El archivo `testcase_generator.py` contiene el código que utiliza la solución de fueza bruta para generar casos de prueba, se pueden modificar en la función `generate` los parametros min_notes, max_notes, no_tests para definir cantidad mínima y/o máxima de notas en la lista, así como cantidad de casos de prueba.

## Tester
Para ejecutar el tester basta correr el archivo `tester.py`