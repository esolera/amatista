import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def enventanado (data,rate,tiempo):
    num_columnas=int(rate*(tiempo/1000)) # datos por ventana
    num_filas=int(len(data)/num_columnas)+1 #cantidad de ventanas
    zero_adding=(num_filas*num_columnas)-len(data)
    datos_with_zeros=np.pad(data, (0, zero_adding), 'constant')
    matriz_datos = np.reshape(datos_with_zeros, (num_filas, num_columnas))
    return matriz_datos

def matrix_H(metadatos,retraso_1,retraso_0,Amplitud1,Amplitud0,filas,rate):

    retraso1_muestras=int((retraso_1*rate)/1000)#retraso en muestras de 1
    retraso0_muestras=int((retraso_0*rate)/1000)#retraso en muestras de 0
    matrix = np.zeros(shape=(filas,retraso0_muestras))#array lleno de 0
    for i in range(len(metadatos)):
        matrix[i][0]=1
        if(metadatos[i]==0):
            matrix[i][retraso0_muestras-1]=Amplitud0
        else:
            matrix[i][retraso1_muestras-1]=Amplitud1
    return matrix

def convolucion_arreglos(matrix_data,matrix_H):
    result_matrix=np.zeros(shape=(len(matrix_data),(len(matrix_data[0])+len(matrix_H[0])-1)))
    for i in range(len(matrix_data)):
        result_matrix[i]=np.convolve(matrix_data[i],matrix_H[i],mode='full')
    return result_matrix

def split_and_sum(matrix_conv,matrix_data):
    matrix_result=np.zeros(shape=(len(matrix_data),len(matrix_data[0])))
    matrix_in_data=np.zeros(shape=(len(matrix_data),len(matrix_data[0])))
    matrix_save_data=np.zeros(shape=(len(matrix_data)+1,(len(matrix_conv[0])-len(matrix_data[0]))))
    for i in range(len(matrix_data)):
        matrix_in_data[i]=matrix_conv[i][:len(matrix_data[0])]
        matrix_save_data[i+1]=matrix_conv[i][-(len(matrix_conv[0])-len(matrix_data[0])):]
        matrix_in_data[i][:(len(matrix_conv[0])-len(matrix_data[0]))]=matrix_in_data[i][:(len(matrix_conv[0])-len(matrix_data[0]))]+matrix_save_data[i]

    matriz_datos = np.reshape(matrix_in_data,(len(matrix_in_data)*len(matrix_in_data[1])))
    return matriz_datos




rate, data = wavfile.read('Market.wav')
datos=np.asarray(data)
datos=datos.astype(float)
if (data.dtype==datos.astype(np.uint8).dtype):
    datos=(datos-128)/256
if (data.dtype==datos.astype(np.uint16).dtype):
    datos=(datos-32768)/65536
a=enventanado(datos,rate,45)
filas=len(a)
metadatos=np.random.randint(2, size=len(a))
np.savetxt('meta.csv', metadatos.astype(np.uint8), delimiter=',')
retraso1=3
restaso2=7
b=matrix_H(metadatos,retraso1,restaso2,0.0005,0.0005,filas,rate)
restaso1_n=int((retraso1*rate)/1000)
restaso2_n=int((restaso2*rate)/1000)
print("retraso_1:",restaso1_n)
print("retraso_0:",restaso2_n)
print("Cantidad ventanas:",filas)
print("Datos por ventana:",len(a[0]))
print("Cantidad metadatos",len(metadatos))
c=convolucion_arreglos(a,b)
y=split_and_sum(c,a)
y=(y*256)+128
if (data.dtype==y.astype(np.uint8).dtype):
    wavfile.write('./pruebasss.wav',rate,y.astype(np.uint8))
if (data.dtype==y.astype(np.uint16).dtype):
    wavfile.write('./pruebasss.wav',rate,y.astype(np.uint16))
