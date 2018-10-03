#Convertir a minusculas, stop words y lemanizar
import csv
import numpy as np #Importamos la utileria de Numpy
################# CARGA DEL DICCIONAIO DE STOP WORDS ##############################
def stop_word():
    with open('/home/cgg/Downloads/stopwords01.txt','r', encoding = 'utf8') as stopw:
         stopwords = []
         for linea in stopw:
             stopwords.append(linea.rstrip())
         return stopwords
############## FUNNCION QUE QUITA LAS MALAS PALABRAS #############################
def quita_stopw(minusculas,carga_stop):
    minus1  = []
    for palabra in minusculas:
        if palabra not in carga_stop:
           minus1.append(palabra)
    return minus1
############### LEMATIZADOR #####################################################
def CargarDiccionarioLemas():
    file=open("/home/cgg/Downloads/diccionarioLematizador.txt","rb")
    lema_d={}

    for line in file:
        #print(line)
        bloques = line.split()
        palabra = bloques[0]
        lema = bloques[1]
        #print("i",a,b)
        #print( bloques[0],bloques[1])
        lema_d.update({palabra:lema})
    return lema_d

def lematizador(lema_d,palabra):
    palabra=palabra.lower()
    if palabra in lema_d:
        lema = str(lema_d.get(palabra))
    else:
        lema = palabra
    return lema

def run_lematizador(stopwords,lema_d):
    lemati = []
    for palabra in stopwords:
        if palabra not in ['', '\n', '"\n', "\n", ""]:
           lemati.append(lematizador(lema_d,palabra))
    return lemati
############# FUNCION QUE CONVIERTE LAS PALABRAS MINUSCULAS ######################
def conv_min(palabra):
    minus = []
    for i in palabra:
        minus.append(i.lower())
    return minus
################  CALCULA EL TAMANO MAXIMO DE FILA ########################
def tam_max(matriz_doc,tam_reng):
    j = 0
    for i in range(tam_reng):
        if j < len(matriz_doc[i]):
            j = len(matriz_doc[i])
    return j
################  VECTOR CONSULTA ##########################################
def vector_consulta(matriz_doc,tam_ren):
    vector_c = []
    for j in range(tam_ren):
        for i in matriz_doc[j]:
            if i not in vector_c:
                vector_c.append(i) 
    return vector_c
###############   MATRIZ RESULTANTE ###########################################
def matriz_resultante(vector,matriz_doc,tam_matriz,tam_max_r):
     x = np.zeros((tam_matriz,tam_max_r))
     k = 0
     for j in range(tam_matriz):
         for i in matriz_doc[j]:
             if i in vector:
                x[j,k] = 1 
             k += 1
         k = 0
     return x
################  EJECUCION PRINCIPAL DEL PROGRAMA  ############################
carga_stop = stop_word() # Carga de diccionrio de malas palabras
lema_d = CargarDiccionarioLemas() # Carga de diccionario lematizador
with open('/home/cgg/Practicas/noticias01.csv', 'r', encoding = 'utf8', errors = 'ignore') as f:
#with open('/home/cgg/Downloads/noticias.csv', 'r', encoding = 'utf8', errors = 'ignore') as f:
    minusculas = []
    stopwords = []
    matriz_doc = [] 
    for linea in f:
        linea1 = linea.replace("\r\n", " ") # Eliminamos los caracteres de retorno 
        lista_palabras = linea1.split(" ")
        minusculas = conv_min(lista_palabras)
        stopwords = quita_stopw(minusculas,carga_stop)
        matriz_doc.append(run_lematizador(stopwords,lema_d))
    tam_matriz = len(matriz_doc)
    tam_max_r = tam_max(matriz_doc,tam_matriz)
    vector = vector_consulta(matriz_doc,tam_matriz)
    matriz_r = matriz_resultante(vector,matriz_doc,tam_matriz,tam_max_r)
    print (tam_matriz)
    print ("Tamano max renglon: ",tam_max_r)
    print (vector)
    print ("Tamano vector consulta: " ,len(vector))
    print ("Matriz resultante ")
    print (matriz_r)
