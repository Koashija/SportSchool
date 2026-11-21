"""Create a PDF appendix with the real browser screenshots, using JPEG XObjects."""
from pathlib import Path
import struct
import build_report as r

root=Path(__file__).resolve().parent
names=['05-inicio.jpg','01-estudiantes.jpg','02-formulario.jpg','03-historial-recarga.jpg','04-desempeno.jpg','06-offline-historial.jpg','07-offline-nuevo-registro.jpg','08-sincronizado-tras-reinicio.jpg']
captions=['Inicio: un estudiante, dos actividades, 75 min y 8 km.',
          'Estudiantes: perfil de prueba, grupo Demo, Atletismo.',
          'Formulario: fecha, duración, distancia y observaciones.',
          'Historial: carrera 30 min/3 km y caminata 45 min/5 km después de recargar.',
          'Desempeño: indicadores calculados en el navegador.',
          'Sin servidor: recarga de la PWA con las dos actividades recuperadas de IndexedDB.',
          'Sin servidor: tercera actividad guardada localmente y conservada tras recargar.',
          'Servidor reiniciado: tercera actividad sincronizada mediante Fetch API.']

def size(jpeg):
    i=2
    while i<len(jpeg):
        if jpeg[i]!=255:i+=1;continue
        marker=jpeg[i+1];i+=2
        if marker in (0xd8,0xd9) or 0xd0<=marker<=0xd7:continue
        n=int.from_bytes(jpeg[i:i+2],'big')
        if marker in (0xc0,0xc1,0xc2):return struct.unpack('>HH',jpeg[i+3:i+7])[::-1]
        i+=n
    raise ValueError('JPEG sin dimensiones')

