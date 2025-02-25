class HalHash:
    def __init__(self):self.version="0.0.2"
    def array_toHex(arr)->str:
        return "".join([hex(i)[2:] for i in arr])
    def getHalfInt(i,h)->int:
        temp=str(i)
        temp=temp[:len(temp)//2] if h==0 else temp[len(temp)//2:]
        return 0 if temp=="" else int(temp)
    def Str2Hash(self,text:str,length:int,count:int,maxIterration:int=100000):
        return self.Bin2Hash(text.encode("utf8"),length,count,maxIterration)
    def Bin2Hash(self,binary:bytes,length:int,count:int,maxIterration:int=100000):
        #if (len(binary)==1):binary+=b'\0'
        count=length if length<count else count
        count=len(binary) if len(binary)<count else count
        sizeD=len(binary)//count
        g=length*count
        d=[int.from_bytes(binary[i*sizeD:i*sizeD+sizeD],byteorder="big",signed=False)*g for i in range(count)]

        if len(binary)%count:
            d[count-1]=int.from_bytes(binary[count*sizeD-sizeD:],byteorder="big",signed=False)*g

        for i in range(int((length-count)/2)):
            d.append(i+2)
            for b in range(count):
                d[len(d)-1]=d[b]*d[len(d)-1]+g*(i+1)
        count=len(d)
        temp=d.copy()
        g=HalHash.getHalfInt(g,0)+HalHash.getHalfInt(g,1)
        for i in range(count):
            for b in range(count):
        #        d[b]=d[b]+temp[i]+g
                d[b]=d[b]+temp[i]*temp[i]+temp[i]*g
        lc=count-1
        mc=0
        h=""
        while True:
            h=HalHash.array_toHex(d)
            if (len(h)<length):
                for i in range(count):
                    if (i==lc):
                        #d[i]=HalHash.getHalfInt(d[i],0)*HalHash.getHalfInt(d[i],1)+g
                        d[i]=d[i]*2+g
                    else:
                        temp=HalHash.getHalfInt(d[i],0)+HalHash.getHalfInt(d[i],1)
                        d[i]=int(str(temp)+str(HalHash.getHalfInt(d[i+1],0)+HalHash.getHalfInt(d[i+1],1)))
                        d[i+1]=int(str(HalHash.getHalfInt(d[i+1],0)+HalHash.getHalfInt(d[i+1],1))+str(temp))
            elif (len(h)>length):
                if mc>maxIterration:
                    h=h[0:length]
                    break
                for i in range(count):
                    if (i==lc):
                        d[i]=HalHash.getHalfInt(d[i],0)+HalHash.getHalfInt(d[i],1)+g
                    else:
                        temp=HalHash.getHalfInt(d[i],1)
                        d[i]=HalHash.getHalfInt(d[i],0)+HalHash.getHalfInt(d[i+1],1)
                        d[i+1]=HalHash.getHalfInt(d[i+1],0)+temp
            else:
                break
            mc+=1
        return h

hh=HalHash()