import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Inicializar la aplicación de Firebase
cred = credentials.Certificate(
    'modelado-810a4-firebase-adminsdk-n75i9-3d6007cd51.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': '*********'
})

# Obtén una referencia a la ubicación donde deseas insertar los datos
ref = db.reference('ruta/datos')

# Inserta los datos en la base de datos
data = {
    'nombre': 'Ejemplo',
    'edad': 25
}
ref.push().set(data)
