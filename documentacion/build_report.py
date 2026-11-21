"""Genera un reporte PDF académico con Python estándar."""
from pathlib import Path
import textwrap

OUTPUT = Path(__file__).resolve().parent / 'Reporte_SportSchool_UTVT.pdf'
W, H = 595, 842
PAGES = []
NAVY = (.045,.11,.16)
GREEN = (.57,.76,.28)
INK = (.12,.18,.23)
GRAY = (.39,.45,.49)


def color(rgb, stroke=False):
    return ' '.join(f'{x:.3f}' for x in rgb) + (' RG' if stroke else ' rg')


class Page:
    def __init__(self, number, heading=None):
        self.n = number
        self.commands = []
        self.rect(0,0,W,H,(1,1,1))
        if heading:
            self.rect(0,H-72,W,72,NAVY)
            self.txt(47,H-44,heading,15,'B',(1,1,1))
            self.txt(47,H-60,'SPORTSCHOOL  /  REPORTE TÉCNICO',8,'R',(.68,.82,.76))
        self.line(47,43,W-47,43,(.76,.8,.81),.6)
        self.txt(47,29,'UTVT  •  Aplicaciones Web Progresivas  •  Noviembre 2026',8,'R',GRAY)
        self.txt(W-66,29,f'{number:02d}',8,'B',INK)

    def rect(self,x,y,w,h,c): self.commands.append(f'{color(c)} {x:.1f} {y:.1f} {w:.1f} {h:.1f} re f')
    def line(self,x,y,xx,yy,c,width=1): self.commands.append(f'{color(c,True)} {width} w {x} {y} m {xx} {yy} l S')
    def txt(self,x,y,s,size=11,font='R',c=INK):
        s=s.replace('→',' > ')
        b = s.encode('cp1252','replace')
        escaped = b.decode('latin1').replace('\\','\\\\').replace('(','\\(').replace(')','\\)')
        self.commands.append(f'{color(c)} BT /F{font} {size} Tf 1 0 0 1 {x:.1f} {y:.1f} Tm ({escaped}) Tj ET')

    def para(self,text,x,y,width=500,size=11,leading=16,c=INK):
        # Approximate Helvetica width to wrap without outside dependencies.
        words=text.split(); line=[]; lines=[]
        for word in words:
            tentative=' '.join(line+[word])
            if len(tentative)*size*.49 > width and line:
                lines.append(' '.join(line));line=[word]
            else: line.append(word)
        if line:lines.append(' '.join(line))
        for l in lines:
            self.txt(x,y,l,size,'R',c);y-=leading
        return y

    def section(self,title,y):
        self.rect(47,y-8,19,3,GREEN)
        self.txt(75,y-9,title,14,'B',INK)
        return y-31

    def bullet(self,title,body,y):
        self.rect(49,y-2,5,5,GREEN)
        self.txt(64,y,title,10,'B',INK)
        y=self.para(body,64,y-16,472,10,14,GRAY)
        return y-13

    def finish(self):PAGES.append('\n'.join(self.commands).encode('cp1252','replace'))


p=Page(1)
p.rect(0,H-13,W,13,NAVY)
p.rect(47,H-153,38,5,GREEN)
p.txt(47,H-83,'UNIVERSIDAD TECNOLÓGICA',18,'B',NAVY)
p.txt(47,H-107,'DEL VALLE DE TOLUCA',18,'B',NAVY)
p.txt(47,H-132,'Dirección de Carrera: Tecnologías de la Información',10,'R',GRAY)
p.txt(47,H-213,'EVALUACIÓN · UNIDAD II',10,'B',(.35,.52,.24))
p.txt(47,H-258,'SportSchool',39,'B',NAVY)
p.txt(47,H-287,'Seguimiento y Desempeño',21,'B',INK)
p.txt(47,H-314,'Deportivo Escolar',21,'B',INK)
p.rect(47,H-366,500,1,(.77,.82,.8))
p.para('Construcción, pruebas y preparación para distribución de una aplicación web progresiva',47,H-393,495,12,18,GRAY)
for i,(a,b) in enumerate([('Asignatura','Aplicaciones Web Progresivas'),('Docente','R. Vinicio Camacho'),('Presenta','Sánchez Jacinto Irving Javier'),('Matrícula','222310482'),('Programa','Ing. en Desarrollo y Gestión del Software'),('Cuatrimestre / grupo','Noveno · IDGS-104'),('Periodo','Septiembre - diciembre 2026')]):
    y=H-462-i*31;p.txt(47,y,a.upper(),8,'B',GRAY);p.txt(198,y,b,10,'R',INK)
