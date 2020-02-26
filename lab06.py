import pyrtl




registerFile = pyrtl.MemBlock(bitwidth=16, addrwidth=32, name="registerFile", max_read_ports=2, max_write_ports=2, asynchronous=False, block=None)


sample_instructions = [201326592, 286326786, 4202528, 2366177284]
mem = pyrtl.RomBlock(bitwidth=32, addrwidth=2, romdata=sample_instructions, max_read_ports=1)

# variable counter will serve as an address in this example 
counter = pyrtl.Register(bitwidth=2)
counter.next <<= counter + 1

data = pyrtl.WireVector(bitwidth=32, name='data')
data <<= mem[counter]

# read data stored in rom
data = pyrtl.WireVector(bitwidth=32, name='data')
data <<= mem[counter]

# decode data
op = pyrtl.Output(bitwidth=6, name='op')
rs = pyrtl.Output(bitwidth=5, name='rs')
rt = pyrtl.Output(bitwidth=5, name='rt')
rd = pyrtl.Output(bitwidth=5, name='rd')
sh = pyrtl.Output(bitwidth=5, name='sh')
func = pyrtl.Output(bitwidth=6, name='func')

# ALU input data
data0 = pyrtl.Output(bitwidth=16, name='data0')
data1 = pyrtl.Output(bitwidth=16, name='data1')

# ALU output data
aluOutput = pyrtl.Output(bitwidth=16, name='aluOutput')

# INSTRUCTION DECODE LOGIC

op <<= data[-6:]
rs <<= data[-11:-6]
rt <<= data[-16:-11]
rd <<= data[-21:-16]
sh <<= data[-26:-21]
func <<= data[-32:-26]


# REGISTER DECODE LOGIC
data0 <<= registerFile[rs]
data1 <<= registerFile[rt]

# ALU LOGIC


# ADD: 0hex / 20hex  10 0000
if ((op == 0b00) and (func == 0b100000)): 
    registerFile[rd] = registerFile[rs] + registerFile[rt]
# SUB: 0hex / 22hex  10 0010
if ((op == 0b00) and (func == 0b100010)):
    registerFile[rd] = registerFile[rs] - registerFile[rt]
# AND: 0hex / 24hex  10 0100
if ((op == 0b00) and (func == 0b100100)):
    registerFile[rd] = registerFile[rs] and registerFile[rt]
# OR:  0hex / 25hex  10 0101
if ((op == 0b00) and (func == 0b100101)):
    registerFile[rd] = registerFile[rs] or registerFile[rt];
# XOR: 0hex / 26hex  10 0110
if ((op == 0b00) and (func == 0b100110)):
    registerFile[rd] = registerFile[rs] ^ registerFile[rs];
# SLL: 0hex / 0hex   00 0000
if ((op == 0b00) and (func == 0b000000)):
# SRL: 0hex / 02hex  00 0010
# SRA: 0hex / 03hex  00 0011
# SLT: 0hex / 2Ahex  10 1010









