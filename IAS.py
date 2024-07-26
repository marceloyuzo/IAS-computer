

class IAS:
    def __init__(self, ram_file):
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
        self.PC = 0

        self.memory = load_memory(ram_file)  # type: ignore

    def load_memory(self, ram_file):
        ram = []
        with open(ram_file, 'r') as ram:
            for line in ram:
                ram.append(line.strip())

        return ram

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

    def display_ram(self):
        print(self.memory)
