# Tool Calling

Tool calling é uma técnica em que uma LLM decide chamar ferramentas externas para resolver partes de uma tarefa. Em vez de responder apenas com texto, o modelo identifica quando precisa consultar agenda, buscar documentos, listar tarefas ou executar outra função do sistema.

Uma implementação controlada pode pedir para a LLM retornar uma estrutura JSON com o nome da ferramenta e os argumentos. O programa executa a ferramenta, registra logs e envia o resultado de volta ao modelo para gerar a resposta final.

Esse padrão é útil porque combina raciocínio linguístico da LLM com ações verificáveis do sistema. Também facilita auditoria, pois os logs registram qual ferramenta foi chamada, qual entrada foi usada e qual saída foi obtida.
