"""Ejercita los handlers HTTP sin sockets; no sustituye prueba de navegador."""
import io
import json
import tempfile
from pathlib import Path
import server

def request(path, payload=None):
    handler = object.__new__(server.Handler)
    body = json.dumps(payload).encode() if payload is not None else b''
    handler.path = path
    handler.headers = {'Content-Length': str(len(body))}
    handler.rfile = io.BytesIO(body)
    response = []
    handler._json = lambda status, data: response.append((status, data))
    (handler.do_POST if payload is not None else handler.do_GET)()
    return response[0]

with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as folder:
    server.DATABASE = Path(folder)/'test.sqlite3'
    server.initialize()
    s = dict(id='student-test-001',name='Estudiante de prueba',group='Demo',discipline='Atletismo',createdAt='2026-11-21T12:00:00Z')
    a = dict(id='activity-test-001',studentId=s['id'],date='2026-11-21',type='Carrera',minutes=30,distance=3,notes='Prueba',location=None,createdAt=s['createdAt'])
    b = {**a,'id':'activity-test-002','minutes':45,'distance':5}
    payload = dict(students=[s],activities=[a,b],deletions=[])
    assert request('/api/health')[0] == 200
    assert request('/api/sync',payload)[0] == 200
    status, data = request('/api/sync',payload)
    assert status==200 and len(data['students'])==1 and len(data['activities'])==2
    assert sum(x['minutes'] for x in data['activities'])==75
    assert sum(x['distance'] for x in data['activities'])==8
    assert len(request('/api/data')[1]['activities'])==2
    assert request('/api/sync',{**payload,'activities':[{**a,'minutes':0}]})[0]==400
    status,data=request('/api/sync',{**payload,'deletions':[a['id']]})
    assert status==200 and [x['id'] for x in data['activities']]==[b['id']]
print('OK: health, 1 estudiante, 2 actividades, 75 min, 8 km, persistencia, idempotencia, validacion y eliminacion. Prueba sin sockets.')
