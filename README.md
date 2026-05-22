# TVD Backend — Resumen en español

Este repositorio contiene el backend de la aplicación TVD implementado con Spring Boot (Java). Se ha limpiado el frontend; el repositorio ahora está preparado para trabajar sólo con el backend.

Resumen del proyecto
- Tecnología principal: Spring Boot (versión gestionada por el `spring-boot-dependencies` en `pom.xml`).
- Lenguaje: Java, objetivo de compilación y ejecución actualizado a Java 25.
- Estructura principal:
	- `backend/pom.xml`: configuración Maven y dependencias.
	- `backend/src/main/java/...`: código fuente Java (controladores, DTOs, servicios, modelos, excepciones).
	- `backend/src/main/resources/application.properties`: configuración de la aplicación.

Cambios realizados
- Se eliminó la carpeta/archivos del frontend (archivos `index.html`, `src/`, `public/`, `package.json`, configuración de Vite/ESLint) para aislar y ejecutar sólo el backend.
- Se actualizó la propiedad `java.version` en `backend/pom.xml` a `25` y se fijó `maven-compiler-plugin` a la versión `3.11.0` usando `<release>${java.version}</release>` para compilar con Java 25.
- Se aplicó una corrección en `GlobalExceptionHandler.java` para compatibilidad con Spring 6 (`HttpStatusCode`).

Cómo ejecutar el backend localmente (Windows)
1. Asegúrate de tener instalado JDK 25 en el sistema. En esta máquina se detectó en `C:\Program Files\Java\jdk-25.0.2`.
2. Instala o usa Maven. Yo instalé una versión disponible (`C:\Users\CESDE\.maven\maven-3.9.16\bin`). Para Java 25 se recomienda Maven 4.x, pero Maven 3.9.x puede funcionar en muchos casos.
3. Ejecuta desde la carpeta `backend`:

```powershell
Push-Location 'c:\Users\CESDE\Downloads\TDV BACK 2\backend'
$env:JAVA_HOME='C:\Program Files\Java\jdk-25.0.2'
& 'C:\Users\CESDE\.maven\maven-3.9.16\bin\mvn.cmd' clean package
Pop-Location
```

4. Para ejecutar la aplicación localmente después de construir:

```powershell
Push-Location 'c:\Users\CESDE\Downloads\TDV BACK 2\backend'
$env:JAVA_HOME='C:\Program Files\Java\jdk-25.0.2'
& 'C:\Program Files\Java\jdk-25.0.2\bin\java.exe' -jar target\tvd-backend-0.0.1-SNAPSHOT.jar
Pop-Location
```

Verificaciones que hice
- Compilación con Java 25: `mvn -DskipTests clean test-compile` — Éxito.
- Ejecución de pruebas: `mvn clean test` — No hay tests definidos (build success).

Recomendaciones finales
- Actualizar CI para usar Java 25 y preferiblemente Maven 4.x si la infraestructura lo permite.
- Revisar y reinstaurar el frontend en un repositorio separado si se necesita mantener la interfaz.

Si quieres, puedo:
- generar un `README_es.md` más detallado con comandos de despliegue y variables de entorno, o
- crear un branch/PR con estos cambios, o
- instalar/actualizar Maven a 4.x y re-verificar la compilación.

— Resultado preparado por el agente (explicación en español).

CORS y conexión con el frontend
- Por defecto el backend permite solicitudes CORS desde `http://localhost:5173` (puerto por defecto del servidor de desarrollo Vite). Puedes cambiar este origen editando la propiedad `cors.allowed.origins` en `backend/src/main/resources/application.properties` (separa múltiples orígenes con comas).

Por ejemplo, para permitir `http://localhost:5173` y `http://localhost:3000`:

```
cors.allowed.origins=http://localhost:5173,http://localhost:3000
```

API disponible para el frontend
- `GET /api/diary`: devuelve las entradas de diario.
- `POST /api/diary`: crea una nueva entrada de diario.
- `GET /api/photos`: devuelve los momentos/fotos guardadas.
- `POST /api/photos`: crea un nuevo momento de foto.
- `GET /api/content/summary`: devuelve `{ diaryCount, photoCount }`.

Base de datos H2
- La base de datos se guarda en `backend/data/tvd-db`.
- La consola H2 está disponible en `http://localhost:8080/h2-console`.
- URL JDBC: `jdbc:h2:file:./data/tvd-db`.

Ejemplo de integración en el frontend (`src/services/contentService.js`):

```js
const API_BASE = 'http://localhost:8080/api';

export async function getDiaryEntries() {
  const response = await fetch(`${API_BASE}/diary`);
  return response.ok ? response.json() : [];
}

export async function addDiaryEntry(entry) {
  const response = await fetch(`${API_BASE}/diary`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(entry),
  });
  return response.json();
}

export async function getPhotoMoments() {
  const response = await fetch(`${API_BASE}/photos`);
  return response.ok ? response.json() : [];
}

export async function addPhotoMoment(moment) {
  const response = await fetch(`${API_BASE}/photos`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(moment),
  });
  return response.json();
}
```
