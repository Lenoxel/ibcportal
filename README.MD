# Portal IBCC2

O **Portal IBCC2** é um sistema de gestão desenvolvido para a Igreja Batista Central do Curado 2 (IBCC2). O projeto tem como objetivo gerenciar diversos aspectos da igreja, incluindo:

- Membros
- Grupos
- Aulas de Escola Bíblica Dominical (EBD)

## Tecnologias

Este projeto foi desenvolvido com as seguintes tecnologias:

- **Python** (Django)
- **PostgreSQL**
- **HTML/CSS/JavaScript**

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/Lenoxel/ibcportal.git
   ```

2. Crie um ambiente virtual python a partir das dependências do projeto (sugiro utilizar [miniconda](https://docs.anaconda.com/miniconda/)):
    ```bash
    conda create -f environment.yml
    ```

3. Ative o ambiente virtual:
    ```bash
    conda activate ibc_portal_env
    ```

4. Crie um arquivo **.env** dentro do diretório **ibcportal** e configure o banco de dados e as variáveis de ambiente necessárias.

## Como usar

1. Inicie o servidor local:
    ```bash
    python manage.py runserver
    ```
2. Acesse o site em http://localhost:8000
3. Acesso o painel admin em http://localhost:8000/admin

## Contribuição

Sinta-se à vontade para abrir issues ou pull requests para contribuir com o projeto.