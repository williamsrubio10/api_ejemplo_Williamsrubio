import os
from flask import Flask, jsonify, request
from conexion import ConexionDB  
import hashlib
from flask_cors import CORS

app = Flask(__name__)

# Permite peticiones desde cualquier origen (incluyendo Live Server)
CORS(app)

# Configuración mediante variables de entorno (Prioriza la red privada de Railway)
app.config['MYSQL_HOST'] = os.getenv('MYSQLHOST', 'mysql.railway.internal')
app.config['MYSQL_USER'] = os.getenv('MYSQLUSER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQLPASSWORD', 'oWmOBAhHxEIgUWBxuYzIIeTTzsZuTYGb')
app.config['MYSQL_DB'] = os.getenv('MYSQLDATABASE', 'ventas')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQLPORT', 3306))

db = ConexionDB(
    app.config['MYSQL_HOST'],
    app.config['MYSQL_USER'],
    app.config['MYSQL_PASSWORD'],
    app.config['MYSQL_DB'],
    app.config['MYSQL_PORT']
)

@app.route('/')
def index():
    return 'Hola Mundo'

@app.route('/usuario', methods=['GET'])
def listar_usuarios():
    try:
        cursor = db.obtener_cursor()
        cursor.execute("SELECT idemp, usuario, clave, estado FROM usuario")
        datos=cursor.fetchall()
        usuarios = [{'idemp': row[0], 'usuario': row[1], 'clave': row[2], 'estado': row[3]} for row in datos]
        cursor.close()
        return jsonify({
            'usuarios': usuarios,
            'mensaje': 'Lista de usuarios obtenida exitosamente',
            'exito': True
        })
    except Exception as ex:
        return jsonify({"mensaje": f"Error: {str(ex)}", "exito": False}), 500
    

@app.route('/usuario/<int:id>', methods=['GET'])
def listar_usuario_por_id(id):
    try:
        usuario = leer_usuario_bd_by_id(id)
        if usuario:
            return jsonify(usuario)
        else:
            return jsonify({'mensaje': "Usuario no encontrado", 'exito': False}), 404
    except Exception as ex:
        return jsonify({'mensaje': "Error al obtener el usuario", 'exito': False})

def leer_usuario_bd_by_id(id):
    try:
        cursor = db.obtener_cursor()
        cursor.execute("SELECT idemp, usuario, clave, estado FROM usuario WHERE idemp = %s", (id,))
        datos = cursor.fetchone()
        if datos != None:
            usuario = {'idemp': datos[0], 'usuario': datos[1], 'clave': datos[2], 'estado': datos[3]}
            return usuario
        else:
            return None
    except Exception as ex:
        raise ex
    
@app.route('/usuario', methods=['POST'])
def registrar_usuario():
    if (request.json['idemp'] and request.json['usuario'] and request.json['clave'] and request.json['estado'] ):
        try:
            usuario = leer_usuario_bd_by_id(request.json['idemp'])
            if usuario != None:
                return jsonify({'mensaje': "Código ya existe, no se puede duplicar.", 'exito': False})
            else:
                cursor = db.obtener_cursor()
                sql = """INSERT INTO usuario (idemp, usuario, clave, estado) 
                VALUES ('{0}', '{1}', '{2}', '{3}')""".format(request.json['idemp'], request.json['usuario'],hashlib.sha1(request.json['clave'].encode('utf-8')).hexdigest(), request.json['estado'])
                cursor.execute(sql)
                db.conexion.commit()  # Confirma la acción de inserción.
                return jsonify({'mensaje': "Usuario registrado.", 'exito': True})
        except Exception as ex:
            print(f"Error al registrar usuario: {ex}")
            return jsonify({'mensaje': 'error', 'exito': False})
    else:
        return jsonify({'mensaje': "Parámetros inválidos...", 'exito': False})


