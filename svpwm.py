import numpy as np
import matplotlib.pyplot as plt
from transformada import clarck,basisChange,sector
import math

#Señales de referencia
freq=60#Hz
Vdc=975
Amp=630#V Vdc*np.cos(np.deg2rad(30)) es el maximo posible sin llegar a sobremodulacion
n=80#Numero de vectores
Ts=(1/freq)/n
l=100#Ts se divide en 100 pasos para simular un continuo
t=np.linspace(0,1/60,n)

S1=Amp*np.cos(2*np.pi*freq*t)#va
S2=Amp*np.cos(2*np.pi*freq*t-2*np.pi/3)#vb
S3=Amp*np.cos(2*np.pi*freq*t+2*np.pi/3)#vc

plt.plot(t,S1,t,S2,t,S3)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend(["S1","S2","S3"])
plt.show()

ref=np.empty((2,len(t)))#Vector referencia [alpha;betta]

#Crea vector de referencia
for i in range(len(t)):
    r=clarck(S1[i],S2[i],S3[i])
    ref[0][i]=r[0]#Valpha
    ref[1][i]=r[1]#Vbetta

pulsos=np.empty((3,7*len(t)))#Una fila por switch y una columna por estado sucesivo. Se usan 5 por periodo para reducir THD
time=np.empty((1,7*len(t)))#Duracion de cada estado
num_rows, num_cols = time.shape
for j in range(len(t)):
    m=sector(ref[0][j],ref[1][j])
    d=basisChange(m,np.array([[ref[0][j]],[ref[1][j]]]),Vdc)#[d_m,d_(m+1)]
    d0=1-d[0]-d[1]

    V0_e0=np.array([0,0,0])
    V0_e1=np.array([1,1,1])

    if(m==1):
        Vm_e=np.array([[1,0,0]])
        Vmp1_e=np.array([[1,1,0]])
        pulsos[:,j*7]=V0_e0
        pulsos[:,j*7+1]=Vm_e
        pulsos[:,j*7+2]=Vmp1_e
        pulsos[:,j*7+3]=V0_e0
        pulsos[:,j*7+4]=Vmp1_e
        pulsos[:,j*7+5]=Vm_e
        pulsos[:,j*7+6]=V0_e0
    elif(m==2):
        Vm_e=np.array([[1,1,0]])
        Vmp1_e=np.array([[0,1,0]])
        pulsos[:,j*7]=V0_e0
        pulsos[:,j*7+1]=Vm_e
        pulsos[:,j*7+2]=Vmp1_e
        pulsos[:,j*7+3]=V0_e0
        pulsos[:,j*7+4]=Vmp1_e
        pulsos[:,j*7+5]=Vm_e
        pulsos[:,j*7+6]=V0_e0
    elif(m==3):
        Vm_e=np.array([[0,1,0]])
        Vmp1_e=np.array([[0,1,1]])
        pulsos[:,j*7]=V0_e0
        pulsos[:,j*7+1]=Vm_e
        pulsos[:,j*7+2]=Vmp1_e
        pulsos[:,j*7+3]=V0_e0
        pulsos[:,j*7+4]=Vmp1_e
        pulsos[:,j*7+5]=Vm_e
        pulsos[:,j*7+6]=V0_e0
    elif(m==4):
        Vm_e=np.array([[0,1,1]])
        Vmp1_e=np.array([[0,0,1]])
        pulsos[:,j*7]=V0_e0
        pulsos[:,j*7+1]=Vm_e
        pulsos[:,j*7+2]=Vmp1_e
        pulsos[:,j*7+3]=V0_e0
        pulsos[:,j*7+4]=Vmp1_e
        pulsos[:,j*7+5]=Vm_e
        pulsos[:,j*7+6]=V0_e0
    elif(m==5):
        Vm_e=np.array([[0,0,1]])
        Vmp1_e=np.array([[1,0,1]])
        pulsos[:,j*7]=V0_e0
        pulsos[:,j*7+1]=Vm_e
        pulsos[:,j*7+2]=Vmp1_e
        pulsos[:,j*7+3]=V0_e0
        pulsos[:,j*7+4]=Vmp1_e
        pulsos[:,j*7+5]=Vm_e
        pulsos[:,j*7+6]=V0_e0
    else:
        Vm_e=np.array([[1,0,1]])
        Vmp1_e=np.array([[1,0,0]])
        pulsos[:,j*7]=V0_e0
        pulsos[:,j*7+1]=Vm_e
        pulsos[:,j*7+2]=Vmp1_e
        pulsos[:,j*7+3]=V0_e0
        pulsos[:,j*7+4]=Vmp1_e
        pulsos[:,j*7+5]=Vm_e
        pulsos[:,j*7+6]=V0_e0

    time[:,j*7]=d0*(1/4)
    time[:,j*7+1]=d[0]/2
    time[:,j*7+2]=d[1]/2
    time[:,j*7+3]=d0*(2/4)
    time[:,j*7+4]=d[1]/2
    time[:,j*7+5]=d[0]/2
    time[:,j*7+6]=d0*(1/4)


#EXTENCION PARA PRUEBA EN TYPHOON

pulsos_T=np.zeros((3,l*n))#l puntos por vector para poder simular el tiempo de cada uno

r=0
k=0 
for i in range(len(time[0,:])):
    h=math.floor(time[0,i]*l)#Numero de entradas que ocupa el vector
    for j in range(h):
        pulsos_T[:,k]=pulsos[:,i]
        k+=1
    if((i+1)%7==0):
        r+=1
        k=r*l



X=range(len(pulsos_T[2,:]))
figure, axis = plt.subplots(3, 1)

# For Sine Function
axis[0].plot(X, pulsos_T[0,:]-pulsos_T[1,:])
axis[0].set_title("S1")

# For Cosine Function
axis[1].plot(X, pulsos_T[1,:]-pulsos_T[2,:])
axis[1].set_title("S2")

# For Tangent Function
axis[2].plot(X, pulsos_T[0,:]-pulsos_T[2,:])
axis[2].set_title("S3")

# Combine all the operations and display
plt.show()
