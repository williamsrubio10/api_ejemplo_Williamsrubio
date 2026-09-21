import pymysql

class ConexionDB:
    def __init__(self, host, user, password, db, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.conexion = None

    def conectar(self):
        if self.conexion is None or not self.conexion.open:
            self.conexion = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                db=self.db,
                cursorclass=pymysql.cursors.Cursor
            )
        return self.conexion

    def obtener_cursor(self):
        return self.conectar().cursor()