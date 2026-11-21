"""Reporte académico con criterios y nueve capturas reales de Chrome."""
from pathlib import Path
import struct
import build_report as r

root = Path(__file__).resolve().parent
evidence = [
    ('05-inicio.jpg', 'Pantalla principal', 'La portada SportSchool ofrece acceso a los módulos. El resumen reflejaba un estudiante, dos sesiones, 75 minutos y 8 km.'),
    ('01-estudiantes.jpg', 'Registro de estudiante', 'Se creó un perfil con nombre, grupo Demo y disciplina Atletismo; quedó visible en la lista.'),
    ('02-formulario.jpg', 'Formulario deportivo', 'Se muestran estudiante, fecha, actividad, minutos, kilómetros, observaciones y ubicación opcional.'),
    ('03-historial-recarga.jpg', 'Historial recuperado', 'Después de recargar Chrome siguieron visibles Carrera (30 min, 3 km) y Caminata (45 min, 5 km).'),
    ('04-desempeno.jpg', 'Indicadores CSR', 'Los cálculos del navegador mostraron dos actividades, 75 minutos y 8 km para el perfil de prueba.'),
    ('06-offline-historial.jpg', 'Consulta sin servidor', 'Con Python detenido, la PWA abrió tras recargar y recuperó las dos sesiones guardadas en el dispositivo.'),
    ('07-offline-nuevo-registro.jpg', 'Captura sin servidor', 'Se agregó Entrenamiento sin servidor (20 min, 2 km). Su estado Local permaneció tras otra recarga.'),
    ('08-sincronizado-tras-reinicio.jpg', 'Sincronización recuperada', 'Al reiniciar Python y pulsar sincronizar, la tercera sesión cambió a Sincronizado.'),
    ('09-vista-movil.jpg', 'Interfaz para teléfono', 'A 390 px de ancho, el formulario se organiza en una columna y conserva sus campos sin desbordamiento horizontal.'),
]

def jpeg_size(data):
    i = 2
    while i < len(data):
        if data[i] != 255:
            i += 1
            continue
        marker = data[i + 1]
        i += 2
        if marker in (0xd8, 0xd9) or 0xd0 <= marker <= 0xd7:
            continue
        length = int.from_bytes(data[i:i + 2], 'big')
        if marker in (0xc0, 0xc1, 0xc2):
            return struct.unpack('>HH', data[i + 3:i + 7])[::-1]
        i += length
    raise ValueError('JPEG sin dimensiones')

objects = []
def obj(data):
    objects.append(data)
    return len(objects)

