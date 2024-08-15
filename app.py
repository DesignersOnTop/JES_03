import os
import pymysql
from flask import Flask, render_template, request, redirect, session, send_from_directory, url_for, flash
from werkzeug.utils import secure_filename
from datetime import datetime
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
# Crear la aplicación
app = Flask(__name__)

# Crear una llave secreta
app.secret_key = 'JES'

# Configurar la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'jes'

# Carpeta para subir los archivos, fotos, pdf, etc.
UPLOAD_FOLDER = '/static/documentos'  # Cambia esto si es necesario
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configurar la carpeta de carga
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'documentos')

# Crear la carpeta si no existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
#-----------------------------------------------------

@app.route('/')
def Index():
    session.clear()
    return render_template('index.html')
    
@app.route('/login', methods=['POST'])
def login():
    matricula = request.form['matricula-sesion']
    password = request.form['pass-sesion']
    
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    # Verificación de estudiantes
    cursor.execute("SELECT * FROM estudiantes WHERE matricula = %s", (matricula,))
    estudiante = cursor.fetchone()
    if estudiante and estudiante['contraseña'] == password:
        session['user_id'] = estudiante['id_estudiante']
        session['role'] = 'estudiante'
        return redirect('/home/estudiante/')

    # Verificación de profesores
    cursor.execute("SELECT * FROM profesores WHERE matricula = %s", (matricula,))
    profesor = cursor.fetchone()
    if profesor and profesor['contraseña'] == password:
        session['user_id'] = profesor['id_profesor']
        session['role'] = 'profesor'
        return redirect('/home/profesor/')

    # Verificación de administradores
    cursor.execute("SELECT * FROM admin WHERE matricula = %s", (matricula,))
    admin = cursor.fetchone()
    if admin and admin['contraseña'] == password:
        session['user_id'] = admin['id_admin']
        session['role'] = 'admin'
        return redirect('/home/admin/')
    return redirect('/')

# HOME ESTUDIANTE
@app.route('/home/estudiante/', methods=['GET'])
def home_estudiante():
    if 'user_id' not in session or session.get('role') != 'estudiante':
        return redirect('/')

    estudiante_id = session['user_id']

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT imagen_perfil FROM estudiantes WHERE id_estudiante = %s", (estudiante_id,))
    estudiante = cursor.fetchone()

    # calificacion estudiante
    cursor.execute("""
        SELECT 
            calificaciones.id_estudiante,
            asignaturas.nom_asignatura AS nom_asignatura,
            calificaciones.C1,
            calificaciones.C2,
            calificaciones.C3,
            calificaciones.C4,
            calificaciones.`C. Final`
        FROM 
            calificaciones
        JOIN 
            asignaturas ON calificaciones.id_asignatura = asignaturas.id_asignatura
        WHERE 
            calificaciones.id_estudiante = %s
    """, (estudiante_id,))
    calificaciones = cursor.fetchall()

    # horario estudiante
    cursor.execute("SELECT * FROM horario WHERE id_estudiante = %s", (estudiante_id,))
    horarios = cursor.fetchall()

    # asistencias estudiante
    cursor.execute("SELECT * FROM asistencias WHERE id_estudiante = %s", (estudiante_id,))
    asistencias = cursor.fetchall()

    cursor.close()

    return render_template('estudiante/e-home.html', calificaciones=calificaciones, horarios=horarios, asistencias=asistencias, estudiante=estudiante)


@app.route('/estudiante/perfil/')
def e_perfil():
    if 'user_id' not in session or session.get('role') != 'estudiante':
        return redirect('/')
    
    estudiante_id = session['user_id']
    
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM `estudiantes` WHERE id_estudiante = %s', (estudiante_id,))
    perfil = cursor.fetchall()
    
    cursor.execute('''
    SELECT cursos.nombre
    FROM estudiantes
    JOIN cursos ON estudiantes.id_curso = cursos.id_curso
    WHERE estudiantes.id_estudiante = %s''', (estudiante_id,))
    curso = cursor.fetchone()
    
    cursor.close()
    
    return render_template('./estudiante/e-perfil.html', perfil=perfil[0], curso=curso)

