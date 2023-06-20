class CountFromBy:
    pass

    def __init__(self,val :int=0, incr :int=1)->None:
        self.val = val
        self.incr = incr
    
    def __repr__(self)->str:
        return f"The value is {self.val}"
    
    def increase(self)->None:
        self.val+=self.incr
    
    
        

a = CountFromBy()
print(a)
a.increase()
a.increase()
print(a)