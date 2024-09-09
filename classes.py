class IAS:
    def __init__(self, ram_file):
        # Inicializando os registradores
        self.MAR = None
        self.IR = None
        self.IBR = None
        self.MBR = None
        self.AC = None
        self.MQ = None
        self.R = None
        self.C = None
        self.Z = None
        # Inicializando a memoria RAM, e colocando a primeira instrução no registrador PC
        self.memory = self.load_memory(ram_file)

        self.running = True # Variável para finalizar as instruções
        self.last_instruction_was_left = False # Variável para saber se a ultima instrução executada foi o da esquerda
        self.jumpedLeft = False # Variável para saber se ocorreu um salto condicional para a parte esquerda da palavra
        self.jumpedRight = False # Variável para saber se ocorreu um salto condicional para a parte direita da palavra

    def load_memory(self, ram_file):
        memory = []
        with open(ram_file, 'r') as file:
            lines = file.read().splitlines()
            startedInstructions = False
            i = 0

            while (i < len(lines)):
                line = lines[i].strip()

                # Se a linha for vazia é porque as proximas linhas são para as intruções
                if (line == ''):
                    startedInstructions = True
                    i += 1
                    continue

                if (startedInstructions):
                    # Se começou a parte das instruções e a linha começa com 0x é porque está indicando o endereço que começa as instruções, então devemos armazenar no registrador PC
                    if (line.startswith('0x')):
                        self.PC = line
                        i += 1
                        continue

                    # No IAS, as instruções são armazenadas em pares (parte esquerda e direita da palavra), então se existir um par de instruções sobrando, junta em uma tupla e armazena
                    if i + 1 < len(lines):
                        nextLine = lines[i + 1].strip()
                        memory.append((line, nextLine))
                        i += 2
                    else: # Se não existir um par, complementa com uma instrução vazia None para não quebrar as tuplas
                        memory.append((line, None))
                        i += 1

                else: # Se não começou as instruções ainda é porque ainda está na parte das variáveis, e cada variável é armazenada em uma palavra inteira
                    memory.append(line)
                    i += 1

        return memory

    # Na operação de leitura da memória, a RAM pega o endereço pelo registador MAR e coloca os dados requisitados no registrador MBR
    def read_data(self, address):
        self.MAR = address
        self.MBR = self.memory[int(self.MAR, 16)].split(' ')[0].strip()

        return self.MBR

    # Na operação de escrita da memória, a RAM pega o endereço pelo registadro MAR e os dados que vão ser armazenados pelo registrador MBR
    def write_data(self, address, data, fieldLeft=True):
        self.MAR = address
        self.MBR = data

        # Verificando o tipo de escrita, caso o valor seja uma tupla, então é uma escrita de instrução
        if (isinstance(self.memory[int(self.MAR, 16)], tuple)):
            if (fieldLeft == True): # Armazenando instrução na parte esquerda
                newLine = (self.MBR, self.memory[int(self.MAR, 16)][1])

            if (fieldLeft == False): # Armazenando instrução na parte direita
                newLine = (self.memory[int(self.MAR, 16)][0], self.MBR)

            self.memory[int(self.MAR, 16)] = newLine
        else: # Se não for uma tupla, é porque é uma variável então precisa armazenar o dado e o endereço na frente (0 0x00) seguindo o padrão da RAM
            self.memory[int(self.MAR, 16)] = str(self.MBR) + ' ' + str(self.MAR)

    # No ciclo de busca da instrução esquerda o endereço da proxima palavra (PC) é armazenado no registrador MAR e a palavra requisitada é colocado no MBR
    def cycle_fetch_instruction_left(self):
        self.MAR = self.PC
        self.MBR = self.memory[int(self.MAR, 16)]

        # IAS busca instruções em pares, a primeira parte (0:19) vai para a IR e a segunda (20:39) vai para IBR
        self.IBR = self.MBR[1]

        # Condicional para EXIT pois é uma instrução especial e precisa ser tratado para não quebrar o código
        if (self.MBR[0] == 'EXIT'):
            self.IR = self.MBR[0]
            newPC = int(self.PC, 16) + 1
            self.PC = f"0x{newPC:02X}"
            return

        # A primeira parte da palavra (0:19) é divida em instrução (opcode) que é armazenada no IR e endereço que a instrução utiliza que é armazenada em MAR
        self.IR = self.MBR[0].split('(')[0].strip()
        self.MAR = self.MBR[0].split('(')[1].strip().split(')')[0].strip()

        # INCREMENTO DO PC
        newPC = int(self.PC, 16) + 1
        self.PC = f"0x{newPC:02X}"

    def cycle_fetch_instruction_right(self):
        # Se a ultima instrução que foi executada for a esquerda e não houve desvio condicional, só puxar a instrução que está armazenada no IBR (que é a segunda parte da palavra)
        if (self.last_instruction_was_left and (not self.jumpedRight)):
            if(self.IBR == 'EXIT'): # Tratamento para instrução especial EXIT para não quebrar
                self.IR = self.IBR
                return

            self.IR = self.IBR.split('(')[0].strip()
            self.MAR = self.IBR.split('(')[1].strip().split(')')[0].strip()
        else:
            # Se chegou aqui é porque houve desvio condicional então temos que buscar uma palavra nova com o endereço que está em PC
            self.MAR = self.PC
            self.MBR = self.memory[int(self.MAR, 16)]

            if(self.MBR[1] == 'EXIT'): # Tratamento para instrução especial EXIT para não quebrar
                newPC = int(self.PC, 16) + 1
                self.PC = f"0x{newPC:02X}"
                return

            self.IR = self.MBR[1].split('(')[0].strip()
            self.MAR = self.MBR[1].split('(')[1].strip().split(')')[0].strip()

            # INCREMENTO DO PC
            newPC = int(self.PC, 16) + 1
            self.PC = f"0x{newPC:02X}"

    def cycle_exec_instruction(self):
        # Swith case para cada tipo de instrução que está em IR
        match self.IR:
            case "LOAD M": # Lê o dado que está no endereço MAR e armazena em AC
                self.AC = self.read_data(self.MAR)
                return

            case "LOAD MQ M": # Lê o dado que está no endereço MAR e armazena em MQ
                self.MQ = self.read_data(self.MAR)
                return

            case "LOAD MQ": # Carrega o valor de MQ em AC
                self.AC = self.MQ
                return

            case "LOAD |M": # Lê o dado que está no endereço MAR e armazena o absoluto desse dado em AC
                self.AC = abs(self.read_data(self.MAR))
                return

            case "LOAD -M": # Lê o dado que está no endereço MAR e armazena o valor vezes (-1) desse dado em AC
                dataNegative = int(self.read_data(self.MAR)) * (-1)
                self.AC = str(dataNegative)
                return

            # Existem dois tipos de STOR M, um para armazenar dados e outro para modificar instrução
            case "STOR M":
                # Se o endereço que estiver no registrador MAR for do tipo '0x00', então é a escrita de um dado
                if (len(self.MAR.split(' ')) == 1):
                    self.write_data(self.MAR, self.AC)
                else: # Se o endereço que estiver no registrador MAR for do tipo '0x00 8:19' é uma modificação de endereço da instrução
                    if(self.MAR.split(' ')[1].strip() == '8:19'): # Modificando a parte esquerda da palavra
                        self.MAR = self.MAR.split(' ')[0].strip()
                        oldInstruction = self.memory[int(self.MAR, 16)]

                        # Se a instrução que vai ser modificada é do tipo JUMP ou STOR tem que ser armazenado diferente pois os endereços indicam se é parte esquerda (0:19) ou direita (20:39)
                        if (oldInstruction[0].split('(')[0].strip().startswith('JUMP')):
                            newInstruction = oldInstruction[0].split('(')[0].strip() + '(' + str(self.AC) + ' ' + oldInstruction[0].split('(')[1].split(' ')[1]
                        elif (oldInstruction[0].split('(')[0].strip().startswith('STOR')):
                            endTemp = oldInstruction[0].split('(')[1].split(')')[0]
                            if(len(endTemp.split(' ')) == 1):
                                newInstruction = oldInstruction[0].split('(')[0].strip() + '(' + str(self.AC) + ')'
                            else:
                                newInstruction = oldInstruction[0].split('(')[0].strip() + '(' + str(self.AC) + ' ' + oldInstruction[0].split('(')[1].split(' ')[1]
                        else:
                            newInstruction = oldInstruction[0].split('(')[0].strip() + '(' + str(self.AC) + ')'
                        self.write_data(self.MAR, newInstruction, True)

                    elif(self.MAR.split(' ')[1].strip() == '28:39'): # Modificando parte direita da palavra, mesmo tratamento da esquerda
                        self.MAR = self.MAR.split(' ')[0].strip()
                        oldInstruction = self.memory[int(self.MAR, 16)]
                        if (oldInstruction[1].split('(')[0].strip().startswith('JUMP')):
                            newInstruction = oldInstruction[1].split('(')[0].strip() + '(' + str(self.AC) + oldInstruction[1].split('(')[1].split(' ')[1]
                        else:
                            newInstruction = oldInstruction[1].split('(')[0].strip() + '(' + str(self.AC) + ')'
                        self.write_data(self.MAR, newInstruction, False)
                    else:
                        print("Erro execução STOR M")

            case "ADD M": # Lê o dado que está no endereço MAR e soma com o valor do registrador AC e armazena em AC 
                self.AC = int(self.AC) + int(self.read_data(self.MAR))
                return

            case "ADD |M": # Lê o dado que está no endereço MAR e soma o valor absoluto desse dado com o valor do registrador AC e armazena em AC 
                self.AC = int(self.AC) + abs(int(self.read_data(self.MAR)))
                return

            case "SUB M": # Lê o dado que está no endereço MAR e subtrai esse dado com o valor do registrador AC e armazena em AC 
                self.AC = int(self.AC) - int(self.read_data(self.MAR))
                return

            case "SUB |M": # Lê o dado que está no endereço MAR e subtrai o valor absoluto desse dado com o valor do registrador AC e armazena em AC 
                self.AC = int(self.AC) - abs(int(self.read_data(self.MAR)))
                return

            case "MUL M": # Lê o dado que está no endereço MAR e multiplica pelo valor de MQ, armazena em MQ e AC
                self.MQ = int(self.MQ) * int(self.read_data(self.MAR))
                self.AC = self.MQ # De acordo com a documentação do trabalho da unicamp, o IAS armazena tanto em MQ quanto em AC
                return

            case "DIV M": # Divide o valor de AC pelo dado que está em MAR e armazena em MQ, o resta dessa divisão é armazenada em AC
                self.MQ = int(self.AC) / int(self.read_data(self.MAR))
                self.AC = int(self.AC) % int(self.read_data(self.MAR))
                return

            case "RSH": # Desloca os bits do AC para a direita, ou seja divide por 2
                self.AC = self.AC / 2
                return

            case "LSH": # Desloca os bits do AC para a esquerda, ou seja multiplica por 2
                self.AC = self.AC * 2
                return

            case "JUMP M": # Instrução de salto
                if(self.MAR.split(' ')[1].strip() == '0:19'): # Salto para a instrução esquerda (0:19) da palavra armazenada em MAR
                    self.MAR = self.MAR.split(' ')[0].strip()
                    self.PC = self.MAR
                    self.jumpedLeft = True

                elif(self.MAR.split(' ')[1].strip() == '20:39'): # Salto para a instrução direita (20:39) da palavra armazenada em MAR
                    self.MAR = self.MAR.split(' ')[0].strip()
                    self.PC = f"0x{int(self.MAR, 16):02X}"
                    self.jumpedRight = True
                else:
                    print("Error execução JUMP M")

            case "JUMP +M": # Instrução de salto condicional
                if(self.MAR.split(' ')[1].strip() == '0:19'): # Salto para a intrução esquerda (0:19) da palavra armazenada em MAR se AC for maior ou igual a 0
                    self.MAR = self.MAR.split(' ')[0].strip()
                    if (int(self.AC) >= 0):
                        self.PC = f"0x{int(self.MAR, 16):02X}"
                        self.jumpedLeft = True
                    else:
                        self.jumpedLeft = False
                elif(self.MAR.split(' ')[1].strip() == '20:39'): # Salto para a intrução direita (20:39) da palavra armazenada em MAR se AC for maior ou igual a 0
                    self.MAR = self.MAR.split(' ')[0].strip()
                    if (int(self.AC) >= 0):
                        self.PC = f"0x{int(self.MAR, 16):02X}"
                        self.jumpedRight = True
                    else:
                        self.jumpedRight = False
                else:
                    print("Error execução JUMP+ M")

            case "EXIT": # Instrução especial para encerrar o IAS.
                self.running = False
                
        return

    # Função para mostrar a memoria RAM
    def display_ram(self):
        print("Memória RAM:")
        for linha in self.memory:
            print(linha)

    # Função para mostrar os registradores
    def display_registers(self):
        print('Registadores da Unidade de Controle:')
        print('PC: ', self.PC)
        print('IR: ', self.IR)
        print('MAR: ', self.MAR)
        print('MBR: ', self.MBR)
        print('IBR: ', self.IBR, '\n')

        print('Registradores da ULA(Unidade Lógica e Aritmética): \b')
        print('AC: ', self.AC)
        print('MQ: ', self.MQ)
        print('R: ', self.R)
        print('C: ', self.C)
        print('Z: ', self.Z, '\n')
        print('-------------------------------------------------------------------------------------------------------------------------------')

    def run(self):
        print("Inicialização do IAS: ")
        self.display_registers()
        self.display_ram()
        print('-------------------------------------------------------------------------------------------------------------------------------')
        while self.running:
            input("Pressione Enter para começar o ciclo de busca...")

            # Se jumpedLeft for True então executa ciclo de busca esquerda, executa a instrução, coloca last_instruction_was_left como verdadeiro e jumpedLeft desativa
            if(self.jumpedLeft):
                self.cycle_fetch_instruction_left()
                print("APÓS CICLO DE BUSCA: ")
                self.display_registers()
                self.display_ram()
                print('-------------------------------------------------------------------------------------------------------------------------------')
                self.jumpedLeft = False
                self.last_instruction_was_left = True
                self.cycle_exec_instruction()
                print(f"APÓS CICLO DE EXECUCAÇÃO DA INSTRUÇÃO {self.IR}")
                self.display_registers()
                self.display_ram()
                print('-------------------------------------------------------------------------------------------------------------------------------')
                continue

            # Se jumpedRight for True então executa ciclo de busca direita, executa a instrução, jumpedRight desativa
            if(self.jumpedRight):
                self.cycle_fetch_instruction_right()
                print("APÓS CICLO DE BUSCA: ")
                self.display_registers()
                self.display_ram()
                print('-------------------------------------------------------------------------------------------------------------------------------')
                self.jumpedRight = False
                self.last_instruction_was_left = False
                self.cycle_exec_instruction()
                print(f"APÓS CICLO DE EXECUCAÇÃO DA INSTRUÇÃO {self.IR}")
                self.display_registers()
                self.display_ram()
                print('-------------------------------------------------------------------------------------------------------------------------------')
                continue

            # Se last_instruction_was_left for falso, então executa o ciclo de busca esquerda
            if(not self.last_instruction_was_left):
                self.cycle_fetch_instruction_left()
                print("APÓS CICLO DE BUSCA: ")
                self.display_registers()
                self.display_ram()
                print('-------------------------------------------------------------------------------------------------------------------------------')
                self.last_instruction_was_left = True
            else: # Se last_instruction_was_left for verdadeiro, então executa o ciclo de busca direita
                self.cycle_fetch_instruction_right()
                print("APÓS CICLO DE BUSCA: ")
                self.display_registers()
                self.display_ram()
                print('-------------------------------------------------------------------------------------------------------------------------------')
                self.last_instruction_was_left = False

            self.cycle_exec_instruction()
            print(f"APÓS CICLO DE EXECUCAÇÃO DA INSTRUÇÃO {self.IR}")
            self.display_registers()
            self.display_ram()
            print('-------------------------------------------------------------------------------------------------------------------------------')

        print("Memória RAM Final:")
        self.display_ram()
        return