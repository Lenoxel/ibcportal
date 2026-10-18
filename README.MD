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

4. Crie um arquivo **.env** dentro do diretório **/ibcportal** e configure o banco de dados e as variáveis de ambiente necessárias.

## Como usar

1. Inicie o servidor local:
    ```bash
    python manage.py runserver
    ```
2. Acesse o site em http://localhost:8000
3. Acesso o painel admin em http://localhost:8000/admin

## Cadastro pelo Google Forms

O endpoint `POST /api/members/google-form-webhook/` recebe o JSON no formato
`{"data": {"Pergunta do formulário": "resposta"}}` e encaminha as respostas
por email para `glenonsilva@gmail.com`. Ele não cria o membro no banco de dados.

Configure `IBC_GOOGLE_FORM_WEBHOOK_SECRET` no ambiente do servidor e use o mesmo
valor na propriedade `API_SECRET` do Apps Script. A propriedade `API_URL` deve
conter a URL HTTPS completa do endpoint. O envio do email também depende das
configurações SMTP `EMAIL_HOST`, `EMAIL_HOST_USER` e `EMAIL_HOST_PASSWORD`.

## Contribuição

Sinta-se à vontade para abrir issues ou pull requests para contribuir com o projeto.