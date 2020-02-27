import pyrtl




registerFile = pyrtl.MemBlock(bitwidth=16, addrwidth=32, name="registerFile", max_read_ports=2, max_write_ports=2, asynchronous=False, block=None)

instr = pyrtl.Input(bitwidth=32, name='instr')


sample_instructions = [201326592, 286326786, 4202528, 2366177284]
mem = pyrtl.RomBlock(bitwidth=32, addrwidth=2, romdata=sample_instructions, max_read_ports=1)

# variable counter will serve as an address in this example 
counter = pyrtl.Register(bitwidth=2)
counter.next <<= counter + 1


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
alu_out = pyrtl.Output(bitwidth=16, name='alu_out')

# INSTRUCTION DECODE LOGIC

op <<= instr[-6:]
rs <<= instr[-11:-6]
rt <<= instr[-16:-11]
rd <<= instr[-21:-16]
sh <<= instr[-26:-21]
func <<= instr[-32:-26]

r_reg0 = pyrtl.WireVector(bitwidth=16,name='r_reg0')
r_reg1 = pyrtl.WireVector(bitwidth=16,name='r_reg1')
w_data = pyrtl.WireVector(bitwidth=16,name='w_data')
w_reg = pyrtl.WireVector(bitwidth=5,name='w_reg')



# REGISTER DECODE LOGIC
data0 <<= registerFile[rs]
data1 <<= registerFile[rt]
r_reg0 <<= rs
r_reg1 <<= rt
w_data <<= alu_out
w_reg <<= rd
registerFile[w_reg] <<= w_data
# ALU LOGIC

with pyrtl.conditional_assignment:
    with func==int(0x20):
        alu_out |= data0 + data1
    with func==int(0x22):
        alu_out |= data0 - data1
    with func==int(0x24):
        alu_out |= data0 and data1
    with func==int(0x25):
        alu_out |= data0 or data1
    with func==int(0x26):
        alu_out |= data0 ^ data1
    with func==int(0x0);
        alu_out |= pyrtl.corecircuits.shift_left_logical(data1, sh)
    with func==int(0x2):
        alu_out |= pyrtl.corecircuits.shift_right_logical(data1, sh)
    with func==int(0x3):
        alu_out |= pyrtl.corecircuits.shift_right_arithmetic(data1, sh)
    with func==int(0x2A)
        alu_out |= data0 > data1
    












