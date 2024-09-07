import os
import pymysql
from flask import Flask, render_template, request, redirect, session, send_from_directory, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import datetime
# Crear la aplicación
app = Flask(__name__)

# Crear una llave secreta
app.secret_key = 'JES'

# Configurar la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'jes'
#-----------------------------------------------------

app.config['UPLOAD_FOLDER'] = 'static/documentos'

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def Index():
    return render_template('index.html', error=False)
    
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
    
    return render_template('index.html', error=True)
# # =========================================================

# HOME ESTUDIANTE
@app.route('/home/estudiante/', methods=['GET'])
def home_estudiante():
        # Verificamos si el usuario ha iniciado sesión y su rol.
    if 'user_id' not in session or session.get('role') != 'estudiante':
        # Si no ha iniciado sesión o no es un estudiante, lo redirigimos a la página principal.
        return redirect('/')

        # Si el usuario es un estudiante, obtenemos su ID desde la sesión.
    estudiante_id = session['user_id']

        # Nos conectamos a la base de datos MySQL.
    connection = pymysql.connect(
        host='localhost',  # Dirección del servidor MySQL.
        user='root',       # Nombre de usuario.
        password='',      
        database='jes'   
    )
    
        # Creamos un cursor que nos permitirá ejecutar las consultas.
        # Usamos DictCursor para que los resultados se devuelvan como diccionarios.
    cursor = connection.cursor(pymysql.cursors.DictCursor)

        # Obtener la imagen de perfil del estudiante utilizando su ID almacenado en la sesión.
    cursor.execute("SELECT imagen_perfil FROM estudiantes WHERE id_estudiante = %s", (estudiante_id,))
    perfil = cursor.fetchone()
    imagen_perfil = perfil.get('imagen_perfil') if perfil else None

    # calificacion estudiante
    cursor.execute("""
        SELECT 
            calificaciones.id_estudiante,
            calificaciones.C1,
            calificaciones.C2,
            calificaciones.C3,
            calificaciones.C4,
            calificaciones.c_final,
            asignaturas.nom_asignatura
        FROM 
            calificaciones
        JOIN 
            asignaturas ON calificaciones.id_asignatura = asignaturas.id_asignatura
        WHERE 
            calificaciones.id_estudiante = %s

    """, (estudiante_id,)) # parametro para ejecutar la consulta.
    calificaciones = cursor.fetchall()
    
        # Seleccionamos el ID del estudiante y las calificaciones. Unimos la tabla calificaciones con la tabla asignaturas para obtener informacion relacionada con asignaturas y sacamos los resultados solo del estudiante que coincida con el ID. 
    
    
    #  Obtener las asistencias del estudiante.
    cursor.execute("SELECT Sect_Oct, Nov_Dic, Ene_Feb, Marz_Abril, May_Jun, Total_de_asistencias FROM asistencias WHERE id_estudiante = %s", (estudiante_id,))

        # Esta consulta recupera las asistencias del estudiante para diferentes períodos y los registros obtenidos se almacenan en la variable "Asistencia".
    asistencias = cursor.fetchall()

    total_asistencias = 0
    total_periodos = 0
    
    for asistencia in asistencias:
        # Convertir los campos a enteros, tratando valores nulos como 0
        sect_oct = int(asistencia['Sect_Oct'] or 0)
        nov_dic = int(asistencia['Nov_Dic'] or 0)
        ene_feb = int(asistencia['Ene_Feb'] or 0)
        marz_abril = int(asistencia['Marz_Abril'] or 0)
        may_jun = int(asistencia['May_Jun'] or 0)
        total_asistencias_periodo = int(asistencia['Total_de_asistencias'] or 0)

        # Sumar las asistencias de todos los períodos
        total_asistencias += sect_oct + nov_dic + ene_feb + marz_abril + may_jun
        
        # Sumar el total de asistencias posibles (para calcular el porcentaje)
        total_periodos += 5 * total_asistencias_periodo
    
    # Calcular el porcentaje de asistencia
    porcentaje_asistencia = (total_asistencias / total_periodos * 100) if total_periodos > 0 else 0
    
    # Asegurarse de que el porcentaje esté en el rango de 0 a 100
    porcentaje_asistencia = min(max(porcentaje_asistencia, 0), 100)

    
    # horario estudiante ( Se unen varias tablas para obtener la H , D y el nombre de la asignatura )
    sql = ("SELECT h.hora, d.dia, a.nom_asignatura  FROM horario AS hor JOIN hora AS h ON hor.id_hora = h.id_hora JOIN dias AS d ON hor.id_dias = d.id_dias JOIN asignaturas AS a ON hor.id_asignatura = a.id_asignatura JOIN estudiantes AS e ON hor.id_curso = e.id_curso WHERE e.id_estudiante = %s ORDER BY h.id_hora, d.id_dias")
    
        # En la consulta estamos buscando la hora en la que se imparte las clase, Día de la semana y el nombre de la asignatura. Se toma la informacion de la tabla horario y se usan los JOIN para unir las tablas y obtener la informacion, con el id correspondiente al estudiante y se ordena por h y d.
        
    cursor.execute(sql,estudiante_id)
        # Ejecutamos la consulta usando el id del estudiante.
    
    horarios = cursor.fetchall()
        # Obtenemos todos los registros devueltos por la consulta y los almacenamos.

        # Creamos un diccionario para organizar el horario. 
    horario_por_hora = {}

        # cada registro de horario obtenido, extraemos la hora, dia y nombre de la asignatura actual 
    for horario in horarios:
        hora = horario['hora']
        dia = horario['dia']
        asignatura = horario['nom_asignatura']
        
         # Si la hora no está en el diccionario, iniciamos un diccionario vacío para cada día de la semana.
        if hora not in horario_por_hora:
            horario_por_hora[hora] = {"Lunes": "", "Martes": "", "Miercoles": "", "Jueves": "", "Viernes": ""}
        
               # Asignamos la asignatura al día correspondiente en el horario.
        horario_por_hora[hora][dia] = asignatura

    cursor.close()

    return render_template('estudiante/index.html', calificaciones=calificaciones, horario_por_hora=horario_por_hora, porcentaje=porcentaje_asistencia, perfil=imagen_perfil)

# Perfil 
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
    
        # Obtener informacion del perfil y recuperamos los resultados.
    cursor.execute('SELECT * FROM `estudiantes` WHERE id_estudiante = %s', (estudiante_id,))
    perfil = cursor.fetchall()
    
        # Consulta para obtener el nombre del curso y recupamos el nombre.
    cursor.execute('''
    SELECT cursos.nombre
    FROM estudiantes
    JOIN cursos ON estudiantes.id_curso = cursos.id_curso
    WHERE estudiantes.id_estudiante = %s''', (estudiante_id,))
    curso = cursor.fetchone()
    
    cursor.close()
    
    return render_template('./estudiante/e-perfil.html', perfil=perfil[0], curso=curso)

