"""Empaqueta el proyecto preservando la estructura de carpetas."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parent
files = ['README.md', 'server.py', 'create_icons.py', 'tests.py', 'tests_api.py', 'tests_sync.cjs', 'package.py', '.gitignore', '.gitattributes',
         'public/index.html', 'public/styles.css', 'public/app.js', 'public/sw.js',
         'public/manifest.webmanifest', 'public/icons/icon-192.png',
         'public/icons/icon-512.png', 'documentacion/build_report.py',
         'documentacion/Reporte_SportSchool_UTVT.pdf', 'documentacion/build_verification.py',
         'documentacion/Anexo_Verificacion_SportSchool.pdf', 'documentacion/VERIFICACION.md',
         'documentacion/build_evidence_pdf.py', 'documentacion/Reporte_final.html',
         'evidencias/01-estudiantes.jpg', 'evidencias/02-formulario.jpg',
         'evidencias/03-historial-recarga.jpg', 'evidencias/04-desempeno.jpg',
         'evidencias/05-inicio.jpg', 'evidencias/06-offline-historial.jpg',
         'evidencias/07-offline-nuevo-registro.jpg',
         'evidencias/08-sincronizado-tras-reinicio.jpg']
with ZipFile(root / 'SportSchool_codigo_y_reporte.zip', 'w', ZIP_DEFLATED) as archive:
    for filename in files:
        archive.write(root / filename, 'SportSchool/' + filename)
print('Paquete creado:', len(files), 'archivos')
