"""Anexo de verificación reproducible; utiliza el generador PDF del proyecto."""
from pathlib import Path
import build_report as report

report.PAGES.clear()
p=report.Page(1,'SportSchool: revisión técnica')
y=730
y=p.section('Resultado al 21 de noviembre de 2026',y)
y=p.para('Se corrigieron errores de arranque, manejo del almacenamiento y sincronización. Las pruebas de lógica interna pasan. La aplicación todavía no se declara lista para entrega: falta verificar la ejecución en Chrome, obtener las capturas y confirmar el repositorio remoto.',47,y,490,12,19)
y=p.section('Correcciones aplicadas',y-22)
for title,body in [
('Arranque verificable','El servidor informa disponibilidad sólo después de abrir el puerto. Informa errores de permisos o puerto y cierra con Ctrl+C.'),
('Almacenamiento y sincronización','Se evita que un error de IndexedDB bloquee el splash. Las peticiones de sincronización se serializan y un registro creado durante Fetch permanece pendiente hasta que el servidor lo confirma.'),
('Recursos PWA','Se actualiza la caché a sportschool-shell-v2 sin borrar cachés ajenas. Se declaran MIME de JavaScript y manifest. La interfaz ya no solicita Google Fonts.'),
('Navegación y mensajes','Los enlaces con hash abren su sección. El mensaje de sincronización diferencia éxito de fallo del servidor.')]:
    y=p.bullet(title,body,y)
y=p.section('Pruebas ejecutadas: aprobadas',y-12)
y=p.para('tests.py: persistencia SQLite y validación. tests_api.py: un estudiante, dos actividades, 75 minutos y 8 km; consulta, repetición sin duplicados, rechazo de datos inválidos y eliminación. tests_sync.cjs: registro creado durante Fetch y conservación local ante fallo de red. Sintaxis JS y compilación de server.py: correctas.',47,y,490,11,17)
y=p.para('Límite de la evidencia: los handlers HTTP se ejecutaron en memoria y Fetch se simuló en la prueba de concurrencia. No equivalen a tráfico HTTP real, IndexedDB en Chrome ni a una prueba offline.',47,y-12,490,11,17)
p.finish()
p=report.Page(2,'Criterios y evidencia pendiente')
y=730
for title,body in [
('1. Pantalla principal y módulos','Splash, Panorama, Estudiantes, Actividades, Historial y Desempeño implementados; validación visual pendiente.'),
('2. Un estudiante y dos actividades','Comprobados en handlers y SQLite; captura en formularios pendiente.'),
('3. Persistencia al recargar','SQLite comprobado al reabrir conexión. IndexedDB implementado; recarga real pendiente.'),
('4. Historial e indicadores','CSR, filtros, conteos, minutos y km implementados; demostración visual pendiente.'),
('5. Fetch API','POST /api/sync implementado. Respuesta real en Network pendiente; no se afirma envío observado.'),
('6. Service Worker y offline','Manifest, iconos, registro, precarga y fallback implementados. Activación y recarga offline pendientes.'),
('7. Notificación con permiso','Solicitud de permiso y notificación local implementadas; confirmación del sistema pendiente.'),
('8. Prueba documentada','Pruebas automatizadas reproducibles aprobadas. Guion completo en VERIFICACION.md.'),
('9. Fuentes y evidencias','Código y documentos disponibles. Faltan capturas auténticas y enlace de repositorio confirmado.')]:
    y=p.bullet(title,body,y)
p.finish()
p=report.Page(3,'Ejecución y diagnóstico')
y=730
y=p.section('Entorno local de evaluación',y)
y=p.para('Desde la carpeta SportSchool, ejecutar python server.py con Python 3.10 o posterior. Abrir http://127.0.0.1:8080/ y mantener la terminal abierta. No se requiere npm install. El origen localhost y el origen 127.0.0.1 tienen almacenes distintos; usar siempre el mismo al evaluar persistencia.',47,y,490,12,19)
y=p.section('Bloqueo observado',y-22)
y=p.para('Chrome devolvió ERR_CONNECTION_TIMED_OUT al abrir localhost y 127.0.0.1 en el puerto 8080. Los comandos del asistente recibieron WinError 10013 al conectar al puerto local. No se determinó todavía la causa del fallo de Chrome. El mensaje antiguo de disponibilidad se imprimía antes de enlazar el puerto y no era evidencia suficiente de servicio activo.',47,y,490,12,19)
y=p.section('Próxima comprobación',y-22)
y=p.para('Reiniciar con el archivo corregido y abrir http://127.0.0.1:8080/api/health. Debe devolver JSON con ok: true. Si aparece un error en la terminal, conservar el texto exacto para diagnosticarlo. No es necesario desactivar protecciones de Windows.',47,y,490,12,19)
y=p.section('Cierre de la entrega',y-22)
y=p.para('Registrar el estudiante Demo y dos sesiones, recargar, verificar IndexedDB y capturar historial e indicadores. Revisar Manifest, Service Workers y Cache Storage; probar Network Offline con recarga y guardar una actividad. Volver a conexión y capturar POST /api/sync 200. Documentar permisos y Lighthouse si están disponibles.',47,y,490,12,19)
y=p.para('El repositorio remoto todavía no está confirmado. GitHub solicitó iniciar sesión en Chrome para poder crearlo. Este anexo no inventa una URL de repositorio o publicación. El entorno de distribución declarado sigue siendo local.',47,y-12,490,12,19)
p.finish()
report.OUTPUT=Path(__file__).parent/'Anexo_Verificacion_SportSchool.pdf'
report.pdf()
print(report.OUTPUT)
