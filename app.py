# Incluir el framework Flask
import os
from flask import Flask

# importar la pantilla html. para guardar datos desde el formulario importamos request, redirect y session (variable de sesion)
from flask import render_template, request, redirect, session

# Importar el enlace a base de datos MySQL
# from flaskext.mysql import MySQL

# Funciona en python avanzado:
from flask_mysqldb import MySQL

# Importar controlador del tiempo
from datetime import datetime

# Importar para obtener informacion de la imagen
from flask import send_from_directory

# Crear la aplicacion
app=Flask(__name__)

# Crear una llave secreta 
app.secret_key='JES'

# Crear una conexion a la de base de datos
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='jes'

# Agregar el valor para inicializar nuestra aplicacion
mysql.init_app(app)
#-----------------------------------------------------

@app.route('/')
def Index():
    return render_template('index.html')

# APARTADO DEL ESTUDIANTE EN PYTHON

@app.route('/Home/estudiante/')
def e_home():
    return render_template('./estudiante/e-home.html')

@app.route('/estudiante/perfil/')
def e_perfil():
    return render_template('./estudiante/e-perfil.html')

@app.route('/estudiante/material/')
def e_material():
    return render_template('./estudiante/e-material_estudio.html')

@app.route('/estudiante/material/trabajo/')
def ver_materia():
    return render_template('./estudiante/e-ver_materias.html')

@app.route('/estudiante/refuerzo/libros')
def e_refuerzo_libros():
    return render_template('./estudiante/e-refuerzo-libros.html')

@app.route('/estudiante/refuerzo/videos')
def e_refuerzo_videos():
    return render_template('./estudiante/e-refuerzo-videos.html')

@app.route('/estudiante/libro/')
def e_libro():
    return render_template('./estudiante/e-libro-refuerzo.html')

# APARTADO DEL ADMIN EN PYTHON

@app.route('/admin/home')
def a_home():
    return render_template('./admin/a-home.html')

@app.route('/admin/cursos')
def a_cursos():
    return render_template('./admin/a-curso.html')

@app.route('/admin/materias')
def a_materias():
    return render_template('./admin/a-materias.html')

@app.route('/admin/reportes')
def a_reportes():
    return render_template('./admin/a-reporte-curso.html')

# @app.route('/admin/reportes-profesor')
# def a_reportes_profesor():
#     return render_template('./admin/a-reporte-profesor.html')

# @app.route('/admin/perfil')
# def a_reportes_profesor():
#     return render_template('./admin/a-perfil.html')

# @app.route('/admin/reportes-calificacion')
# def a_reportes_profesor():
#     return render_template('./admin/a-calificaciones-reporte.html')

# @app.route('/admin/reportes-asistencias')
# def a_reportes_profesor():
#     return render_template('./admin/a-asistencias-reporte.html')

# @app.route('/admin/registro-E')
# def a_reportes_profesor():
#     return render_template('./admin/a-formulario-registro-e.html')

# @app.route('/admin/registro-P')
# def a_reportes_profesor():
#     return render_template('./admin/a-formulario-registro-p.html')

# @app.route('/admin/profesores')
# def a_reportes_profesor():
#     return render_template('./admin/a-profesor-1_a.html')

# @app.route('/admin/horario')
# def a_reportes_profesor():
#     return render_template('./admin/a-horario-1a.html')

# APARTADO DEL PROFESORES EN PYTHON

@app.route('/profesor/home/')
def p_home():
    return render_template('./profesor/p-home-a.html')

@app.route('/profesor/perfil')
def p_perfil():
    return render_template('./profesor/p-perfil.html')

@app.route('/profesor/refuerzo/libros/')
def p_refuerzo_libros():
    return render_template('./profesor/p-refuerzo-libros.html')

@app.route('/profesor/refuerzo/libro/fuenteAbriir/')
def p_libro_refuerzo():
    return render_template('./profesor/p-libro-refuerzo.html')

@app.route('/profesor/refuerzo/videos')
def p_refuerzo_videos():
    return render_template('./profesor/p-refuerzo-videos.html')

@app.route('/profesor/agregarVideo')
def p_agregar():
    return render_template('./profesor/p-agregar-video.html')

@app.route('/profesor/materiales')
def p_material_estudio():
    return render_template('/profesor/p-material_estudio.html')

@app.route('/profesor/agregar_material')
def p_agregar_material():
    return render_template('./profesor/p-agregar-material.html')

@app.route('/profesor/recuerdoEstudio')
def p_recurso_estudio():
    return render_template('./profesor/p-recurso_estudio.html')

@app.route('/profesor/materialSubido')
def p_material_de_curso_subido():
    return render_template('./profesor/p-material-de-curso-subido.html')

@app.route('/profesor/clasesEnviadas')
def p_clases_enviadas():
    return render_template('./profesor/p-clases-enviada.html')

@app.route('/profesor/tareaEstudiante')
def p_tarea_e():
    return render_template('./profesor/p-tarea-e.html')

@app.route('/profesor/reporte')
def p_report_a():
    return render_template('./profesor/p-report-a.html')

@app.route('/profesor/perfil')
def p_perfil_e():
    return render_template('/profesor/p-perfil-e.html')

if __name__ == '__main__':
    app.run(port = 3000, debug=True)