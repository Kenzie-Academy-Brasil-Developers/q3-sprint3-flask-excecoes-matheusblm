import dotenv
from json import dump, load, loads
import os
from flask import Flask, jsonify, request
from app.exceptions import UserAlreadyExistsError, FieldError
from http import HTTPStatus

app = Flask(__name__)
dotenv.load_dotenv()
FILES_DIRECTORY = os.getenv('FILES_DIRECTORY')

@app.get('/')
def home():
    return jsonify(message=" Entrega 8 Q3")
@app.get('/user')
def user():
    try:
        os.makedirs(FILES_DIRECTORY)
        with open(f'{FILES_DIRECTORY}/database.json', 'w') as database:
            dump({"data": []}, database, indent=4)
        return jsonify(database), 200
    except FileExistsError:
        open_file = open(f'{FILES_DIRECTORY}/database.json')
        load_file = load(open_file)
        open_file.close()
        return load_file

@app.post("/user")
def add_user():
    data = request.get_json()
    try: 
        if type(data["nome"]) != str or type(data["email"]) != str:
           raise FieldError("Tipo dos dados Incorretos!")
        open_file = open(f'{FILES_DIRECTORY}/database.json')
        load_file = load(open_file)
        novo_nome = data.get('nome')
        novo_email = data.get('email')
        novo_id = len(load_file.get('data')) + 1 
        for user in load_file.get("data"):    
            if user.get("email") == novo_email:
                raise UserAlreadyExistsError("Email já existe")
        with open(f'{FILES_DIRECTORY}/database.json', 'w') as database:
            load_file.get('data').append({"email": novo_email, "id":novo_id,"nome": novo_nome})
            dump(load_file, database, indent=4)
            return load_file, 201
    except FieldError:
          return FieldError.message, HTTPStatus.BAD_REQUEST

    except UserAlreadyExistsError:
        return UserAlreadyExistsError.message, HTTPStatus.CONFLICT   

    