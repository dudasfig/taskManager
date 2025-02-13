from flask import Flask, jsonify, request
from flask_cors import CORS
import json

# Importando suas classes
class Usuario:
    _id_counter = 1

    def __init__(self, nome: str, email: str):
        self.id = Usuario._id_counter
        self.nome = nome
        self.email = email
        Usuario._id_counter += 1

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "email": self.email}


class Tarefa:
    _id_counter = 1

    def __init__(self, titulo: str, descricao: str, status: str, usuario: Usuario):
        if status not in ["Pendente", "Em Andamento", "Concluído"]:
            raise ValueError("Status inválido. Use: 'Pendente', 'Em Andamento' ou 'Concluído'.")
        
        self.id = Tarefa._id_counter
        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        self.usuario = usuario
        Tarefa._id_counter += 1

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "status": self.status,
            "usuario": self.usuario.to_dict(),
        }


class GerenciadorTarefas:
    def __init__(self):
        self.usuarios = []
        self.tarefas = []

    def cadastrar_usuario(self, nome, email):
        usuario = Usuario(nome, email)
        self.usuarios.append(usuario)
        return usuario.to_dict()

    def listar_usuarios(self):
        return [usuario.to_dict() for usuario in self.usuarios]

    def obter_usuario_por_id(self, usuario_id):
        for usuario in self.usuarios:
            if usuario.id == usuario_id:
                return usuario
        return None

    def criar_tarefa(self, titulo, descricao, status, usuario_id):
        usuario = self.obter_usuario_por_id(usuario_id)
        if not usuario:
            return None  # Retorna None caso o usuário não exista

        tarefa = Tarefa(titulo, descricao, status, usuario)
        self.tarefas.append(tarefa)
        return tarefa.to_dict()

    def listar_tarefas(self):
        return [tarefa.to_dict() for tarefa in self.tarefas]

    def exportar_para_json(self):
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(self.listar_tarefas(), f, indent=4, ensure_ascii=False)


# Criando o servidor Flask
app = Flask(__name__)
CORS(app)  # Habilitando CORS para o React consumir essa API
sistema = GerenciadorTarefas()

# ===================== ROTAS ===================== #

@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    return jsonify(sistema.listar_usuarios())


@app.route("/usuarios", methods=["POST"])
def cadastrar_usuario():
    dados = request.json
    if "nome" not in dados or "email" not in dados:
        return jsonify({"erro": "Nome e email são obrigatórios"}), 400

    usuario = sistema.cadastrar_usuario(dados["nome"], dados["email"])
    return jsonify(usuario), 201


@app.route("/tarefas", methods=["GET"])
def listar_tarefas():
    return jsonify(sistema.listar_tarefas())


@app.route("/tarefas", methods=["POST"])
def criar_tarefa():
    dados = request.json
    if not all(k in dados for k in ["titulo", "descricao", "status", "usuario_id"]):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    tarefa = sistema.criar_tarefa(dados["titulo"], dados["descricao"], dados["status"], int(dados["usuario_id"]))
    if not tarefa:
        return jsonify({"erro": "Usuário não encontrado"}), 400

    return jsonify(tarefa), 201


@app.route("/exportar", methods=["GET"])
def exportar_json():
    sistema.exportar_para_json()
    return jsonify({"mensagem": "Exportado para tasks.json"}), 200


# ===================== EXECUÇÃO ===================== #
if __name__ == "__main__":
    app.run(debug=True)