p.txt(47,85,'Santa María Atarasquillo, Lerma, Estado de México',9,'R',GRAY)
p.txt(47,68,'21 de noviembre de 2026',9,'B',NAVY)
p.finish()

p=Page(2,'Índice y alcance')
p.txt(47,734,'ÍNDICE',9,'B',(.38,.55,.28))
for i,(title,page) in enumerate([('1. Introducción y justificación','03'),('2. Objetivos y alcance','03'),('3. Arquitectura y decisiones técnicas','04'),('4. Módulos y experiencia de usuario','05'),('5. Pruebas y criterios de aceptación','06'),('6. Evidencias y distribución','07'),('7. Conclusiones y referencias','08')]):
    y=700-i*35;p.txt(52,y,title,11,'R',INK);p.line(52,y-8,540,y-8,(.86,.89,.88),.5);p.txt(518,y,page,10,'B',INK)
y=414;p.section('Resumen ejecutivo',y)
y=p.para('SportSchool permite a docentes y entrenadores registrar estudiantes, documentar sesiones deportivas y consultar indicadores de actividad, tiempo y distancia. Se diseñó como una PWA que responde de inmediato con información guardada en el dispositivo y que intenta sincronizarla con una API local cuando hay conectividad.',47,372,497,11,17)
y=p.para('La interfaz presenta un tablero de control, perfiles, registro de sesiones, historial filtrable y análisis visual. Su lenguaje visual usa planos profundos, órbitas y movimiento moderado inspirado en la referencia de diseño indicada, con adaptación a teléfonos y preferencias de movimiento reducido.',47,y-13,497,11,17)
p.finish()

p=Page(3,'Introducción, justificación y objetivos')
y=729;y=p.section('1. Introducción y justificación',y)
y=p.para('En la institución educativa, el seguimiento deportivo suele quedar repartido entre hojas de cálculo y anotaciones manuales. Esta dispersión dificulta recuperar el historial individual, comparar periodos y reconocer avances. La propuesta reúne los registros en una interfaz que permanece consultable aun cuando falla la conexión; el docente puede capturar una actividad en el lugar de entrenamiento y continuar el análisis más tarde.',47,y,498,11,17)
y=p.para('Se eligió almacenamiento IndexedDB porque conserva registros estructurados sin imponer límites prácticos tan estrictos como una sola cadena en localStorage. SQLite añade persistencia del lado del servidor para el entorno de evaluación. La sincronización se realiza con Fetch y identificadores únicos para evitar duplicados al repetir el envío. Esta combinación responde a la exigencia de demostrar datos locales y remotos sin depender de servicios de terceros.',47,y-12,498,11,17)
y=p.section('2. Objetivos y alcance',y-23)
y=p.bullet('Objetivo general','Construir una PWA funcional para registrar, consultar y analizar el desempeño deportivo escolar, con consulta sin conexión y demostración de sincronización.',y)
y=p.bullet('Objetivos específicos','Registrar estudiantes y actividades; mostrar historial e indicadores CSR; conservar datos tras recargar; precargar recursos con Service Worker; probar una solicitud Fetch; solicitar permisos sólo cuando el usuario active notificaciones o ubicación.',y)
y=p.para('El alcance corresponde a una demostración académica local. La API no incluye cuentas, control de acceso institucional ni resolución de ediciones simultáneas entre varios docentes. Para una distribución pública con datos reales, esos controles deberán implementarse antes de usar el sistema con información escolar.',47,y-2,498,10,15,GRAY)
p.finish()

p=Page(4,'Arquitectura y decisiones técnicas')
y=729;y=p.section('3. Arquitectura',y)
for title,body in [
('Interfaz y renderizado CSR','HTML semántico, CSS adaptable y JavaScript modular en funciones. Los formularios actualizan inmediatamente tarjetas, historial, gráfica de ocho semanas y totales sin recargar la página.'),
('Persistencia local','IndexedDB mantiene almacenes students, activities y deletions. Los registros se recuperan al iniciar y se escriben antes de cualquier petición de red.'),
('Servicio remoto','Python sirve la aplicación y expone GET /api/health, GET /api/data, POST /api/sync y DELETE /api/activities/:id. SQLite valida y persiste los datos. La solicitud POST via Fetch envía los datos locales y recibe el estado del servidor.'),
('Trabajo sin conexión','El Service Worker precarga HTML, CSS, JS, manifest e iconos. Cache API responde solicitudes del shell; IndexedDB responde consultas y guarda nuevas actividades. Una cola de eliminaciones evita la reaparición de registros al volver la red.'),
('Permisos del dispositivo','La notificación se solicita al guardar una actividad y sólo aparece si se concede permiso. La geolocalización es opcional y se solicita al pulsar Usar ubicación.')]:
    y=p.bullet(title,body,y)
