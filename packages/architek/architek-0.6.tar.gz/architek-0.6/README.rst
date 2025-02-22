architek
========

**architek** é uma ferramenta CLI para criar automaticamente a estrutura de projetos.

Instalação
----------

Para instalar, use:

.. code-block:: bash

    pip install architek

Uso
---

Para criar um novo projeto no diretorio atual, execute:

.. code-block:: bash

    arc create

Ou para criar um novo projeto com um nome específico num diretorio novo:

.. code-block:: bash

    arc create --name nome_do_projeto

Se você preferir **não criar** um ambiente virtual, adicione a flag `--no-venv`:

.. code-block:: bash

    arc create --no-venv

Ou, ao criar o projeto com nome específico:

.. code-block:: bash

    arc create --name nome_do_projeto --no-venv


Se você deseja inicializar um repositório Git no projeto, adicione a flag --git:

.. code-block:: bash

    arc create --git

Ou, ao criar o projeto com nome específico:

.. code-block:: bash

    arc create --name nome_do_projeto --git




Estrutura do Projeto
====================

.. code-block:: text

    ├── src/                # Código-fonte principal
    │   ├── app/            # Aplicação principal
    │   ├── core/           # Módulos essenciais e configurações
    │   ├── integracoes/    # Integrações com serviços externos
    │   ├── utils/          # Funções utilitárias
    │   ├── api/            # Endpoints da API
    ├── config/             # Arquivos de configuração
    ├── dados/              # Entrada/Saída de arquivos
    ├── logs/               # Logs detalhados de execução
    ├── tests/              # Testes unitários
    ├── requirements.txt    # Dependências do projeto
    ├── .env                # Variáveis de ambiente
    ├── Dockerfile          # Configuração do container Docker
    ├── README.md           # Documentação do projeto
    ├── main.py             # Ponto de entrada do projeto

📂 src/ (Código-fonte principal)
--------------------------------
Aqui ficam todos os scripts e módulos essenciais para o funcionamento do seu.

- **app/** → Contém os projeto individuais, responsáveis pela automação das tarefas.  
  *Exemplo: Um projeto de automação `bot_exemplo.py` que pode fazer login em um sistema e extrair dados.*

- **core/** → Contém funcionalidades reutilizáveis essenciais, como manipulação de logs, autenticação e controle de erros.  
  *Exemplo: `logger.py` para registrar atividades do robô.*

- **integracoes/** → Guarda os módulos que fazem comunicação com sistemas externos, como APIs, bancos de dados, ou WebServices.  
  *Exemplo: `api_cliente.py` pode conter funções para enviar e receber dados de uma API.*

- **utils/** → Contém funções auxiliares comuns ao projeto, como manipulação de arquivos, datas e formatação de strings.  
  *Exemplo: `arquivos.py` pode ter funções para ler e escrever CSV, Excel, etc.*

- **api/** → Caso seu projeto precise expor serviços via API, aqui ficarão os endpoints necessários.  
  *Exemplo: `server.py` pode rodar um FastAPI/Flask para disponibilizar um serviço.*

📁 config/ (Configurações do projeto)
--------------------------------------
Contém arquivos de configuração, como variáveis de ambiente ou JSON/YAML para armazenar credenciais e parâmetros.  
*Exemplo: `config.yaml` pode armazenar URLs de APIs, usuários e senhas criptografadas.*

📁 dados/ (Entrada e saída de arquivos)
---------------------------------------
Diretório destinado para armazenar arquivos usados, como planilhas, XMLs, PDFs e outros dados de entrada/saída.  
*Exemplo: O bot pode buscar arquivos CSV aqui e gerar relatórios em Excel.*

📁 logs/ (Registro das execuções)
---------------------------------
Armazena logs detalhados das execuções. É essencial para rastrear erros e entender o comportamento do projeto.  
*Exemplo: `execucao_20240207.log` conterá um histórico do que o codigo fez durante uma execução.*

📁 tests/ (Testes automatizados)
--------------------------------
Guarda os testes unitários para validar a funcionalidade dos módulos do projeto.  
*Exemplo: `test_bots.py` pode conter testes para garantir que um bot de automação se comporta corretamente.*

📄 requirements.txt (Lista de dependências)
-------------------------------------------
Este arquivo contém todas as bibliotecas Python necessárias para o projeto rodar corretamente.  
O comando abaixo instalará tudo automaticamente:

.. code-block:: bash

    pip install -r requirements.txt

📄 .env (Variáveis de ambiente)
-------------------------------
Arquivo utilizado para armazenar variáveis de ambiente, como chaves secretas, configurações de banco de dados ou API, e flags de desenvolvimento. 
Exemplo:

.. code-block:: bash

    SECRET_KEY=your_secret_key_here
    DEBUG=True

📄 Dockerfile (Configuração do container Docker)
------------------------------------------------
Arquivo de configuração para criar uma imagem Docker do projeto, facilitando o processo de deploy em containers. 
Exemplo de conteúdo:

.. code-block:: bash

    # Dockerfile exemplo
    FROM python:3.12
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    CMD ["python", "main.py"]

📄 README.md (Documentação do projeto)
--------------------------------------
Arquivo de documentação que explica o objetivo do projeto, como instalar, rodar e configurar.  
Deve conter um guia passo a passo para que qualquer pessoa possa entender e contribuir.

📄 main.py (Ponto de entrada do projeto)
----------------------------------------
Arquivo principal que inicia a execução.  

Exemplo de código:

.. code-block:: python

    if __name__ == "__main__":
        print("iniciado!")

💡 Com essa estrutura organizada, fica muito mais fácil manter o código limpo, escalável e reutilizável! 🚀