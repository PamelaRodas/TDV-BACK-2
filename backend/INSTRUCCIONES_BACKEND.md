# Instalación y ejecución del backend

## 1. Instalar Java JDK
Asegúrate de tener Java 17 o superior instalado. Puedes descargarlo desde:
https://adoptium.net/

## 2. Instalar Maven
Descarga Maven desde:
https://maven.apache.org/download.cgi

Agrega la carpeta `bin` de Maven a la variable de entorno `PATH`.

Para verificar la instalación, ejecuta en la terminal:

```
mvn -v
```

## 3. Ejecutar el backend
Desde la raíz del proyecto, ejecuta:

```
cd backend
mvn spring-boot:run
```

Esto levantará el backend en http://localhost:8080

## 4. Acceder a Swagger
Abre en tu navegador:

```
http://localhost:8080/swagger-ui.html
```

Aquí podrás probar los endpoints y ver la documentación interactiva.

---

¿Listo para continuar con la organización y documentación de la API?