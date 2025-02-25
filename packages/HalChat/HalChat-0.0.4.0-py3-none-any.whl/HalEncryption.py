from HalHash import HalHash

class HalEncryption:
    def __init__(self):
        self.version="0.0.3"
        self.hh=HalHash()

    def shift_forward(self,a:int,b:int):
        o=a+b
        return o-256 if (o>255) else o

    def shift_back(self,a:int,b:int):
        o=a-b
        return 256+o if o<0 else o

    def encode(self,data:bytes,password:str,hashlength:int=256,hashcount:int=64,secretData:str="") -> bytes:
        return self.encodeByHash(data,self.hh.Str2Hash(password,hashlength,hashcount),hashcount,secretData)

    def encodeByHash(self,data:bytes,passw:str,hashcount:int=64,secretData:str="")->bytes:
        out=[]
        a=0
        b=len(passw)-1
        newPassw=self.hh.Str2Hash(passw+passw+secretData,len(passw),hashcount)
        for i in range(len(data)):
            out+=[self.shift_forward(int(data[i]),int(newPassw[a:a+2],16))]
            a+=1
            if a>=b:newPassw=self.hh.Str2Hash(passw+newPassw,len(passw),hashcount);a=0
        return bytes(out)

    def decode(self,data:bytes,password:str,hashlength:int=256,hashcount:int=64,secretData:str="")->bytes:
        return self.decodeByHash(self.hh.Str2Hash(password,hashlength,hashcount),hashcount,secretData)

    def decodeByHash(self,data:bytes,passw:str,hashcount:int=64,secretData:str="")->bytes:
        out=[]
        a=0
        b=len(passw)-1
        newPassw=self.hh.Str2Hash(passw+passw+secretData,len(passw),hashcount)
        for i in range(len(data)):
            out+=[self.shift_back(int(data[i]),int(newPassw[a:a+2],16))]
            a+=1
            if a>=b:newPassw=self.hh.Str2Hash(passw+newPassw,len(passw),hashcount);a=0
        return bytes(out)