# Material del estudiante
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
    SELECT DISTINCT asignaturas.id_asignatura, asignaturas.nom_asignatura
    FROM asignaturas
    JOIN material_estudio ON asignaturas.id_asignatura = material_estudio.id_asignatura
    JOIN estudiantes ON estudiantes.id_curso = material_estudio.id_curso
    WHERE estudiantes.id_estudiante = %s''', (estudiante_id,))
    asignaturas = cursor.fetchall()
        # Solo se ejecutara si el id estudiante es valido y recuperamos todas las asignaturas disponibles.

    # Lista materiales vacía
    materiales = []

        # Si el método de la solicitud es POST, significa que el usuario ha enviado un formulario.
    if request.method == 'POST':
        materia_seleccionada = request.form.get('materias-agg')
        # Obtenemos la asignatura seleccionada del formulario.
        
        if materia_seleccionada:
            # Buscar materiales para la asignatura seleccionada
            cursor.execute('''
                SELECT material_estudio.*, asignaturas.nom_asignatura
                FROM material_estudio
                JOIN estudiantes ON material_estudio.id_curso = estudiantes.id_curso
                JOIN asignaturas ON material_estudio.id_asignatura = asignaturas.id_asignatura
                WHERE material_estudio.id_asignatura = %s AND estudiantes.id_estudiante = %s''', (materia_seleccionada, estudiante_id))
            materiales = cursor.fetchall()
        else:
            # Obtener todos los materiales si no se selecciona una asignatura específica
            cursor.execute('''
                SELECT material_estudio.*, asignaturas.nom_asignatura
                FROM material_estudio
                JOIN estudiantes ON material_estudio.id_curso = estudiantes.id_curso
                JOIN asignaturas ON material_estudio.id_asignatura = asignaturas.id_asignatura
                WHERE estudiantes.id_estudiante = %s''', (estudiante_id,))
            materiales = cursor.fetchall()
    else:
        # Obtener todos los materiales si no se realizó una búsqueda
        cursor.execute('''
            SELECT material_estudio.*, asignaturas.nom_asignatura
            FROM material_estudio
            JOIN estudiantes ON material_estudio.id_curso = estudiantes.id_curso
            JOIN asignaturas ON material_estudio.id_asignatura = asignaturas.id_asignatura
            WHERE estudiantes.id_estudiante = %s''', (estudiante_id,))
        materiales = cursor.fetchall()

        # Cerramos el cursor para renderizar la plantilla con las asignaturas y materiales obtenidos.
    cursor.close()
    
    return render_template('./estudiante/e-material_estudio.html', asignaturas=asignaturas, materiales=materiales)

# Ver materiales del estudiante.
@app.route('/ver_materia/<titulo>/')
def ver_materia(titulo):
    if 'user_id' not in session or session.get('role') != 'estudiante':
        return redirect('/')

    estudiante_id = session['user_id']

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
        # Parametros obtenidos desde la url 
    curso = request.args.get('curso')
    asignatura = request.args.get('asignatura') 
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Obtener detalles del material basados por el título.
    cursor.execute('''
        SELECT material_estudio.*, asignaturas.nom_asignatura
        FROM material_estudio
        JOIN asignaturas ON material_estudio.id_asignatura = asignaturas.id_asignatura
        WHERE material_estudio.titulo = %s
    ''', (titulo,))
    material = cursor.fetchone()

    cursor.execute('''
        SELECT 
            profesores.nombre AS pnom, 
            profesores.apellido AS pape, 
            profesores.imagen_perfil 
        FROM 
            profesor_asignado 
        JOIN 
            profesores ON profesores.id_profesor = profesor_asignado.id_profesor 
        JOIN 
            estudiantes ON estudiantes.id_curso = profesor_asignado.id_curso 
        WHERE 
            estudiantes.id_curso = %s 
        AND 
            profesores.id_asignatura = %s
    ''', (curso, asignatura))

    prof = cursor.fetchone()

        # Obtiene el nombre, apellido y foto del profesor asignado, la información del profesor se une con las tablas profesor_asignado y estudiantes utilizando JOIN para obtener según el curso y la asignatura del  estudiante. Todo la informacion del profesor se almacenara en la variable prof. 
        
    cursor.close()
        # Cierre del cursor, Renderiza a la plantilla html pasando los detalles del material y el profesor.
    return render_template('estudiante/e-ver_materias.html', material=material, prof=prof)

# Enviar tareas. 
@app.route('/estudiante/enviar/tarea/', methods=['POST'])
def enviar_tarea():
    if 'user_id' not in session or session.get('role') != 'estudiante':
        return redirect('/')

    estudiante_id = session['user_id']
        #Se obtienen material y curso desde el formulario enviado por el usuario.
    material_id = request.form.get('material_id')
    curso = request.form.get('curso')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)

        # Se verifica si el archivo fue subido correctamente. Si no se encuentra el archivo en request.files, se cierra el cursor de la base de datos y se muestra un mensaje de error.
    if 'subir-tarea' not in request.files:
        cursor.close()
        flash('No se ha subido ningún archivo')
        return redirect('/estudiante/material/')

        # Si el archivo subido no tiene nombre (tarea.filename), se cierra el cursor y se muestra un mensaje indicando que no se seleccionó ningún archivo.
    tarea = request.files['subir-tarea']
    if tarea.filename == '':
        cursor.close()
        flash('No se seleccionó ningún archivo')
        return redirect('/estudiante/material/')

        # Si se ha subido un archivo,
    if tarea:
            # Asegurar que el nombre del archivo sea seguro.
        archivo_nombre = secure_filename(tarea.filename)
        
            # Construir la ruta completa donde se guardará el archivo en el servidor
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], archivo_nombre)
        
            # Guardar el archivo en la ubicación especificada
        tarea.save(file_path)

        cursor.execute('''
            INSERT INTO tareas_estudiante (id_material, id_estudiante, id_curso, tarea)
            VALUES (%s, %s, %s, %s)
        ''', (material_id, estudiante_id, curso, archivo_nombre))

        # Confirmar para guardar los cambios
        connection.commit()
        
        # Cerrar 
        cursor.close()
        flash('Tarea enviada exitosamente')
        return redirect('/estudiante/material/')

    cursor.close()
    flash('Error al subir el archivo')
    return redirect('/estudiante/material/')

# Rezuerzo libros.
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
    
        # Obtener los libros para el refuerzo.
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

    # Obtener los detalles del libro según el título
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

        # Obtener los videos de refuerzo asociados con el curso del estudiante
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

         # Obtener los detalles del video por su título
    cursor.execute('''
        SELECT videos.*, asignaturas.nom_asignatura
        FROM videos
        JOIN asignaturas ON videos.id_asignatura = asignaturas.id_asignatura
        WHERE videos.titulo = %s
    ''', (titulo,))
    
    video = cursor.fetchone()
    cursor.close()
    
    return render_template('./estudiante/e-video-clase.html', video = video)


# APARTADO DEL PROFESORES
@app.route('/home/profesor/', methods=['GET', 'POST'])
def p_home():
    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')

    id_profesor = session['user_id']
    
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Obtener el id_asignatura para el profesor
    cursor.execute('''
        SELECT asignaturas.id_asignatura
        FROM profesores
        JOIN asignaturas ON asignaturas.id_asignatura = profesores.id_asignatura
        WHERE profesores.id_profesor = %s
    ''', (id_profesor,))

    asignatura = cursor.fetchone()
    id_asignatura = asignatura['id_asignatura']

    cursor.execute("""
        SELECT DISTINCT c.id_curso, c.nombre
        FROM cursos c
        JOIN profesor_asignado pa ON c.id_curso = pa.id_curso
        WHERE pa.id_profesor = %s
    """, (id_profesor,))
    cursos = cursor.fetchall()
    
    if request.method == 'POST':
        curso_seleccionado = request.form.get('curso_seleccionado')
        session['curso_seleccionado'] = curso_seleccionado
    else:
        curso_seleccionado = session.get('curso_seleccionado')
        if not curso_seleccionado and cursos:
            curso_seleccionado = cursos[0]['id_curso'] if isinstance(cursos[0], dict) else cursos[0][0]
            session['curso_seleccionado'] = curso_seleccionado
    
    cursor.execute("""
        SELECT estudiantes.id_estudiante, estudiantes.nombre, estudiantes.apellidos, estudiantes.matricula
        FROM estudiantes
        WHERE estudiantes.id_curso = %s
    """, (curso_seleccionado,))
    estudiantes = cursor.fetchall()

    cursor.execute("""
        SELECT a.id_estudiante, a.Sect_Oct, a.Nov_Dic, a.Ene_Feb, a.Marz_Abril, a.May_Jun, a.Total_de_asistencias
        FROM asistencias AS a
        WHERE a.id_curso = %s AND a.id_asignatura = %s
    """, (curso_seleccionado, id_asignatura))
    asistencia = cursor.fetchall()

    asistencias = {a['id_estudiante']: a for a in asistencia}

    calificaciones = {}
    for estudiante in estudiantes:
        cursor.execute("""
            SELECT c1, c2, c3, c4, c_final
            FROM calificaciones
            WHERE id_estudiante = %s AND id_curso = %s AND id_asignatura = %s
        """, (estudiante['id_estudiante'], curso_seleccionado, id_asignatura))
        result = cursor.fetchone()
        if result:
            calificaciones[estudiante['id_estudiante']] = result
        else:
            calificaciones[estudiante['id_estudiante']] = {'c1': '', 'c2': '', 'c3': '', 'c4': '', 'c_final': ''}
        
    # Obtener el perfil del profesor
    cursor.execute('SELECT imagen_perfil, nombre, apellido FROM profesores WHERE id_profesor = %s', (id_profesor,))  
    perfil = cursor.fetchone()
    
    cursor.close()
    connection.close()

    return render_template('./profesor/index.html', estudiantes=estudiantes, asistencias=asistencias, calificaciones=calificaciones, perfil=perfil, curso_seleccionado=curso_seleccionado, cursos=cursos)



@app.route('/profesor/perfil/')
def p_perfil():
    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')
    
    id_profesor = session['user_id']
    
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('''
        SELECT profesores.*, asignaturas.nom_asignatura
        FROM profesores
        JOIN asignaturas ON asignaturas.id_asignatura = profesores.id_asignatura
        WHERE profesores.id_profesor = %s
    ''', (id_profesor,))
    perfil = cursor.fetchall()
    
    cursor.close()
    return render_template('./profesor/p-perfil.html', perfil=perfil[0])

@app.route('/home/profesor/asistencia/', methods=['POST'])
def p_asistencia():
    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')

    id_profesor = session['user_id']
    id_estudiante = request.form.get('id_estudiante')
    curso_seleccionado = session['curso_seleccionado']

    sect_oct = request.form.get("sect_oct")
    nov_dic = request.form.get("nov_dic")
    ene_feb = request.form.get("ene_feb")
    marz_abril = request.form.get("marz_abril")
    may_jun = request.form.get("may_jun")
    total_asistencias = request.form.get("total_asistencias")

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute('''
        SELECT asignaturas.id_asignatura
        FROM profesores
        JOIN asignaturas ON asignaturas.id_asignatura = profesores.id_asignatura
        WHERE profesores.id_profesor = %s
    ''', (id_profesor,))

    asignatura = cursor.fetchone()

    id_asignatura = asignatura['id_asignatura']

    # esto se va usar para ver si el estudiante ya esta en la tabla para asi decidir si es un insert o un update
    sql = """
    SELECT COUNT(*) AS count FROM asistencias
    WHERE id_estudiante = %s AND id_curso = %s AND id_asignatura = %s
    """
    cursor.execute(sql, (id_estudiante, curso_seleccionado, id_asignatura))
    resultado = cursor.fetchone()

    if resultado['count'] > 0:
        # Si el estudiante habia tenido algun insertar previo entonces usara update
        update = """
        UPDATE asistencias
        SET Sect_Oct = %s, Nov_Dic = %s, Ene_Feb = %s, Marz_Abril = %s, May_Jun = %s, Total_de_asistencias WHERE id_estudiante = %s AND id_curso = %s AND id_asignatura = %s
        """

        datos = (sect_oct, nov_dic, ene_feb, marz_abril, may_jun, total_asistencias, id_estudiante, curso_seleccionado, id_asignatura)
        cursor.execute(update, datos)
    else:
        # Si el estudiante no habia tenido alguna inserccion entonces insertara
        insertar = """
        INSERT INTO asistencias (id_asistencia, id_estudiante, id_curso, id_asignatura, Sect_Oct, Nov_Dic, Ene_Feb, Marz_Abril, May_Jun, Total_de_asistencias)
        VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        datos = (id_estudiante, curso_seleccionado, id_asignatura, sect_oct, nov_dic, ene_feb, marz_abril, may_jun, total_asistencias)

        cursor.execute(insertar, datos)


    connection.commit()
    connection.close()

    return redirect('/home/profesor/')

@app.route('/home/profesor/calificaciones/', methods=['POST'])
def p_calificaciones():
    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')

    id_profesor = session['user_id']
    id_estudiante = request.form.get('id_estudiante')
    curso_seleccionado = session['curso_seleccionado']

    c1 = request.form.get("c1")
    c2 = request.form.get("c2")
    c3 = request.form.get("c3")
    c4 = request.form.get("c4")
    c_final = request.form.get("c_final")

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute('''
        SELECT asignaturas.id_asignatura
        FROM profesores
        JOIN asignaturas ON asignaturas.id_asignatura = profesores.id_asignatura
        WHERE profesores.id_profesor = %s
    ''', (id_profesor,))

    asignatura = cursor.fetchone()
    id_asignatura = asignatura['id_asignatura']

    # Verifica si el estudiante ya está en la tabla para decidir si es un insert o un update
    sql = """
    SELECT COUNT(*) AS count FROM calificaciones
    WHERE id_estudiante = %s AND id_curso = %s AND id_asignatura = %s
    """
    cursor.execute(sql, (id_estudiante, curso_seleccionado, id_asignatura))
    resultado = cursor.fetchone()

    if resultado['count'] > 0:
        # Actualiza los datos si el estudiante ya existe
        update = """
        UPDATE calificaciones
        SET C1 = %s, C2 = %s, C3 = %s, C4 = %s, c_final = %s
        WHERE id_estudiante = %s AND id_curso = %s AND id_asignatura = %s
        """
        datos = (c1, c2, c3, c4, c_final, id_estudiante, curso_seleccionado, id_asignatura)
        cursor.execute(update, datos)
    else:
        # Inserta los datos si el estudiante no existe
        insertar = """
        INSERT INTO calificaciones (id_calificacion, id_estudiante, id_curso, id_asignatura, C1, C2, C3, C4, c_final)
        VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        datos = (id_estudiante, curso_seleccionado, id_asignatura, c1, c2, c3, c4, c_final)
        cursor.execute(insertar, datos)

    connection.commit()
    connection.close()

    return redirect('/home/profesor/')


@app.route('/profesor/refuerzo/libros/', methods=['GET', 'POST'])
def p_refuerzo_libros():
    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')

    curso_seleccionado = session['curso_seleccionado']
    id_profesor = session['user_id']

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        id_libro_a_eliminar = request.form.get('id_libro')
        if id_libro_a_eliminar:
            cursor.execute('''
                SELECT subir_libro, portada
                FROM libros
                WHERE id_libro = %s AND id_curso = %s
            ''', (id_libro_a_eliminar, curso_seleccionado))
            libro = cursor.fetchone()
            
            if libro:
                libro_filename = libro['subir_libro']
                portada_filename = libro['portada']
                
                # Eliminar el archivo del sistema de archivos
                if libro_filename:
                    libro_path = os.path.join(app.config['UPLOAD_FOLDER'], libro_filename)
                    if os.path.exists(libro_path):
                        os.remove(libro_path)
                
                # Eliminar la portada del archivo
                if portada_filename:
                    portada_path = os.path.join(app.config['UPLOAD_FOLDER'], portada_filename)
                    if os.path.exists(portada_path):
                        os.remove(portada_path)

                # Eliminar el libro de la base de datos
                cursor.execute('''
                    DELETE FROM libros
                    WHERE id_libro = %s AND id_curso = %s
                ''', (id_libro_a_eliminar, curso_seleccionado))
                connection.commit()
                
            return redirect('/profesor/refuerzo/libros/')

    sql = """
        SELECT libros.*, asignaturas.nom_asignatura
        FROM libros
        JOIN asignaturas ON libros.id_asignatura = asignaturas.id_asignatura
        JOIN profesores ON profesores.id_asignatura = libros.id_asignatura
        WHERE libros.id_curso = %s AND profesores.id_profesor = %s
    """
    cursor.execute(sql, (curso_seleccionado, id_profesor))
    libros = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('./profesor/p-refuerzo-libros.html', libros=libros)


@app.route('/ver/libro/')
def ver_libro():
    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')

    id_libro = request.args.get('id_libro')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT libros.id_libro, libros.titulo, libros.subir_libro FROM libros WHERE id_libro = %s', (id_libro,))
    libro = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('./profesor/p-libro-refuerzo.html', libro=libro)


@app.route('/profesor/refuerzo/videos/', methods=['GET', 'POST'])
def p_refuerzo_videos():
    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')

    id_profesor = session['user_id']
    curso_seleccionado = session['curso_seleccionado']
    
    if not curso_seleccionado:
        return redirect('/home/profesor/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Obtener el id_asignatura del profesor
    cursor.execute('''
        SELECT asignaturas.id_asignatura
        FROM profesores
        JOIN asignaturas ON asignaturas.id_asignatura = profesores.id_asignatura
        WHERE profesores.id_profesor = %s
    ''', (id_profesor,))
    
    asignatura = cursor.fetchone()
    if not asignatura:
        cursor.close()
        connection.close()
        return redirect('/home/profesor/')

    id_asignatura = asignatura['id_asignatura']

    sql = '''
        SELECT 
            videos.id AS id_video,
            videos.titulo, 
            asignaturas.nom_asignatura
        FROM 
            videos 
        JOIN 
            asignaturas ON asignaturas.id_asignatura = videos.id_asignatura
        WHERE 
            videos.id_curso = %s AND asignaturas.id_asignatura = %s
    '''
    cursor.execute(sql, (curso_seleccionado, id_asignatura))

    videos = cursor.fetchall()

    if request.method == 'POST':
        id_video_a_eliminar = request.form.get('id_video')
        if id_video_a_eliminar:
            cursor.execute('''
                DELETE FROM videos
                WHERE id = %s AND id_asignatura = %s
            ''', (id_video_a_eliminar, id_asignatura))
            connection.commit()
            return redirect('/profesor/refuerzo/videos/')

    cursor.close()
    connection.close()

    return render_template('./profesor/p-refuerzo-videos.html', videos=videos)

@app.route('/profesor/video/')
def p_mostrar_videos():
    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')
    
    id_video = request.args.get('id_video')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM videos WHERE id = %s', (id_video,))
    video = cursor.fetchone()
    cursor.close()
    connection.close()
    
    return render_template('./profesor/p-ver-videos.html', video=video)

@app.route('/agregar/libros/')
def p_agg_libro():
    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')
    
    curso_seleccionado = session['curso_seleccionado']

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute('SELECT nombre FROM cursos WHERE id_curso = %s', (curso_seleccionado,))
    curso = cursor.fetchone()

    return render_template('./profesor/p-agregar-libro.html', curso = curso)


@app.route('/add/libros/', methods=['POST'])
def agregar_libro():
    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')

    id_profesor = session['user_id']
    curso_seleccionado = session['curso_seleccionado']

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    portada = request.files.get('portada')
    titulo = request.form.get('titulo')
    libro = request.files.get('libro')

    cursor.execute("SELECT * FROM asignaturas JOIN profesores ON profesores.id_asignatura = asignaturas.id_asignatura WHERE id_profesor = %s", (id_profesor,))
    id_asignatura_result = cursor.fetchone()
    if id_asignatura_result:
        id_asignatura = id_asignatura_result['id_asignatura']

    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    portada_filename = f'portada_{timestamp}_{portada.filename}' if portada else None
    libro_filename = f'libro_{timestamp}_{libro.filename}' if libro else None

    if portada_filename:
        portada_path = os.path.join(app.config['UPLOAD_FOLDER'], portada_filename)
        portada.save(portada_path)

    if libro_filename:
        libro_path = os.path.join(app.config['UPLOAD_FOLDER'], libro_filename)
        libro.save(libro_path)

    cursor.execute(" INSERT INTO libros (id_libro, id_asignatura, id_curso, titulo, subir_libro, portada) VALUES (NULL, %s, %s, %s, %s, %s)", (id_asignatura, curso_seleccionado, titulo, libro_filename, portada_filename))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect('/profesor/refuerzo/libros/')
    

@app.route('/profesor/agregar/video/')
def p_agg_video():    
    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')
    
    curso_seleccionado = session['curso_seleccionado']

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute('SELECT nombre FROM cursos WHERE id_curso = %s',(curso_seleccionado))
    curso = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template('./profesor/p-agregar-video.html', curso=curso)

@app.route('/p/agregar/video/', methods=['POST'])
def p_agregar():
    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')
    
    id_profesor = session['user_id']
    curso_seleccionado = session['curso_seleccionado']

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    titulo = request.form.get('titulo-video')
    video = request.form.get('insertar-video')

    cursor.execute("SELECT * FROM asignaturas JOIN profesores ON profesores.id_asignatura = asignaturas.id_asignatura WHERE id_profesor = %s", (id_profesor,))
    id_asignatura_result = cursor.fetchone()
    if id_asignatura_result:
        id_asignatura = id_asignatura_result['id_asignatura']

    cursor.execute('INSERT INTO `videos` (id, titulo, id_curso, id_asignatura, video) VALUES (NULL, %s, %s, %s, %s)', (titulo,curso_seleccionado,id_asignatura, video))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect ('/profesor/refuerzo/videos/')

@app.route('/profesor/materiales/')
def p_material_estudio():
    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')
    
    id_profesor = session.get('user_id')
    curso_seleccionado = session['curso_seleccionado']

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute('SELECT id_asignatura FROM profesores WHERE id_profesor = %s', (id_profesor,))
    asignatura = cursor.fetchone()
    
    id_asignatura = asignatura['id_asignatura']
    
    if id_asignatura is not None:
        cursor.execute('''
            SELECT *
            FROM material_estudio
            JOIN profesor_asignado ON profesor_asignado.id_curso = material_estudio.id_curso
            JOIN profesores ON profesores.id_profesor = profesor_asignado.id_profesor
            WHERE profesores.id_asignatura = material_estudio.id_asignatura
            AND profesores.id_profesor = %s
            AND profesor_asignado.id_curso = %s
            AND material_estudio.id_asignatura = %s
        ''', (id_profesor, curso_seleccionado, id_asignatura))

        estudio = cursor.fetchall()
    else:
        estudio = []

    cursor.close()
    connection.close()

    return render_template('/profesor/p-material_estudio.html', estudios=estudio)


@app.route('/profesor/agregar/material/')
def agregar_material():

    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')

    curso_seleccionado = session['curso_seleccionado']

    connection = pymysql.connect(
        host= 'localhost',
        user= 'root',
        password= '',
        database= 'jes' 
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute('SELECT nombre FROM cursos WHERE id_curso = %s', (curso_seleccionado,))
    curso = cursor.fetchone()

    connection.close()
    cursor.close()
    return render_template('./profesor/p-agregar-material.html', curso=curso)

@app.route('/agregar/material/', methods=['POST'])
def p_agg_material():

    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    id_profesor = session.get('user_id')
    curso_seleccionado = session.get('curso_seleccionado')
    
    # datos del formulario
    titulo = request.form['titulo-material']
    recurso_estudio = request.files['recurso-de-estudio']
    descripcion = request.form['descripcion_material']


    if recurso_estudio:
        recurso_filename = secure_filename(recurso_estudio.filename)
        recurso_path = os.path.join(app.config['UPLOAD_FOLDER'], recurso_filename)
        recurso_estudio.save(recurso_path)

    # Obtener el id_asignatura del profesor
    cursor.execute('SELECT id_asignatura FROM profesores WHERE id_profesor = %s', (id_profesor,))
    asignatura = cursor.fetchone()
    id_asignatura = asignatura['id_asignatura']    

    cursor.execute('''
        INSERT INTO material_estudio (id_material, id_curso, titulo, material_subido, descripcion, id_asignatura)
        VALUES (NULL, %s, %s, %s, %s, %s)
    ''', (curso_seleccionado, titulo, recurso_filename, descripcion, id_asignatura))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect('/profesor/materiales/')

@app.route('/profesor/recurso/estudio/')
def p_recurso_estudio():

    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')

    id_profesor = session['user_id']
    id_estudio = request.args.get('id_estudio')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute('SELECT *, nom_asignatura FROM material_estudio JOIN asignaturas ON asignaturas.id_asignatura = material_estudio.id_asignatura  WHERE id_material = %s', (id_estudio,))
    recurso = cursor.fetchone()

    cursor.execute('SELECT nombre, apellido, imagen_perfil  FROM profesores WHERE id_profesor = %s', (id_profesor,))
    profesor = cursor.fetchone()

    connection.close()
    cursor.close()
    return render_template('./profesor/p-recurso_estudio.html', recurso=recurso, profesor=profesor)

@app.route('/eliminar/recurso/estudio/', methods=['POST'])
def eliminar_recurso_p():

    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    id_material =  request.form.get('id_material')

    cursor.execute('DELETE FROM material_estudio WHERE id_material = %s', (id_material,))

    connection.commit()
    cursor.close()
    return redirect('/profesor/materiales/')


@app.route('/profesor/material/subido/')
def p_material_de_curso_subido():

    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')
    
    material = request.args.get('material')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute('SELECT titulo, material_subido FROM material_estudio WHERE id_material = %s', (material,))

    material = cursor.fetchone()

    cursor.close()
    connection.close()
    return render_template('./profesor/p-material-de-curso-subido.html', material=material)


@app.route('/profesor/clases/enviadas/')
def p_clases_enviadas():

    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')

    id_estudio = request.args.get('id_estudio')
    curso_seleccionado = session['curso_seleccionado']
    id_profesor = session['user_id']

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute('SELECT *, estudiantes.id_estudiante, estudiantes.nombre, estudiantes.apellidos, estudiantes.matricula FROM tareas_estudiante JOIN estudiantes ON estudiantes.id_estudiante = tareas_estudiante.id_estudiante WHERE id_material = %s AND tareas_estudiante.id_curso  = %s', (id_estudio, curso_seleccionado))

    estudiantes = cursor.fetchall()

    cursor.execute('SELECT nombre FROM cursos WHERE id_curso = %s ', (curso_seleccionado,))
    curso = cursor.fetchone()

    cursor.execute('SELECT nom_asignatura FROM asignaturas JOIN profesores ON profesores.id_asignatura = asignaturas.id_asignatura WHERE profesores.id_profesor = %s',(id_profesor,))
    asignatura = cursor.fetchone()

    cursor.execute('SELECT titulo FROM material_estudio WHERE  id_material = %s', (id_estudio,))
    titulo = cursor.fetchone()

    return render_template('./profesor/p-clases-enviada.html', curso=curso, estudiantes=estudiantes, asignatura = asignatura, titulo=titulo)

@app.route('/profesor/tarea/estudiante/')
def p_tarea_e():

    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')

    id_material =  request.args.get('id_material')
    id_estudiante =  request.args.get('id_estudiante')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute('SELECT tarea FROM tareas_estudiante WHERE id_material =  %s AND id_estudiante = %s', (id_material, id_estudiante))
    tarea = cursor.fetchone()

    cursor.execute('SELECT titulo FROM material_estudio WHERE id_material = %s',(id_material,))
    titulo = cursor.fetchone()
    return render_template('./profesor/p-tarea-e.html', tarea=tarea, titulo=titulo)


@app.route('/profesor/perfil/estudiante/<int:id_estudiante>')
def p_perfil_e(id_estudiante):

    if 'user_id' not in session or session.get('role') != 'profesor':
        return redirect('/')

    connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='jes'
        )
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute("""
            SELECT *, cursos.nombre AS nom_curso
            FROM estudiantes
            JOIN cursos ON cursos.id_curso = estudiantes.id_curso
            WHERE id_estudiante = %s
        """, (id_estudiante,))
    estudiante = cursor.fetchone()

    return render_template('./profesor/p-perfil-e.html', estudiante=estudiante)

# APARTADO DEL ADMIN EN PYTHON

@app.route('/home/admin/')
def a_home():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )

    id_admin = session.get('user_id')

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Estudiantes
    cursor.execute('SELECT *, cursos.nombre AS nombre_curso FROM estudiantes JOIN cursos on cursos.id_curso = estudiantes.id_curso')
    estudiantes = cursor.fetchall()
    # Profesores
    cursor.execute('SELECT * FROM profesores JOIN asignaturas on asignaturas.id_asignatura = profesores.id_asignatura')
    profesores = cursor.fetchall()

    #admin
    cursor.execute('SELECT a_img_perfil, nombre_admin, a_apellido FROM admin WHERE id_admin = %s',(id_admin,))
    admin = cursor.fetchone()
    # Cerrar la conexion para seguridad
    cursor.close()
    return render_template('./admin/index.html', estudiantes=estudiantes, profesores=profesores, admin=admin)

@app.route('/admin/cursos/')
def a_cursos():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute('SELECT * FROM cursos')
    cursos = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('./admin/a-cursos.html', cursos=cursos)

@app.route('/admin/getCursos', methods=['GET'])
def getCursos():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM cursos")
    cursos = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return jsonify(cursos)

@app.route('/admin/curso/<int:id_curso>', methods = ['GET'])
def mostrar_estudiantes(id_curso):

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute('SELECT * FROM estudiantes WHERE id_curso = %s', (id_curso,))
    estudiantes = cursor.fetchall()

    cursor.execute('''SELECT p.*, asignaturas.nom_asignatura AS asignatura FROM profesores p JOIN profesor_asignado pa ON p.id_profesor = pa.id_profesor JOIN asignaturas ON asignaturas.id_asignatura = p.id_asignatura WHERE pa.id_curso = %s''', (id_curso,))
    profesores = cursor.fetchall()

    cursor.execute('SELECT * FROM cursos WHERE id_curso = %s', (id_curso,))
    curso = cursor.fetchone()


    sql_cursos = 'SELECT * FROM cursos'
    cursor.execute(sql_cursos)
    cursos = cursor.fetchall()

    sql_profesor = 'SELECT * FROM profesores'
    cursor.execute(sql_profesor)
    profesor = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('./admin/a-curso.html', curso=curso, estudiantes=estudiantes, profesores=profesores, id_curso=id_curso, cursos=cursos, profesor=profesor)

@app.route('/eliminar/profesor/curso/', methods = ['POST'])
def eliminar_profesor_curso():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    id_profesor = request.form.get('id_profesor')
    id_curso = request.form.get('id_curso')
    
    if id_profesor and id_curso:
        eliminar_relacion(id_profesor, id_curso)
    
    return redirect('/admin/cursos')

def eliminar_relacion(id_profesor, id_curso):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute('DELETE FROM profesor_asignado WHERE id_profesor = %s AND id_curso = %s', (id_profesor, id_curso,))
    connection.commit()

    cursor.close()
    connection.close()

@app.route('/admin/materias/')
def a_materias():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM asignaturas')
    asignaturas = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('./admin/a-materias.html', asignaturas=asignaturas)

@app.route('/admin/asignar-profesores/', methods=['GET'])
def a_asignar_profesores():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    sql_cursos = 'SELECT * FROM cursos'
    cursor.execute(sql_cursos)
    cursos = cursor.fetchall()

    sql_profesor = 'SELECT * FROM profesores'
    cursor.execute(sql_profesor)
    profesores = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('./admin/a-agregar-profesor-cursos.html', cursos=cursos, profesores=profesores)

@app.route('/admin/buscar-profesores')
def search_profesores():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    search_option = request.args.get('searchOption')
    query = request.args.get('query')

    if search_option == 'asignatura':
        cursor.execute('SELECT * FROM profesores WHERE id_asignatura = %s', (query,))
    elif search_option == 'matricula':
        cursor.execute('SELECT * FROM profesores WHERE matricula = %s', (query,))
    else:
        cursor.execute('SELECT * FROM profesores')

    profesores = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(profesores)

@app.route('/admin/asignar-profesor', methods=['POST'])
def asignar_profesor():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')    

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    id_profesor = request.form.get('id_profesor')
    id_curso = request.form.get('id_curso')

    cursor.execute('INSERT INTO profesor_asignado (id_profesor_asignado, id_profesor, id_curso) VALUES (NULL, %s, %s)', (id_profesor, id_curso))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for('mostrar_estudiantes', id_curso=id_curso))

@app.route('/admin/agregar_materias/', methods = ['POST', 'GET'])
def a_agg_materias():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    sql_asignaturas = ('SELECT * FROM asignaturas')
    cursor.execute(sql_asignaturas)
    asignaturas = cursor.fetchall()

    sql_curso = ('SELECT * FROM asignatura_curso')
    cursor.execute(sql_curso)
    curso = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('./admin/a-agg-materias.html', asignaturas=asignaturas, curso=curso)

@app.route('/admin/subir_materia/', methods = ['POST'])
def subir_materia():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='jes'
        )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    nom_asignatura = request.form.get("nom_asignatura")
    
    datos = (nom_asignatura)
    
    sql = '''INSERT INTO `asignaturas` (`id_asignatura`, `nom_asignatura`) VALUES (NULL, %s)'''
    
    cursor.execute(sql,datos)
    connection.commit()

    cursor.close()
    connection.close()

    return redirect('/admin/materias/')

@app.route('/admin/eliminar_materia/<int:id_asignatura>', methods = ['POST'])
def eliminar_materia(id_asignatura):

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute('DELETE FROM profesores WHERE id_asignatura = %s', (id_asignatura,))

    cursor.execute('DELETE FROM asignaturas WHERE id_asignatura = %s', (id_asignatura,))

    connection.commit()

    cursor.close()
    connection.close()
    
    return redirect('/admin/materias/')

@app.route('/admin/reportes/')
def a_reportes():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute('SELECT * FROM profesores JOIN asignaturas on asignaturas.id_asignatura = profesores.id_asignatura')
    profesores = cursor.fetchall()

    cursor.execute('SELECT * FROM cursos')
    cursos = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('./admin/a-reporte-curso.html', profesores=profesores, cursos=cursos)

@app.route('/admin/reportes-profesor/<int:id_profesor_asignado>')
def a_reporte_profesor(id_profesor_asignado):

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    sql_reporte = ('SELECT * FROM reporte_profesor WHERE id_profesor_asignado = %s')
    cursor.execute(sql_reporte, (id_profesor_asignado,))
    reportes = cursor.fetchall()

    sql_profesor = ('SELECT * FROM profesores JOIN asignaturas on asignaturas.id_asignatura = profesores.id_asignatura WHERE id_profesor = %s')
    cursor.execute(sql_profesor, (id_profesor_asignado,))
    profesores = cursor.fetchone()

    cursor.close()
    connection.close()
    
    return render_template('./admin/a-reporte-profesor.html', reportes=reportes, profesores=profesores)

@app.route('/admin/perfil/')
def a_perfil():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    sql = 'SELECT nombre_admin, matricula, a_email, a_genero, a_direccion, a_telefono, a_img_perfil FROM admin'

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)

    admin = cursor.fetchone()
    cursor.close()

    return render_template('./admin/a-perfil.html', admin = admin)

@app.route('/admin/reportes-calificacion/')
def a_reporte_calificaciones():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    connection.close()
    cursor.close()

    return render_template('./admin/a-calificaciones-reporte.html')

@app.route('/admin/reportes-asistencias/')
def a_reportes_asistencia():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    return render_template('./admin/a-asistencia-reporte.html')

@app.route('/admin/registro/estudiante/')
def a_formulario_registro_e():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')
        
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM cursos')
    cursos = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('./admin/a-formulario-registro-e.html', cursos=cursos)

@app.route('/admin/agregar_estudiantes', methods=['POST'])
def agregar_estudiante():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes',
        connect_timeout=60
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Obtener datos del formulario
    id_curso = request.form.get("id_curso")
    matricula = request.form.get("matricula")
    nombre = request.form.get("nombre")
    apellidos = request.form.get("apellidos")
    direccion = request.form.get("direccion")
    fecha_nacimiento = request.form.get("fecha_nacimiento")
    genero = request.form.get("genero")
    correo = request.form.get("email")
    telefono = request.form.get("telefono")
    contrasena = request.form.get("contrasena")
    
    imagen_perfil = request.files.get("imagen_perfil")
    imagen_perfil_filename = None

    if imagen_perfil:
        imagen_perfil_filename = secure_filename(imagen_perfil.filename)
        imagen_perfil.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_perfil_filename))
    
    # Insertar datos en la base de datos
    sql = '''
        INSERT INTO `estudiantes` 
        (`id_estudiante`, `id_curso`, `matricula`, `nombre`, `apellidos`, `direccion`, `fecha_nacimiento`, `genero`, `email`, `telefono`, `imagen_perfil`, `contraseña`) 
        VALUES 
        (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    datos = (id_curso, matricula, nombre, apellidos, direccion, fecha_nacimiento, genero, correo, telefono, imagen_perfil_filename, contrasena)
    cursor.execute(sql, datos)

    connection.commit()
    cursor.close()

    return redirect('/home/admin/')

@app.route('/admin/editar_estudiante/<int:id_estudiante>', methods=['GET'])
def editar_estudiante(id_estudiante):

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)


    cursor.execute("SELECT * FROM estudiantes WHERE id_estudiante = %s", (id_estudiante,))
    estudiante = cursor.fetchone()
    
    # Obtener todos los cursos
    cursor.execute("SELECT id_curso, nombre FROM cursos")
    cursos = cursor.fetchall()

    cursor.close()
    connection.close()

    if estudiante:
        return render_template('./admin/a-editar-datos-estudiante.html', estudiante=estudiante, cursos=cursos)
    else:
        return "Estudiante no encontrado", 404
    
