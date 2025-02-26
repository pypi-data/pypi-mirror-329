### 🚀 **README.md**

# 🌐 Scrapy-HTML

🔍 **Scrapy-HTML** é um pacote Python simples e eficiente para scraping de conteúdo HTML de qualquer página web. Agora com **parâmetros avançados** para filtragem por tag, múltiplas tags, classe CSS e atributos personalizados, tornando a raspagem muito mais flexível e poderosa. Ele utiliza as bibliotecas **BeautifulSoup4** e **Requests** para realizar a raspagem e retornar o HTML de forma estruturada e legível.

---

## ✨ **Características Principais**

- 🌎 Faz scraping de qualquer página web com uma URL válida.
- 🔍 **Filtragem avançada** por:
  - Tag única (`tag`)
  - Múltiplas tags (`tags`)
  - Classe CSS (`class_`)
  - ID (`id_`)
  - Atributos personalizados (`attrs`)
- ⚡ Retorna o HTML formatado e legível usando `BeautifulSoup`.
- 🔒 Tratamento de erros robusto para URLs inválidas ou problemas de rede.
- 💡 Leve e fácil de usar, com dependências mínimas.

---

## ⚡ **Instalação**

Instale o pacote diretamente do **PyPI**:

```bash
pip install scrapy_html
```

---

## 💻 **Como Usar**

### 🔥 **Exemplo básico de uso:**
```python
from scrapy_html.scraper import get_html_content

# 🌐 URL da página
url = "https://www.example.com"

# 🔄 Obtendo o conteúdo HTML completo
dados = get_html_content(url)
print(dados)
```

### 🎯 **Filtragem Avançada:**

#### 🔍 **Filtrar por tag única:**
```python
dados = get_html_content(url, tag="p")
print(dados)  # Exibe todas as tags <p>
```

#### 🏷 **Filtrar por múltiplas tags:**
```python
dados = get_html_content(url, tags="div,span")
print(dados)  # Exibe todas as tags <div> e <span>
```

#### 🎨 **Filtrar por classe CSS:**
```python
dados = get_html_content(url, tag="a", class_="link-destaque")
print(dados)
```

#### 🆔 **Filtrar por ID:**
```python
dados = get_html_content(url, tag="section", id_="conteudo-principal")
print(dados)
```

#### 🛠 **Filtrar por atributos personalizados:**
```python
dados = get_html_content(url, tag="img", attrs={"alt": "Imagem principal"})
print(dados)
```

---

## 🛠 **Requisitos**

- Python >= 3.6
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [requests](https://pypi.org/project/requests/)

As dependências são instaladas automaticamente com:

```bash
pip install scrapy_html
```

---

## 🧪 **Testes**

Este projeto inclui testes usando **pytest**. Para rodar os testes localmente:

```bash
pip install pytest
pytest tests/
```

---

## 🎨 **Recursos Futuros**

- [x] 🔍 Parâmetros avançados para scraping filtrado.
- [ ] 🌐 Suporte a diferentes parsers (`lxml`, `html5lib`).
- [ ] 🔄 Scraping assíncrono para maior desempenho.
- [ ] ⚡ Download de recursos estáticos (imagens, CSS, JS).
- [ ] 🧪 Testes automatizados avançados com `requests-mock`.

---

## 🏗 **Estrutura do Projeto**

```
scrapy_html/
│
├── scrapy_html/             # 📦 Código principal
│   ├── __init__.py
│   └── scraper.py           # ⚡ Função principal: get_html_content()
│
├── tests/                   # 🧪 Testes automatizados
│   └── test_scraper.py
│
├── setup.py                 # ⚙️ Configuração para PyPI
├── pyproject.toml           # 📦 Configuração moderna
├── README.md                # 📚 Documentação do projeto
├── LICENSE                  # 📜 Licença MIT
└── MANIFEST.in              # 📋 Inclusão de arquivos extras
```

---

## 🔧 **Contribuindo**

Contribuições são bem-vindas! 🚀  
Para contribuir, siga estas etapas:

1. **Fork** este repositório.
2. Crie uma nova branch:
   ```bash
   git checkout -b minha-nova-funcionalidade
   ```
3. Faça suas alterações e commit:
   ```bash
   git commit -m "✨ Adicionando nova funcionalidade incrível"
   ```
4. Envie para o branch:
   ```bash
   git push origin minha-nova-funcionalidade
   ```
5. **Abra um Pull Request**. 💡

---

## 📝 **Licença**

Distribuído sob a **Licença MIT**. Veja o arquivo [LICENSE](LICENSE) para mais informações.

---

## 👨‍💻 **Autor**

Desenvolvido por **[Roberto Lima](https://robertolima-developer.vercel.app/)** 🚀✨

---

## 💬 **Contato**

- 📧 **Email**: robertolima.izphera@gmail.com
- 💼 **LinkedIn**: [Roberto Lima](https://www.linkedin.com/in/roberto-lima-01/)

---

## ⭐ **Gostou do projeto?**

Deixe uma ⭐ no repositório e compartilhe com a comunidade! 🚀✨

---

## 🌟 **O que este README oferece?**
- 🎯 **Descrição clara** do projeto e seu propósito.
- 🛠 **Instruções detalhadas de instalação** e **uso prático**.
- 🧪 **Guia de testes** para garantir que o código funciona.
- 🏗 **Estrutura do projeto** para facilitar a navegação.
- 🔄 **Seção de contribuição** para quem deseja ajudar no desenvolvimento.
- 📝 **Licença e informações do autor** para transparência.
