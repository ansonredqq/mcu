from calib.Eq import *
from reg.Reg_Handle import *
# spi例化
#spi = spi()
#handle = Reg_Handle(spi)

handle = Reg_Handle(1)
eq_inst = Eq(handle)
eq_inst.set("ffe_taps", 0x78)
print(eq_inst.get('ffe_taps'))