@app.route('/editar_profesor/<int:id_profesor>', methods = ['GET'])
def editar_profesor(id_profesor):

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM profesores WHERE id_profesor = %s", (id_profesor,))
    profesor = cursor.fetchone()

    cursor.execute('SELECT * FROM asignaturas')
    asignaturas = cursor.fetchall()
    cursor.close()

    if profesor:
        return render_template('./admin/a-editar-datos-profesores.html', profesor=profesor, asignaturas=asignaturas)
    else:
        return "Profesor no encontrado", 404

@app.route('/admin/actualizar_estudiantes/', methods=['POST'])
def actualizar_estudiantes():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    id_estudiante = request.form.get("id_estudiante")
    id_curso = request.form.get("id_curso")
    nombre = request.form.get("nombre")
    apellidos = request.form.get("apellidos")
    fecha_nacimiento = request.form.get("fecha_nacimiento")
    genero = request.form.get("genero")
    correo = request.form.get("email")
    telefono = request.form.get("telefono")
    direccion = request.form.get("direccion")
    matricula = request.form.get("matricula")
    contraseña = request.form.get("contraseña")
    
    cursor.execute('SELECT imagen_perfil FROM estudiantes WHERE id_estudiante = %s', (id_estudiante,))
    old_image_path = cursor.fetchone().get('imagen_perfil')

    imagen_perfil = request.files.get("imagen_perfil")
    
    imagen_perfil_path = old_image_path

    if imagen_perfil and imagen_perfil.filename:
        filename = secure_filename(imagen_perfil.filename)
        imagen_perfil_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        imagen_perfil.save(imagen_perfil_path)

        if old_image_path and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], old_image_path)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], old_image_path))

    sql = '''UPDATE estudiantes 
             SET nombre = %s, apellidos = %s, fecha_nacimiento = %s, genero = %s, id_curso = %s, email = %s, telefono = %s, direccion = %s, imagen_perfil = %s, matricula = %s, contraseña = %s 
             WHERE id_estudiante = %s'''

    cursor.execute(sql, (nombre, apellidos, fecha_nacimiento, genero, id_curso, correo, telefono, direccion, imagen_perfil_path, matricula, contraseña, id_estudiante))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect('/home/admin/')

