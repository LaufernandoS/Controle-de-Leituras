# Controle de Leituras

## O que o projeto faz

O **Controle de Leituras** tem como proposta ser um web app simples para organizar livros que o usuário deseja ler, está lendo ou já leu. A aplicação permite registrar livros, associá-los a autores e acompanhar o progresso da leitura.

O sistema possui funcionalidades básicas de gerenciamento, incluindo:

- [x] Cadastro de livros com associação a autores
- [x] Barra de progresso calculada automaticamente
- [x] Status: Quero ler / Lendo / Concluído
- [x] Edição inline sem recarregar a página
- [x] Busca por título ou autor em tempo real
- [x] Remoção com confirmação

O projeto está **em fase inicial de desenvolvimento**, portanto as funcionalidades e a estrutura do sistema ainda podem sofrer alterações.

---

## Por que o projeto é útil

Muitas pessoas mantêm listas informais de livros em anotações, planilhas ou aplicativos genéricos. Este projeto busca oferecer uma interface simples para organizar leituras de forma estruturada.

Além disso, o projeto também serve como **exercício prático de desenvolvimento web**, explorando tecnologias como:

- FastAPI + SQLAlchemy + SQLite
- Jinja2 (templates)
- HTMX (operações CRUD sem reload)
- HTML + CSS puro

---

## Como os usuários podem começar a usar o projeto

Como o projeto ainda está em desenvolvimento, a forma de utilização pode mudar ao longo do tempo. De forma geral, o fluxo esperado será:

1. Clonar o repositório
2. Instalar as dependências do projeto
3. Executar o servidor da aplicação
4. Acessar o sistema pelo navegador

## Como rodar

### 1. Criar e ativar o ambiente virtual

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Rodar o servidor

```bash
# Na raiz do projeto (controle-leituras/)
uvicorn app.main:app --reload
```

Ou simplesmente:

```bash
bash run.sh
```

### 4. Acessar

Abra o navegador em: [http://localhost:8000](http://localhost:8000)
Instruções mais detalhadas serão adicionadas conforme o projeto evoluir.

---

## Estrutura

app/
├── main.py        # entrada FastAPI, seed de dados
├── database.py    # conexão SQLite
├── models.py      # Author e Book (relação 1:N)
├── crud.py        # operações de banco isoladas
├── routes/
│   └── books.py   # endpoints CRUD
├── templates/     # Jinja2 + partials HTMX
└── static/        # CSS

## Uso de Inteligência Artificial

Foi usada Inteligência Artificial para acelerar o desenvolvimento do front-end, tirar dúvidas quanto
à arquitetura do projeto, e gerar a base de dados padrão de inicialização na seed em main.py.

## Modelo de dados
Author (1) ──< Book (N)
- Um autor pode ter vários livros
- Um livro pertence a exatamente um autor

## Onde os usuários podem obter ajuda

Como o projeto ainda está em estágio inicial, o principal canal para dúvidas ou sugestões é:

* Abrir uma **Issue no repositório do GitHub**

Isso permitirá acompanhar problemas, melhorias e discussões relacionadas ao desenvolvimento do projeto.

---

## Quem mantém e contribui com o projeto

Este projeto é atualmente mantido e desenvolvido por mim; o desenvolvimento é **individual**, mas sugestões e feedback são bem-vindos.
