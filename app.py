#API Buscador de alquileres de Dptos por provincia
__author__ = "Leandro Ibarra"
__email__ = "lhibarra3@gmail.com"
__version__ = "1.0"
import math
import traceback
from urllib import response
from flask import Flask,flash, request, jsonify, render_template, Response, redirect, url_for
import grafico
import obtener_datos
import provincias
# Crear el server Flask
app = Flask(__name__)

# Indicamos al sistema (app) de donde leer la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///provincias.db"
# Asociamos nuestro controlador de la base de datos con la aplicacion
provincias.db.init_app(app)

@app.route("/")
def index():
    try:
        # Renderizar el temaplate HTML index.html
        return render_template('index.html')
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/cantidades")
def cantidades():
    try:
        #obtengo la cantidad de veces que fue consultada cada provincia
        x, y = provincias.dashboard()
        #print(x, y)
        image_html = grafico.graficar(x,y)
        return Response(image_html.getvalue(), mimetype='image/png')

    except:
        return jsonify({'trace': traceback.format_exc()})

@app.route('/total_alquileres', methods=['GET','POST'])
def total_alquileres():
    if request.method == 'GET':
        try:
       
            return render_template('alquileres.html')
        except:
            return jsonify({'trace': traceback.format_exc()})
    if request.method == 'POST':
        try:
            nom_provincia = None
            nom_provincia = str(request.form.get('nom_provincia')).upper()
            #valido que lo ingresado no sea un número y que no este vacío
            if nom_provincia is None or nom_provincia.isdigit():
                return Response(status=400)
            if nom_provincia != "":
                #busco todos los alquileres por provincia, luego paso como parametro la lista
                #y obtengo nueva lista solo con el tipo de moneda cargado por usuario
                provincia = obtener_datos.fetch(nom_provincia)
                data = obtener_datos.cant_tipo_moneda(provincia)
                provincias.insert(nom_provincia)
                return render_template('tabla1.html', data= data)
        except:
            return jsonify({'trace': traceback.format_exc()})

@app.route('/alquileres',methods=['GET', 'POST'])
def alquileres():   
    if request.method == 'GET':
        try:
            #rendarizar el formulario para que el usuario ingrese datos 
            return render_template('form.html')
        except:
            return jsonify({'trace': traceback.format_exc()})
    if  request.method == 'POST': 
        try:
            #capturo los valores ingresados por el usuario
            nom_provincia = None
            nom_provincia = str(request.form.get('nom_provincia')).upper()
            minimo = int(request.form.get('minimo'))
            maximo = int(request.form.get('maximo'))
            #valido que lo ingresado no sea un número y que no este vacío 
            if nom_provincia is None or nom_provincia.isdigit():
                return Response(status=400)
           
            if ((minimo and maximo) > 0 and  minimo < maximo and nom_provincia !="" ):
                provincias.insert(nom_provincia)
                provincia = obtener_datos.fetch(nom_provincia)
                moneda = request.form.get("tipo_moneda")
                data = obtener_datos.seleccionar_datos(provincia, moneda,minimo,maximo)
                #calcuo el total de registros obtenidos
                total_alq=len(data)
                lista_precio =[]
                for x in  data:
                    lista_precio.append(x["Precio"])
                    precio_min = min(lista_precio)
                    precio_max = max(lista_precio)
                    total = 0.0
                for n in lista_precio:
                    total = total + n
                    promedio =0.0
                    promedio = total/ len(lista_precio)
                    prom = round(promedio,2)
                return render_template('tabla.html', data= data,data2=total_alq,data3=precio_min,data4=precio_max,data5=prom)

        except:
                return jsonify({'trace': traceback.format_exc()})

@app.before_first_request
def before_first_request_func():
    # Creamos bases de datos
    provincias.db.create_all()
    print("Base de datos generada")

if __name__ == '__main__':
    print('Inove@Server start!')
    # Lanzar servidor
    app.run(host="127.0.0.1", port=5000)