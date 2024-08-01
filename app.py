import os
from flask import Flask, render_template, request, redirect, session, send_from_directory, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime
# Importar el enlace a base de datos MySQL
# from flaskext.mysql import MySQL

# Crear la aplicación
app = Flask(__name__)

# Crear una llave secreta
app.secret_key = 'JES'

# Configurar la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'jes'

# Inicializar MySQL
mysql = MySQL(app)
#-----------------------------------------------------

@app.route('/')
def Index():
    return render_template('index.html')
    
@app.route('/login', methods=['POST'])
def login():
    matricula = request.form['matricula-sesion']
    password = request.form['pass-sesion']
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
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

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

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

    session.clear()

    return render_template('estudiante/e-home.html', calificaciones=calificaciones, horarios=horarios, asistencias=asistencias, estudiante=estudiante)



@app.route('/estudiante/perfil/')
def e_perfil():
    
    estudiante_id = session['user_id']
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM `estudiantes` WHERE id_estudiante = %s', (estudiante_id,))
    
    perfil = cursor.fetchall()
    cursor.close()
    
    return render_template('./estudiante/e-perfil.html', perfil =perfil[0])

@app.route('/estudiante/material/')
def e_material():
    return render_template('./estudiante/e-material_estudio.html')

@app.route('/estudiante/material/trabajo/')
def ver_materia():
    return render_template('./estudiante/e-ver_materias.html')

@app.route('/estudiante/refuerzo/libros/')
def e_refuerzo_libros():
    return render_template('./estudiante/e_refuerzo_libros.html')

@app.route('/estudiante/refuerzo/videos/')
def e_refuerzo_videos():
    return render_template('./estudiante/e_refuerzo_videos.html')

@app.route('/estudiante/video/')
def e_videos():
    return render_template('./estudiante/e-video-clase.html')

@app.route('/estudiante/libro/')
def e_libro():
    return render_template('./estudiante/e-libro-refuerzo.html')

# APARTADO DEL ADMIN EN PYTHON

@app.route('/home/admin/')
def a_home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
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
    return render_template('./admin/a-cursos.html')

@app.route('/admin/curso/')
def a_curso():
    return render_template('./admin/a-curso.html')

@app.route('/admin/materias/')
def a_materias():
    return render_template('./admin/a-materias.html')

@app.route('/admin/reportes/')
def a_reportes():
    return render_template('./admin/a-reporte-curso.html')

@app.route('/admin/reportes-profesor/')
def a_reporte_profesor():
    return render_template('./admin/a-reporte-profesor.html')

@app.route('/admin/perfil/')
def a_perfil():
    return render_template('./admin/a-perfil.html')

@app.route('/admin/reportes-calificacion/')
def a_reporte_calificaciones():
    return render_template('./admin/a-calificaciones-reporte.html')

@app.route('/admin/reportes-asistencias/')
def a_reportes_asistencia():
    return render_template('./admin/a-asistencias-reporte.html')

@app.route('/admin/registro/estudiante/')
def a_formulario_registro_e():
    return render_template('./admin/a-formulario-registro-e.html')

