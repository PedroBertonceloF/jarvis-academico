# K-vizinhos mais próximos — KNN

KNN é um algoritmo de aprendizado baseado em instâncias. Durante o treinamento, ele basicamente armazena os exemplos. Na classificação de um novo exemplo, calcula a distância entre esse exemplo e os exemplos armazenados.

No problema de classificação, o KNN retorna a classe mais frequente entre os k vizinhos mais próximos. No problema de regressão, retorna a média dos valores dos k vizinhos mais próximos.

O parâmetro k controla quantos vizinhos serão considerados. Se k for muito pequeno, o modelo pode ficar sensível a ruído. Se k for muito grande, pode considerar exemplos distantes demais e perder precisão local.
