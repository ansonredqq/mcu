from ctypes import *

# 每32位寄存器的位域定义
class Reg0bits(Structure):
    _fields_ = [("ffe_taps", c_uint32,18),
                ("dfe_taps", c_uint32,14),
    ]    
class Reg0(Union):
    _fields_ = [("bits", Reg0bits),
                ("value", c_uint32),
    ]

class Reg1bits(Structure):
    _fields_ = [( "offset_kp", c_uint32,10),
                ("offset_ki", c_uint32,22),
    ]    
class Reg1(Union):
    _fields_ = [("bits", Reg0bits),
                ("value", c_uint32),
    ]  
    
# 每个配置项对应的寄存器      
dict_cfgs = {
    "ffe_taps": "reg0",
    "dfe_taps": "reg0",
    "offset_kp": "reg1",
    "offset_ki": "reg1",
}    

# 寄存器表排布
base_address = 0x0
class RegTbl(Structure):
    _fields_ = [("reg0", c_uint32),
                ("reg1", c_uint32),          
    ]
    
def regoffset(reg) :
    return getattr(RegTbl,reg).offset 
 