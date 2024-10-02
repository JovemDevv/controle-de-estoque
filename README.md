# Sistema de Estoque da Padaria
**version: 1.0**

## Descrição

Este é um sistema web desenvolvido com **Flask**, que permite o gerenciamento do estoque de uma padaria, incluindo:

- **Upload de arquivos CSV** para carregar dados de produtos e vendas.
- **Visualização de gráficos** sobre o estoque atual e as vendas (diárias, semanais e mensais).
- **Login** para acesso à área de gerenciamento do estoque.
  
Os gráficos gerados ajudam a monitorar a quantidade de produtos em estoque e as vendas, com uma visualização clara para facilitar a tomada de decisões.

## Estrutura do Projeto

### Arquivos Principais

1. **app.py**: O arquivo principal que contém a lógica do backend usando Flask.
2. **templates/**:
   - **login.html**: Página de login.
   - **estoque.html**: Página de visualização do estoque e gráficos.
3. **static/**:
   - **estilo.css**: Folha de estilo para a interface do sistema.

### Funcionalidades

- **Login**:
  - Usuário precisa se autenticar para acessar o sistema.
  - As credenciais são verificadas com dados predefinidos no código.
  
- **Upload de CSV**:
  - O sistema permite o upload de arquivos CSV contendo dados de produtos, quantidades e vendas.
  - A partir do CSV, os dados são processados e exibidos em tabelas e gráficos.

- **Visualização de Gráficos**:
  - **Gráfico de Estoque**: Exibe a quantidade de produtos em estoque.
  - **Vendas por Dia, Semana e Mês**: Exibe tabelas de vendas agrupadas por dia, semana e mês.
  - **Vendas Totais por Mês**: Exibe um gráfico de vendas mensais acumuladas.

- **Logout**: 
  - Permite o logout, redirecionando para a página de login.

## Requisitos

- **Python 3.x**
- **Flask**: Framework para o backend.
- **Pandas**: Para manipulação de dados CSV e cálculos de vendas.
- **Matplotlib**: Para gerar gráficos.
- **dotenv**: Para carregar variáveis de ambiente (ex: credenciais de login).

## Como Rodar o Projeto

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

Crie um arquivo `requirements.txt` com os seguintes conteúdos:

```plaintext
Flask==2.0.3
pandas==1.3.3
matplotlib==3.4.3
python-dotenv==0.19.0
```

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env` no diretório raiz e adicione as credenciais de login:

```plaintext
EMAIL=seu_email@example.com
PASSWORD=sua_senha
```

### 3. Rodar o servidor

No terminal, execute:

```bash
python app.py
```

O sistema estará disponível em `http://localhost:5000`.

## Endpoints

### `/` (Login)

- Método: **GET** | **POST**
- Descrição: Página de login. O usuário deve inserir seu email e senha para acessar o sistema.

### `/estoque` (Gestão de Estoque)

- Método: **GET** | **POST**
- Descrição: Página principal do sistema. Permite o upload de arquivos CSV e exibe gráficos e dados de vendas e estoque.
- Parâmetros:
  - **POST**: Enviar um arquivo CSV com dados de estoque e vendas.
  
### `/logout` (Logout)

- Método: **GET**
- Descrição: Realiza o logout e redireciona para a página de login.

## Estrutura de Diretórios

```plaintext
.
├── app.py
├── .env
├── requirements.txt
├── static/
│   └── estilo.css
├── templates/
│   ├── login.html
│   └── estoque.html
└── uploads/  # Pasta onde os arquivos CSV serão salvos
```

## Como o Sistema Funciona

### Carregamento de Dados

Quando o arquivo CSV é enviado, ele é processado pela função `carregar_estoque()`, que usa o **pandas** para ler o arquivo e preparar os dados. Depois, os dados são agrupados por dia, semana e mês usando a função `calcular_vendas()`.

### Geração de Gráficos

Os gráficos são gerados com o **matplotlib** e convertidos em imagens codificadas em base64 para serem exibidos no frontend, sem necessidade de salvar os gráficos no servidor.

### Gráficos gerados

- **Quantidade de Produtos em Estoque**: Gráfico de barras que mostra a quantidade de produtos disponíveis.
- **Vendas Totais por Mês**: Gráfico de linha que mostra o total de vendas mês a mês.