@app.route('/usuario/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    if (request.json['usuario'] and request.json['clave'] and request.json['estado'] is not None):
        try:
            usuario = leer_usuario_bd_by_id(id)
            if usuario != None:
                cursor = db.obtener_cursor()
                sql = """UPDATE usuario SET usuario = '{0}', clave = '{1}' , estado = '{2}' 
                WHERE idemp = '{3}'""".format(request.json['usuario'], hashlib.sha1(request.json['clave'].encode('utf-8')).hexdigest(), request.json['estado'], id)
                cursor.execute(sql)
                db.conexion.commit()  # Confirma la acción de actualización.
                return jsonify({'mensaje': "Usuario actualizado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    else: 
        return jsonify({'mensaje': "Parámetros inválidos...", 'exito': False})
    

@app.route('/usuario/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    try:
        usuario = leer_usuario_bd_by_id(id)import os
from flask import Flask, jsonify, request
from conexion import ConexionDB  
import hashlib
from flask_cors import CORS

app = Flask(__name__)

# Permite peticiones desde cualquier origen (incluyendo Live Server)
CORS(app)

# Configuración mediante variables de entorno (Prioriza la red privada de Railway)
app.config['MYSQL_HOST'] = os.getenv('MYSQLHOST', 'mysql.railway.internal')
app.config['MYSQL_USER'] = os.getenv('MYSQLUSER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQLPASSWORD', 'oWmOBAhHxEIgUWBxuYzIIeTTzsZuTYGb')
app.config['MYSQL_DB'] = os.getenv('MYSQLDATABASE', 'ventas')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQLPORT', 3306))

db = ConexionDB(
    app.config['MYSQL_HOST'],
    app.config['MYSQL_USER'],
    app.config['MYSQL_PASSWORD'],
    app.config['MYSQL_DB'],
    app.config['MYSQL_PORT']
)

@app.route('/')
def index():
    return 'Hola Mundo'

@app.route('/usuario', methods=['GET'])
def listar_usuarios():
    try:
        cursor = db.obtener_cursor()
        cursor.execute("SELECT idemp, usuario, clave, estado FROM usuario")
        datos = cursor.fetchall()
        usuarios = [{'idemp': row[0], 'usuario': row[1], 'clave': row[2], 'estado': row[3]} for row in datos]
        cursor.close()
        return jsonify({
            'usuarios': usuarios,
            'mensaje': 'Lista de usuarios obtenida exitosamente',
            'exito': True
        })
    except Exception as ex:
        return jsonify({"mensaje": f"Error: {str(ex)}", "exito": False}), 500

@app.route('/usuario/<int:id>', methods=['GET'])
def listar_usuario_por_id(id):
    try:
        usuario = leer_usuario_bd_by_id(id)
        if usuario:
            return jsonify(usuario)
        else:
            return jsonify({'mensaje': "Usuario no encontrado", 'exito': False}), 404
    except Exception as ex:
        return jsonify({'mensaje': "Error al obtener el usuario", 'exito': False})

def leer_usuario_bd_by_id(id):
    try:
        cursor = db.obtener_cursor()
        cursor.execute("SELECT idemp, usuario, clave, estado FROM usuario WHERE idemp = %s", (id,))
        datos = cursor.fetchone()
        if datos is not None:
            return {'idemp': datos[0], 'usuario': datos[1], 'clave': datos[2], 'estado': datos[3]}
        else:
            return None
    except Exception as ex:
        raise ex

@app.route('/usuario', methods=['POST'])
def registrar_usuario():
    if request.json.get('idemp') and request.json.get('usuario') and request.json.get('clave') and request.json.get('estado') is not None:
        try:
            usuario = leer_usuario_bd_by_id(request.json['idemp'])
            if usuario is not None:
                return jsonify({'mensaje': "Código ya existe, no se puede duplicar.", 'exito': False})
            else:
                cursor = db.obtener_cursor()
                sql = "INSERT INTO usuario (idemp, usuario, clave, estado) VALUES (%s, %s, %s, %s)"
                clave_hash = hashlib.sha1(request.json['clave'].encode('utf-8')).hexdigest()
                cursor.execute(sql, (request.json['idemp'], request.json['usuario'], clave_hash, request.json['estado']))
                db.conexion.commit()
                cursor.close()
                return jsonify({'mensaje': "Usuario registrado.", 'exito': True})
        except Exception as ex:
            print(f"Error al registrar usuario: {ex}")
            return jsonify({'mensaje': 'error', 'exito': False})
    else:
        return jsonify({'mensaje': "Parámetros inválidos...", 'exito': False})

@app.route('/usuario/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    if request.json.get('usuario') and request.json.get('clave') and request.json.get('estado') is not None:
        try:
            usuario = leer_usuario_bd_by_id(id)
            if usuario is not None:
                cursor = db.obtener_cursor()
                sql = "UPDATE usuario SET usuario = %s, clave = %s, estado = %s WHERE idemp = %s"
                clave_hash = hashlib.sha1(request.json['clave'].encode('utf-8')).hexdigest()
                cursor.execute(sql, (request.json['usuario'], clave_hash, request.json['estado'], id))
                db.conexion.commit()
                cursor.close()
                return jsonify({'mensaje': "Usuario actualizado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    else:
        return jsonify({'mensaje': "Parámetros inválidos...", 'exito': False})

@app.route('/usuario/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    try:
        usuario = leer_usuario_bd_by_id(id)
        if usuario is not None:
            cursor = db.obtener_cursor()
            sql = "DELETE FROM usuario WHERE idemp = %s"
            cursor.execute(sql, (id,))
            db.conexion.commit()
            cursor.close()
            return jsonify({'mensaje': "Usuario eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

@app.route('/usuario/login', methods=['POST'])
def autenticar_usuario():
    datos = request.get_json(silent=True) or {}
    
    usuario_input = datos.get('usuario') or datos.get('email')
    password_input = datos.get('password') or datos.get('clave')

    if not usuario_input or not password_input:
        return jsonify({'mensaje': "Parámetros inválidos. Se requiere usuario y contraseña.", 'exito': False}), 400

    try:
        cursor = db.obtener_cursor()
        sql = "SELECT idemp, usuario, clave FROM usuario WHERE usuario = %s AND estado = 1"
        cursor.execute(sql, (usuario_input,))
        usuario_db = cursor.fetchone()
        cursor.close()

        if usuario_db is None:
            return jsonify({'mensaje': 'Usuario no encontrado o inactivo', 'exito': False}), 404

        clave_hash = hashlib.sha1(password_input.encode('utf-8')).hexdigest()
        if clave_hash == usuario_db[2]:
            return jsonify({
                'mensaje': 'Login exitoso',
                'exito': True,
                'usuario': {
                    'idemp': usuario_db[0],
                    'usuario': usuario_db[1]
                }
            }), 200
        else:
            return jsonify({'mensaje': 'Contraseña incorrecta', 'exito': False}), 401

    except Exception as ex:
        return jsonify({'mensaje': f'Error en el servidor: {str(ex)}', 'exito': False}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)