@app.route('/estudiante/material/', methods=['GET', 'POST'])
def e_material():
    if 'user_id' not in session or session.get('role') != 'estudiante':
        return redirect('/')

    estudiante_id = session['user_id']
    
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    # las asignaturas disponibles
    cursor.execute('''
    SELECT asignaturas.id_asignatura, asignaturas.nom_asignatura
    FROM asignaturas
    JOIN material_estudio ON asignaturas.id_asignatura = material_estudio.id_asignatura
    JOIN estudiantes ON estudiantes.id_curso = material_estudio.id_curso
    WHERE estudiantes.id_estudiante = %s''', (estudiante_id,))
    asignaturas = cursor.fetchall()

    # materiales vacío
    materiales = []

    if request.method == 'POST':
        materia_seleccionada = request.form.get('materias-agg')

        # Buscar materiales para la asignatura seleccionada
        cursor.execute('''
            SELECT material_estudio.*, asignaturas.nom_asignatura
            FROM material_estudio
            JOIN estudiantes ON material_estudio.id_curso = estudiantes.id_curso
            JOIN asignaturas ON material_estudio.id_asignatura = asignaturas.id_asignatura
            WHERE material_estudio.id_asignatura = %s AND estudiantes.id_estudiante = %s''', (materia_seleccionada, estudiante_id))
        materiales = cursor.fetchall()

    cursor.close()
    
    return render_template('./estudiante/e-material_estudio.html', asignaturas=asignaturas, materiales=materiales)

@app.route('/estudiante/material/<titulo>')
def ver_materia(titulo):
    if 'user_id' not in session or session.get('role') != 'estudiante':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Obtener detalles del material por título
    cursor.execute('''
        SELECT material_estudio.*, asignaturas.nom_asignatura
        FROM material_estudio
        JOIN asignaturas ON material_estudio.id_asignatura = asignaturas.id_asignatura
        WHERE material_estudio.titulo = %s
    ''', (titulo,))
    material = cursor.fetchone()

    cursor.close()

    return render_template('estudiante/e-ver_materias.html', material=material)

@app.route('/estudiante/enviar/tarea/', methods=['POST'])
def enviar_tarea():
    if 'user_id' not in session or session.get('role') != 'estudiante':
        return redirect('/')

    estudiante_id = session['user_id']
    material_id = request.form.get('material_id')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Obtener la información del material
    cursor.execute('''
        SELECT id_curso
        FROM material_estudio
        WHERE id_material = %s
    ''', (material_id,))
    material = cursor.fetchone()

    if material:
        id_curso = material['id_curso']
    else:
        cursor.close()
        flash('Material no encontrado')
        return redirect('/estudiante/material/')

    # Procesar el archivo subido
    if 'subir-tarea' not in request.files:
        cursor.close()
        flash('No se ha subido ningún archivo')
        return redirect('/estudiante/material/')

    tarea = request.files['subir-tarea']
    if tarea.filename == '':
        cursor.close()
        flash('No se seleccionó ningún archivo')
        return redirect('/estudiante/material/')

    if tarea:
        archivos = secure_filename(tarea.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], archivos)
        tarea.save(file_path)

        cursor.execute('''
            INSERT INTO tareas_estudiante (id_estudiante, id_curso, tarea)
            VALUES (%s, %s, %s)
        ''', (estudiante_id, id_curso, archivos))

        connection.commit()
        cursor.close()

        flash('Tarea enviada exitosamente')
        return redirect('/estudiante/material/')

    cursor.close()
    flash('Error al subir el archivo')
    return redirect('/estudiante/material/')

@app.route('/estudiante/refuerzo/libros/')
def e_refuerzo_libros():
    if 'user_id' not in session or session.get('role') != 'estudiante':
        return redirect('/')

    estudiante_id = session['user_id']
    
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute(
    '''
        SELECT libros.*, asignaturas.nom_asignatura
        FROM libros
        JOIN estudiantes ON libros.id_curso = estudiantes.id_curso
        JOIN asignaturas ON libros.id_asignatura = asignaturas.id_asignatura
        WHERE estudiantes.id_estudiante = %s
    ''', (estudiante_id,))
    
    libros = cursor.fetchall()
    cursor.close()
    
    return render_template('./estudiante/e_refuerzo_libros.html', libros=libros)

