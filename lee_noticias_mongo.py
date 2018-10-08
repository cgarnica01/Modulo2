import nltk
import math
from nltk import word_tokenize, ngrams
import numpy as np 
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import BSON
from bson import json_util
import json

################ OBTENCION DE DATOS DESDE MONGO  #####################
def conexion_mongo(query):
    datos = []
    id_doc = []
    client = MongoClient('localhost', 27017)
    db = client['test']
    db.authenticate('root', 'Cic1234*')
    collection = db["noticias"]
    for doc in collection.find({"$text": {"$search": query}}):
        id_doc.append(doc['_id'])
        datos.append(doc['Texto'])
    return(datos,id_doc)
################# CARGA DE STOP WORDS ###################################
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
        bloques = line.split()
        palabra = bloques[0]
        lema = bloques[1]
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
################  DICCIONARIO DE PALABRAS  ##########################################
def dicc_palabras(matriz_doc,tam_ren):
    dicc_p = []
    for j in range(tam_ren):
        for i in matriz_doc[j]:
            if i not in dicc_p:
                dicc_p.append(i)
    return dicc_p
###############   MATRIZ RESULTANTE ###########################################
def matriz_resultante(dicc,matriz_doc,tam_matriz,tam_dic):
     x = np.zeros((tam_matriz,tam_dic))
     k = 0
     for j in range(tam_matriz):
         for i in matriz_doc[j]:
             if i in dicc:
                x[j,k] = 1
             k += 1
         k = 0
     return x
################ VECTOR CONSULTA ##############################################
def vector_consulta(diccionario,texto,tam_dic):
    x = np.zeros((tam_dic))
    palabras = word_tokenize(texto)
    for word in palabras:
        wordmin = word.lower()
        if wordmin in diccionario:
            x[diccionario.index(wordmin)] = 1
    return x
###############   FUNCION SIMILITUD SENO #######################################
def cosine_similarity(v1,v2):
    sumxx, sumxy, sumyy = 0, 0, 0
    values = {}
    for i in range(len(v2)):
        for j in range(len(v1)):
            x = v1[j]
            y = v2[i,j]
            sumxx += x*x
            sumyy += y*y
            sumxy += x*y
        values[i] = [sumxy/math.sqrt(sumxx*sumyy)]
        sumxx, sumxy, sumyy = 0, 0, 0
    return values
################ OBTENCION DE LOS TOP TEN ######################################
def imprime_topten(top_ten,texto,vector,id_texto):
    doc_final = []
    ini = '{Texto : '
    fin = '}'
    vector_r = ""
    for i in vector:
        vector_r += str(i) + " "
    vector_r = vector_r[:-1]
    for i in top_ten:
        doc_final.append('{id: ' + str(id_texto[i]) + '}' + ini + texto[i] + fin + ',{Vector : ' + vector_r + '}')
    return doc_final
################  EJECUCION PRINCIPAL DEL PROGRAMA  ############################
carga_stop = stop_word() # Carga de diccionario de malas palabras
lema_d = CargarDiccionarioLemas() # Carga de diccionario lematizador
############### CARGA DEL END POINT #########################################
app = Flask(__name__)

@app.route("/")
def hello():
  return "hola mundo"

@app.route('/noticias/<query>',  methods=['GET'])
def getData(query):
    res_con = []
    matriz_doc = []
    doc = []
    texto = []
    id_texto = []
    texto,id_texto = conexion_mongo(query)
    for linea in texto:
        linea1 = linea.replace("\r\n", " ") # Eliminamos los caracteres de retorno, y espacios en blanco 
        lista_palabras = linea1.split(" ") 
        lista_palabras = word_tokenize(linea1) 
        minusculas = conv_min(lista_palabras) # Convertimos en minusculas
        stopwords = quita_stopw(minusculas,carga_stop) # Eliminamos stop words
        matriz_doc.append(run_lematizador(stopwords,lema_d))# Lematizador
    tam_matriz = len(matriz_doc)
    tam_max_r = tam_max(matriz_doc,tam_matriz)
    diccionario = dicc_palabras(matriz_doc,tam_matriz) # Creacion de diccionario
    tam_dic = len(diccionario)
    matriz_r = matriz_resultante(diccionario,matriz_doc,tam_matriz,tam_dic)
    vector = vector_consulta(diccionario,query,tam_dic) # Vector Consulta
    similitud_coseno =  cosine_similarity(vector,matriz_r) # Calculo de similitud coseno
    get_topten = sorted(range(len(list(similitud_coseno))), key=lambda i: list(similitud_coseno[i]), reverse=True)[:10] # Obtencion del TOP TEN
    top_ten = imprime_topten(get_topten,texto,vector,id_texto)
    return jsonify(top_ten)

if __name__ == "__main__":
  app.run(host='localhost', port=5000, debug=True)
