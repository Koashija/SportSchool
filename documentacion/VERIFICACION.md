# Verificación de SportSchool

Fecha: 21 de noviembre de 2026. Esta matriz distingue implementación de comprobación real.

| Criterio | Implementación | Evidencia y estado |
|---|---|---|
| Splash y Home | public/index.html, app.js, styles.css | Comprobado en Chrome; captura 05-inicio.jpg |
| Estudiante: nombre, grupo, disciplina | Formulario, IndexedDB y validación en servidor | Comprobado en Chrome; captura 01-estudiantes.jpg |
| Actividad: fecha, tipo, minutos, km, observaciones | Formulario y validación | Dos actividades comprobadas en Chrome; captura 02-formulario.jpg |
| Historial individual | Filtro por estudiante y búsqueda | Dos registros tras recargar; captura 03-historial-recarga.jpg |
| Desempeño CSR | Tarjetas y gráfica calculadas desde los registros | 75 min y 8 km comprobados; captura 04-desempeno.jpg |
| Persistencia y recuperación | IndexedDB en cliente, SQLite en servidor | Tres actividades sobrevivieron a recargas; una se creó con el servidor detenido. Inspección de IndexedDB en DevTools pendiente |
| Fetch API | POST /api/sync con JSON y timeout | Tercera actividad pasó de Local a Sincronizado tras reiniciar el servidor; captura 08. Tráfico Network pendiente |
| Manifest | Nombre, start_url, scope, colores, display e iconos PNG | Chrome mostró la opción Instalar; inspección DevTools pendiente |
| Service Worker y caché | Precarga de siete recursos; recuperación cache-first | DevTools mostró Service Worker activado; se detuvo Python y Chrome recargó la PWA y sus datos locales. Capturas 06 y 07 |
| Notificación local | Notification.requestPermission y showNotification | Implementado; requiere permiso y prueba del navegador |
| Geolocalización opcional | getCurrentPosition al pulsar Usar ubicación | Implementado; requiere permiso; no impide registro si se deniega |
| Distribución | Python 3.10+, sin instalación de dependencias | Entorno local documentado; repositorio público en https://github.com/Koashija/SportSchool |
| Código y reporte | Fuentes, pruebas, README y PDF | Reporte final con ocho capturas reales y código en https://github.com/Koashija/SportSchool |

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

## Prueba real sin servidor y guion de evaluación

Se detuvo `python server.py` con Ctrl+C. Chrome recargó `http://localhost:8080/` desde el Service Worker y mostró «Servidor no disponible / Trabajando con datos locales». Historial conservó Carrera y Caminata. Se añadió «Entrenamiento sin servidor», 20 min y 2 km, con estado «Local»; tras una segunda recarga sin servidor seguía disponible. Al reiniciar Python y pulsar sincronizar pasó a «Sincronizado». Desempeño indicó 3 actividades, 95 min y 10 km. Capturas 06, 07 y 08. Esta prueba detuvo el servidor real; no afirma que se haya capturado la opción Network Offline de DevTools.

1. Ejecutar `python server.py`. Abrir siempre el mismo origen, `http://127.0.0.1:8080/`. localhost y 127.0.0.1 tienen almacenes distintos.
2. Registrar «Estudiante de prueba», grupo «Demo», disciplina «Atletismo». Capturar Estudiantes.
3. Registrar Carrera, 30 min, 3 km; registrar Caminata, 45 min, 5 km. Capturar formulario, Historial y Desempeño. Totales esperados: 2 actividades, 75 min y 8 km.
4. Recargar y verificar los mismos registros. Capturar Application > IndexedDB > sportschool-v1 > activities.
5. Capturar Application > Manifest, Service Workers (activated) y Cache Storage (sportschool-shell-v2).
6. En Network, activar Preserve log, pulsar sincronización y capturar POST /api/sync con estado 200 y JSON. Es un envío real a la API Python local; no es un servicio alojado en Internet.
7. La prueba sin servidor ya está documentada. Como evidencia adicional opcional, seleccionar Offline en Network y capturar el selector y la app.
8. La tercera actividad local y su sincronización ya están documentadas en las capturas 07 y 08.
9. Autorizar notificaciones si se desean comprobar; guardar una sesión y observar la notificación del sistema. Un mensaje dentro de la app no sustituye esta prueba.
10. Probar geolocalización sólo si se desea compartir la ubicación con la aplicación local. La denegación debe permitir continuar.
11. Probar anchura móvil y, si Lighthouse está disponible, guardar su informe. No se declara una puntuación no obtenida.

## Diagnóstico del bloqueo actual

Inicialmente Chrome devolvió ERR_CONNECTION_TIMED_OUT para localhost:8080 y 127.0.0.1:8080. Tras reiniciar el servidor, el usuario obtuvo /api/health con ok: true y la aplicación abrió en Chrome. Se registraron un estudiante y dos actividades; persistieron tras recarga. El mensaje antiguo se imprimía antes de abrir el puerto.

Después de reiniciar con la corrección, comprobar `/api/health`. Debe responder JSON con `ok: true`. No abrir index.html con doble clic ni usar Live Server para esta API. No desactivar antivirus o firewall como prueba.

## Alcance

Proyecto académico local, sin autenticación ni resolución avanzada de conflictos entre varios dispositivos. SQLite e IndexedDB no deben subirse con datos personales. El repositorio contiene fuentes y evidencias de prueba, no bases de datos de uso real. Las capturas adicionales de DevTools, notificación, geolocalización y Lighthouse requieren ejecutarse en el navegador de evaluación; no se les atribuyen resultados que no se observaron.