@app.route('/estudiante/libro/<titulo>')
def e_libro(titulo):
    if 'user_id' not in session or session.get('role') != 'estudiante':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Obtener detalles del libro por título
    cursor.execute('''
        SELECT libros.*, asignaturas.nom_asignatura
        FROM libros
        JOIN asignaturas ON libros.id_asignatura = asignaturas.id_asignatura
        WHERE libros.titulo = %s
    ''', (titulo,))
    
    libro = cursor.fetchone()
    cursor.close()

    return render_template('estudiante/e-libro-refuerzo.html', libro=libro)

@app.route('/estudiante/refuerzo/videos/')
def e_refuerzo_videos():
    estudiante_id = session['user_id']
    if 'user_id' not in session or session.get('role') != 'estudiante':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute(
        '''
        SELECT videos.*, asignaturas.nom_asignatura
        FROM videos
        JOIN estudiantes ON videos.id_curso = estudiantes.id_curso
        JOIN asignaturas ON videos.id_asignatura = asignaturas.id_asignatura
        WHERE estudiantes.id_estudiante = %s
        ''', (estudiante_id,)
    )
    
    videos = cursor.fetchall()
    cursor.close()
    return render_template('./estudiante/e_refuerzo_videos.html', videos=videos)

@app.route('/estudiante/video/<titulo>')
def e_videos(titulo):
    if 'user_id' not in session or session.get('role') != 'estudiante':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute('''
        SELECT videos.*, asignaturas.nom_asignatura
        FROM videos
        JOIN asignaturas ON videos.id_asignatura = asignaturas.id_asignatura
        WHERE videos.titulo = %s
    ''', (titulo,))
    
    video = cursor.fetchone()
    cursor.close()
    
    return render_template('./estudiante/e-video-clase.html', video = video)


# APARTADO DEL ADMIN EN PYTHON

@app.route('/home/admin/')
def a_home():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    # Estudiantes
    cursor.execute('SELECT * FROM estudiantes')
    estudiantes = cursor.fetchall()
    # Profesores
    cursor.execute('SELECT * FROM profesores')
    profesores = cursor.fetchall()
    # Cerrar la conexion para seguridad
    cursor.close()
    return render_template('./admin/a-home.html', estudiantes=estudiantes, profesores=profesores)

@app.route('/admin/cursos/')
def a_cursos():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM `cursos`')
    cursos = cursor.fetchall()
    cursor.close()
    return render_template('./admin/a-cursos.html', cursos=cursos)

# @app.route('/admin/agregar_cursos', methods = ['POST'])
# def agregar_cursos():


@app.route('/admin/curso/', methods = ['GET'])
def mostrar_estudiantes():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM estudiantes')
    estudiantes = cursor.fetchall()
    cursor.close()
    return render_template('./admin/a-curso.html', estudiantes=estudiantes)

@app.route('/admin/materias/')
def a_materias():
    return render_template('./admin/a-materias.html')

@app.route('/admin/asignar-profesores')
def a_asignar_profesores():
    return render_template('./admin/a-agregar-profesor-cursos.html')

@app.route('/admin/agregar-materias')
def a_agg_materias():
    return render_template('./admin/a-agg-materias.html')

@app.route('/admin/subir_materia', methods = ['POST'])
def subir_materia():
    nom_asignatura = request.form["nom_asignatura"]

    datos = (nom_asignatura)
    
    sql = '''INSERT INTO `asignaturas` (`id_asignatura`, `nom_asignatura`) VALUES (NULL, %s,)'''

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql,datos)
    connection.commit()
    cursor.close()
    return redirect('/admin/materias/')

@app.route('/admin/eliminar_materia/<int:id_asignatura>', methods = ['POST'])
def eliminar_materia(id_asignatura):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute('DELETE FROM asignaturas WHERE id_asignatura = %s', (id_asignatura))

    return redirect('/admin/materias/')

@app.route('/admin/reportes/')
def a_reportes():
    return render_template('./admin/a-reporte-curso.html')

@app.route('/admin/reportes-profesor/')
def a_reporte_profesor():
    return render_template('./admin/a-reporte-profesor.html')

@app.route('/admin/perfil/')
def a_perfil():
    sql = 'SELECT nombre_admin, matricula, a_email, a_genero, a_direccion, a_telefono FROM admin'

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)

    admin = cursor.fetchall()
    cursor.close()

    return render_template('./admin/a-perfil.html', admin = admin)

