#Dean Narlock and Justin Tjoa

import pyrtl




rf = pyrtl.MemBlock(bitwidth=16, addrwidth=5, name='rf')

instr = pyrtl.Input(bitwidth=32, name='instr')





# decode data
rs = pyrtl.WireVector(bitwidth=5, name='rs')
rt = pyrtl.WireVector(bitwidth=5, name='rt')
rd = pyrtl.WireVector(bitwidth=5, name='rd')
sh = pyrtl.WireVector(bitwidth=5, name='sh')
func = pyrtl.WireVector(bitwidth=6, name='func')

# ALU input data
data0 = pyrtl.WireVector(bitwidth=16, name='data0')
data1 = pyrtl.WireVector(bitwidth=16, name='data1')

# ALU output data
alu_out = pyrtl.WireVector(bitwidth=16, name='alu_out')

# INSTRUCTION DECODE LOGIC

rs <<= instr[21:26]
rt <<= instr[16:21]
rd <<= instr[11:16]
sh <<= instr[6:11]
func <<= instr[0:6]

r_reg0 = pyrtl.WireVector(bitwidth=16,name='r_reg0')
r_reg1 = pyrtl.WireVector(bitwidth=16,name='r_reg1')
w_data = pyrtl.WireVector(bitwidth=16,name='w_data')
w_reg = pyrtl.WireVector(bitwidth=5,name='w_reg')



# REGISTER DECODE LOGIC
data0 <<= rf[rs]
data1 <<= rf[rt]
r_reg0 <<= rs
r_reg1 <<= rt
w_data <<= alu_out
w_reg <<= rd
rf[w_reg] <<= w_data
# ALU LOGIC



with pyrtl.conditional_assignment:
    with func==int(0x20):
        value = data0 + data1
        alu_out |= value
    with func==int(0x22):
        value = data0 - data1
        alu_out |= value
    with func==int(0x24):
        value = data0 & data1
        alu_out |= value
    with func==int(0x25):
        value = data0 | data1
        alu_out |= value
    with func==int(0x26):
        value = data0 ^ data1
        alu_out |= value
    with func==int(0x0):
        alu_out |= pyrtl.corecircuits.shift_left_logical(data1, sh)
    with func==int(0x2):
        alu_out |= pyrtl.corecircuits.shift_right_logical(data1, sh)
    with func==int(0x3):
        alu_out |= pyrtl.corecircuits.shift_right_arithmetic(data1, sh)
    with func==int(0x2A):
        value = data0 > data1
        alu_out |= value
    

