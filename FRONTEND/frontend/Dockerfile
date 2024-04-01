# Utiliza una imagen de Node.js como base
FROM node:18.16.0

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el package.json y package-lock.json a la carpeta de trabajo
COPY package*.json ./

# Instala las dependencias del proyecto
RUN npm install

# Copia todos los archivos del proyecto a la carpeta de trabajo
COPY . .

# Expone el puerto 3000 (o el puerto que estés utilizando en tu proyecto)
EXPOSE 3000

# Define el comando para iniciar la aplicación
CMD ["npm", "start"]