@app.route('/admin/reportes-calificacion/')
def a_reporte_calificaciones():
    return render_template('./admin/a-calificaciones-reporte.html')

@app.route('/admin/reportes-asistencias/')
def a_reportes_asistencia():
    return render_template('./admin/a-asistencia-reporte.html')

@app.route('/admin/registro/estudiante/')
def a_formulario_registro_e():
    return render_template('./admin/a-formulario-registro-e.html')

@app.route('/agregar_estudiantes', methods = ['POST'])
def agregar_estudiante():
    # Insertar estudiantes
    id_curso = request.form["id_curso"]
    matricula = request.form["matricula"]
    nombre = request.form["nombre"]
    apellidos = request.form["apellidos"]
    direccion = request.form["direccion"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    genero = request.form["genero"]
    correo = request.form["email"]
    telefono = request.form["telefono"]
    imagen_perfil = request.files["imagen_perfil"].filename
    contrasena = request.form["contrasena"]
    
    if imagen_perfil and imagen_perfil.filename:
        estudiante_perfil = imagen_perfil.read()

    sql = 'INSERT INTO `estudiantes` (`id_estudiante`,`id_curso`, `matricula`, `nombre`, `apellidos`, `direccion`, `fecha_nacimiento`, `genero`, `email`, `telefono`, `imagen_perfil`, `contraseña`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    datos = (id_curso, matricula, nombre, apellidos, direccion, fecha_nacimiento, genero, correo, telefono, estudiante_perfil, contrasena)

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql,datos)
    
    connection.commit()
    cursor.close()

    return redirect('/admin/curso/')

@app.route('/editar_estudiante/<int:id>', methods=['GET'])
def editar_estudiante(id):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM estudiantes WHERE id = %s", (id))
    estudiante = cursor.fetchone()
    cursor.close()

    if estudiante:
        return render_template('./admin/a-editar-datos-estudiantes.html', estudiante=estudiante)
    else:
        return "Estudiante no encontrado", 404
    
@app.route('/editar_profesor/<int:id>', methods=['GET'])
def editar_profesor(id):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM profesores WHERE id = %s", (id))
    profesor = cursor.fetchone()
    cursor.close()

    if profesor:
        return render_template('./admin/a-editar-datos-profesores.html', profesor = profesor)
    else:
        return "Profesor no encontrado", 404

@app.route('/actualizar_estudiantes', methods = ['POST'])
def actualizar_estudiantes():
    # Actualizar estudiantes
    id_estudiante = request.form["id_estudiante"]
    nombre = request.form["nombre"]
    apellidos = request.form["apellidos"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    genero = request.form["genero"]
    curso = request.form["curso"]
    correo = request.form["email"]
    telefono = request.form["telefono"]
    direccion = request.form["direccion"]
    matricula = request.form["matricula"]
    contrasena = request.form["contrasena"]

    # Aqui indicamos lo que se cambiará y de donde lo hará
    sql =  '''UPDATE estudiantes SET nombre = %s, apellidos = %s, fecha_nacimiento = %s, genero = %s, curso = %s, correo = %s, telefono = %s, direccion = %s, matricula = %s, contraseña = %s WHERE id_estudiante = %s'''
    
    datos = (nombre, apellidos, fecha_nacimiento, genero, curso, correo, telefono, direccion, matricula, contrasena)

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql, datos)

    connection.commit()
    cursor.close()

    return redirect('/admin/curso/')

@app.route('/admin/eliminar_estudiantes', methods = ['POST'])
def eliminar_estudiantes():
    id_estudiante = request.form["id_estudiante"]

    # Se hace una confirmación de si el id introducido existe
    if id_estudiante in 'estudiantes':
        sql = 'DELETE FROM estudiantes WHERE id_estudiante = %s', (id_estudiante)
        return redirect('/admin/curso/')
    
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)

    connection.commit()
    cursor.close()

@app.route('/admin/registro/profesor/')
def a_formulario_registro_p():
    return render_template('./admin/a-formulario-registro-p.html')

