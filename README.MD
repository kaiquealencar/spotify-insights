# 🎧 Spotify Insights

Aplicação web que integra com a API do Spotify para exibir seus artistas mais ouvidos no último mês, com uma interface interativa baseada em cards que permitem visualizar e reproduzir suas músicas diretamente na tela.

---

## 🚀 Funcionalidades

* 🔐 Autenticação com a API do Spotify
* 🎤 Listagem dos artistas mais ouvidos no último mês
* 💿 Exibição das músicas mais populares de cada artista
* 🔄 Cards interativos com efeito de "flip"
* ▶️ Player embutido do Spotify para reprodução das faixas

---

## 🛠️ Tecnologias utilizadas

* Python
* Flask
* HTML5
* CSS3
* JavaScript
* API do Spotify

---

## 📦 Dependências

```txt
Flask==3.1.3
requests==2.32.5
python-dotenv==1.2.2
```

> Obs: outras dependências são gerenciadas automaticamente pelo Flask e suas bibliotecas internas.

---

## ⚙️ Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/kaiquealencar/spotify-insights
cd spotify-insights
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv .venv
```

Ativar:

* Windows:

```bash
venv\Scripts\activate
```

* Linux/Mac:

```bash
source venv/bin/activate
```

---

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto e adicione:

```env
CLIENT_ID=seu_client_id
CLIENT_SECRET=seu_client_secret
REDIRECT_URI=http://localhost:9000/callback
```

---

### 5. Execute a aplicação

```bash
python app.py
```

Acesse em:
👉 http://localhost:9000

---

## 🧠 Aprendizados

Este projeto foi desenvolvido com foco em:

* Integração com APIs externas
* Manipulação de dados em aplicações web
* Estruturação de projetos com Flask
* Separação de responsabilidades (HTML, CSS e JavaScript)
* Criação de interfaces interativas

---

## 🔮 Melhorias futuras

* Responsividade aprimorada para mobile
* Deploy em ambiente de produção
* Paginação ou filtros de artistas
* Histórico de músicas ao longo do tempo

---

## 📸 Preview


---

## 📄 Licença

Este projeto é de uso educacional e livre para estudos.
