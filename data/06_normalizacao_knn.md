# Normalização no KNN

A normalização é importante no KNN porque o algoritmo depende de medidas de distância. Se um atributo possui escala muito maior que os demais, ele pode dominar o cálculo da distância.

Por exemplo, se um atributo varia de 0 a 1 e outro varia de 0 a 1000, a distância euclidiana será muito mais influenciada pelo segundo atributo. Isso pode gerar classificações ruins, pois nem todos os atributos contribuem de forma equilibrada.

Uma estratégia comum é a normalização min-max, que transforma valores para o intervalo entre 0 e 1. A fórmula é: valor normalizado igual a valor menos mínimo dividido por máximo menos mínimo.
