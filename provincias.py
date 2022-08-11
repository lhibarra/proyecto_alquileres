from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from numpy import append
db = SQLAlchemy()

class Provincia(db.Model):
    __tablename__ = "provincia"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    
    def __repr__(self):
        return f"Persona:{self.name} "


def insert(name):
    # Crear una nueva provincia
    person = Provincia(name=name)

    # Agregar la persona a la DB
    db.session.add(person)
    db.session.commit()

def dashboard():
    nom_prov = []
    query = db.session.query(Provincia)
    for datos in query:
        if datos.name != "":
            nom_prov.append(datos.name)
        
    frecuencia = {}
    for  n in nom_prov : 
        if n in frecuencia:
            frecuencia[n]+=1
        else:
            frecuencia[n]= 1
    x = []
    y = []
    for k,v in frecuencia.items():
        x.append(k)
        y.append(v)
    return x,y
