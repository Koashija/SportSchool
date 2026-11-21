"""SportSchool: servidor HTTP local y API SQLite, sin dependencias externas."""
from __future__ import annotations

import json
import os
import re
import sqlite3
import sys
from contextlib import contextmanager
from datetime import date
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import RLock
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / 'public'
DATABASE = Path(os.environ.get('SPORTSCHOOL_DB', str(ROOT / 'sportschool.sqlite3')))
LOCK = RLock()
MAX_BODY = 2_000_000


@contextmanager
def connect():
    con = sqlite3.connect(DATABASE, timeout=10)
    con.row_factory = sqlite3.Row
    con.execute('PRAGMA foreign_keys=ON')
    con.execute('PRAGMA journal_mode=WAL')
    try:
        with con:
            yield con
    finally:
        con.close()


def initialize():
    with connect() as con:
        con.executescript('''
          CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY, name TEXT NOT NULL, group_name TEXT NOT NULL,
            discipline TEXT NOT NULL, created_at TEXT NOT NULL
          );
          CREATE TABLE IF NOT EXISTS activities (
            id TEXT PRIMARY KEY, student_id TEXT NOT NULL REFERENCES students(id),
            date TEXT NOT NULL, type TEXT NOT NULL, minutes INTEGER NOT NULL,
            distance REAL NOT NULL, notes TEXT NOT NULL, location TEXT,
            created_at TEXT NOT NULL
          );
          CREATE INDEX IF NOT EXISTS idx_activity_student_date ON activities(student_id,date);
        ''')


def check_student(s):
    if not isinstance(s, dict) or not isinstance(s.get('id'), str) or not re.fullmatch(r'[\w-]{8,80}', s['id']):
        raise ValueError('Identificador de estudiante inválido.')
    for field, limit in [('name', 100), ('group', 40), ('discipline', 60)]:
        if not isinstance(s.get(field), str) or not 1 <= len(s[field].strip()) <= limit:
            raise ValueError(f'Campo {field} inválido.')
    if not isinstance(s.get('createdAt'), str):
        raise ValueError('Fecha de creación inválida.')


def check_activity(a):
    if not isinstance(a, dict) or not isinstance(a.get('id'), str) or not re.fullmatch(r'[\w-]{8,80}', a['id']):
        raise ValueError('Identificador de actividad inválido.')
    if not isinstance(a.get('studentId'), str):
        raise ValueError('Estudiante inválido.')
    try:
        date.fromisoformat(a['date'])
    except (ValueError, KeyError, TypeError):
        raise ValueError('Fecha inválida.') from None
    if not isinstance(a.get('type'), str) or not 1 <= len(a['type'].strip()) <= 80:
        raise ValueError('Tipo de actividad inválido.')
    if type(a.get('minutes')) is not int or not 1 <= a['minutes'] <= 1440:
        raise ValueError('Duración inválida.')
    if type(a.get('distance')) not in (float, int) or not 0 <= a['distance'] <= 1000:
        raise ValueError('Distancia inválida.')
    if not isinstance(a.get('notes', ''), str) or len(a.get('notes', '')) > 500:
        raise ValueError('Observaciones inválidas.')
    if not isinstance(a.get('createdAt'), str):
        raise ValueError('Fecha de creación inválida.')
    location = a.get('location')
    if location is not None and (not isinstance(location, dict) or
            type(location.get('latitude')) not in (float, int) or
            type(location.get('longitude')) not in (float, int) or
            not -90 <= location['latitude'] <= 90 or not -180 <= location['longitude'] <= 180):
        raise ValueError('Ubicación inválida.')