@app.route('/admin/eliminar_estudiantes', methods = ['POST'])
def eliminar_estudiantes():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
        
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    id_estudiante = request.form.get("id_estudiante")

    cursor.execute('DELETE FROM estudiantes WHERE id_estudiante = %s', (id_estudiante,))
    connection.commit()
    
    cursor.close()
    connection.close()

    return redirect('/home/admin/')

@app.route('/admin/registro/profesor/')
def a_formulario_registro_p():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT id_asignatura, nom_asignatura FROM asignaturas'

    cursor.execute(sql)
    asignaturas = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('./admin/a-formulario-registro-p.html', asignaturas=asignaturas)

@app.route('/admin/agregar_profesores', methods = ['POST'])
def agregar_profesores():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes',
        connect_timeout=60
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Insertar profesores
    id_asignatura = request.form.get("id_asignatura")
    matricula = request.form.get("matricula")
    nombre = request.form.get("nombre")
    apellidos = request.form.get("apellidos")
    direccion = request.form.get("direccion")
    cedula = request.form.get("cedula")
    genero = request.form.get("genero")
    correo = request.form.get("email")
    telefono = request.form.get("telefono")
    imagen_perfil = request.files.get("imagen_perfil")
    contrasena = request.form.get("contrasena")

    sql = 'INSERT INTO `profesores` (`id_profesor`,`id_asignatura`, `matricula`, `nombre`, `apellido`, `direccion`, `cedula`, `genero`, `email`, `telefono`, `imagen_perfil`, `contraseña`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    datos = (id_asignatura, matricula, nombre, apellidos, direccion, cedula, genero, correo, telefono, imagen_perfil, contrasena)

    cursor.execute(sql,datos)
    
    connection.commit()
    cursor.close()
    
    return redirect('/home/admin/')

