PASSO A PASSO PARA EXECUTAR O PROGRAMA:
1. Extrair o codigo fonte do zip
2. Abrir a pasta do codigo fonte no terminal
3. Executar o programa principal ("py .\main.py")

ALTERAÇÃO DE QUAL ALGORITMO EXECUTAR
1. Abrir o .txt do algoritmo que quer Executar
2. Copiar o que está dentro
3. Colar no ram.txt

OU:

1. Abrir o main.py
2. Alterar o ram_file de "ram.txt" para o nome do arquivo do algoritmo (potencia.txt, sort.txt, fatorial.txt)
3. Executar normalmente o passo a passo para executar o programa

Mapeamento das variáveis de cada algoritmo na memória RAM (os comentários são acompanhados anteriormente por "//"), apenas os algoritmos de potência e fatorial está funcionando corretamente.

Selection Sort: (NÃO CONSEGUI FAZER FUNCIONAR, mas estava nessa ideia)
2 0x00 // tamanho do array (originalmente estava 3, mas diminuindo 1 estava percorrendo o array corretamente)
4 0x01 // primeiro elemento do array
24 0x02 // segundo elemento do array
42 0x03 // terceiro elemento do array
0 0x04 // variavel temp
0 0x05 // indice atual externo
0 0x06 // indice do menor elemento
0 0x07 // valor menor elemento
1 0x08 // constante 1
1 0x09 // endereço base que começa o array (no caso é 0x01)
1 0x0A // variavel temp
1 0x0B // indice atual interno

0x0C
LOAD M(0x00) // carrega tamanho da array
STOR M(0x04) // guarda na variavel temp
LOAD M(0x05) // carrega indice atual externo (começa em 0)
STOR M(0x06) // guarda no indice do menor valor
LOAD M(0x01) // carrega o elemento do indice externo (tem que ser endereço DINAMICO aqui)
STOR M(0x07) // guarda no menor valor
LOAD M(0x05) // carrega indice atual externo
ADD M(0x08) // acrescenta um
STOR M(0x05) // atualiza indice atual externo
ADD M(0x09) // soma o indice atual externo atualizado com o endereço base do array
STOR M(0x0E 8:19) // atualiza o carregamento dinamico do elemento do indice externo
JUMP M(0x12 0:19) // pula para a parte da comparação (loop interno)
LOAD M(0x0B) // carrega indice atual interno
ADD M(0x09) // adiciona endereço base
STOR M(0x1A 28:39) // atualiza endereço da parte da atualização do mínimo
LOAD M(0x0B)
SUB M(0x04) // subtrai com o tamanho do array para ver se chegou ao final do loop interno
JUMP +M(0x1C 0:19) // se chegou ao fim do loop interno, troca as posições com o valor minimo
LOAD M(0x07) // carrega valor minimo
SUB M(0x02) // subtrai pelo valor atual do valor do indice atual (DINAMICO)
JUMP +M(0x19 20:39) // se resultar em positivo, troca o elemento minimo
LOAD M(0x0B) // carrega indice atual interno
ADD M(0x08) // acrescenta um
STOR M(0x0B) // atualiza indice atual interno
ADD M(0x09) // acrecenta com o endereço base do array
STOR M(0x15 28:39) // muda o endereço dinamico
JUMP M(0x12 0:19) // pula para a parte de comparação de novo (mais uma iteração)
LOAD M(0x0B) // carrega indice atual interno (parte de trocar o menor valor, só cai aqui se o indice atual for o menor valor)
STOR M(0x06) // armazena no indice do menor valor
LOAD M(0x02) // carrega o valor do indice atual (DINAMICO)
STOR M(0x07) // armazena no campo de menor valor
JUMP M(0x12 0:19) // pula para mais uma iteração do menor valor
LOAD M(0x01) // carrega o elemento do indice externo (DINAMICO) @@@@@
STOR M(0X0A) // armazena em uma variavel temp
LOAD M(0x05) // carrega o indice atual externo
SUB M(0x08) // subtrai um (gambiarra)
ADD M(0x09) // soma com o endereço base do array
STOR M(0x22 8:19) // atualiza o endereço com o endereço do indice externo a ser trocado
ADD M(0x08) // gambiarra
STOR M(0x1C 8:19)
LOAD M(0x06) // carrega o indice do menor valor
ADD M(0x09) // soma com o endereço base do array
STOR M(0x23 8:19) // atualiza o endereço com o endereço do indice menor a ser trocado
LOAD M(0x07) // carrega o valor do menor elemento
STOR M(0X01) // guarda no endereço DINAMICO a ser trocado
LOAD M(0x0A) // carrega o valor do indice externo
STOR M(0x02) // guarda no endereço DINAMICO a ser trocado
LOAD M(0x04) // pega o tamanho do array
SUB M(0x05) // subtrai pelo indice externo
JUMP +M(0x0D 0:19) // se for negativo, é pq acabou
EXIT


Potência:
5 0x00 // base da potenciação
3 0x01 // expoentee da potenciação
0 0x02 // contador
1 0x03 // resultado da potenciação
1 0X04 // constante 1

0x05
LOAD M(0x01)
SUB M(0x04)
STOR M(0x02)
LOAD MQ M(0x03)
MUL M(0x00)
STOR M(0x03)
LOAD M(0x02)
SUB M(0x04)
STOR M(0x02)
JUMP +M(0x06 20:39)
EXIT


Fatorial: (visto em aula)
4 0x00 // fatorial
1 0x01 // constante 1
1 0x02 // resultado do fatorial
1 0x03 // contador

0x04
LOAD MQ M(0X02)
MUL M(0X03)
STOR M(0X02)
LOAD M(0X03)
ADD M(0X01)
STOR M(0X03)
LOAD M(0X00)
SUB M(0X03)
JUMP +M(0X04 0:19)
EXIT
