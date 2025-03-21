class Eq:
    def __init__(self, handle):
        self.handle = handle
        #初始化配置值
        self.ffe_taps =0x10
        self.dfe_taps = 0x23
        handle.write_reg("ffe_taps", self.ffe_taps)
        
    def set(self,name,value):
        setattr(self,name,value)
        self.handle.write_reg(name, value)
        
    def get(self,name):
        return self.handle.read_reg(name)   
    
    

   