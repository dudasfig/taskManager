import json

class Usuario:
    idCounter = 1 

    def __init__(self, nome: str, email: str):
        self.id = Usuario.idCounter
        self.nome = nome
        self.email = email
        Usuario.idCounter += 1

    def __repr__(self):
        return f"Usuario(ID={self.id}, Nome={self.nome}, Email={self.email})"


class Tarefa:
    idCounter = 1  

    def __init__(self, titulo: str, descricao: str, status: str, usuario: Usuario):
        if status not in ["Pendente", "Em Andamento", "Concluído"]:
            raise ValueError("Status inválido. Use: 'Pendente', 'Em Andamento' ou 'Concluído'.")
        
        self.id = Tarefa.idCounter
        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        self.usuario = usuario  
        Tarefa.idCounter += 1

    def __repr__(self):
        return f"Tarefa(ID={self.id}, Título={self.titulo}, Status={self.status}, Usuário={self.usuario.nome})"


class GerenciadorTarefas:
   
    def __init__(self):
        self.usuarios = []  
        self.tarefas = []  

    def cadastrar_usuario(self):
        nome = input("Digite o nome do usuário: ")
        email = input("Digite o e-mail do usuário: ")
        usuario = Usuario(nome, email)
        self.usuarios.append(usuario)
        print(f"\n✅ Usuário cadastrado com sucesso: {usuario}\n")

    def listar_usuarios(self):
        if not self.usuarios:
            print("\n⚠️ Nenhum usuário cadastrado.\n")
        else:
            print("\n📋 Lista de Usuários:")
            for usuario in self.usuarios:
                print(usuario)
            print()

    def obter_usuario_por_id(self, usuario_id: int):
        for usuario in self.usuarios:
            if usuario.id == usuario_id:
                return usuario
        return None

    def criar_tarefa(self):
        if not self.usuarios:
            print("\n⚠️ Nenhum usuário cadastrado! Cadastre um usuário primeiro.\n")
            return
        
        titulo = input("Digite o título da tarefa: ")
        descricao = input("Digite a descrição da tarefa: ")
        print("Escolha o status da tarefa:\n1 - Pendente\n2 - Em Andamento\n3 - Concluído")
        status_opcao = input("Digite o número correspondente ao status: ")

        status_map = {"1": "Pendente", "2": "Em Andamento", "3": "Concluído"}
        status = status_map.get(status_opcao)

        if not status:
            print("\n⚠️ Status inválido! Escolha 1, 2 ou 3.\n")
            return

        self.listar_usuarios()
        try:
            usuario_id = int(input("Digite o ID do usuário responsável: "))
            usuario = self.obter_usuario_por_id(usuario_id)
            if not usuario:
                print("\n⚠️ Usuário não encontrado! Tente novamente.\n")
                return
        except ValueError:
            print("\n⚠️ Entrada inválida! Digite um número válido.\n")
            return

        tarefa = Tarefa(titulo, descricao, status, usuario)
        self.tarefas.append(tarefa)
        print(f"\n✅ Tarefa criada com sucesso: {tarefa}\n")

    def listar_tarefas(self):
        if not self.tarefas:
            print("\n⚠️ Nenhuma tarefa cadastrada.\n")
        else:
            print("\n📋 Lista de Tarefas:")
            for tarefa in self.tarefas:
                print(tarefa)
            print()

    def exportar_para_json(self):
        if not self.tarefas:
            print("\n⚠️ Nenhuma tarefa cadastrada para exportar.\n")
            return

        dados = [
            {
                "id": tarefa.id,
                "titulo": tarefa.titulo,
                "descricao": tarefa.descricao,
                "status": tarefa.status,
                "usuario": {
                    "id": tarefa.usuario.id,
                    "nome": tarefa.usuario.nome,
                    "email": tarefa.usuario.email
                }
            }
            for tarefa in self.tarefas
        ]

        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

        print("\n✅ Dados exportados para 'tasks.json' com sucesso!\n")

def menu():
    sistema = GerenciadorTarefas()
    
    while True:
        print("\n🔹 Menu - Gerenciador de Tarefas")
        print("1️⃣ - Cadastrar Usuário")
        print("2️⃣ - Listar Usuários")
        print("3️⃣ - Criar Tarefa")
        print("4️⃣ - Listar Tarefas")
        print("5️⃣ - Exportar Tarefas para JSON")
        print("0️⃣ - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            sistema.cadastrar_usuario()
        elif opcao == "2":
            sistema.listar_usuarios()
        elif opcao == "3":
            sistema.criar_tarefa()
        elif opcao == "4":
            sistema.listar_tarefas()
        elif opcao == "5":
            sistema.exportar_para_json()
        elif opcao == "0":
            print("\n👋 Saindo do sistema. Até logo!\n")
            break
        else:
            print("\n⚠️ Opção inválida! Tente novamente.\n")

if __name__ == "__main__":
    menu()