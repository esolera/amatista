from __main__ import *
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sys
SYNDROME_CHECK = [-1, 6, 5, 0, 4, 1, 2, 3]

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
def metadatos(matriz_in,retaso0,retraso1):
    matrix_out=np.zeros(len(matriz_in))
    restaso1_n=int((retraso1*rate)/1000)
    restaso0_n=int((retraso0*rate)/1000)
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
def correcion_errores(metadatos,Numero_ventanas):
    numero_hamming=int(Numero_ventanas/8)
    ventanas_nohamming=Numero_ventanas-numero_hamming*8
    ventanas_hamming=numero_hamming*8
    datos_proscesar=metadatos[:ventanas_hamming]
    datos_div_8=np.reshape(datos_proscesar,(numero_hamming,8))
    metadatos_recuperados=np.empty( shape=(0, 0) )
    for i in range(numero_hamming):
        out=0
        for bit in datos_div_8[i]:
            out = (out << 1) | int(bit)
        dato,ls_error,ls_corrected=hamming_decode_byte(out)
        codif_en_int=hamming_encode_nibble(dato)
        array_hamming=[int(x) for x in bin(codif_en_int)[2:]]
        array_hamming=np.asarray(array_hamming)
        while (len(array_hamming)<8):
            array_hamming=np.insert(array_hamming,0,0)
        metadatos_recuperados=np.append(metadatos_recuperados,array_hamming)
    metadatos_recuperados=np.append(metadatos_recuperados,metadatos[-ventanas_nohamming:])
    return metadatos_recuperados

def hamming_decode_byte(byte):
    """
    Decode a single hamming encoded byte, and return a decoded nibble.
    Input is in form P H2 H1 H0 D3 D2 D1 D0
    Decoded nibble is in form 0b0000DDDD == 0 0 0 0 D3 D2 D1 D0
    """
    error = 0
    corrected = 0

    # Calculate syndrome
    s = [0, 0, 0]

    # D1 + D2 + D3 + H0
    s[0] = (extract_bit(byte, 1) + extract_bit(byte, 2) +
            extract_bit(byte, 3) + extract_bit(byte, 4)) % 2

    # D0 + D2 + D3 + H1
    s[1] = (extract_bit(byte, 0) + extract_bit(byte, 2) +
            extract_bit(byte, 3) + extract_bit(byte, 5)) % 2

    # D0 + D1 + D3 + H2
    s[2] = (extract_bit(byte, 0) + extract_bit(byte, 1) +
            extract_bit(byte, 3) + extract_bit(byte, 6)) % 2

    syndrome = (s[0] << 2) | (s[1] << 1) | s[2]

    if syndrome:
        # Syndrome is not 0, so correct and log the error
        error += 1
        byte ^= (1 << SYNDROME_CHECK[syndrome])
        corrected += 1

    # Check parity
    p = 0
    for i in range(0, 7):
        p ^= extract_bit(byte, i)

    if p != extract_bit(byte, 7):
        # Parity bit is wrong, so log error
        if syndrome:
            # Parity is wrong and syndrome was also bad, so error is not corrected
            corrected -= 1
        else:
            # Parity is wrong and syndrome is fine, so corrected parity bit
            error += 1
            corrected += 1

    return ((byte & 0x0f), error, corrected)

def extract_bit(byte, pos):
    """
    Extract a bit from a given byte using MS ordering.
    ie. B7 B6 B5 B4 B3 B2 B1 B0
    """
    return (byte >> pos) & 0x01
def hamming_encode_nibble(data):
    """
    Encode a nibble using Hamming encoding.
    Nibble is provided in form 0b0000DDDD == 0 0 0 0 D3 D2 D1 D0
    Encoded byte is in form P H2 H1 H0 D3 D2 D1 D0
    """
    # Get data bits
    d = [0, 0, 0, 0]
    d[0] = extract_bit(data, 0)
    d[1] = extract_bit(data, 1)
    d[2] = extract_bit(data, 2)
    d[3] = extract_bit(data, 3)

    # Calculate hamming bits
    h = [0, 0, 0]
    h[0] = (d[1] + d[2] + d[3]) % 2
    h[1] = (d[0] + d[2] + d[3]) % 2
    h[2] = (d[0] + d[1] + d[3]) % 2
     # Calculate parity bit, using even parity
    p = 0 ^ d[0] ^ d[1] ^ d[2] ^ d[3] ^ h[0] ^ h[1] ^ h[2]

    # Encode byte
    encoded = (data & 0x0f)
    encoded |= (p << 7) | (h[2] << 6) | (h[1] << 5) | (h[0] << 4)

    return encoded

#----------------------------------------------------------------------------------------------------------------
#--------------------------------Lectura del Wav-----------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
file_rep=sys.argv[1]
rate, data = wavfile.read('pruebasss.wav')
#----------------------------------------------------------------------------------------------------------------
#-------------------------------------Parametros-----------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
ventana_size=int(sys.argv[4])
retraso1=int(sys.argv[2])
retraso0=int(sys.argv[3])
#----------------------------------------------------------------------------------------------------------------
#-------------------------------------Enventanado----------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
Datos_enventanado=enventanado(data,rate,ventana_size)
filas=len(Datos_enventanado)
#----------------------------------------------------------------------------------------------------------------
#-------------------------------------filtrado de hamming--------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
filtro=np.hamming(len(Datos_enventanado[0]))
for i in range(len(Datos_enventanado)):
    Datos_enventanado[i]=Datos_enventanado[i]*filtro
#----------------------------------------------------------------------------------------------------------------
#--------------------------------Calculo de la autocorrelacion de Ceptro----------------------------------------
#----------------------------------------------------------------------------------------------------------------
autocor=autocorrelacion_ceptro(Datos_enventanado)
#----------------------------------------------------------------------------------------------------------------
#--------------------------------Obtencion metadatos-------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
nuevos_metadatos=metadatos(autocor,retraso0,retraso1)
meta_original = genfromtxt('meta.csv', delimiter=',')
#----------------------------------------------------------------------------------------------------------------
#--------------------------------Comparacion Metadatos-----------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
numero_datos_correctos=comparing(meta_original,nuevos_metadatos)
#----------------------------------------------------------------------------------------------------------------
#--------------------------------Porcentaje----------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
procentaje=(numero_datos_correctos/(len(Datos_enventanado)-1))*100
#----------------------------------------------------------------------------------------------------------------
#--------------------------------Reportaje----------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
#print("----------------------------------------------------------------------------------------------------------")
#print("------------------------------------Decodificaion----------------------------------------------------------")
meta_corregidos=correcion_errores(nuevos_metadatos,filas)

numero_datos_correctos=comparing(meta_original,meta_corregidos)
procentaje=(numero_datos_correctos/(len(Datos_enventanado)-1))*100
print(procentaje)
