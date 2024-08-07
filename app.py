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

    return render_template('estudiante/e-home.html', calificaciones=calificaciones, horarios=horarios, asistencias=asistencias, estudiante=estudiante)



@app.route('/estudiante/perfil/')
def e_perfil():
    if 'user_id' not in session or session.get('role') != 'estudiante':
        return redirect('/')
    
    estudiante_id = session['user_id']
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
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
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
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

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

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

@app.route('/admin/curso/', methods = ['GET'])
def mostrar_estudiantes():
    conexion = mysql.connection
    cursor = conexion.cursor()
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

    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    
    conexion.commit()
    cursor.close()
    return redirect('./a-materias.html')

@app.route('/admin/eliminar_materia/<int:id_asignatura>', methods = ['POST'])
def eliminar_materia(id_asignatura):
    conexion = mysql.connection
    cursor = conexion.cursor()

    cursor.execute('DELETE FROM asignaturas WHERE id_asignatura = %s', (id_asignatura))

    return redirect('./a-materias.html')

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
    return render_template('./admin/a-asistencia-reporte.html')

@app.route('/admin/registro/estudiante/')
def a_formulario_registro_e():
    return render_template('./admin/a-formulario-registro-e.html')

@app.route('/agregar_estudiantes', methods = ['POST'])
def agregar_estudiante():
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
    
    if imagen_perfil:
        estudiante_perfil = imagen_perfil.read()

    sql = 'INSERT INTO `estudiantes` (`id_estudiante`,`id_curso`, `matricula`, `nombre`, `apellidos`, `direccion`, `fecha_nacimiento`, `genero`, `email`, `telefono`, `imagen_perfil`, `contraseña`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    datos = (curso, matricula, nombre, apellidos, direccion, fecha_nacimiento, genero, correo, telefono, estudiante_perfil, contraseña)

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

    # Aqui indicamos lo que se cambiará y de donde lo hará
    sql =  '''UPDATE estudiantes SET nombre = %s, apellidos = %s, fecha_nacimiento = %s, genero = %s, curso = %s, correo = %s, telefono = %s, direccion = %s, matricula = %s, contraseña = %s WHERE id_estudiante = %s'''
    
    datos = (nombre, apellidos, fecha_nacimiento, genero, curso, correo, telefono, direccion, matricula, contraseña)

    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql, datos)

    conexion.commit()
    cursor.close()

    return redirect('./admin/a-curso.html')

@app.route('/admin/eliminar_estudiantes', methods = ['POST'])
def eliminar_estudiantes():
    id_estudiante = request.form["id_estudiante"]

    # Se hace una confirmación de si el id introducido existe
    if id_estudiante in 'estudiantes':
        sql = 'DELETE FROM estudiantes WHERE id_estudiante = %s'
        return redirect('./admin/a-curso.html')
    
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql, (id_estudiante))

    conexion.commit()
    cursor.close()

@app.route('/admin/registro/profesor/')
def a_formulario_registro_p():
    return render_template('./admin/a-formulario-registro-p.html')

@app.route('/admin/agregar_profesores', methods = ['POST'])
def agregar_profesores():
    # Insertar profesores
    asignatura = request.form["id_asignatura"]
    matricula = request.form["matricula"]
    nombre = request.form["nombre"]
    apellidos = request.form["apellido"]
    direccion = request.form["direccion"]
    cedula = request.form["cedula"]
    genero = request.form["genero"]
    correo = request.form["email"]
    telefono = request.form["telefono"]
    imagen_perfil = request.files["imagen_perfil"]
    contraseña = request.form["contraseña"]
    
    if imagen_perfil:
        profesor_perfil = imagen_perfil.read()

    sql = 'INSERT INTO `profesores` (`id_profesor`,`id_asignatura`, `matricula`, `nombre`, `apellido`, `direccion`, `cedula`, `genero`, `email`, `telefono`, `imagen_perfil`, `contraseña`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    datos = (asignatura, matricula, nombre, apellidos, direccion, cedula, genero, correo, telefono, profesor_perfil, contraseña)

    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    
    conexion.commit()
    cursor.close()

    # return redirect('./admin/a-curso.html')

@app.route('/admin/actualizar_profesor', methods = ['POST'])
def actualizar_profesores():
    # Actualizar estudiantes
    id = request.form["id_profesor"]
    asignatura = request.form["id_asignatura"]
    nombre = request.form["nombre"]
    apellidos = request.form["apellidos"]
    direccion = request.form["fecha_nacimiento"]
    cedula = request.form["genero"]
    genero = request.form["genero"]
    correo = request.form["email"]
    telefono = request.form["telefono"]
    matricula = request.form["matricula"]
    imagen_perfil = request.files["imagen_perfil"]
    contraseña = request.form["contraseña"]

    # Aqui indicamos lo que se cambiará y de donde lo hará
    sql =  '''UPDATE profesores SET asignatura = %s, nombre = %s, apellidos = %s, direccion = %s, cedula = %s, genero = %s, correo = %s, telefono = %s, matricula = %s,imagen_perfil = %s, contraseña = %s WHERE id_profesor = %s'''
    
    datos = (asignatura, nombre, apellidos, direccion, cedula, genero, correo, telefono, matricula,imagen_perfil, contraseña)

    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql, datos)

    conexion.commit()
    cursor.close()

@app.route('/admin/eliminar_profesores', methods = ['POST'])
def eliminar_profesores():
    id_profesor = request.form["id_profesor"]

    # Se hace una confirmación de si el id introducido existe
    if id_profesor in 'profesores':
        sql = 'DELETE FROM profesores WHERE id_profesor = %s'
        # return redirect('./admin/a-curso.html')
    
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql, (id_profesor))

    conexion.commit()
    cursor.close()

@app.route('/admin/profesores/')
def a_cursos_profesor():
    return render_template('./admin/a-profesor-1_a.html')

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

    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql,datos)

    conexion.commit()
    cursor.close()

    return redirect(url_for('listar_calificaciones'))

@app.route('/editar/calificacion/<int:id>', methods=['POST'])
def editar_calificacion(id):
    C1 = request.form['C1']
    C2 = request.form['C2']
    C3 = request.form['C3']
    C4 = request.form['C4']
    calificacion_final = request.form['calificacion_final']

    sql = 'UPDATE calificaciones SET C1 = %s, C2 = %s, C3 = %s, C4 = %s, `C. Final` = %s WHERE id_calificacion = %s'
    datos = (C1, C2, C3, C4, calificacion_final, id)
    
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql,datos)

    conexion.commit()
    cursor.close()

    return redirect(url_for('listar_calificaciones'))

# @app.route('/listar/calificaciones')
# def listar_calificaciones():
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute('SELECT * FROM calificaciones')
#     calificaciones = cursor.fetchall()
#     cursor.close()

#     return render_template('list_calificaciones.html', calificaciones=calificaciones)


# @app.route('/eliminar/calificacion/<int:id>', methods=['POST'])
# def eliminar_calificacion(id):
#     cursor = mysql.connection.cursor()
#     cursor.execute('DELETE FROM calificaciones WHERE id_calificacion = %s', (id,))
#     mysql.connection.commit()
#     cursor.close()

#     return redirect(url_for('listar_calificaciones'))

if __name__ == '__main__':
    app.run(port = 3000, debug=True)