catalog, pages = obj(b''), obj(b'')
regular = obj(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>')
bold = obj(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>')
refs = []

def textpage(page):
    content = '\n'.join(page.commands).encode('cp1252', 'replace')
    stream = obj(b'<< /Length ' + str(len(content)).encode() + b' >>\nstream\n' + content + b'\nendstream')
    refs.append(obj(f'<< /Type /Page /Parent {pages} 0 R /MediaBox [0 0 595 842] /Resources << /Font << /FR {regular} 0 R /FB {bold} 0 R >> >> /Contents {stream} 0 R >>'.encode()))

p = r.Page(1, 'SportSchool - reporte de construcción y pruebas')
y = 714
p.txt(47, y, 'Seguimiento y Desempeño Deportivo Escolar', 19, 'B')
y -= 57
for label, value in [
    ('Presenta', 'Sánchez Jacinto Irving Javier'),
    ('Matrícula', '222310482'),
    ('Asignatura', 'Aplicaciones Web Progresivas'),
    ('Docente', 'R. Vinicio Camacho'),
    ('Fecha', '21 de noviembre de 2026'),
    ('Repositorio', 'https://github.com/Koashija/SportSchool'),
    ('Entorno local', 'http://localhost:8080/; python server.py'),
]:
    p.txt(47, y, label, 10, 'B')
    p.txt(165, y, value, 10)
    y -= 32
y = p.section('Problema y solución', y - 20)
y = p.para('La institución registra actividades deportivas en hojas de cálculo o papel, lo que dificulta consultar el historial y reconocer avances. SportSchool reúne perfiles y sesiones en una PWA que calcula actividades, tiempo y distancia. IndexedDB mantiene los datos disponibles en el dispositivo; una API Python con SQLite permite su intercambio mediante Fetch cuando el servidor local responde.', 47, y, 495, 11, 17)
p.para('Este reporte distingue las funciones implementadas de las pruebas observadas. Las capturas proceden de Chrome durante la ejecución local del proyecto.', 47, y - 12, 495, 10, 15)
textpage(p)

p = r.Page(2, 'Construcción de la aplicación')
y = 713
for title, body in [
    ('Parte 1. Estructura y configuración', 'public/ contiene Splash, Home, manifest.webmanifest, iconos PNG, estilos, JavaScript y Service Worker. El servidor se inicia con python server.py sin instalar paquetes.'),
    ('Parte 2. Interfaz y renderizado', 'Los formularios solicitan nombre, grupo, disciplina, fecha, actividad, minutos, kilómetros y observaciones. El historial se filtra por estudiante. Las tarjetas y la gráfica se recalculan en el navegador mediante CSR.'),
    ('Parte 3. Almacenamiento y Fetch', 'IndexedDB recupera estudiantes y actividades al iniciar. POST /api/sync envía y recibe JSON mediante Fetch; la API local guarda en SQLite. No requiere un servicio externo.'),
    ('Parte 4. Programación PWA', 'El Service Worker precarga recursos y responde desde Cache API. La notificación local se intenta al guardar una actividad si el usuario concede permiso. La ubicación sólo se solicita al pulsar Usar ubicación.'),
    ('Parte 5. Pruebas y distribución', 'Se probaron los formularios, recarga, indicadores, servidor detenido y sincronización posterior. El repositorio de GitHub entrega el código; la aplicación se demuestra en localhost.'),
    ('Parte 6. Evidencias', 'Este PDF incluye nueve capturas de pantallas y pruebas, el enlace al repositorio y el entorno de ejecución. VERIFICACION.md contiene la matriz detallada.'),
]:
    y = p.bullet(title, body, y)
textpage(p)

p = r.Page(3, 'Criterios de aceptación')
y = p.section('Resultado de los nueve criterios', 714)
for title, body in [
    ('1. Pantalla y módulos - comprobado', 'Splash y Home identifican SportSchool. Se visualizaron Estudiantes, Actividades, Historial y Desempeño.'),
    ('2. Estudiante y dos actividades - comprobado', 'Un perfil y Carrera/Caminata se registraron en Chrome. Hubo una tercera sesión en la prueba sin servidor.'),
    ('3. Persistencia tras recarga - comprobado', 'Las dos primeras sesiones permanecieron tras recargar. La tercera permaneció aun con Python detenido.'),
    ('4. Historial e indicadores - comprobado', 'El historial muestra sesiones por estudiante. Los totales llegaron a tres sesiones, 95 min y 10 km.'),
    ('5. Solicitud Fetch - comprobado funcionalmente', 'POST /api/sync sincroniza. La tercera sesión pasó de Local a Sincronizado; falta captura de Network.'),
    ('6. Service Worker sin conexión - comprobado', 'Se observó el worker activo. Con el servidor detenido, la PWA recargó y siguió mostrando registros locales.'),
    ('7. Notificación - condicionada al permiso', 'El código solicita autorización y genera confirmación local; el permiso no se concedió en esta revisión.'),
    ('8. Prueba documentada - comprobado', 'Las páginas siguientes muestran registro, recarga, prueba sin servidor y sincronización posterior.'),
    ('9. Código y evidencias - entregado', 'Repositorio público, fuentes, manifest, Service Worker, nueve capturas y este PDF.'),
]:
    y = p.bullet(title, body, y)
textpage(p)

p = r.Page(4, 'Prueba sin servidor y sincronización')
y = p.section('Secuencia observada en Chrome', 713)
for title, body in [
    ('Preparación', 'Se registró Estudiante de prueba, grupo Demo, Atletismo. Carrera duró 30 min y recorrió 3 km; Caminata duró 45 min y recorrió 5 km. La recarga conservó ambas.'),
    ('Servidor detenido', 'Se cerró python server.py con Ctrl+C. Chrome recargó http://localhost:8080/ y mostró Servidor no disponible / Trabajando con datos locales. La PWA y el historial continuaron accesibles.'),
    ('Nueva actividad local', 'Se guardó Entrenamiento sin servidor con 20 min y 2 km. Apareció con estado Local y siguió presente después de otra recarga sin Python.'),
    ('Recuperación', 'Se inició de nuevo python server.py. Al pulsar Sincronizar, la actividad pasó a Sincronizado. Desempeño presentó tres actividades, 95 min y 10 km.'),
    ('Pruebas automatizadas', 'tests.py, tests_api.py y tests_sync.cjs pasaron persistencia, validaciones, idempotencia y conservación de un registro creado durante Fetch. La prueba API invoca handlers sin sockets y la prueba de sincronización simula Fetch.'),
]:
    y = p.bullet(title, body, y)
y = p.section('Cómo repetirla', y - 4)
p.para('Desde la raíz, ejecutar python server.py y abrir http://localhost:8080/. Mantener siempre el mismo origen: localhost y 127.0.0.1 guardan IndexedDB por separado. En DevTools revisar Application para Manifest, Service Workers, Cache Storage e IndexedDB; en Network observar POST /api/sync. La evidencia de las páginas 11 y 12 se obtuvo deteniendo el servidor real, sin afirmar que se capturó el selector Offline de DevTools.', 47, y, 495, 10, 15)
textpage(p)

p = r.Page(5, 'Distribución y alcance')
y = p.section('Entregables para el docente', 713)
for title, body in [
    ('Repositorio y código fuente', 'https://github.com/Koashija/SportSchool contiene README, servidor Python, pruebas, public/ con manifest y Service Worker, documentación y capturas.'),
    ('Ejecución local', 'Instalar Python 3.10 o posterior, ejecutar python server.py desde la raíz y abrir http://localhost:8080/. La terminal debe permanecer abierta; SQLite se crea automáticamente.'),
    ('Evidencia incluida', 'Páginas 6 a 14: Home, estudiante, formulario, historial tras recarga, desempeño, uso sin servidor, sincronización y vista móvil.'),
]:
    y = p.bullet(title, body, y)
y = p.section('Límites de esta revisión', y - 7)
y = p.para('La notificación y la geolocalización requieren permiso del navegador y un contexto seguro; no se otorgaron permisos en esta prueba. La captura de Network, la inspección visual de IndexedDB y una puntuación Lighthouse no forman parte de las evidencias obtenidas. La ubicación es opcional. La sincronización observada utiliza la API local; GitHub distribuye el código, pero no aloja la aplicación en ejecución.', 47, y, 495, 10, 16)
y = p.section('Conclusión personal', y - 12)
p.para('Comprobé que SportSchool permite registrar actividades, consultar su historial y analizar el tiempo y la distancia acumulados. También comprobé que la pantalla y los datos locales permanecen disponibles al detener el servidor y que el registro pendiente se sincroniza al volver a iniciarlo. Para usar datos escolares reales harían falta cuentas, permisos institucionales y una política de protección de información.', 47, y, 495, 10, 16)
textpage(p)

for n, (filename, title, explanation) in enumerate(evidence, 1):
    data = (root.parent / 'evidencias' / filename).read_bytes()
    if data[:3] != b'\xff\xd8\xff':
        raise ValueError('No es JPEG: ' + filename)
    w, h = jpeg_size(data)
    image_ref = obj(f'<< /Type /XObject /Subtype /Image /Width {w} /Height {h} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length {len(data)} >>\nstream\n'.encode() + data + b'\nendstream')
    p = r.Page(n + 5, 'Evidencias reales de SportSchool')
    p.txt(47, 725, f'Evidencia {n}. {title}', 16, 'B')
    if h > w:
        height = 530
        width = height * w / h
        bottom = 132
        p.commands.append(f'q {width:.2f} 0 0 {height:.2f} 47 {bottom:.2f} cm /Im1 Do Q')
        p.txt(310, 630, 'Qué muestra esta captura', 13, 'B')
        p.para(explanation, 310, 600, 230, 11, 17)
    else:
        width = min(500, 610 * w / h)
        height = width * h / w
        bottom = 677 - height
        p.commands.append(f'q {width:.2f} 0 0 {height:.2f} 47 {bottom:.2f} cm /Im1 Do Q')
        y = p.section('Qué muestra esta captura', bottom - 36)
        p.para(explanation, 47, y, 495, 11, 17)
    content = '\n'.join(p.commands).encode('cp1252', 'replace')
    stream = obj(b'<< /Length ' + str(len(content)).encode() + b' >>\nstream\n' + content + b'\nendstream')
    refs.append(obj(f'<< /Type /Page /Parent {pages} 0 R /MediaBox [0 0 595 842] /Resources << /Font << /FR {regular} 0 R /FB {bold} 0 R >> /XObject << /Im1 {image_ref} 0 R >> >> /Contents {stream} 0 R >>'.encode()))

objects[catalog - 1] = f'<< /Type /Catalog /Pages {pages} 0 R >>'.encode()
objects[pages - 1] = (f'<< /Type /Pages /Kids [ ' + ' '.join(f'{ref} 0 R' for ref in refs) + f' ] /Count {len(refs)} >>').encode()
out = bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
offsets = [0]
for n, data in enumerate(objects, 1):
    offsets.append(len(out))
    out += f'{n} 0 obj\n'.encode() + data + b'\nendobj\n'
start = len(out)
out += f'xref\n0 {len(offsets)}\n0000000000 65535 f \n'.encode()
for off in offsets[1:]:
    out += f'{off:010d} 00000 n \n'.encode()
out += f'trailer\n<< /Size {len(offsets)} /Root {catalog} 0 R >>\nstartxref\n{start}\n%%EOF\n'.encode()
path = root / 'Reporte_SportSchool_UTVT.pdf'
path.write_bytes(out)
print(path, len(out), 'bytes', len(refs), 'pages')