p.rect(47,y-65,500,43,(.92,.96,.91));p.txt(60,y-41,'Flujo de datos',10,'B',INK);p.txt(60,y-56,'Formulario > IndexedDB > CSR > Fetch /api/sync > SQLite',10,'R',INK)
p.finish()

p=Page(5,'Módulos y experiencia de usuario')
y=729;y=p.section('4. Funciones implementadas',y)
for title,body in [
('Splash y Panorama','Pantalla inicial, presentación de SportSchool, estado de conexión, datos resumidos, actividad reciente y accesos directos a los módulos.'),
('Estudiantes','Alta de nombre, grupo y disciplina; búsqueda por esos campos; tarjetas con conteo de sesiones y acceso al historial individual.'),
('Actividades','Captura de fecha, estudiante, tipo, duración, distancia y observaciones. Valida límites y permite adjuntar coordenadas con permiso explícito.'),
('Historial','Lista por estudiante con búsqueda de actividad, fecha, duración, distancia y estado local o sincronizado. Incluye exportación CSV y eliminación.'),
('Desempeño','Totales de actividades, minutos y kilómetros, gráfica de las ocho semanas previas, distribución de disciplinas y filtro por estudiante.'),
('Diseño adaptable','Navegación lateral en escritorio, menú móvil, tarjetas con perspectiva, luces y órbitas CSS. La opción prefers-reduced-motion reduce las animaciones.')]:y=p.bullet(title,body,y)
p.finish()

p=Page(6,'Pruebas y criterios de aceptación')
y=729;y=p.section('5. Resultados comprobados',y)
y=p.para('Se ejecutaron pruebas de reglas de negocio y persistencia SQLite mediante tests.py. La suite confirmó creación y consulta de estudiante y actividad, lectura en una conexión nueva y rechazo de duración, distancia y fecha inválidas. node --check confirmó sintaxis válida de app.js y sw.js. Estos resultados no sustituyen una prueba visual de navegador.',47,y,498,10,15)
rows=[('Registro de estudiante y dos sesiones','Implementado; pendiente de prueba visual'),('Persistencia tras recarga / historial / indicadores','Implementado; pendiente de prueba visual'),('Fetch API y respuesta de sincronización','Implementado; endpoint no observable por restricción de sockets'),('Service Worker, manifest y Cache API','Implementado; pendiente de inspección DevTools'),('Notificación y geolocalización','Implementado; sujeto a permisos del navegador'),('Prueba offline y Lighthouse','Pendiente de ejecución en Chrome del entorno docente')]
y-=22
for title,status in rows:
    p.rect(47,y-27,500,37,(.95,.97,.96) if int((702-y)/37)%2==0 else (1,1,1))
    p.txt(56,y-5,title,9,'B',INK);p.txt(56,y-19,status,8,'R',GRAY);y-=40
y=p.section('Procedimiento de verificación en Chrome',y-8)
y=p.para('Abra http://localhost:8080; registre un estudiante y dos actividades; recargue la página. En DevTools, revise Application → Manifest, Service Workers, Cache Storage e IndexedDB. En Network compruebe POST /api/sync; active Offline, recargue y consulte el historial; registre otra sesión y vuelva a Online. Si dispone de Lighthouse, ejecute la auditoría PWA. Conceda notificaciones sólo si desea verificar la confirmación.',47,y,498,10,15)
p.finish()

