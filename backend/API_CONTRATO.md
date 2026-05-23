# Contrato de la API (Swagger)

## Endpoints disponibles

### Diario (Diary)
- **GET** `/api/diary`
  - Descripción: Obtiene todas las entradas del diario.
  - Respuesta:
    ```json
    [
      {
        "id": 1,
        "title": "string",
        "content": "string",
        "date": "2024-05-22"
      }
    ]
    ```
- **POST** `/api/diary`
  - Descripción: Crea una nueva entrada en el diario.
  - RequestBody:
    ```json
    {
      "title": "string",
      "content": "string",
      "date": "2024-05-22"
    }
    ```
  - Respuesta:
    ```json
    {
      "id": 1,
      "title": "string",
      "content": "string",
      "date": "2024-05-22"
    }
    ```

### Fotos (Photo Moments)
- **GET** `/api/photos`
  - Descripción: Obtiene todos los momentos fotográficos.
  - Respuesta:
    ```json
    [
      {
        "id": 1,
        "url": "string",
        "description": "string",
        "date": "2024-05-22"
      }
    ]
    ```
- **POST** `/api/photos`
  - Descripción: Crea un nuevo momento fotográfico.
  - RequestBody:
    ```json
    {
      "url": "string",
      "description": "string",
      "date": "2024-05-22"
    }
    ```
  - Respuesta:
    ```json
    {
      "id": 1,
      "url": "string",
      "description": "string",
      "date": "2024-05-22"
    }
    ```

### Resumen de contenido
- **GET** `/api/content/summary`
  - Descripción: Devuelve el conteo de entradas de diario y fotos.
  - Respuesta:
    ```json
    {
      "diaryCount": 10,
      "photoCount": 5
    }
    ```

## Códigos de respuesta
- 200 OK: Solicitud exitosa.
- 201 Created: Recurso creado correctamente.
- 404 Not Found: Recurso no encontrado.

## Probar la API
Accede a la documentación interactiva en: `http://localhost:8080/swagger-ui.html`

---

Este documento sirve como contrato para el equipo frontend. Cualquier petición debe seguir la estructura aquí definida.