import os
import sys
import subprocess
import numpy as np
import matplotlib.pyplot as plt
var=os.listdir("Canciones/")
print(var)
graf=np.zeros(10)
contador=0
Cantidad=int(sys.argv[1])
for i in var:
    plt.figure(figsize=(10,10))
    print("----------------------------------------------------------------------------------------------------------")
    print("------------------------------------%s-----------------------------------------------------"%(i))
    print("----------------------------------------------------------------------------------------------------------")
    p=np.zeros(Cantidad)
    for ventana in range(10,60,10):
        contador2=0
        print("----------------------------------------------------------------------------------------------------------")
        print("Tamaño de la ventana:",ventana)
        for amplitudes in np.arange(0.1,0.6,0.05):
            print("----------------------------------------------------------------------------------------------------------")
            print("Amplitud:",amplitudes)
            print("----------------------------------------------------------------------------------------------------------")
            for a in range(Cantidad):
                os.system('python3 Codificador_Multiple.py Canciones/%s 1 3 5 7 %f %f %i' %(i,amplitudes,amplitudes,ventana))
                s2_out = subprocess.check_output([sys.executable, "Deodificador_multiple.py", "pruebasss.wav","1","3","5","7","%i"%(ventana)])
                p[a]=float(s2_out.decode("utf-8"))
            print("Data Recovery Prom:",np.average(p))
            print("Varianza:",np.std(p))
            graf[contador2]=np.average(p)
            contador2=contador2+1
        with plt.style.context('Solarize_Light2'):
            plt.plot(np.arange(0.1,0.6,0.05),graf)
        contador=contador+1
    plt.title('Archivo Wav: %s'%(i))
    plt.legend(('10 ms','20 ms','30 ms','40 ms', '50 ms'),bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    plt.xlabel("Amplitudes")
    plt.ylabel("Data Recover %")
    plt.savefig('%s.png'%(i))
    plt.close()
    os.system('mv %s.png Resultados_Multiples/'%(i))


# Con subplot
#        if(contador==0):
#            ax1 = plt.subplot(311)
#            plt.plot(range(1,6,1),graf)
#            plt.setp(ax1.get_xticklabels(), visible=False)
#            plt.title('Cancion %s'%(i))
#        if(contador==1):
#            ax2 = plt.subplot(312, sharex=ax1)
#            plt.plot(range(1,6,1),graf)
#            plt.setp(ax2.get_xticklabels(), visible=False)
#        if(contador==2):
#            ax3 = plt.subplot(313, sharex=ax1)
#            plt.plot(range(1,6,1),graf)
    contador=contador+1