p=Page(7,'Evidencias y distribución')
y=729;y=p.section('6. Evidencias solicitadas',y)
y=p.para('El código fuente y los archivos PWA se entregan con este reporte. En el entorno de trabajo, el navegador rechazó el acceso a la dirección local y a archivos del sistema, de modo que no fue posible obtener capturas auténticas de las pantallas ni imágenes de DevTools. Para mantener la integridad de la evidencia, este documento no incluye capturas recreadas o generadas. Las pruebas visuales, el modo offline y Lighthouse quedan señalados como pendientes de ejecución en Chrome.',47,y,498,11,17)
y=p.section('Capturas que debe adjuntar el docente o alumno',y-23)
for title,body in [
('Pantallas principales','Panorama, estudiantes con un perfil, formulario de actividad, historial con dos registros y desempeño con indicadores.'),
('Almacenamiento y funcionamiento offline','DevTools → Application → IndexedDB y Cache Storage; luego Network → Offline y la PWA con historial visible después de recargar.'),
('Servicio y PWA','Network con POST /api/sync y respuesta 200; Application con manifest y Service Worker activo; resultado Lighthouse si está disponible.')]:y=p.bullet(title,body,y)
y=p.section('Ejecución y distribución local',y-10)
y=p.para('Descomprima el proyecto, ejecute python server.py desde la carpeta SportSchool y abra http://localhost:8080. Python crea automáticamente sportschool.sqlite3. No hay URL pública ni repositorio remoto para este trabajo: el código fuente se entrega en el ZIP adjunto y el entorno de ejecución declarado es localhost. La instalación como PWA puede hacerse desde el menú de Chrome en un contexto compatible.',47,y,498,10,15)
p.finish()

p=Page(8,'Conclusiones y referencias')
y=729;y=p.section('7. Conclusiones',y)
y=p.para('Con SportSchool integré la captura de actividades deportivas, la consulta de antecedentes y una lectura visual del progreso del equipo. La decisión de guardar cada registro primero en IndexedDB permite que la información permanezca al alcance del docente incluso si se interrumpe la red. Después, Fetch lleva los cambios a una base SQLite local, y el Service Worker conserva los recursos necesarios para abrir la interfaz.',47,y,498,11,17)
y=p.para('También comprobé que la persistencia y las validaciones del servidor funcionan mediante pruebas directas. Para cerrar la evaluación en el navegador todavía debo incorporar capturas reales de la aplicación, de DevTools y de la prueba sin conexión; no considero esas pruebas aprobadas sin observarlas. Como mejora futura, propondría autenticación por docente, protección de datos escolares, despliegue HTTPS y una estrategia formal para conflictos entre dispositivos.',47,y-12,498,11,17)
y=p.section('Referencias consultadas',y-26)
for title,body in [
('MDN Web Docs','Service Worker API, Web App Manifest, IndexedDB API, Notifications API, Geolocation API y Fetch API. https://developer.mozilla.org/'),
('web.dev','Learn PWA: instalación, trabajo sin conexión y estrategias de almacenamiento. https://web.dev/learn/pwa/'),
('Referencia visual','eXelentex, sitio de diseño utilizado como inspiración de profundidad e interacción. https://www.exelentex.com/')]:y=p.bullet(title,body,y)
p.txt(47,88,'Nota metodológica: las pruebas no observadas se reportan como pendientes.',9,'R',GRAY)
p.finish()


def pdf():
    objects=[]
    def obj(data):objects.append(data);return len(objects)
    catalog=obj(b'')
    pages=obj(b'')
    f1=obj(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>')
    f2=obj(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>')
    refs=[]
    for content in PAGES:
        stream=obj(b'<< /Length '+str(len(content)).encode()+b' >>\nstream\n'+content+b'\nendstream')
        refs.append(obj(f'<< /Type /Page /Parent {pages} 0 R /MediaBox [0 0 {W} {H}] /Resources << /Font << /FR {f1} 0 R /FB {f2} 0 R >> >> /Contents {stream} 0 R >>'.encode()))
    objects[catalog-1]=f'<< /Type /Catalog /Pages {pages} 0 R >>'.encode()
    objects[pages-1]=f'<< /Type /Pages /Kids [ '+ ' '.join(f'{r} 0 R' for r in refs)+f' ] /Count {len(refs)} >>'
    objects[pages-1]=objects[pages-1].encode()
    result=bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n');offsets=[0]
    for i,o in enumerate(objects,1):
        offsets.append(len(result));result.extend(f'{i} 0 obj\n'.encode()+o+b'\nendobj\n')
    start=len(result);result.extend(f'xref\n0 {len(offsets)}\n0000000000 65535 f \n'.encode())
    for off in offsets[1:]:result.extend(f'{off:010d} 00000 n \n'.encode())
    result.extend(f'trailer\n<< /Size {len(offsets)} /Root {catalog} 0 R >>\nstartxref\n{start}\n%%EOF\n'.encode())
    OUTPUT.write_bytes(result)


if __name__=='__main__':
    # La versión actual incluye capturas auténticas y resultados observados.
    import build_evidence_pdf
