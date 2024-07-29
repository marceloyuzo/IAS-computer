class RAM:
    def __init__(self, ram_file):
        self.memory = []
        self.load_memory(ram_file)

    def load_memory(self, ram_file):
        with open(ram_file, 'r') as file:
            for line in file:
                self.memory.append(line.strip())
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
            if(line.startswith('0x') and (not startedInstructions)):
                startedInstructions = True
                self.PC = line

    def read_data(self, address, memoryRam):
        self.MAR = address
        self.MBR = memoryRam.read_ram(self.MAR)

    # def write_data(self, address, data, memoryRam):
    #    self.MAR = address
    #    self.MBR = data

    def cycle_fetch(self):
       pass

    def cycle_exec(self):
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

