import json

def gerar_id(lista):
    return max(lista, default=0) + 1

def cadastrar_usuario(usuarios, ids):
    nome = input("Digite o nome do usuário: ")
    email = input("Digite o e-mail do usuário: ")
    usuario_id = gerar_id(ids)
    usuarios.append((usuario_id, nome, email))
    ids.append(usuario_id)
    print(f"\n✅ Usuário cadastrado com sucesso: ID={usuario_id}, Nome={nome}, Email={email}\n")

def listar_usuarios(usuarios):
    if not usuarios:
        print("\n⚠️ Nenhum usuário cadastrado.\n")
    else:
        print("\n📋 Lista de Usuários:")
        for usuario in usuarios:
            print(f"ID={usuario[0]}, Nome={usuario[1]}, Email={usuario[2]}")
        print()

def obter_usuario_por_id(usuarios, usuario_id):
    for usuario in usuarios:
        if usuario[0] == usuario_id:
            return usuario
    return None

def criar_tarefa(tarefas, usuarios, tarefa_ids):
    if not usuarios:
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
    
    listar_usuarios(usuarios)
    try:
        usuario_id = int(input("Digite o ID do usuário responsável: "))
        usuario = obter_usuario_por_id(usuarios, usuario_id)
        if not usuario:
            print("\n⚠️ Usuário não encontrado! Tente novamente.\n")
            return
    except ValueError:
        print("\n⚠️ Entrada inválida! Digite um número válido.\n")
        return
    
    tarefa_id = gerar_id(tarefa_ids)
    tarefas.append((tarefa_id, titulo, descricao, status, usuario_id, usuario[1], usuario[2]))
    tarefa_ids.append(tarefa_id)
    print(f"\n✅ Tarefa criada com sucesso: ID={tarefa_id}, Título={titulo}, Status={status}, Usuário={usuario[1]}\n")

def listar_tarefas(tarefas):
    if not tarefas:
        print("\n⚠️ Nenhuma tarefa cadastrada.\n")
    else:
        print("\n📋 Lista de Tarefas:")
        for tarefa in tarefas:
            print(f"ID={tarefa[0]}, Título={tarefa[1]}, Status={tarefa[3]}, Usuário={tarefa[5]}")
        print()

def exportar_para_json(tarefas):
    if not tarefas:
        print("\n⚠️ Nenhuma tarefa cadastrada para exportar.\n")
        return
    
    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump([list(tarefa) for tarefa in tarefas], f, indent=4, ensure_ascii=False)
    
    print("\n✅ Dados exportados para 'tasks.json' com sucesso!\n")

def menu():
    usuarios = []
    tarefas = []
    usuario_ids = []
    tarefa_ids = []
    
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
            cadastrar_usuario(usuarios, usuario_ids)
        elif opcao == "2":
            listar_usuarios(usuarios)
        elif opcao == "3":
            criar_tarefa(tarefas, usuarios, tarefa_ids)
        elif opcao == "4":
            listar_tarefas(tarefas)
        elif opcao == "5":
            exportar_para_json(tarefas)
        elif opcao == "0":
            print("\n👋 Saindo do sistema. Até logo!\n")
            break
        else:
            print("\n⚠️ Opção inválida! Tente novamente.\n")

if __name__ == "__main__":
    menu()
