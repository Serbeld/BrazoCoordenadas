import cv2, serial, graphviz
import numpy as np
from sklearn import tree

##Caracteristicas del Árbol de decisiones
caracteristicas = [[0],[0]]  

##Salidas del clustering
targets = ['Mano abierta','Mano cerrada']

##Asignamos clasificador como un clasificador tipo Árbol de decisión
clasificador = tree.DecisionTreeClassifier()

##Asignamos la camara
cap = cv2.VideoCapture(0)

##Comunicación Serial
ser = serial.Serial('/dev/ttyUSB0', 9600)

while(True):
    
    # Capture frame-by-frame
    ret, camara = cap.read()

    # Our operations on the frame come here
    camara = cv2.cvtColor(camara, cv2.COLOR_BGR2GRAY)

    gris_bajos = np.array([10], dtype=np.uint8)
    gris_altos = np.array([100], dtype=np.uint8)

    mask = cv2.inRange(camara,gris_bajos,gris_altos)
    
    moments = cv2.moments(mask)
    
    area = int(moments['m00'])
    
    if (caracteristicas[0][0] != 0 and caracteristicas[1][0] != 0):
          
        ## Se realiza el Ajuste interno del clustering   
        clasificador = clasificador.fit(caracteristicas, targets)
        
        ## Salida de la clasificación   
        prediccion = clasificador.predict(area)
    
        if   (prediccion == 'Mano abierta'):
            resultado = "El led del arduino esta en AZUL"
            encendido = b"H"
            ser.write(encendido)
            print(resultado)
        
        elif (prediccion == 'Mano cerrada'):
            resultado = "El led del arduino esta en ROJO"
            apagado = b"L"
            ser.write(apagado)
            print(resultado)

    
    cv2.imshow('Python Camara', mask)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
##        Sale del ciclo while
        break
    
    if cv2.waitKey(1) & 0xFF == ord('a'):
##        Guarda el valor de pixeles con la mano abierta
        caracteristicas[0][0] = area
        print('Abierta')
        
    if cv2.waitKey(1) & 0xFF == ord('c'):
##        Guarda el valor de pixeles con la mano cerrada
        caracteristicas[1][0] = area
        print('Cerrada')
        
    if cv2.waitKey(1) & 0xFF == ord('g'):
##        Genera el gráfico del Arbol de decisiones
        dot_data = tree.export_graphviz(clasificador, out_file=None, 
                         feature_names =  ['Cantidad de pixeles en Blanco'],
                        class_names =  ['Mano abierta','Mano cerrada'],  
                         filled=True, rounded=True,  
                         special_characters=True)
        graph = graphviz.Source(dot_data)
        graph.render("Visión Artificial")
        
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
ser.close();
print("Saliste")
##Autor Sergio Beleño
