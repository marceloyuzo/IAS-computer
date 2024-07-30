class IAS:
    def __init__(self, ram_file):
        # Inicializando os registradores'
        self.running = True
        self.last_instruction_was_left = False
        self.jumped = False
        self.MAR = None
        self.IR = None
        self.IBR = None
        self.MBR = None
        self.AC = 0
        self.MQ = 0
        self.R = 0
        self.C = 0
        self.Z = 0
        self.memory = self.load_memory(ram_file)

        # Percorrendo memoria RAM para inicializar o registrador PC com o endereço da primeira instrução
        startedInstructions = False
        for line in self.memory:
            if (line.startswith('0x') and (not startedInstructions)):
                startedInstructions = True
                self.PC = line
                break

    def load_memory(self, ram_file):
        memory = []
        with open(ram_file, 'r') as file:
            lines = file.read().splitlines()
            startedInstructions = False
            i = 0

            while (i < len(lines)):
                line = lines[i].strip()

                if (line.startswith('0x') and (not startedInstructions)):
                    startedInstructions = True
                    memory.append(line)
                    i += 1
                    continue

                if (startedInstructions):
                    if i + 1 < len(lines):
                        nextLine = lines[i + 1].strip()
                        memory.append((line, nextLine))
                        i += 2
                    else:
                        memory.append((line, None))
                        i += 1

                else:
                    memory.append(line)
                    i += 1

        return memory

    def read_data(self, address):
        self.MAR = address
        self.MBR = self.memory[int(self.MAR, 16)]
        if(isinstance(self.MBR, tuple)):
          return self.MBR
        else:
          self.MBR = self.MBR.split(' ')[0]

        return self.MBR

    def write_data(self, address, data, field):
        self.MAR = address
        self.MBR = data

        # verificando o tipo de escrita, caso o valor seja uma tupla, então é uma escrita de instrução
        if (isinstance(self.memory[int(self.MAR, 16)], tuple)):
            if (field == 0):
                newLine = (self.MBR, self.memory[int(self.MAR, 16)][1])

            if (field == 1):
                newLine = (self.memory[int(self.MAR, 16)][0], self.MBR)

            self.memory[int(self.MAR, 16)] = newLine
        else:
            self.memory[int(self.MAR, 16)] = self.MBR + '' + self.MAR
            # talvez chamar uma funcao memoryRam.write_ram para atualizar o arquivo txt, depende se o prof quer

    def cycle_fetch_instruction_left(self):
        self.MAR = self.PC
        self.MBR = self.memory[int(self.MAR, 16)]

        self.IBR = self.MBR[1]

        divider = self.MBR[0].split(',')
        self.IR = divider[0]
        self.MAR = divider[1] if len(divider) > 1 else None

        # INCREMENTO DO PC
        newPC = int(self.PC, 16) + 1
        self.PC = f"0x{newPC:02X}"

    def cycle_fetch_instruction_right(self):
        # DESCOBRIR COMO SABER SE A ULTIMA INSTRUÇÃO EXECUTADA FOI A ESQUERDA
        print(self.IR)

        if (self.IR in ["JUMP M(X 0:19)", "JUMP M(X 20:39)", "JUMP+ M(X 0:19)", "JUMP+ M(X 20:39)"]):
            self.MAR = self.PC
            self.MBR = self.memory[int(self.MAR, 16)]

            divider = self.MBR[0].split(',')
            self.IR = divider[0]
            self.MAR = divider[1] if len(divider) > 1 else None

            # INCREMENTO DO PC
            newPC = int(self.PC, 16) + 1
            self.PC = f"0x{newPC:02X}"
        else:
            divider = self.IBR.split(',')
            self.IR = divider[0]
            self.MAR = divider[1] if len(divider) > 1 else None

    def cycle_exec_instruction(self):
        # Se a instrução for de busca
        match self.IR:
            case "LOAD M(X)":
                self.load_mx()

            case "LOAD MQ M(X)":
                self.load_mq_mx()

            case "STOR M(X)":
                self.stor_mx()

            case "LOAD MQ":
                self.load_mq()

            case "LOAD |M(X)|":
                self.load_mx_absolute()

            case "LOAD -M(X)":
                self.load_mx_negative()

            case "ADD M(X)":
                self.add_mx()

            case "ADD |M(X)|":
                self.add_mx_absolute()

            case "SUB M(X)":
                self.sub_mx()

            case "SUB |M(X)|":
                self.sub_mx_absolute()

            case "MUL M(X)":
                self.mul_mx()

            case "DIV M(X)":
                self.div_mx()

            case "RSH":
                self.rsh()

            case "LSH":
                self.lsh()

            case "JUMP M(X 0:19)":
                self.jump_m_left()

            case "JUMP M(X 20:39)":
                self.jump_m_right()

            case "JUMP+ M(X 0:19)":
                self.jump_plus_m_left()

            case "JUMP+ M(X 20:39)":
                self.jump_plus_m_right()

            case "STOR M(X 8:19)":
                self.stor_m_left()

            case "STOR M(X 28:39)":
                self.stor_m_right()

            case "EXIT":
                self.running = False
        return

    # INSTRUÇÕES DE TRANSFERÊNCIA DE DADOS
    def load_mx(self):
        self.AC = self.read_data(self.MAR)
        return

    def load_mq_mx(self):
        self.MQ = self.read_data(self.MAR)
        return

    def stor_mx(self):
        self.write_data(self.MAR, str(self.AC), None)
        return

    def load_mq(self):
        self.AC = self.MQ
        return

    def load_mx_absolute(self):
        self.AC = abs(self.read_data(self.MAR))
        return

    def load_mx_negative(self):
        dataNegative = int(self.read_data(self.MAR)) * (-1)
        self.AC = str(dataNegative)
        return

    # INSTRUÇÕES ARITMÉTICAS

    def add_mx(self):
        self.AC = int(self.AC) + int(self.read_data(self.MAR))
        return

    def add_mx_absolute(self):
        self.AC = int(self.AC) + abs(int(self.read_data(self.MAR)))
        return

    def sub_mx(self):
        self.AC = int(self.AC) - int(self.read_data(self.MAR))
        return

    def sub_mx_absolute(self):
        self.AC = int(self.AC) - abs(int(self.read_data(self.MAR)))
        return

    def mul_mx(self):
        self.AC = int(self.MQ) * int(self.read_data(self.MAR))
        return

    def div_mx(self):
        self.MQ = int(self.AC) / int(self.read_data(self.MAR))
        self.AC = int(self.AC) % int(self.read_data(self.MAR))
        return

    def rsh(self):
        return

    def lsh(self):
        return

    # INSTRUÇÕES DE SALTO

    def jump_m_left(self):
        if (isinstance(self.memory[int(self.MAR, 16)], tuple)):  
            self.PC = self.MAR
            self.jumped = True
        else:
            self.jumped = False


    def jump_m_right(self):
        if (isinstance(self.memory[int(self.MAR, 16)], tuple)):  
            self.PC = self.MAR
            self.jumped = True
        else:
            self.jumped = False

    def jump_plus_m_left(self):
        if (self.AC >= 0):
            self.jump_m_left()
            self.jumped = True
        else: 
            self.jumped = False

    def jump_plus_m_right(self):
        if (int(self.AC) >= 0):
            self.jump_m_right()
            self.jumped = True

        else: 
            self.jumped = False


    # INSTRUÇÕES DE MODIFICAÇÃO DE ENDEREÇO

    def stor_m_left(self):
        return

    def stor_m_right(self):
        return

    # FUNÇÕES PARA DISPLAY

    def display_ram(self):
        print(self.memory)

    def display_registers(self):
        print('Registadores da Unidade de Controle:')
        print('MAR: ', self.MAR)
        print('IR: ', self.IR)
        print('IBR: ', self.IBR)
        print('PC: ', self.PC, '\n')

        print('Registradores da ULA(Unidade Lógica e Aritmética): \b')
        print('MBR: ', self.MBR)
        print('AC: ', self.AC)
        print('MQ: ', self.MQ)
        print('R: ', self.R)
        print('C: ', self.C)
        print('Z: ', self.Z, '\n')
        print('------------------------------------------')

    def run(self):
        print("Inicialização do IAS: ")
        self.display_registers()
        self.display_ram()
        while self.running:
            input("Pressione Enter para continuar para a próxima instrução...")

            if self.jumped:
                if self.IR in ["JUMP+ M(X 0:19)", "JUMP M(X 0:19)"]:
                    self.cycle_fetch_instruction_left()
                    self.last_instruction_was_left = True
                    
                else:
                    self.cycle_fetch_instruction_right()
                    self.last_instruction_was_left = False

                print("REGISTRADORES APOS CICLO DE BUSCA")
                self.display_registers()
                self.cycle_exec_instruction()
                print("REGISTRADORES APOS CICLO DE EXECUCAO")
                self.display_registers()

            else:
                if self.last_instruction_was_left:
                    self.cycle_fetch_instruction_right()
                    self.last_instruction_was_left = False
                else:
                    self.cycle_fetch_instruction_left()
                    self.last_instruction_was_left = True

                print("REGISTRADORES APOS CICLO DE BUSCA")
                self.display_registers()
                self.cycle_exec_instruction()
                print("REGISTRADORES APOS CICLO DE EXECUCAO")
                self.display_registers()


        return