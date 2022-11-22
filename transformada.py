import numpy as np
from numpy.linalg import inv
def clarck(va,vb,vc)->np.array:#[alpha;betta]
    M=(2/3)*np.array([[1,-1/2,-1/2],[0,np.sqrt(3)/2,-np.sqrt(3)/2]])
    R=np.matmul(M,[[va],[vb],[vc]])
    return R

def basisChange(m,Vr,Vdc)->np.array:#[d_m,d_(m+1)]
    M=Vdc*np.array([[np.cos((2*np.pi/6)*(m-1)), np.cos((2*np.pi/6)*(m))],[np.sin((2*np.pi/6)*(m-1)), np.sin((2*np.pi/6)*(m))]])
    d=np.matmul(inv(M),Vr)
    return d

def sector(Va,Vb)->int:
    if(Va==0):
        if(Vb>=0):
            m=2
        else:
            m=5
    elif(Va>=0):
        if(2*np.pi/6>np.arctan(Vb/Va) and np.arctan(Vb/Va)>=0):
            m=1
        elif(np.pi/2>np.arctan(Vb/Va) and np.arctan(Vb/Va)>=2*np.pi/6):
            m=2
        elif(0>np.arctan(Vb/Va) and np.arctan(Vb/Va)>=-2*np.pi/6):
            m=6
        elif(-2*np.pi/6>np.arctan(Vb/Va) and np.arctan(Vb/Va)>-np.pi/2):
            m=5
    elif(Va<0):
        if(2*np.pi/6>np.arctan(Vb/Va) and np.arctan(Vb/Va)>=0):
            m=4
        elif(np.pi/2>np.arctan(Vb/Va) and np.arctan(Vb/Va)>=2*np.pi/6):
            m=5
        elif(0>np.arctan(Vb/Va) and np.arctan(Vb/Va)>=-2*np.pi/6):
            m=3
        elif(-2*np.pi/6>np.arctan(Vb/Va) and np.arctan(Vb/Va)>-np.pi/2):
            m=2

    return m




