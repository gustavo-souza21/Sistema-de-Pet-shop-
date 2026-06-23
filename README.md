<div align="center">

# 🐾 Sistema de Pet Shop
*Gestão de Clientes, Pets e Agendamentos em Python + PostgreSQL*

![STATUS](https://img.shields.io/badge/STATUS-EM%20DESENVOLVIMENTO-blue?style=flat-square)
![DISCIPLINA](https://img.shields.io/badge/PROGRAMA%C3%87%C3%83O%20ORIENTADA%20A%20OBJETOS%20E%20BD-6a0dad?style=flat-square)
![INSTITUIÇÃO](https://img.shields.io/badge/ICET--UFAM-00663C?style=flat-square)
![REPO SIZE](https://img.shields.io/github/repo-size/gustavo-souza21/Sistema-de-Pet-shop-?style=flat-square&color=555)

</div>

---

## 📄 Sobre o Projeto

O **Sistema de Pet Shop** é uma aplicação em **Python** que integra os conceitos de **Programação Orientada a Objetos** a um **banco de dados relacional (PostgreSQL)**. O sistema simula o dia a dia de um pet shop, permitindo o cadastro de clientes e seus pets, o gerenciamento dos serviços oferecidos (banho, tosa, consulta veterinária) e o controle de agendamentos.

> **Trabalho Prático** da disciplina de Programação Orientada a Objetos e Banco de Dados — ICET/UFAM, sob orientação do Prof. Alternei Brito.

## 🚀 Principais Funcionalidades

* **Cadastro de Clientes e Pets:** registro completo com vínculo entre tutor e animal.
* **Gestão de Serviços:** banho/tosa e consulta veterinária, cada um com regra de cálculo própria.
* **Agendamento de Serviços:** marcação de horários com validação de disponibilidade.
* **CRUD Completo:** cadastro, listagem, busca, edição e exclusão de registros.
* **Regra de Negócio:** impede agendamento duplicado para o mesmo horário.
* **Persistência em Banco:** todos os dados armazenados em PostgreSQL.

---

## 🏛️ Padrões Arquiteturais

O sistema adota organização em **pacotes por responsabilidade**, separando claramente domínio, acesso a dados, regras de negócio e interface:

| Camada | Pacote | Responsabilidade |
| :--- | :--- | :--- |
| **Domínio** | `models/` | Entidades do sistema (classes, atributos, métodos) |
| **Persistência** | `repositories/` | Acesso ao banco de dados (INSERT, SELECT, UPDATE, DELETE) |
| **Negócio** | `services/` | Regras de negócio (ex: validação de agendamento) |
| **Apresentação** | `ui/` | Menu textual e interação com o usuário no terminal |
| **Infraestrutura** | `database/` | Conexão e criação das tabelas no PostgreSQL |

```
┌─────────────────────────────────────────────┐
│        UI — Menu textual (terminal)          │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│        SERVICES — Regras de negócio          │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│        MODELS — Entidades (Pessoa, Pet,      │
│        Servico, Agendamento)                 │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│        REPOSITORIES — Acesso a dados         │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│        DATABASE — PostgreSQL + psycopg2      │
└─────────────────────────────────────────────┘
```

**Conceitos de POO aplicados:**
- **Encapsulamento** na classe `Pessoa`.
- **Herança:** `Cliente` e `Funcionario` herdam de `Pessoa`; `BanhoTosa` e `ConsultaVeterinaria` herdam de `Servico`.
- **Polimorfismo:** cálculo de valor do serviço varia conforme o tipo concreto de `Servico`.
- **Classe abstrata** (`ABC` + `@abstractmethod`): `Servico` define o contrato que toda subclasse deve implementar.
- **Tratamento de exceções** nas regras de negócio (ex: agendamento duplicado).

---

## 📁 Estrutura do Repositório

```
Sistema-de-Pet-shop/
├── main.py
├── models/
├── repositories/
├── services/
├── ui/
├── database/
├── sql/
├── docs/
│   └── diagramas/
├── requirements.txt
├── .env.example
└── README.md
```

| Pasta/Arquivo | Descrição |
| :--- | :--- |
| `models/` | Classes do domínio (Pessoa, Cliente, Funcionario, Pet, Servico, Agendamento) |
| `repositories/` | Acesso ao banco de dados (CRUD) |
| `services/` | Regras de negócio do sistema |
| `ui/` | Menu textual de interação |
| `database/` | Conexão e criação automática das tabelas |
| `sql/` | Script SQL alternativo de criação do banco |
| `docs/diagramas/` | Diagrama ER e Diagrama de Classes UML |

📌 Documento completo da estrutura: [`ESTRUTURA_PROJETO.md`](./ESTRUTURA_PROJETO.md)

---

## 🗄️ Banco de Dados

| Tabela | Descrição |
| :--- | :--- |
| `clientes` | Dados dos tutores cadastrados |
| `pets` | Animais vinculados a cada cliente |
| `servicos` | Serviços oferecidos pelo pet shop |
| `agendamentos` | Marcações de serviços para os pets |

**Relacionamentos:** `pets` → `clientes` | `agendamentos` → `pets` e `servicos`

O banco pode ser criado automaticamente via `database/create_tables.py` ou manualmente com `sql/schema.sql`.

📊 Diagramas disponíveis em `docs/diagramas/`:
- Diagrama Entidade-Relacionamento (DER)
- Diagrama de Classes (UML)

---

## 👥 Equipe do Projeto

| Nome | Papel |
| :--- | :--- |
| **Gustavo Souza** | Desenvolvedor / POO e Banco de Dados |
| **Marcelo Barros** | Scrum master |

---

<div align="center">

**Universidade Federal do Amazonas — ICET | Programação Orientada a Objetos e Banco de Dados | 2026**

</div>