@app.route('/admin/agregar_profesores', methods = ['POST'])
def agregar_profesores():
    # Insertar profesores
    id_asignatura = request.form["id_asignatura"]
    matricula = request.form["matricula"]
    nombre = request.form["nombre"]
    apellidos = request.form["apellidos"]
    direccion = request.form["direccion"]
    cedula = request.form["cedula"]
    genero = request.form["genero"]
    correo = request.form["email"]
    telefono = request.form["telefono"]
    imagen_perfil = request.files["imagen_perfil"].filename
    contrasena = request.form["contrasena"]
    
    if imagen_perfil and imagen_perfil.filename:
        profesor_perfil = imagen_perfil.read()

    sql = 'INSERT INTO `profesores` (`id_profesor`,`id_asignatura`, `matricula`, `nombre`, `apellido`, `direccion`, `cedula`, `genero`, `email`, `telefono`, `imagen_perfil`, `contraseña`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    datos = (id_asignatura, matricula, nombre, apellidos, direccion, cedula, genero, correo, telefono, profesor_perfil, contrasena)

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql,datos)
    
    connection.commit()
    cursor.close()
    
    return redirect('/home/admin/')

    # return redirect('./admin/a-curso.html')

@app.route('/admin/actualizar_profesor', methods=['POST'])
def actualizar_profesor():
    id_profesor = request.form["id_profesor"]
    id_asignatura = request.form["id_asignatura"]
    nombre = request.form["nombre"]
    apellidos = request.form["apellidos"]
    direccion = request.form["direccion"]
    cedula = request.form["cedula"]
    genero = request.form["genero"]
    correo = request.form["email"]
    telefono = request.form["telefono"]
    matricula = request.form["matricula"]
    imagen_perfil = request.files["imagen_perfil"].filename
    contrasena = request.form["contrasena"]

    sql =  '''UPDATE profesores SET id_asignatura = %s, nombre = %s, apellido = %s, direccion = %s, cedula = %s, genero = %s, correo = %s, telefono = %s, matricula = %s,imagen_perfil = %s, contraseña = %s WHERE id_profesor = %s'''
    
    datos = (id_asignatura, nombre, apellidos, direccion, cedula, genero, correo, telefono, matricula,imagen_perfil, contrasena)

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql, datos)

    connection.commit()
    cursor.close()

    return redirect('/home/admin/')

@app.route('/admin/eliminar_profesores', methods = ['POST'])
def eliminar_profesores():
    id_profesor = request.form["id_profesor"]

    # Se hace una confirmación de si el id introducido existe
    if id_profesor in 'profesores':
        sql = 'DELETE FROM profesores WHERE id_profesor = %s', (id_profesor)
        return redirect('/home/admin/')
    
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)

    connection.commit()
    cursor.close()

@app.route('/admin/profesores/')
def a_cursos_profesor():
    sql = 'SELECT id_profesor, nombre, apellido, cedula, id_asignatura FROM profesores'

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)

    profesores = cursor.fetchall()
    cursor.close()
    return render_template('./admin/a-profesor-1_a.html', profesores=profesores)

@app.route('/admin/estudiantes')
def a_cursos_estudiantes():
    sql = 'SELECT id_estudiante, nombre, apellido, fecha_nacimiento, id_curso FROM estudiantes'

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)

    estudiantes = cursor.fetchall()
    cursor.close()
    return render_template('./admin/a-estudiante-1_a.html')

@app.route('/admin/horario/')
def a_horario_profesor():
    return render_template('./admin/a-horario-1a.html')

# =========================================================

# APARTADO DEL PROFESORES EN PYTHON Smailyn 
@app.route('/home/profesor/')
def p_home():
    return render_template('./profesor/p-home-a.html')

@app.route('/profesor/perfil/')
def p_perfil():
    return render_template('./profesor/p-perfil.html')

@app.route('/profesor/refuerzo/libros/')
def p_refuerzo_libros():
    return render_template('./profesor/p-refuerzo-libros.html')

@app.route('/profesor/refuerzo/libros/')
def p_refuerzo_libro():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM libros')
    libros = cursor.fetchall()
    cursor.close()
    
    return render_template('./profesor/p-refuerzo-libros.html', libros=libros)