@app.route('/admin/actualizar_profesor', methods=['POST'])
def actualizar_profesor():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    id_asignatura = request.form.get("id_asignatura")
    nombre = request.form.get("nombre")
    apellidos = request.form.get("apellido")
    direccion = request.form.get("direccion")
    cedula = request.form.get("cedula")
    genero = request.form.get("genero")
    correo = request.form.get("email")
    telefono = request.form.get("telefono")
    matricula = request.form.get("matricula")
    contraseña = request.form.get("contraseña")
    id_profesor = request.form.get("id_profesor")

    # Obtén la ruta actual de la imagen de perfil
    cursor.execute('SELECT imagen_perfil FROM profesores WHERE id_profesor = %s', (id_profesor,))
    old_image_path = cursor.fetchone().get('imagen_perfil')

    imagen_perfil = request.files.get("imagen_perfil")
    
    imagen_perfil_path = old_image_path

    if imagen_perfil and imagen_perfil.filename:
        filename = secure_filename(imagen_perfil.filename)
        imagen_perfil_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        imagen_perfil.save(imagen_perfil_path)

        if old_image_path and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], old_image_path)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], old_image_path))

    sql = '''UPDATE profesores 
        SET id_asignatura = %s, nombre = %s, apellido = %s, direccion = %s, cedula = %s, genero = %s, email = %s, telefono = %s, matricula = %s, imagen_perfil = %s, contraseña = %s 
        WHERE id_profesor = %s
    '''

    cursor.execute(sql, (id_asignatura, nombre, apellidos, direccion, cedula, genero, correo, telefono, matricula, imagen_perfil_path, contraseña, id_profesor))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect('/home/admin/')

