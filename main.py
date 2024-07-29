from classes import IAS, RAM

ram_file = 'ram.txt'
memoryRam = RAM(ram_file)
teste = IAS(memoryRam)

teste.display_registers()
# teste.read_data('0X0A', memoryRam)
teste.display_registers()

memoryRam.write_ram('0x00', 2)