@app.route('/eliminar/libro/<int:libro_id>', methods=['POST'])
def eliminar_libro(libro_id):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor()
    # Obtener el nombre del archivo asociado al libro
    cursor.execute('SELECT libro FROM libros WHERE id = %s', (libro_id,))
    libro = cursor.fetchone()
    
    # Eliminar el archivo del sistema de archivos si existe
    if libro and libro['libro']:
        libro_path = os.path.join(app.config['UPLOAD_FOLDER'], libro['libro'])
        if os.path.exists(libro_path):
            os.remove(libro_path)
    
    # Eliminar el registro de la base de datos
    cursor.execute('DELETE FROM libros WHERE id = %s', (libro_id,))
    connection.commit()
    cursor.close()
    
    return redirect('/profesor/refuerzo/libros/')


@app.route('/profesor/refuerzo/libros/nombre_libro')
def p_libro_refuerzo():
    return render_template('./profesor/p-libro-refuerzo.html')

@app.route('/ver/libro/<int:libro_id>')
def ver_libro(libro_id):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM libros WHERE id = %s', (libro_id,))
    libro = cursor.fetchone()
    cursor.close()

    if libro:
        # Asegúrate de que `libro` tenga un campo para el archivo, como `libro`
        archivo = libro.get('subir_libro')
        return render_template('p-libro-refuerzo.html', libro=libro, archivo=archivo)
    else:
        return 'Libro no encontrado', 404

@app.route('/profesor/refuerzo/videos/')
def p_refuerzo_videos():
    return render_template('./profesor/p-refuerzo-videos.html')

@app.route('/profesor/agregar/libros/')
def agregar_libro():
    return render_template('/profesor/p-agregar-libro.html')

@app.route('/profesor/agregar/libros/', methods=['GET', 'POST'])
def p_agregar_libro():
    if request.method == 'POST':
        # Obtener el archivo de portada del formulario
        portada = request.files.get('portada_libro')
        
        # Obtener los datos del libro del formulario
        titulo = request.form.get('titulo-libro')
        materia = request.form.get('materia-libro')
        
        # Obtener el archivo del libro del formulario
        libro = request.files.get('subir-libro')
        
        # Procesar el archivo de portada
        portada_nombre = portada.filename if portada and portada.filename else None

        # Procesar el archivo del libro
        if libro and libro.filename:
            tiempo = datetime.now()
            horaActual = tiempo.strftime('%Y%H%M%S')
            nuevoNombre = horaActual + "_" + libro.filename
            libro.save(os.path.join(app.config['UPLOAD_FOLDER'], nuevoNombre))
        else:
            nuevoNombre = None
        
        # Valores de asignación y curso
        id_asignatura = 2408
        id_curso = 1
        
        # SQL para insertar el nuevo libro en la base de datos
        sql = '''
        INSERT INTO libros (id_asignatura, id_curso, titulo, subir_libro, portada)
        VALUES (%s, %s, %s, %s, %s)
        '''
        datos = (id_asignatura, id_curso, titulo, nuevoNombre, portada_nombre)
        
        try:
            # Conectar a la base de datos
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                database='jes'
            )
            cursor = connection.cursor()
            
            # Ejecutar la consulta SQL
            cursor.execute(sql, datos)
            connection.commit()  # Confirmar los cambios en la base de datos
            print("Datos guardados en la base de datos.")
        except pymysql.MySQLError as e:
            print(f"Error en la base de datos: {e}")
            connection.rollback()  # Deshacer los cambios en caso de error
        finally:
            cursor.close()  # Cerrar el cursor
            connection.close()  # Cerrar la conexión a la base de datos
        
        # Redirigir a la página de libros después de guardar
        return redirect('/profesor/refuerzo/libros/')
    
    # Renderizar la plantilla del formulario cuando se accede con GET
    return render_template('p-agregar-libro.html')

@app.route('/profesor/agregar/video/')
def p_agregar():
    return render_template('./profesor/p-agregar-video.html')

@app.route('/profesor/agregar/video', methods=['GET', 'POST'])
def p_agregar_video():
    if request.method == 'POST':
        _titulo = request.form['titulo-video']
        _materia = request.form['materia-video']
        _insertar = request.form['insertar-video']
        
        sql = 'INSERT INTO videos (titulo, id_seccion_curso, id_asignatura, video) VALUES (%s, 2, %s, %s)'
        datos = (_titulo, _materia, _insertar)
        
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='jes'
        )
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, datos)
        connection.commit()
        cursor.close()
        
        return redirect(url_for('p_refuerzo_videos'))
    return render_template('./profesor/p-agregar-video.html')
    