@app.route('/guardar_estudiantes', methods = ['POST'])
def guardar_estudiante():
    # Insertar estudiantes
    curso = request.form["curso"]
    matricula = request.form["matricula"]
    nombre = request.form["nombre"]
    apellidos = request.form["apellidos"]
    direccion = request.form["direccion"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    genero = request.form["genero"]
    correo = request.form["email"]
    telefono = request.form["telefono"]
    imagen_perfil = request.files["imagen_perfil"]
    contraseña = request.form["contraseña"]

    sql = 'INSERT INTO `estudiantes` (`id_estudiante`,`id_curso`, `matricula`, `nombre`, `apellidos`, `direccion`, `fecha_nacimiento`, `genero`, `email`, `telefono`, `imagen_perfil`, `contraseña`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    datos = (curso, matricula, nombre, apellidos, direccion, fecha_nacimiento, genero, correo, telefono, imagen_perfil, contraseña)

    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    
    conexion.commit()
    cursor.close()

    return redirect('./admin/a-curso.html')

@app.route('/actualizar_estudiantes', methods = ['POST'])
def actualizar_estudiantes():
    # Actualizar estudiantes
    id = request.form["id_estudiante"]
    nombre = request.form["nombre"]
    apellidos = request.form["apellidos"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    genero = request.form["genero"]
    curso = request.form["curso"]
    correo = request.form["email"]
    telefono = request.form["telefono"]
    direccion = request.form["direccion"]
    matricula = request.form["matricula"]
    contraseña = request.form["contraseña"]
    return redirect('./admin/a-curso.html')

@app.route('/admin/registro/profesor/')
def a_formulario_registro_p():
    return render_template('./admin/a-formulario-registro-p.html')

@app.route('/admin/profesores/')
def a_cursos_profesor():
    return render_template('./admin/a-profesor-1_a.html')

@app.route('/admin/horario/')
def a_horario_profesor():
    return render_template('./admin/a-horario-1a.html')

# =========================================================

# APARTADO DEL PROFESORES EN PYTHON
@app.route('/home/profesor/')
def p_home():
    return render_template('./profesor/p-home-a.html')

@app.route('/profesor/perfil/')
def p_perfil():
    return render_template('./profesor/p-perfil.html')

@app.route('/profesor/refuerzo/libros/')
def p_refuerzo_libros():
    return render_template('./profesor/p-refuerzo-libros.html')

@app.route('/profesor/refuerzo/libros/nombre_libro')
def p_libro_refuerzo():
    return render_template('./profesor/p-libro-refuerzo.html')

@app.route('/profesor/refuerzo/videos/')
def p_refuerzo_videos():
    return render_template('./profesor/p-refuerzo-videos.html')

@app.route('/profesor/agregar/libros/')
def agregar_libro():
    return render_template('/profesor/p-agregar-libro.html')

@app.route('/agregar/libro/', methods=['GET','POST'])
def p_agregar_libro():
    _portada = request.files['portada_libro'].filename
    _titulo = request.form['titulo-libro']
    _materia = request.form['materia-libro']
    _subir = request.files['subir-libro'].filename
    
    tiempo = datetime.now()
    horaActual = tiempo.strftime('%Y%H%M%S')
    
    # if _subir.filename!= " ":
    #     nuevoNombre = horaActual+ "_" + _subir.filename
    #     _subir.save('static/img/'+nuevoNombre)
        
    sql = 'INSERT INTO `libros` (`id`,`portada`, `titulo`, `id_asignatura`, `libro`, `id_curso_seccion`) VALUES (NULL, %s, %s, %s, %s, 2)'
    
    datos = (_portada, _titulo, _materia, _subir)
    
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    
    conexion.commit()
    cursor.close()
    
    return redirect('/profesor/refuerzo/libros/')

@app.route('/profesor/agregar/video/')
def p_agregar():
    return render_template('./profesor/p-agregar-video.html')

@app.route('/agregar/video/profesor/', methods=['POST'])
def p_agregar_video():
    _titulo = request.form['titulo-video']
    _materia = request.form['materia-video']
    _insertar = request.form['insertar-video']
    
    sql = 'INSERT INTO `videos` (`id`, `titulo`, `id_seccion_curso`, `id_asignatura`, `video`) VALUES (NULL, %s, %s, %s, 2)'
    
    datos = (_titulo, _materia, _insertar)
    
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    
    conexion.commit()
    cursor.close()
    
    return redirect('/profesor/refuerzo/videos/')
    

@app.route('/profesor/materiales/')
def p_material_estudio():
    return render_template('/profesor/p-material_estudio.html')

@app.route('/profesor/agregar/material/')
def p_agregar_material():
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

@app.route('/profesor/perfil/estudiante/')
def p_perfil_e():
    return render_template('./profesor/p-perfil-e.html')

if __name__ == '__main__':
    app.run(port = 3000, debug=True)