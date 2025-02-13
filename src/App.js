import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

export default function App() {
  const [usuarios, setUsuarios] = useState([]);
  const [tarefas, setTarefas] = useState([]);
  const [nomeUsuario, setNomeUsuario] = useState("");
  const [emailUsuario, setEmailUsuario] = useState("");
  const [tituloTarefa, setTituloTarefa] = useState("");
  const [descricaoTarefa, setDescricaoTarefa] = useState("");
  const [statusTarefa, setStatusTarefa] = useState("Pendente");
  const [usuarioSelecionado, setUsuarioSelecionado] = useState("");
  const [erro, setErro] = useState("");
  const [abaAtiva, setAbaAtiva] = useState("tarefas"); // Alternar entre abas
  const [exibirFormularioTarefa, setExibirFormularioTarefa] = useState(false); // Exibir formulário de nova tarefa

  useEffect(() => {
    carregarDados();
  }, []);

  const carregarDados = async () => {
    try {
      const usuariosRes = await axios.get("http://127.0.0.1:5000/usuarios");
      setUsuarios(usuariosRes.data);
      const tarefasRes = await axios.get("http://127.0.0.1:5000/tarefas");
      setTarefas(tarefasRes.data);
    } catch (error) {
      setErro("Erro ao carregar tarefas. Verifique a API.");
    }
  };

  const adicionarUsuario = async () => {
    if (!nomeUsuario || !emailUsuario) {
      setErro("Preencha todos os campos!");
      setTimeout(() => setErro(""), 3000);
      return;
    }
    const res = await axios.post("http://127.0.0.1:5000/usuarios", {
      nome: nomeUsuario,
      email: emailUsuario,
    });
    setUsuarios([...usuarios, res.data]);
    setNomeUsuario("");
    setEmailUsuario("");
  };

  const adicionarTarefa = async () => {
    if (!tituloTarefa || !descricaoTarefa || !usuarioSelecionado) {
      setErro("Preencha todos os campos!");
      setTimeout(() => setErro(""), 3000);
      return;
    }
    try {
      const res = await axios.post("http://127.0.0.1:5000/tarefas", {
        titulo: tituloTarefa,
        descricao: descricaoTarefa,
        status: statusTarefa,
        usuario_id: Number(usuarioSelecionado),
      });
      setTarefas([...tarefas, res.data]);
      setTituloTarefa("");
      setDescricaoTarefa("");
      setStatusTarefa("Pendente");
      setUsuarioSelecionado("");
      setExibirFormularioTarefa(false); // Esconder o formulário após adicionar
    } catch (error) {
      setErro("Erro ao criar tarefa: " + error.response.data.erro);
    }
  };

  return (
    <div className="container">
      <h1>TaskFlow - Gerenciamento de Tarefas</h1>

      {erro && <p className="erro">{erro}</p>}

      {/* Botões de Navegação */}
      <div className="buttons">
        <button onClick={() => setAbaAtiva("tarefas")} className={`btn-primary ${abaAtiva === "tarefas" ? "ativo" : ""}`}>
          📋 Tarefas
        </button>
        <button onClick={() => setAbaAtiva("usuarios")} className={`btn-secondary ${abaAtiva === "usuarios" ? "ativo" : ""}`}>
          👥 Usuários
        </button>
        <button onClick={() => setExibirFormularioTarefa(!exibirFormularioTarefa)} className="btn-success">
          ➕ Nova Tarefa
        </button>
      </div>

      {/* Seção de Tarefas */}
      {abaAtiva === "tarefas" && (
        <table className="table">
          <thead>
            <tr>
              <th>TÍTULO</th>
              <th>DESCRIÇÃO</th>
              <th>RESPONSÁVEL</th>
              <th>STATUS</th>
            </tr>
          </thead>
          <tbody>
            {tarefas.length === 0 ? (
              <tr>
                <td colSpan="4" style={{ textAlign: "center", color: "#666" }}>
                  Nenhuma tarefa cadastrada.
                </td>
              </tr>
            ) : (
              tarefas.map((tarefa) => (
                <tr key={tarefa.id}>
                  <td>{tarefa.titulo}</td>
                  <td>{tarefa.descricao}</td>
                  <td>{tarefa.usuario.nome}</td>
                  <td>{tarefa.status}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      )}

      {/* Seção de Usuários */}
      {abaAtiva === "usuarios" && (
        <div>
          <h2>Cadastrar Usuário</h2>
          <input type="text" placeholder="Nome" value={nomeUsuario} onChange={(e) => setNomeUsuario(e.target.value)} />
          <input type="email" placeholder="E-mail" value={emailUsuario} onChange={(e) => setEmailUsuario(e.target.value)} />
          <button onClick={adicionarUsuario} className="btn-primary">Adicionar Usuário</button>
        </div>
      )}

      {/* Formulário para Nova Tarefa */}
      {exibirFormularioTarefa && (
        <div className="form-tarefa">
          <h2>Adicionar Nova Tarefa</h2>
          <input type="text" placeholder="Título da Tarefa" value={tituloTarefa} onChange={(e) => setTituloTarefa(e.target.value)} />
          <input type="text" placeholder="Descrição" value={descricaoTarefa} onChange={(e) => setDescricaoTarefa(e.target.value)} />
          <select value={statusTarefa} onChange={(e) => setStatusTarefa(e.target.value)}>
            <option value="Pendente">Pendente</option>
            <option value="Em Andamento">Em Andamento</option>
            <option value="Concluído">Concluído</option>
          </select>
          <select value={usuarioSelecionado} onChange={(e) => setUsuarioSelecionado(e.target.value)}>
            <option value="">Selecione um Usuário</option>
            {usuarios.map((usuario) => (
              <option key={usuario.id} value={usuario.id}>{usuario.nome}</option>
            ))}
          </select>
          <button onClick={adicionarTarefa} className="btn-success">Salvar Tarefa</button>
        </div>
      )}
    </div>
  );
}
