# --------------------------------------------------------------------------------------------------- #
#                                                                                                     #
#                                            Les imports                                              #
#                                                                                                     #
# --------------------------------------------------------------------------------------------------- #

from sqlite3.dbapi2 import Date
from flask import Flask, render_template, request, session, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from datetime import datetime


# --------------------------------------------------------------------------------------------------- #
#                                                                                                     #
#                                    Création de la base de donnée                                    #
#                                                                                                     #
# --------------------------------------------------------------------------------------------------- #

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class Devoir(db.Model):
    id_work = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    nom_categorie = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    done = db.Column(db.Boolean(), nullable=False)

class Categorie(db.Model):
    nom = db.Column(db.String(200), primary_key=True)
    couleur = db.Column(db.String(200), nullable=False)

db.create_all()

def connection_db():
    connection = sqlite3.Connection("database.db")
    connection.row_factory = sqlite3.Row
    return connection


# --------------------------------------------------------------------------------------------------- #
#                                                                                                     #
#                                        Définition des URL                                           #
#                                                                                                     #
# --------------------------------------------------------------------------------------------------- #

@app.route("/")
def index():
    datenow = datetime.now()
    connection = connection_db()
    work = connection.execute('SELECT * FROM Devoir JOIN Categorie ON Devoir.nom_categorie = Categorie.nom WHERE ? < date and done = False ORDER BY date ASC;',(datenow,)).fetchall()
    workdone = connection.execute('SELECT * FROM Devoir JOIN Categorie ON Devoir.nom_categorie = Categorie.nom WHERE ? < date and done = True ORDER BY date ASC;',(datenow,)).fetchall()
    connection.close()
    return render_template('main.html', work=work, workdone=workdone)

@app.route("/create_work")
def create_work():
    connection = connection_db()
    catego = connection.execute('SELECT * FROM Categorie').fetchall()
    connection.close()
    return render_template('create_work.html', catego=catego)

@app.route("/create_categorie")
def create_caterogie():
    return render_template("create_categorie.html")


# --------------------------------------------------------------------------------------------------- #
#                                                                                                     #
#                              Trouvez un nom a cette partie du programme                             #
#                                                                                                     #
# --------------------------------------------------------------------------------------------------- #

@app.route("/", methods=["POST"])
def sexe_done():
    """ easter egg le nom ptdrrrrrrr, alors tu l'as bien ****** mon con :) !! Le travaille s'appelle Isabelle hein ? A ce que je vois tu l'as fini ;)"""
    json_id_work = request.get_json("post")
    connection = connection_db()
    workdone = connection.execute('SELECT done FROM Devoir WHERE id_work = ? ;',(json_id_work["id_work"],)).fetchall()
    connection.close()
    print(workdone[0][0])

    if workdone[0][0] == 1 :
        devoir = Devoir.query.filter_by(id_work=json_id_work["id_work"]).first()
        devoir.done = 0
        db.session.commit()
        print("done : False")

    elif workdone[0][0] == 0 :
        devoir = Devoir.query.filter_by(id_work=json_id_work["id_work"]).first()
        devoir.done = 1
        db.session.commit()
        print("Done : TRUE")

    else :
        print("WTF")

    return "C'est ok !"

@app.route('/create_work', methods=['POST'])  
def send_work():
    """ Permet de créer un travaille dans la base de donnée Devoir"""
    print("-----------------------------------------------------------------")
    print("                       Création de Devoir                        ")

    # Récupère les données entrée dans l'HTML
    titre = request.form.get("titre")
    desscrition = request.form.get("descirption")
    typeD = request.form.get("type")
    date = request.form.get("date")
    done = False

    # Change la date dans la bonne forme
    date_time_obj = datetime.strptime(date, '%Y-%m-%dT%H:%M')

    # Crée le nouveau devoir dans la base de donnée Devoir
    new_work = Devoir(titre=titre, description=desscrition, nom_categorie=typeD, date=date_time_obj, done=done)
    db.session.add(new_work)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/create_categorie', methods=['POST'])  
def send_catego():
    """" Permet de crée un catégorie dans la base de donnée Catégorie """
    print("-----------------------------------------------------------------")
    print("                      Création de Catégorie                      ")
    # Récupère les données entré dans l'HTML
    nom = request.form.get("nom_categorie")
    color = request.form.get("color")

    # Récupère et verifie si il n'y a pas une clé primaire déjà existante
    connection = connection_db()
    noms_categorie = connection.execute('SELECT nom FROM Categorie').fetchall()
    connection.close()
    if nom in [nom[0] for nom in noms_categorie] :
        return render_template("create_categorie.html", error=True)

        
    # Crée la nouvelle catérgorie dans la base de donnée Catégorie
    else :
        new_catego = Categorie(nom=nom, couleur=color)
        db.session.add(new_catego)
        db.session.commit()
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run('127.0.0.1', debug=True)