@app.route('/admin/eliminar_profesor', methods = ['POST'])
def eliminar_profesores():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    id_profesor = request.form.get('id_profesor')

    cursor.execute('DELETE FROM profesores WHERE id_profesor = %s', (id_profesor,)) 
    connection.commit()

    cursor.close()
    connection.close()

    return redirect('/home/admin/')

@app.route('/admin/horario/<int:id_curso>')
def horario(id_curso):

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes'
    )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Obtener datos del curso
    cursor.execute('SELECT * FROM cursos WHERE id_curso = %s', (id_curso,))
    curso = cursor.fetchone()

    # Obtener datos del horario
    query = '''
        SELECT 
            h.id_hora,
            h.id_dias,
            d.dia AS dia,
            hora.hora AS hora,
            a.id_asignatura AS id_asignatura,
            a.nom_asignatura AS asignatura
        FROM horario h
        JOIN hora ON h.id_hora = hora.id_hora
        JOIN dias d ON h.id_dias = d.id_dias
        JOIN asignaturas a ON h.id_asignatura = a.id_asignatura
        WHERE h.id_curso = %s
        ORDER BY hora.hora, d.id_dias
    '''
    cursor.execute(query, (id_curso,))
    rows = cursor.fetchall()

    # Obtener todos los días
    cursor.execute('SELECT * FROM dias')
    dias = cursor.fetchall()

    # Obtener todas las horas
    cursor.execute('SELECT * FROM hora')
    horas = cursor.fetchall()

    # Obtener todas las asignaturas
    cursor.execute('SELECT * FROM asignaturas')
    asignaturas = cursor.fetchall()

    # Organizar los datos del horario en un diccionario
    horarios = {}
    for row in rows:
        hora = row['hora']
        dia = row['dia']
        if hora not in horarios:
            horarios[hora] = {}
        horarios[hora][dia] = row['id_asignatura']

    cursor.close()
    connection.close()

    return render_template('./admin/a-horario-1a.html', curso=curso, horarios=horarios, dias=dias, horas=horas, asignaturas=asignaturas)


