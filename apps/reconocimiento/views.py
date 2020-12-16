from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from . import models as personal
from datetime import datetime
import cv2, numpy, json, os, time


# Create your views here.
@csrf_exempt
def get_imagen_post(request):
    status = {}
    if ( request.method == "POST" ):
        imagen = request.FILES['imagen']
        with open("media/tmp/"+str(imagen), 'wb+') as destination:
            for chunk in imagen.chunks():
                destination.write(chunk)
            destination.close()

        status = convertir_imagen(str(imagen))
    else:
        status['status'] = False
        status['mensaje'] = "Error 404"
        
    return HttpResponse(json.dumps(status), "application/json")

# funcion que convierte la foto a un formado de blanco y negro
def convertir_imagen(img):
    path = os.path.join(settings.BASE_DIR, 'media', 'tmp')
    fecha = datetime.now()
    (im_width, im_height) = (112, 92)
    size = 4

    # agregamos la imagen an cv2
    #foto = "%s/%s" % (path, img)
    frame = cv2.imread("%s/%s" % (path, img))
    
    #convertimos la imagen a blanco y negro
    path_cascade = os.path.join(settings.BASE_DIR, 'static', 'cascades')
    face_cascade = cv2.CascadeClassifier('%s/haarcascade_frontalface_default.xml' % (path_cascade)) # agregamos los patrones de reconocimiento    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))
    faces = face_cascade.detectMultiScale(mini)
    faces = sorted(faces, key=lambda x: x[3])

    if faces:
        face_i = faces[0]
        (x, y, w, h) = [v * size for v in face_i]
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (im_width, im_height))
        
        pin = fecha.strftime('%d-%m-%Y-%H_%M_%S.png')
        ruta_imagen = "%s/%s" % (path, pin)
        #guardamos la foto la foto en el directorio
        guardado = cv2.imwrite(ruta_imagen, face_resize)

        if (guardado):
            os.remove("media/tmp/%s" % (img) )
            return reconocer_imagen(pin)
    else:
        return {"status": False, "Mensaje": "No se encontro un rostro", 'codigo':300}

# funcion que reconoce la imagen enviada, esta imagen debe estar en blanco y negro        
def reconocer_imagen(img):
    # variables
    lista = personal.personas_imagenes.objects.all() # obtenemos las fotos de las personas registradas previamente
    (images, labels, names, id) = ([], [], {}, 0)
    usuarios = []
    
    if (len(lista) == 0):
        os.remove("media/tmp/%s" % (img) )
        return {"status": False, 'codigo': 0}

    for i in range( len(lista) ):
        usuarios.append( lista[i].persona_id )
        images.append( cv2.imread( "%s/%s" % (settings.BASE_DIR, lista[i].archivo.url), 0 ) ) # agregamos las imagenes a un arreglo de imagenes para el cv
        labels.append(int(i))

    # Crear una matriz Numpy de las dos listas anteriores
    (images, label) = [numpy.array(lis) for lis in [images, labels]]

    # iniciamos la red neuronal para el reconocimiento
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(images, label)
    # imagen a analizar
    imagen = cv2.imread("media/tmp/%s" % (img), 0)

    # realizo la prediccion de la imagen
    prediction = model.predict(imagen)

    os.remove("media/tmp/%s" % (img) )
    #Si la prediccion tiene una exactitud menor a 100 se toma como prediccion valida
    if prediction[1] < 100 :
        persona = personal.personas.objects.filter(id=usuarios[prediction[0]]  ).first()
        return {"status": True, 'codigo':200, "clave": usuarios[prediction[0]], "foto": persona.foto.url }

    #Si la prediccion es mayor a 100 no es un reconomiento con la exactitud suficiente
    elif prediction[1] > 101 and prediction[1] < 500:   
        return {"status": False, 'codigo':404}