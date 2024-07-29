class RAM:
    def __init__(self, ram_file):
        self.memory = []
        self.load_memory(ram_file)

    def load_memory(self, ram_file):
        startedInstructions = False

        with open(ram_file, 'r') as file:
            lines = file.read().splitlines()
            for i in range(0, len(lines), 2):
                print(i)

        return self.memory

    def display_ram(self):
        print(self.memory)

    def read_ram(self, address):
        return self.memory[int(address, 16)]

#   def write_ram(self, address, data, ram_file):
#     for i in range(len(self.memory)):
#         if(i == int(address, 16)):
#             with open(ram_file, 'w') as file:


#             return self.memory[i]

#     return -1

class IAS:
    def __init__(self, memoryRam):
        # Inicializando os registradores
        self.MAR = None
        self.IR = None
        self.IBR = None
        self.MBR = None
        self.AC = 0
        self.MQ = 0
        self.R = 0
        self.C = 0
        self.Z = 0

        # Percorrendo memoria RAM para inicializar o registrador PC com o endereço da primeira instrução
        startedInstructions = False
        for line in memoryRam.memory:
            if (line.startswith('0x') and (not startedInstructions)):
                startedInstructions = True
                self.PC = line

    def read_data(self, address, memoryRam):
        self.MAR = address
        self.MBR = memoryRam.read_ram(self.MAR)

    def write_data(self, address: str, data: str, memoryRam: RAM):
        self.MAR = address
        self.MBR = data
        memoryRam.memory[int(self.MAR, 16)] = data + ' ' + self.MAR
        # talvez chamar uma funcao memoryRam.write_ram para atualizar o arquivo txt, depende se o prof quer

    def cycle_fetch_instruction(self):
        pass

    def cycle_exec_instruction(self):
        pass

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
