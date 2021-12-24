#import SQLAlchemy as SQLAlchemy
#import pymysql as pymysql
from flask import Flask, render_template, request, jsonify, make_response
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:souha@localhost:3306/transaction_management'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
db = SQLAlchemy(app)

#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'souha'
#app.config['MYSQL_DB'] = 'transaction_management'


#mysql = MySQL(app)

#our models
class Compte(db.Model):
    __tablename__ = 'compte'
    idcompte = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(45))
    nom_user = db.Column(db.String(45))
    prenom_user = db.Column(db.String(45))
    phone = db.Column(db.String(45))
    sexe = db.Column(db.String(45))
    solde = db.Column(db.Float, default=0)

    def __init__(self, libelle, nom_user, prenom_user, phone, sexe):
        self.libelle = libelle
        self.nom_user = nom_user
        self.prenom_user = prenom_user
        self.phone = phone
        self.sexe = sexe



    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class Transaction(db.Model):
    __tablename__ = 'transaction'
    idtransaction = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(45))
    montant = db.Column(db.Float)
    descriptif = db.Column(db.String(45))
    date = db.Column(db.Date)

    def __init__(self, type, montant, descriptif, date):
        self.type = type
        self.montant = montant
        self.descriptif = descriptif
        self.date = date

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


#creating our routes
@app.route('/CreateCompte', methods=['POST'])
@cross_origin()
def createcompte():
    print(request.json)
    libellé = request.json['libelle']
    print(libellé)
    # solde = request.json['solde']
    nom_user = request.json['nom_user']
    prenom_user = request.json['prenom_user']
    phone = request.json['phone']
    sexe = request.json['sexe']
    compte = Compte(libellé, nom_user, prenom_user, phone, sexe)
    db.session.add(compte)
    db.session.commit()
    return("succes")


@app.route('/GetAllCompte')
@cross_origin()
def GetAllCompte():
    resp = []
    print(db.session.query(Compte).all())
    for c in db.session.query(Compte).all():
        resp.append({'idcompte' : c.idcompte, 'libelle' : c.libelle, 'nom_user' : c.nom_user,
                     'prenom_user' : c.prenom_user, 'phone' : c.phone , 'sexe' : c.sexe, 'solde' : c.solde })
    return(jsonify(resp))


@app.route('/GetCompteById/<int:idCompte>')
@cross_origin()
def GetCompteById(idCompte):
    print(db.session.query(Compte).filter(Compte.idcompte == idCompte).all())
    c = db.session.query(Compte).filter(Compte.idcompte == idCompte).all()
    print (c[0].idcompte)
    if len(c) == 0:
        return "Not found"
    else:
        return jsonify({'idcompte' : c[0].idcompte, 'libelle' : c[0].libelle,
                        'nom_user' : c[0].nom_user, 'prenom_user' : c[0].prenom_user, 'phone' : c[0].phone ,
                        'sexe' : c[0].sexe, 'solde' : c[0].solde })



@app.route('/GetTransactionById/<int:idTransaction>')
@cross_origin()
def GetTransactionById(idTransaction):
    print(db.session.query(Transaction).filter(Transaction.idtransaction == idTransaction).all())
    c = db.session.query(Transaction).filter(Transaction.idtransaction == idTransaction).all()
    print (c[0].idtransaction)
    if len(c) == 0:
        return "Not found"
    return jsonify({'idtransaction': c[0].idtransaction, 'type': c[0].type, 'montant': c[0].montant,
                    'descriptif': c[0].descriptif, 'date': c[0].date})




@app.route('/RetirerArgent', methods=['PUT'])
@cross_origin()
def retirerargent():
    idcompte = request.json['idcompte']
    montant = request.json['montant']
    for c in db.session.query(Compte).all():
        if c.idcompte == idcompte:
            c.solde -= montant
        break
    descriptif = request.json['descriptif']
    date = datetime.now()
    transaction = Transaction("débit", montant, descriptif, date.strftime("%d/%m/%y"))
    db.session.add(transaction)
    db.session.commit()
    return ("succes")


@app.route('/DeposerArgent', methods=['PUT'])
@cross_origin()
def deposerargent():
    idcompte = request.json['idcompte']
    montant = request.json['montant']
    for c in db.session.query(Compte).all():
        if c.idcompte == idcompte:
            c.solde += montant
        break
    descriptif = request.json['descriptif']
    date = datetime.now()
    transaction = Transaction("débit", montant, descriptif, date.strftime("%y/%m/%d"))
    db.session.add(transaction)
    db.session.commit()
    return ("succes")





@app.route('/GetAllTransaction')
@cross_origin()
def GetAlltransaction():
    resp = []
    print(db.session.query(Transaction).all())
    for t in db.session.query(Transaction).all():
        resp.append({'idtransaction' : t.idtransaction, 'type' : t.type, 'montant' : t.montant,
                     'descriptif' : t.descriptif})
    return(jsonify(resp))







db.create_all()
app.run()

