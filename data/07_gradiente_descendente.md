# Gradiente Descendente

Gradiente descendente é um método de otimização usado para minimizar uma função de custo. A ideia é ajustar os parâmetros na direção oposta ao gradiente, pois o gradiente aponta a direção de maior crescimento da função.

A regra geral é atualizar o parâmetro subtraindo a taxa de aprendizado multiplicada pela derivada da função de custo. A taxa de aprendizado controla o tamanho do passo.

Se a taxa de aprendizado for muito pequena, a convergência será lenta. Se for muito grande, o algoritmo pode ultrapassar o mínimo e divergir. Em funções convexas, o gradiente descendente tende a convergir para o mínimo global. Em funções não convexas, pode ficar preso em mínimos locais.
