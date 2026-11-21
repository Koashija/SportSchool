"""Pruebas del almacenamiento y reglas de negocio sin abrir sockets."""
import tempfile
from pathlib import Path

import server

with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as folder:
    server.DATABASE = Path(folder) / 'test.sqlite3'
    server.initialize()
    student = {'id': 'student-12345678', 'name': 'Andrea Martínez', 'group': 'IDGS-104',
               'discipline': 'Atletismo', 'createdAt': '2026-11-21T12:00:00Z'}
    activity = {'id': 'activity-12345678', 'studentId': student['id'], 'date': '2026-11-21',
                'type': 'Carrera', 'minutes': 45, 'distance': 5.2, 'notes': 'Buen ritmo',
                'location': None, 'createdAt': '2026-11-21T12:05:00Z'}
    server.check_student(student)
    server.check_activity(activity)
    with server.connect() as db:
        db.execute('INSERT INTO students VALUES (?,?,?,?,?)',
                   (student['id'], student['name'], student['group'], student['discipline'], student['createdAt']))
        db.execute('INSERT INTO activities VALUES (?,?,?,?,?,?,?,?,?)',
                   (activity['id'], student['id'], activity['date'], activity['type'], 45, 5.2, activity['notes'], None, activity['createdAt']))
        result = server.snapshot(db)
        assert result['students'][0]['name'] == student['name']
        assert result['activities'][0]['distance'] == 5.2
    with server.connect() as db:
        assert len(server.snapshot(db)['activities']) == 1, 'SQLite debe sobrevivir a nueva conexión'
    for invalid in [{**activity, 'minutes': 0}, {**activity, 'distance': -1}, {**activity, 'date': 'ayer'}]:
        try:
            server.check_activity(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError('Se aceptó una actividad inválida')
print('OK: SQLite, persistencia, consulta y validación')