def snapshot(con):
    students = [dict(id=r['id'], name=r['name'], group=r['group_name'], discipline=r['discipline'], createdAt=r['created_at'])
                for r in con.execute('SELECT * FROM students ORDER BY name')]
    activities = [dict(id=r['id'], studentId=r['student_id'], date=r['date'], type=r['type'],
                       minutes=r['minutes'], distance=r['distance'], notes=r['notes'],
                       location=json.loads(r['location']) if r['location'] else None, createdAt=r['created_at'])
                  for r in con.execute('SELECT * FROM activities ORDER BY date DESC, created_at DESC')]
    return {'students': students, 'activities': activities}


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map,
                      '.js': 'application/javascript',
                      '.webmanifest': 'application/manifest+json'}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC), **kwargs)

    def _json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        if not self.path.startswith('/api/'):
            self.send_header('Cache-Control', 'no-cache')
        self.send_header('X-Content-Type-Options', 'nosniff')
        super().end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/api/health':
            return self._json(200, {'ok': True, 'service': 'SportSchool API', 'storage': 'SQLite'})
        if path == '/api/data':
            with LOCK, connect() as con:
                return self._json(200, snapshot(con))
        if path.startswith('/api/'):
            return self._json(404, {'error': 'Ruta no encontrada.'})
        return super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != '/api/sync':
            return self._json(404, {'error': 'Ruta no encontrada.'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= MAX_BODY:
                return self._json(413, {'error': 'Solicitud vacía o demasiado grande.'})
            payload = json.loads(self.rfile.read(length))
            students, activities, deletions = payload['students'], payload['activities'], payload.get('deletions', [])
            if not isinstance(students, list) or not isinstance(activities, list) or not isinstance(deletions, list) or len(students) > 5000 or len(activities) > 50000 or len(deletions) > 50000:
                raise ValueError('Listas de registros inválidas.')
            for s in students:
                check_student(s)
            for a in activities:
                check_activity(a)
            if any(not isinstance(x, str) or not re.fullmatch(r'[\w-]{8,80}', x) for x in deletions):
                raise ValueError('Eliminaciones inválidas.')
            with LOCK, connect() as con:
                for s in students:
                    con.execute('INSERT OR IGNORE INTO students VALUES (?,?,?,?,?)',
                                (s['id'], s['name'].strip(), s['group'].strip(), s['discipline'].strip(), s['createdAt']))
                for a in activities:
                    con.execute('INSERT OR IGNORE INTO activities VALUES (?,?,?,?,?,?,?,?,?)',
                                (a['id'], a['studentId'], a['date'], a['type'].strip(), a['minutes'], a['distance'],
                                 a.get('notes', '').strip(), json.dumps(a.get('location')) if a.get('location') else None, a['createdAt']))
                for identifier in deletions:
                    con.execute('DELETE FROM activities WHERE id=?', (identifier,))
                result = snapshot(con)
            return self._json(200, result)
        except (ValueError, KeyError, TypeError, json.JSONDecodeError, sqlite3.IntegrityError) as exc:
            return self._json(400, {'error': str(exc)})

    def do_DELETE(self):
        match = re.fullmatch(r'/api/activities/([\w-]{8,80})', urlparse(self.path).path)
        if not match:
            return self._json(404, {'error': 'Ruta no encontrada.'})
        with LOCK, connect() as con:
            con.execute('DELETE FROM activities WHERE id=?', (match[1],))
        return self._json(200, {'ok': True})


if __name__ == '__main__':
    try:
        initialize()
        port = int(os.environ.get('SPORTSCHOOL_PORT', '8080'))
        httpd = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    except (OSError, ValueError, sqlite3.Error) as error:
        print(f'No se pudo iniciar SportSchool: {error}', file=sys.stderr, flush=True)
        print('Comprueba el puerto y los permisos. No hay servidor disponible.', file=sys.stderr)
        sys.exit(1)
    print(f'Servidor iniciado. Abre http://127.0.0.1:{port}/', flush=True)
    print(f'Diagnostico: http://127.0.0.1:{port}/api/health', flush=True)
    print('Manten esta terminal abierta. Ctrl+C detiene el servidor.', flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nSportSchool detenido.')
    finally:
        httpd.server_close()
