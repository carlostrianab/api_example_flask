from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__) #Creates an app using flask

#CONNECTING THE APP WITH THE DATABASE 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/categoriaapi' #Connect the app with the database 
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False # Avoids alerts or warnings if the connection with the database is failing

#INITIALIZING SQLALCHEMY AND MARSHMALLOW MODULES 
db = SQLAlchemy(app)
ma = Marshmallow(app)

app.app_context().push()

#CREATING DATABASE MODEL TABLE
class Categoria(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True) #Column id is an integer and is primary key
    cat_nom = db.Column(db.String(100)) #Column cat_nom is a string and has a limit of 100 charaters 
    cat_desp = db.Column(db.String(100)) #Column cat_desp is a string and has a limit of 100 characters 

    #Contructor is declared, so when the class is instanciated it recieves the data 
    def __init__(self, cat_nom, cat_desp):
        self.cat_nom = cat_nom
        self.cat_desp = cat_desp
        
db.create_all() #Creates the database table 

#CREATE DATABASE SCHEMA 
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id', 'cat_nom', 'cat_desp') #Database schema 

categoria_schema = CategoriaSchema() #Initializing the database schema with a single response 

categorias_schema = CategoriaSchema(many=True) #Initializing the database schema with multiple responses

#DATABASE ROUTES 

#GET route 

@app.route('/categoria',methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all() #Calls all the categorias table 
    result = categorias_schema.dump(all_categorias) #Asigns the table data to the 'result' variable using 'categorias_schema'schema 
    return jsonify(result) #Turns the data in the 'result' variable into json format 

#GET route with id

@app.route('/categoria/<id>',methods=['GET'])
def get_categoria_id(id):
    una_categoria = Categoria.query.get(id) #Calls a category row depending on its id and asigns it to the variable 'una_categoria'
    return categoria_schema.jsonify(una_categoria) #uses the 'categoria_schema' to process the data in the desired schema and returns it in json format 

#POST route

@app.route('/categoria', methods=['POST'])
def insert_categoria():
    data = request.get_json(force=True)#Forces the request, avoiding problems 

    cat_nom = request.json['cat_nom'] #Receives the json request for the 'cat_nom' field and assigns it to the cat_nom variable
    cat_desp = request.json['cat_desp'] #Recieves the json request for the 'cat_desp' field and assigns it to the cat_desp variable 

    nuevo_registro =Categoria(cat_nom, cat_desp) # Adjusts our cat_nom and cat_desp data to fit our Categoria schema, so it can be received by the database 

    db.session.add(nuevo_registro) #Adds our new registry to the database 
    db.session.commit()#Commits the changes to our database

    return categoria_schema.jsonify(nuevo_registro) #Returns the registry that ha been done, so we can verify the new registry has actually been made 

#PUT route

@app.route('/categoria/<id>', methods=['PUT'])
def update_categoria(id):
    data = request.get_json(force=True)#Forces the request avoiding problems 

    actualizar_categoria = Categoria.query.get(id) #Calls a category row depending on its is and asigns it to the cariable 'actualizar_categoria'

    cat_nom = data['cat_nom'] #Assigns the requested cat_nom value to a 'cat_nom' variable
    cat_desp = data['cat_desp'] #Assigns the requested cat_desp value to a 'cat_desp' variable 

    actualizar_categoria.cat_nom = cat_nom #It access the cat_nom element on the row and assigns the new 'cat_nom' value 
    actualizar_categoria.cat_desp = cat_desp #It access the cat_desp element on the row and assign the new 'cat_desp' value 

    db.session.commit() #Commits the chanage made in the DB 

    return categoria_schema.jsonify(actualizar_categoria) #Returns the registry that has been done, so qe can verify the new registry actually has been made 

#DELETE route 

@app.route('/categoria/<id>', methods=['DELETE'])
def delete_categoria(id):

    eliminar_categoria = Categoria.query.get(id) #Calls the category row depending on the id and saves it in the variable 'eliminar_categoria'
    db.session.delete(eliminar_categoria) #Deletes the row saved in the 'eliminar_categoria' variable 
    db.session.commit() #Commits the change in the database 

    return categoria_schema.jsonify(eliminar_categoria) #Returns 'eliminar_categoria' row in json format according to the 'categoria_schema' schema 

#Welcome message
@app.route('/', methods=['GET']) #an api GET route 

def index():
    return jsonify({'Mensaje':'Bienvenido'})  #index route , return the object {'Mensaje' : 'Bienvenido'}

if __name__ == '__main__':
    app.run(debug=True)  #initiates the app, equivalent to npm start in node.js