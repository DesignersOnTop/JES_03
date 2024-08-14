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
UPLOAD_FOLDER = os.path.join('static', 'documentos')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear la carpeta si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def Index():
    session.clear()
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    matricula = request.form['matricula-sesion']
    password = request.form['pass-sesion']
    
    # Conectar a la base de datos
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
        cursor.close()
        connection.close()
        return redirect('/home/estudiante/')

    # Verificación de profesores
    cursor.execute("SELECT * FROM profesores WHERE matricula = %s", (matricula,))
    profesor = cursor.fetchone()
    if profesor and profesor['contraseña'] == password:
        session['user_id'] = profesor['id_profesor']
        session['role'] = 'profesor'
        cursor.close()
        connection.close()
        return redirect('/home/profesor/')

    # Verificación de administradores
    cursor.execute("SELECT * FROM admin WHERE matricula = %s", (matricula,))
    admin = cursor.fetchone()
    if admin and admin['contraseña'] == password:
        session['user_id'] = admin['id_admin']
        session['role'] = 'admin'
        cursor.close()
        connection.close()
        return redirect('/home/admin/')
    
    # Cerrar conexión
    cursor.close()
    connection.close()

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
            INSERT INTO tareas_estudiantes (id_estudiante, id_curso, tarea)
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

if __name__ == '__main__':
    app.run(debug=True)