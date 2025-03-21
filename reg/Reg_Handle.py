from reg.regTbl import *
class Reg_Handle:
    def __init__(self, spi):
        self.spi = spi
        # 例化所有的寄存器
        self.reg0  = Reg0()
        self.reg1 = Reg1()
       
        
   
    def read_reg(self,cfg_name):
        address = base_address + regoffset(dict_cfgs[cfg_name])
        reg_inst = getattr(self,dict_cfgs[cfg_name])
        # spi 读
        # reg_inst.values= spi_read(address)
        return getattr(reg_inst.bits,cfg_name)
    
    def write_reg(self,cfg_name, value):
        address = base_address + regoffset(dict_cfgs[cfg_name])
        reg_inst = getattr(self,dict_cfgs[cfg_name])
        setattr(reg_inst.bits,cfg_name,value)
        print('write',dict_cfgs[cfg_name],reg_inst.value)
        # spi 写
        #self.spi.write(address, reg_inst.value)
        