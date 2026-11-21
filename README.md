# SportSchool

Aplicación web progresiva de seguimiento y desempeño deportivo escolar. Permite registrar estudiantes y sesiones, consultar el historial individual y calcular actividades, minutos y kilómetros desde el navegador.

## Inicio rápido

1. Instala Python 3.10 o posterior.
2. Abre una terminal en la raíz del proyecto y ejecuta `python server.py`.
3. Abre [http://localhost:8080/](http://localhost:8080/) en Chrome.
4. Mantén la terminal abierta durante la demostración.

No requiere `npm install` ni un servicio externo. El servidor escucha localmente y crea `sportschool.sqlite3` al iniciar. Los iconos ya están incluidos; `python create_icons.py` sólo se necesita para regenerarlos. Usa siempre el mismo origen: `localhost` y `127.0.0.1` guardan datos IndexedDB por separado.

## Funciones y criterios de la actividad

| Requisito | Dónde se demuestra |
|---|---|
| Splash y Home | Pantalla inicial y sección **Panorama**, con el nombre SportSchool |
| Estudiantes | **Estudiantes → Nuevo estudiante**: nombre, grupo y disciplina |
| Actividades | **Actividades**: fecha, tipo, minutos, kilómetros y observaciones |
| Historial | **Historial**: lista, filtro por estudiante y búsqueda |
| Desempeño CSR | **Desempeño**: sesiones, tiempo, distancia y gráfica recalculados en el cliente |
| Almacenamiento local | IndexedDB conserva los registros tras recargar; SQLite respalda la API local |
| Fetch API | `POST /api/sync` intercambia JSON con el servidor Python |
| PWA sin conexión | `manifest.webmanifest`, `sw.js` y Cache API mantienen los recursos principales |
| Notificación local | Al guardar una actividad se solicita autorización, si el navegador lo permite |
| Geolocalización opcional | **Usar ubicación** solicita permiso sólo cuando se pulsa |

La sincronización sí usa una API funcional, pero es local: el repositorio distribuye el código y no aloja la aplicación ejecutándose. Las funciones principales siguen disponibles con el servidor detenido después de la primera visita y activación del Service Worker.

## Prueba de aceptación realizada

En Chrome se registró **Estudiante de prueba**, grupo **Demo**, disciplina **Atletismo**, y dos sesiones: **Carrera** (30 min, 3 km) y **Caminata** (45 min, 5 km). Ambas permanecieron tras recargar. Se detuvo `python server.py` y la PWA volvió a abrir con el historial desde los datos locales. Se añadió **Entrenamiento sin servidor** (20 min, 2 km), que siguió en estado **Local** tras otra recarga. Al reiniciar Python y pulsar sincronizar pasó a **Sincronizado**. Los totales finales fueron **3 actividades, 95 min y 10 km**.

Las nueve capturas auténticas están en `evidencias/` y en `documentacion/Reporte_SportSchool_UTVT.pdf`. La matriz por criterio y el guion de demostración están en `documentacion/VERIFICACION.md`.

## Pruebas reproducibles

```text
python tests.py
python tests_api.py
node tests_sync.cjs
node --check public/app.js
node --check public/sw.js
python -m py_compile server.py
```

Las pruebas automatizadas comprueban persistencia, validación, idempotencia, concurrencia y fallos de red. `tests_api.py` invoca los handlers sin sockets y `tests_sync.cjs` simula Fetch; la prueba real del navegador y del servidor está documentada por separado.

## Estructura y alcance

- `public/`: interfaz CSR, estilos, manifest, iconos y Service Worker.
- `server.py`: recursos web y API `GET /api/health`, `GET /api/data`, `POST /api/sync` y `DELETE /api/activities/:id`.
- `documentacion/`: reporte PDF, matriz de verificación y scripts para regenerar documentos.
- `evidencias/`: capturas de la aplicación, recarga sin servidor y sincronización.

Las notificaciones y la ubicación requieren permiso y `localhost` o HTTPS. No se concedieron esos permisos durante la prueba documentada. Tampoco se incluye una puntuación Lighthouse ni una captura de la pestaña Network. Esta es una demostración académica local: antes de utilizar datos escolares reales hacen falta autenticación, autorización y controles institucionales de privacidad.
