# VentureGotchi

VentureGotchi é uma aplicação web desenvolvida em Python com Django, com foco na aplicação prática de conceitos de backend, autenticação, modelagem de dados e gamificação.

O sistema permite que usuários criem missões e subtarefas, acompanhem seu progresso por meio de XP e níveis e visualizem a evolução do seu avatar (Gotchi), consolidando conceitos fundamentais do framework Django.

## Objetivo do Projeto

Este projeto foi desenvolvido com o objetivo de:

- Praticar o desenvolvimento de aplicações web com Django
- Aplicar conceitos de autenticação e autorização de usuários
- Trabalhar com modelagem de dados utilizando o Django ORM
- Implementar um sistema de gamificação com XP, níveis e progresso
- Integrar o backend Django com frontend utilizando Bootstrap

## Tecnologias Utilizadas

- Python
- Django
- Django ORM
- SQLite (desenvolvimento local)
- PostgreSQL (produção – Render)
- Bootstrap 5
- Chart.js
- HTML e CSS

## Funcionalidades Implementadas

### Autenticação
- Cadastro de usuários
- Login e logout
- Recuperação de senha
- Proteção de rotas utilizando autenticação do Django

### Dashboard
- Exibição do nível e XP do usuário
- Barra de progresso até o próximo nível
- Gráfico de XP ganho por dia
- Histórico de ações realizadas
- Sugestões de trilhas de aprendizado

### Missões e Subtarefas
- Criação de missões diárias e semanais
- Associação de missões a trilhas temáticas
- Criação de subtarefas com valor de XP definido
- Conclusão de subtarefas com ganho automático de XP

### Gamificação
- Sistema de XP e níveis
- Evolução progressiva do usuário
- Conquistas iniciais
- Estatísticas personalizadas:
  - Técnica
  - Criatividade
  - Disciplina
  - Liderança

### Meu Gotchi
- Avatar representando o usuário
- Exibição de nível, XP e estatísticas
- Evolução visual do avatar conforme o nível alcançado

## Como Executar o Projeto Localmente

1. Criar e ativar o ambiente virtual:
python -m venv .venv  
.venv\Scripts\activate  

2. Instalar as dependências:
pip install -r requirements.txt  

3. Executar as migrações:
python manage.py makemigrations  
python manage.py migrate  

4. Criar um superusuário (opcional):
python manage.py createsuperuser  

5. Iniciar o servidor:
python manage.py runserver  

A aplicação estará disponível em:  
http://127.0.0.1:8000/login/

## Checklist de Testes Manuais

- Cadastro de usuário
- Login e logout
- Criação de missão
- Criação de subtarefas
- Conclusão de subtarefas
- Atualização de XP e nível
- Atualização da barra de progresso
- Registro no histórico
- Atualização do gráfico de XP
- Visualização da tela “Meu Gotchi”

## Público-Alvo e Permissões

Usuário autenticado:
- Criar missões e subtarefas
- Concluir tarefas
- Acompanhar progresso e evolução

Administrador:
- Gerenciar usuários por meio do Django Admin

## Deploy

O projeto está preparado para deploy utilizando PostgreSQL em ambiente de produção (Render).

Variáveis de ambiente utilizadas:
- SECRET_KEY
- DEBUG
- DATABASE_URL

## Autores

Projeto desenvolvido por:

Jherika Pereira da Silva  
Pericles Santos Silva Junior  

Projeto acadêmico desenvolvido no curso de Python com Django, com foco em backend, organização de código e boas práticas de desenvolvimento web.
