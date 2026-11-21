# Verificación de SportSchool

Fecha: 21 de noviembre de 2026. Esta matriz distingue implementación de comprobación real. No se declara aprobada una prueba de navegador que no pudo ejecutarse.

| Criterio | Implementación | Evidencia y estado |
|---|---|---|
| Splash y Home | public/index.html, app.js, styles.css | Implementado; revisión visual pendiente por timeout local |
| Estudiante: nombre, grupo, disciplina | Formulario, IndexedDB y validación en servidor | Handler probado con un estudiante; captura UI pendiente |
| Actividad: fecha, tipo, minutos, km, observaciones | Formulario y validación | Handler probado con dos actividades, 75 min y 8 km |
| Historial individual | Filtro por estudiante y búsqueda | Implementado; prueba UI pendiente |
| Desempeño CSR | Tarjetas y gráfica calculadas desde los registros | Implementado; prueba UI pendiente |
| Persistencia y recuperación | IndexedDB en cliente, SQLite en servidor | SQLite comprobado al reabrir conexión; recarga de navegador pendiente |
| Fetch API | POST /api/sync con JSON y timeout | Handler y errores probados sin sockets; tráfico Network pendiente |
| Manifest | Nombre, start_url, scope, colores, display e iconos PNG | Archivos presentes; instalación pendiente |
| Service Worker y caché | Precarga de siete recursos; recuperación cache-first | Código revisado; registro y recarga offline pendientes |
| Notificación local | Notification.requestPermission y showNotification | Implementado; requiere permiso y prueba del navegador |
| Geolocalización opcional | getCurrentPosition al pulsar Usar ubicación | Implementado; requiere permiso; no impide registro si se deniega |
| Distribución | Python 3.10+, sin instalación de dependencias | Entorno local documentado; publicación no comprobada |
| Código y reporte | Fuentes, pruebas, README y PDF | Actualizados; capturas y repositorio remoto pendientes |

## Correcciones realizadas

- El servidor anuncia disponibilidad después de enlazar el puerto, muestra errores reales y cierra limpiamente con Ctrl+C.
- Se declaran los tipos MIME de JavaScript y manifest y se pide revalidar recursos estáticos.
- Un fallo al abrir IndexedDB ya no mantiene el splash bloqueando el mensaje de error.
- La sincronización se serializa y sólo marca confirmados los registros devueltos por el servidor; un registro nuevo durante Fetch permanece pendiente.
- El mensaje de sincronización distingue éxito y servidor no disponible.
- Al abrir un enlace con hash se recupera la sección solicitada.
- La caché se actualiza a v2 y sólo elimina versiones de SportSchool.
- Se elimina la petición de Google Fonts; la interfaz usa fuentes del sistema.

## Pruebas ejecutadas

Ejecutar desde la raíz:

```text
python tests.py
python tests_api.py
node tests_sync.cjs
node --check public/app.js
node --check public/sw.js
python -m py_compile server.py
```

Resultado: aprobadas. tests_api.py invoca handlers en memoria, sin conexión HTTP. tests_sync.cjs simula la respuesta de Fetch para comprobar concurrencia y fallos de red; no sustituye IndexedDB real ni Service Worker.

## Guion de evaluación y capturas pendientes

1. Ejecutar `python server.py`. Abrir siempre el mismo origen, `http://127.0.0.1:8080/`. localhost y 127.0.0.1 tienen almacenes distintos.
2. Registrar «Estudiante de prueba», grupo «Demo», disciplina «Atletismo». Capturar Estudiantes.
3. Registrar Carrera, 30 min, 3 km; registrar Caminata, 45 min, 5 km. Capturar formulario, Historial y Desempeño. Totales esperados: 2 actividades, 75 min y 8 km.
4. Recargar y verificar los mismos registros. Capturar Application > IndexedDB > sportschool-v1 > activities.
5. Capturar Application > Manifest, Service Workers (activated) y Cache Storage (sportschool-shell-v2).
6. En Network, activar Preserve log, pulsar sincronización y capturar POST /api/sync con estado 200 y JSON. Es un envío real a la API Python local; no es un servicio alojado en Internet.
7. Con el Service Worker activo, seleccionar Offline en Network. Recargar y consultar Historial. Capturar la app y el selector Offline en la misma imagen.
8. Registrar una tercera actividad sin conexión. Confirmar estado Local. Volver a No throttling, sincronizar y confirmar Sincronizado.
9. Autorizar notificaciones si se desean comprobar; guardar una sesión y observar la notificación del sistema. Un mensaje dentro de la app no sustituye esta prueba.
10. Probar geolocalización sólo si se desea compartir la ubicación con la aplicación local. La denegación debe permitir continuar.
11. Probar anchura móvil y, si Lighthouse está disponible, guardar su informe. No se declara una puntuación no obtenida.

## Diagnóstico del bloqueo actual

Chrome devolvió ERR_CONNECTION_TIMED_OUT para localhost:8080 y 127.0.0.1:8080. El entorno de comandos del asistente devuelve WinError 10013 al intentar una conexión local. Esto limita la verificación desde el asistente y no identifica por sí solo la causa del navegador del usuario. El mensaje antiguo se imprimía antes de abrir el puerto.

Después de reiniciar con la corrección, comprobar `/api/health`. Debe responder JSON con `ok: true`. No abrir index.html con doble clic ni usar Live Server para esta API. No desactivar antivirus o firewall como prueba.

## Alcance

Proyecto académico local, sin autenticación ni resolución avanzada de conflictos entre varios dispositivos. SQLite e IndexedDB no deben subirse con datos personales. El repositorio debe contener fuentes y evidencias de prueba, no bases de datos de uso real. Las capturas faltantes deben obtenerse de la ejecución real.
