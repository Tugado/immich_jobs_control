Immich Jobs Control (HACS Custom Component)
[][releases]

Integración personalizada de Home Assistant para controlar y monitorizar los trabajos (jobs) de fondo de tu servidor Immich a través de su API.
Esta integración crea:
 * Un Sensor de Estado Global: Indica si Immich tiene trabajos en ejecución o en cola.
 * Interruptores (Switches) Individuales: Permite pausar y reanudar cada tipo de trabajo de fondo (ej. Detección de Caras, Extracción de Metadatos) de forma independiente.
🚀 Instalación y Configuración
1. Instalación a través de HACS (Recomendado)
 * Abre HACS en tu interfaz de Home Assistant.
 * Ve a Integraciones y haz clic en el menú de tres puntos (⋮) en la esquina superior derecha.
 * Selecciona Repositorios personalizados.
 * Introduce la URL de este repositorio y selecciona la categoría Integración.
 * Busca "Immich Jobs Control" e instálalo.
 * Reinicia Home Assistant.
2. Configuración en configuration.yaml
Añade el siguiente bloque a tu archivo configuration.yaml. Debes reemplazar los valores de host y api_key con los datos de tu servidor Immich.
# configuration.yaml
immich_jobs_control:
  host: "http://<TU_IP_IMMICH>:<PUERTO>" # Ejemplo: [http://192.168.1.10:2283](http://192.168.1.10:2283)
  api_key: "TU_CLAVE_API_SECRETA"        # Clave API generada en la configuración de Immich

Reinicia Home Assistant para que la integración se cargue por primera vez.
💡 Entidades Creadas
Una vez configurada y reiniciada, la integración creará automáticamente las siguientes entidades:
1. Sensor de Estado Global
Entidad: sensor.immich_global_job_status
| Estado | Significado |
|---|---|
| running | Hay trabajos activos o en cola. |
| idle | No hay trabajos en ejecución ni en cola. |
| unavailable | No se pudo conectar con el servidor Immich. |
Atributos: Este sensor contendrá atributos de estado para cada trabajo individual reportado por Immich (ej. face_detection_status, metadata_extraction_queue).
2. Interruptores de Control Individual
Se creará un interruptor por cada tipo de trabajo detectado en el servidor Immich (por ejemplo, si Immich tiene un trabajo llamado face-detection, se creará un switch para él).
Formato de Entidad: switch.immich_job_<nombre_del_trabajo>
| Estado del Switch | Comando de la API | Significado |
|---|---|---|
| ON | POST /job/<jobName>/resume | El trabajo está activo (Resume). |
| OFF | POST /job/<jobName>/pause | El trabajo está pausado (Pause). |
Ejemplos Comunes:
 * switch.immich_job_metadata_extraction
 * switch.immich_job_face_detection
 * switch.immich_job_thumbnail_generation
🛠️ Desarrollo y Notas
Dependencias
 * La integración utiliza la biblioteca estándar requests de Python para comunicarse con la API de Immich.
Estructura de la API
 * Pausa de Trabajo Individual: POST /api/job/<jobName>/pause
 * Reanudación de Trabajo Individual: POST /api/job/<jobName>/resume
 * Consulta de Estado Global: GET /api/job/status
Soporte
Si tienes algún problema o encuentras un error, por favor, abre un "Issue" en el repositorio de GitHub.
[]: #
[releases]: https://www.google.com/search?q=https://github.com/Tugado/immich_jobs_control/releases
[]: #
