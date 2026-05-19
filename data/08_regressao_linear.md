# Regressão Linear

Regressão linear é um modelo supervisionado usado para prever valores contínuos. Um modelo univariado pode ser representado por h(x) = theta0 + theta1 vezes x, em que theta0 é o intercepto e theta1 é o coeficiente angular.

A função de custo mais comum é o erro quadrático médio. Ela mede a diferença entre o valor previsto pelo modelo e o valor real. O objetivo do treinamento é encontrar parâmetros que minimizem essa função de custo.

O gradiente descendente pode ser usado para ajustar os parâmetros da regressão linear. No modo batch, o gradiente é calculado usando todos os exemplos. No modo estocástico, os parâmetros são atualizados a cada exemplo. No mini-batch, usa-se pequenos grupos de exemplos.