@app.route('/profesor/materiales/')
def p_material_estudio():
    return render_template('/profesor/p-material_estudio.html')

@app.route('/profesor/agregar/material/')
def p_agregar_material():
    return render_template('./profesor/p-agregar-material.html')

@app.route('/profesor/agregar/material', methods=['GET', 'POST'])
def agregar_material():
    if request.method == 'POST':
        fondo_material = request.files['fondo-material']
        nombre_material = request.form['nombre-material']
        recurso_de_estudio = request.files['recurso-de-estudio']
        descripcion_material = request.form['descripcion-material']

        tiempo = datetime.now()
        horaActual = tiempo.strftime('%Y%H%M%S')
        nombreArchivo = horaActual + "_" + secure_filename(recurso_de_estudio.filename)
        recurso_de_estudio.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreArchivo))
        
        sql = "INSERT INTO material_estudio (id_curso, id_asignatura, titulo, fondo, material, descripcion) VALUES (2, %s, %s, %s, %s, %s)"
        datos = (nombre_material, secure_filename(fondo_material.filename), nombreArchivo, descripcion_material)
        
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='jes'
        )
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, datos)
        connection.commit()
        cursor.close()

        return redirect(url_for('p_material_estudio'))
    return render_template('./profesor/p-agregar-material.html')

@app.route('/profesor/recurso/estudio/')
def p_recurso_estudio():
    return render_template('./profesor/p-recurso_estudio.html')

@app.route('/profesor/material/subido/')
def p_material_de_curso_subido():
    return render_template('./profesor/p-material-de-curso-subido.html')

@app.route('/profesor/clases/enviadas/')
def p_clases_enviadas():
    return render_template('./profesor/p-clases-enviada.html')

@app.route('/profesor/tarea/estudiante/')
def p_tarea_e():
    return render_template('./profesor/p-tarea-e.html')

@app.route('/profesor/reporte/')
def p_report_a():
    return render_template('./profesor/p-report-a.html')

@app.route('/profesor/reporte', methods=['POST'])
def reporte():
    archivo_asistencia_nombre = request.files['archivo-asistencia']
    archivo_calificacion_nombre = request.files['archivo-calificacion']
    descripcion_material = request.form['descripcion-material']

    tiempo = datetime.now()
    horaActual = tiempo.strftime('%Y%H%M%S')
    nombreArchivoAsistencia = horaActual + "_" + secure_filename(archivo_asistencia_nombre.filename)
    nombreArchivoCalificacion = horaActual + "_" + secure_filename(archivo_calificacion_nombre.filename)
    
    archivo_asistencia_nombre.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreArchivoAsistencia))
    archivo_calificacion_nombre.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreArchivoCalificacion))
    
    sql = "INSERT INTO materiales (asistencia, calificacion, descripcion) VALUES (%s, %s, %s)"
    datos = (nombreArchivoAsistencia, nombreArchivoCalificacion, descripcion_material)
    
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql, datos)
    connection.commit()
    cursor.close()

    return redirect(url_for('p_report_a'))
@app.route('/profesor/perfil/estudiante/')
def p_perfil_e():
    return render_template('./profesor/p-perfil-e.html')

@app.route('/agregar/calificacion', methods=['POST'])
def agregar_calificacion():
    id_estudiante = request.form['id_estudiante']
    id_asignatura = request.form['id_asignatura']
    C1 = request.form['C1']
    C2 = request.form['C2']
    C3 = request.form['C3']
    C4 = request.form['C4']
    calificacion_final = request.form['calificacion_final']

    sql = 'INSERT INTO calificaciones (id_estudiante, id_asignatura, C1, C2, C3, C4, `C. Final`) VALUES (%s, %s, %s, %s, %s, %s, %s)'

    datos = (id_estudiante, id_asignatura, C1, C2, C3, C4, calificacion_final)

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql,datos)

    connection.commit()
    cursor.close()

    return redirect(url_for('listar_calificaciones'))



if __name__ == '__main__':
    app.run(port = 3000, debug=True)