# SportSchool

PWA de seguimiento y desempeño deportivo escolar. Frontend sin dependencias externas, API local en Python y SQLite. Los registros se guardan primero en IndexedDB; la sincronización mediante Fetch es bidireccional e idempotente por identificador. Las funciones esenciales funcionan sin Internet.

## Ejecutar

1. Instala Python 3.10 o posterior.
2. Desde esta carpeta, ejecuta `python create_icons.py` si necesitas regenerar los iconos.
3. Ejecuta `python server.py`.
4. Abre `http://127.0.0.1:8080` en Chrome. Mantén el servidor activo durante la demostración.

No se requiere `npm install`. El servidor escucha en `127.0.0.1` por seguridad; para uso en otros dispositivos se debe configurar HTTPS y un acceso controlado. Se utilizan fuentes del sistema sin peticiones externas.

## Demostración de los criterios

1. Registra un estudiante en **Estudiantes → Nuevo estudiante**.
2. Registra al menos dos sesiones en **Actividades**. La solicitud de permiso de notificaciones aparecerá tras la primera sesión en un contexto seguro, si el navegador la permite.
3. Consulta **Historial** y **Desempeño**. Recarga: los registros se conservan.
4. Abre Chrome DevTools → Application: comprueba Manifest, Service Workers, Cache Storage e IndexedDB `sportschool-v1`.
5. En DevTools → Network, comprueba `POST /api/sync` con respuesta 200. El servidor guarda los registros en `sportschool.sqlite3`.
6. En DevTools → Network, selecciona **Offline**, recarga y consulta el historial. Registra otra actividad sin conexión; al volver a **Online**, el estado pasa a **Sincronizado**.
7. El botón **Usar ubicación** es opcional; el navegador solicita permiso. Si no se concede, el formulario sigue siendo funcional.
8. Se puede exportar el historial en CSV. Eliminar una actividad elimina el registro local y solicita su eliminación remota cuando hay red.

## Arquitectura

`public/` contiene la aplicación CSR, estilos, manifest, iconos y Service Worker. `server.py` sirve esos recursos y expone `GET /api/health`, `GET /api/data`, `POST /api/sync`, `DELETE /api/activities/:id`. `sportschool.sqlite3` se crea automáticamente y no forma parte del código fuente. `IndexedDB` es la fuente de respuesta inmediata; SQLite es el respaldo remoto para el entorno local. `POST /api/sync` envía los registros del dispositivo y devuelve los registros del servidor. No incluye autenticación ni resolución avanzada de cambios concurrentes, por lo que el entorno está pensado para una demostración académica local.

Los permisos de notificación y geolocalización dependen del navegador y de `localhost` o HTTPS. La aplicación no solicita ubicación por adelantado; se guarda únicamente al pulsar el botón de ubicación y luego guardar la actividad.


## Verificación y entrega

Consulta documentacion/VERIFICACION.md para los nueve criterios, resultados comprobados, limitaciones y guion de capturas. Ejecuta python tests.py, python tests_api.py y node tests_sync.cjs. Las pruebas de navegador no se consideran aprobadas hasta obtener evidencia real.