@app.route('/admin/guardar_horario/', methods=['POST'])
def guardar_horario():

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    id_curso_str = request.form.get('id_curso')
    if id_curso_str is None:
        return "Error: id_curso no proporcionado", 400

    if not id_curso_str.isdigit():
        return "Error: id_curso inválido", 400

    id_curso = int(id_curso_str)
    horario_data = request.form.to_dict(flat=False)

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='jes',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    cursor = connection.cursor()

    # Eliminar horarios existentes para el curso
    cursor.execute('DELETE FROM horario WHERE id_curso = %s', (id_curso,))

    # Insertar nuevos horarios
    for key, values in horario_data.items():
        if key.startswith('horario['):
            hora = key.split('[')[1].split(']')[0]
            dia = key.split('[')[2].split(']')[0]
            asignatura = values[0]
            
            if asignatura:
                # Obtener ID de hora
                cursor.execute('SELECT id_hora FROM hora WHERE hora = %s', (hora,))
                id_hora_result = cursor.fetchone()
                if not id_hora_result:
                    continue
                id_hora = id_hora_result['id_hora']

                # Obtener ID de día
                cursor.execute('SELECT id_dias FROM dias WHERE dia = %s', (dia,))
                id_dias_result = cursor.fetchone()
                if not id_dias_result:
                    continue
                id_dias = id_dias_result['id_dias']

                # Obtener ID de asignatura
                cursor.execute('SELECT id_asignatura FROM asignaturas WHERE id_asignatura = %s', (asignatura,))
                id_asignatura_result = cursor.fetchone()
                if not id_asignatura_result:
                    continue
                id_asignatura = id_asignatura_result['id_asignatura']

                # Insertar nuevo horario
                cursor.execute('''
                    INSERT INTO horario (id_curso, id_hora, id_dias, id_asignatura)
                    VALUES (%s, %s, %s, %s)
                ''', (id_curso, id_hora, id_dias, id_asignatura))

    connection.commit()
    cursor.close()
    connection.close()
    
    return redirect(url_for('horario', id_curso=id_curso))

@app.route('/admin/perfil/estudiante/<int:id_estudiante>')
def a_perfil_e(id_estudiante):

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    
    connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='jes'
        )
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute("""
            SELECT *, cursos.nombre AS nom_curso
            FROM estudiantes
            JOIN cursos ON cursos.id_curso = estudiantes.id_curso
            WHERE id_estudiante = %s
        """, (id_estudiante,))
    estudiante = cursor.fetchone()

    return render_template('./admin/a-perfil-e.html', estudiante=estudiante)

@app.route('/admin/perfil/profesor/<int:id_profesor>')
def a_perfil_p(id_profesor):

    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/')

    connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='jes'
        )
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute("""
            SELECT *, nom_asignatura
            FROM profesores
            JOIN asignaturas ON asignaturas.id_asignatura = profesores.id_asignatura
            WHERE id_profesor = %s
        """, (id_profesor,))
    profesor = cursor.fetchone()

    return render_template('./admin/a-perfil-p.html', profesor=profesor)
        
# =========================================================

@app.route('/cerrar/session/')
def cerra_sesion():
    session.clear()
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 3000, debug=True)