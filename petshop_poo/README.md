# Sistema de Pet Shop (E-Project)

Trabalho Pratico da disciplina de Engenharia de Software / POO -- UFAM/ICET
(Prof. Alternei Brito).

## Integrantes do grupo

- Gustavi Pinheiro de Souza
- Marcelo Barros da Silva

## Descricao do sistema

Sistema de gestao para um pet shop, com cadastro de clientes, seus animais,
funcionarios (que podem ser veterinarios e/ou tosadores), servicos
oferecidos, agendamentos e vendas (de servicos e de produtos, com controle
de estoque). O foco do trabalho e demonstrar a integracao entre
Programacao Orientada a Objetos e persistencia em banco de dados
relacional (PostgreSQL).

### Organizacao do projeto (pacotes)

```
petshop_poo/
├── main.py            -> ponto de entrada (menu principal em terminal)
├── models/            -> classes de dominio (Pessoa, Cliente, Funcionario,
│                          Animal, Servico, Agendamento, Produto, Venda...)
├── repositories/       -> acesso ao banco (uma classe por entidade,
│                          todas herdando de RepositorioBase)
├── services/           -> regras de negocio orientadas a objetos
├── ui/                 -> menu textual (terminal) por entidade
└── database/           -> conexao com o PostgreSQL + schema.sql
```

### Conceitos de POO aplicados

- **Heranca**: `Pessoa` (classe abstrata) -> `Cliente`, `Funcionario`.
- **Classe abstrata / ABC**: `Pessoa` (`descricao_papel`), `RepositorioBase`
  (contrato de `criar/listar/buscar_por_id/atualizar/deletar`), `ItemBase`
  (`subtotal`/`descricao`).
- **Polimorfismo**: `Cliente` e `Funcionario` implementam `descricao_papel()`
  de formas diferentes (usado por `__str__`, herdado de `Pessoa`);
  `ItemServico` e `ItemProduto` implementam `subtotal()`/`descricao()` e sao
  percorridos de forma uniforme em `Venda.calcular_total()` e no menu de
  vendas.
- **Encapsulamento**: atributos validados via `@property` (ex: `Pessoa.nome`,
  `Pessoa.cpf` — aceita formatado, mas exige exatamente 11 numeros —,
  `Cliente.email`, `Agendamento.status`, `Servico.valor`).
- **Excecoes customizadas**: `models/excecoes.py` centraliza os erros de
  dominio (`ClienteNaoEncontradoError`, `EmailDuplicadoError`,
  `EstoqueInsuficienteError`, `HorarioIndisponivelError`, etc.), traduzidos
  a partir de erros crus do banco quando necessario (ex:
  `ForeignKeyViolation` -> `RegistroVinculadoError`).
- **Regras de negocio orientadas a objetos**:
  - `Produto.baixar_estoque()` nunca deixa o estoque ficar negativo;
  - `Agendamento.status` so aceita valores validos (`Agendado`,
    `Concluido`, `Cancelado`);
  - `AgendamentoService.agendar()` impede dois agendamentos do mesmo
    funcionario no mesmo horario;
  - `ClienteService.cadastrar()` impede cadastro com e-mail duplicado.

### Banco de dados

- PostgreSQL, com 10 tabelas (`Cliente`, `Animal`, `Servico`, `Funcionario`,
  `Veterinario`, `Tosador`, `Agendamento`, `Venda`, `Item_venda`,
  `Intem_Produto`, `Produto`), chaves primarias/estrangeiras e uma trigger
  (`fn_recalcula_valor_venda`) que recalcula automaticamente o valor de
  uma venda sempre que um item e alterado.
- Script completo de criacao em `database/schema.sql`.

## Instrucoes de execucao

1. Crie um banco PostgreSQL vazio (ex: `petshop`).
2. Rode o script de criacao das tabelas:
   ```
   psql -U postgres -d petshop -f database/schema.sql
   ```
3. Ajuste as credenciais em `database/connection.py` (`DB_CONFIG`).
4. Instale as dependencias:
   ```
   pip install -r requirements.txt
   ```
5. Rode o sistema:
   ```
   python main.py
   ```
6. Navegue pelo menu textual exibido no terminal.