objects=[]
def obj(data):objects.append(data);return len(objects)
catalog=obj(b'');pages=obj(b'')
regular=obj(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>')
bold=obj(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>')
refs=[]
def textpage(p):
    content='\n'.join(p.commands).encode('cp1252','replace')
    stream=obj(b'<< /Length '+str(len(content)).encode()+b' >>\nstream\n'+content+b'\nendstream')
    refs.append(obj(f'<< /Type /Page /Parent {pages} 0 R /MediaBox [0 0 595 842] /Resources << /Font << /FR {regular} 0 R /FB {bold} 0 R >> >> /Contents {stream} 0 R >>'.encode()))
p=r.Page(1,'SportSchool - reporte de construcción y pruebas')
y=715;p.txt(47,y,'Seguimiento y Desempeño Deportivo Escolar',20,'B');y-=56
for label,value in [('Presenta','Sánchez Jacinto Irving Javier'),('Matrícula','222310482'),('Docente','R. Vinicio Camacho'),('Fecha','21 de noviembre de 2026'),('Repositorio','https://github.com/Koashija/SportSchool'),('Entorno local','http://127.0.0.1:8080/; python server.py')]:
    p.txt(47,y,label,10,'B');p.txt(165,y,value,10);y-=34
y=p.section('Problema y solución',y-20)
y=p.para('El registro deportivo en papel y hojas de cálculo dificulta recuperar el historial de cada estudiante. SportSchool registra alumnos y actividades, muestra indicadores de sesiones, tiempo y distancia, y conserva los datos de este dispositivo en IndexedDB. Una API Python con SQLite respalda la sincronización local mediante Fetch.',47,y,495,11,17)
textpage(p)
p=r.Page(2,'Componentes, pruebas y alcance')
y=715
for title,body in [('Estructura y presentación','Splash, Home, manifest.webmanifest, iconos y diseño móvil en public/.'),('CSR y formularios','Registro de nombre, grupo, disciplina, fecha, actividad, minutos, kilómetros y observaciones; historial filtrable e indicadores dinámicos.'),('Datos locales y remotos','IndexedDB recupera los registros al iniciar. Fetch POST /api/sync intercambia datos con la API local SQLite; no depende de servicios externos para las funciones esenciales.'),('PWA y dispositivo','Service Worker y Cache API guardan recursos principales. Notificación local y geolocalización opcional requieren permiso.'),('Pruebas observadas','En Chrome se registró un estudiante y dos actividades. Tras recargar permanecen Carrera (30 min/3 km) y Caminata (45 min/5 km). Desempeño muestra 75 min y 8 km.'),('Pruebas automatizadas','tests.py, tests_api.py y tests_sync.cjs pasaron persistencia, validaciones, idempotencia y conservación de cambios durante Fetch.')]:
    y=p.bullet(title,body,y)
textpage(p)
p=r.Page(3,'Verificación y demostración')
y=715
y=p.section('Resultados y límites',y)
for title,body in [('Arranque corregido','El servidor informa disponibilidad sólo después de abrir el puerto. El usuario obtuvo /api/health con ok: true.'),('Persistencia y desempeño','Aprobadas con capturas reales de Chrome incluidas en las páginas siguientes.'),('Service Worker y manifest','Chrome mostró la opción de instalar y DevTools mostró el worker activado. Falta una captura de DevTools.'),('Prueba offline','Se detuvo el servidor, se recargó Chrome y la PWA abrió desde caché. Se consultaron dos sesiones; se guardó una tercera y persistió tras otra recarga sin servidor. Páginas 9 y 10.'),('Sincronización recuperada','Tras reiniciar Python, la tercera sesión pasó de Local a Sincronizado. Los indicadores sumaron 3 actividades, 95 min y 10 km. Página 11.'),('Notificación y geolocalización','Los permisos de notificación y ubicación no se concedieron en estas pruebas. Lighthouse no se ejecutó.')]:y=p.bullet(title,body,y)
y=p.section('Guion para entregar al docente',y-5)
y=p.para('Ejecutar python server.py, abrir http://127.0.0.1:8080/ y mantener la terminal abierta. En DevTools revisar Application: Manifest, Service Workers, Cache Storage e IndexedDB. En Network observar POST /api/sync; activar Offline, recargar y consultar Historial. Volver a Online y sincronizar. Usar el mismo origen, porque localhost y 127.0.0.1 tienen datos IndexedDB separados.',47,y,495,10,15)
y=p.section('Conclusión',y-10)
p.para('Con SportSchool comprobé el registro, el historial tras recarga, los indicadores deportivos y el funcionamiento con el servidor detenido. Quedan por capturar las solicitudes en DevTools y, si se conceden permisos, la notificación y la ubicación. El proyecto es una demostración académica local sin autenticación institucional para datos reales.',47,y,495,10,15)
textpage(p)
for i,(name,caption) in enumerate(zip(names,captions),4):
    jpeg=(root.parent/'evidencias'/name).read_bytes()
    assert jpeg[:3]==b'\xff\xd8\xff'
    w,h=size(jpeg)
    im=obj(f'<< /Type /XObject /Subtype /Image /Width {w} /Height {h} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length {len(jpeg)} >>\nstream\n'.encode()+jpeg+b'\nendstream')
    p=r.Page(i,'Evidencias reales de SportSchool')
    p.txt(47,724,f'Captura {i}: {name}',16,'B')
    p.para(caption,47,694,490,11,16)
    width=min(500,610*w/h);height=width*h/w
    p.commands.append(f'q {width:.2f} 0 0 {height:.2f} 47 {665-height:.2f} cm /Im1 Do Q')
    content='\n'.join(p.commands).encode('cp1252','replace')
    stream=obj(b'<< /Length '+str(len(content)).encode()+b' >>\nstream\n'+content+b'\nendstream')
    refs.append(obj(f'<< /Type /Page /Parent {pages} 0 R /MediaBox [0 0 595 842] /Resources << /Font << /FR {regular} 0 R /FB {bold} 0 R >> /XObject << /Im1 {im} 0 R >> >> /Contents {stream} 0 R >>'.encode()))
objects[catalog-1]=f'<< /Type /Catalog /Pages {pages} 0 R >>'.encode()
objects[pages-1]=f'<< /Type /Pages /Kids [ '+ ' '.join(f'{n} 0 R' for n in refs)+f' ] /Count {len(refs)} >>'
objects[pages-1]=objects[pages-1].encode()
output=bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n');offsets=[0]
for n,data in enumerate(objects,1):
    offsets.append(len(output));output+=f'{n} 0 obj\n'.encode()+data+b'\nendobj\n'
start=len(output);output+=f'xref\n0 {len(offsets)}\n0000000000 65535 f \n'.encode()
for off in offsets[1:]:output+=f'{off:010d} 00000 n \n'.encode()
output+=f'trailer\n<< /Size {len(offsets)} /Root {catalog} 0 R >>\nstartxref\n{start}\n%%EOF\n'.encode()
path=root/'Reporte_SportSchool_UTVT.pdf';path.write_bytes(output)
print(path,len(output),'bytes',len(refs),'pages')
