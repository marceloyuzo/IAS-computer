VARIAVEIS FIXAS
* ENDEREÇO PARA O TAMANHO DO ARRAY
* ELEMENTOS DO ARRAY A SEREM ORDENADOS

VARIAVEIS TEMPORARIAS
* TAMANHO DO ARRAY
* INDICE INICIAL DO LOOP
* INDICE DO MENOR ELEMENTO ENCONTRADO
* TAMANHO RESTANTE DO ARRAY
* VALOR DO MENOR ELEMENTO ENCONTRADO
* INDICE INTERNO DO LOOP

ARRAY DE EXEMPLO = [8, 15, 2, 10, 20] 
MEMORIA RAM

IBR: o Instruction Buffer Register serve para armazenar temporariamente uma instru¸c˜ao. O IAS
busca instru¸c˜oes da mem´oria em pares - lembre-se de que uma palavra da mem´oria (de 40 bits) cont´em
duas instru¸c˜oes (de 20 bits). Dessa forma, quando o IAS busca um par de instru¸c˜oes, a primeira
instru¸c˜ao ´e armazenada diretamente em IR e a segunda em IBR. Ao t´ermino da execu¸c˜ao da primeira
instru¸c˜ao (em IR), o computador move a segunda instru¸c˜ao (armazenada em IBR) para IR e a executa

FLUXO PRINCIPAL
Inicializa memoria ram
Inicializa processador
Processador faz um ciclo de busca da primeira instrucao armazenada em PC
Processador faz um ciclo de execucacao
Se o endereco de PC nao existir, acabou as instrucoes

LOAD MQ M(X), 0X02
MUL M(X), 0X03
STOR M(X), 0X02
LOAD M(X), 0X03
ADD M(X), 0X01
STOR M(X), 0X03
LOAD M(X), 0X00
SUB M(X), 0X01
JUMP+ M(X: 0:19), 0X05