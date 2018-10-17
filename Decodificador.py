import numpy as np
from numpy import genfromtxt
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
def autocorrelacion_ceptro(matrix_in):
    matrix_out=np.zeros(shape=(len(matrix_in),len(matrix_in[0])))
    for i in range(len(matrix_in)):
        matrix_out[i]=np.absolute(np.fft.ifft(np.power(np.absolute(np.log(np.fft.fft(matrix_in[i]))),2)))
    return matrix_out
def metadatos(matriz_in,retaso0,retaso1):
    matrix_out=np.zeros(len(matriz_in)-1)
    restaso1_n=int((retraso1*rate)/1000)
    restaso0_n=int((restaso0*rate)/1000)
    for i in range(len(matriz_in)):
        if(matriz_in[i][restaso0_n-1]<matriz_in[i][restaso1_n-1]):
            matrix_out[i]=1
    return matrix_out
def comparing(meta_original,meta_calculado):
    cont=0
    for i in range(len(meta_original)):
        if(meta_original[i]==meta_calculado[i]):
            cont=cont+1
    return cont




rate, data = wavfile.read('pruebasss.wav')

a=enventanado(data,rate,15)
print("Cantidad de ventanas",len(a))
filtro=np.hamming(len(a[0]))
for i in range(len(a)):
    a[i]=a[i]*filtro
b=autocorrelacion_ceptro(a)
retraso1=3
restaso0=8
c=metadatos(b,restaso0,retraso1)
meta_original = genfromtxt('meta.csv', delimiter=',')
numero_datos_correctos=comparing(meta_original,c)
procentaje=(numero_datos_correctos/(len(a)-1))*100
print(procentaje)
