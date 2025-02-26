import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# 🧪 tests/test_scraper.py

import pytest
from scrapy_html.scraper import get_html_content
from unittest.mock import patch


# 🔄 Mock para simular respostas HTTP
class MockResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception(f"❌ Falha ao acessar a URL. Status code: {self.status_code}")


# 🌐 ✅ Testes para get_html_content
@patch("scrapy_html.scraper.requests.get")
def test_get_html_content_tag(mock_get):
    """🔍 Testa filtragem por tag única."""
    mock_get.return_value = MockResponse("""
        <html><body><p>Parágrafo 1</p><p>Parágrafo 2</p></body></html>
    """)
    resultado = get_html_content("https://exemplo.com", tag="p")
    assert len(resultado) == 2
    assert "Parágrafo 1" in resultado[0]
    assert "Parágrafo 2" in resultado[1]


@patch("scrapy_html.scraper.requests.get")
def test_get_html_content_tags(mock_get):
    """🔍 Testa filtragem por múltiplas tags."""
    mock_get.return_value = MockResponse("""
        <html><body><div>Conteúdo div</div><span>Texto span</span></body></html>
    """)
    resultado = get_html_content("https://exemplo.com", tags="div,span")
    assert len(resultado) == 2
    assert "Conteúdo div" in resultado[0]
    assert "Texto span" in resultado[1]


@patch("scrapy_html.scraper.requests.get")
def test_get_html_content_class(mock_get):
    """🎯 Testa filtragem por classe CSS."""
    mock_get.return_value = MockResponse("""
        <html><body><p class='destaque'>Texto destacado</p></body></html>
    """)
    resultado = get_html_content("https://exemplo.com", tag="p", class_="destaque")
    assert len(resultado) == 1
    assert "Texto destacado" in resultado[0]


@patch("scrapy_html.scraper.requests.get")
def test_get_html_content_id(mock_get):
    """🆔 Testa filtragem por ID."""
    mock_get.return_value = MockResponse("""
        <html><body><div id='principal'>Conteúdo principal</div></body></html>
    """)
    resultado = get_html_content("https://exemplo.com", tag="div", id_="principal")
    assert len(resultado) == 1
    assert "Conteúdo principal" in resultado[0]


@patch("scrapy_html.scraper.requests.get")
def test_get_html_content_attrs(mock_get):
    """🛠 Testa filtragem com atributos adicionais."""
    mock_get.return_value = MockResponse("""
        <html><body><img src='imagem.jpg' alt='Imagem principal'></body></html>
    """)
    resultado = get_html_content("https://exemplo.com", tag="img", attrs={"alt": "Imagem principal"})
    assert len(resultado) == 1
    assert "imagem.jpg" in resultado[0]


@patch("scrapy_html.scraper.requests.get")
def test_get_html_content_sem_filtros(mock_get):
    """🌟 Testa retorno de todo o conteúdo HTML sem filtros."""
    mock_get.return_value = MockResponse("""
        <html><body><h1>Título</h1><p>Parágrafo</p></body></html>
    """)
    resultado = get_html_content("https://exemplo.com")
    assert len(resultado) == 4  # html, body, h1, p
    assert "<h1>Título</h1>" in resultado[2]
    assert "<p>Parágrafo</p>" in resultado[3]


# 🚨 Teste para erro de requisição HTTP
@patch("scrapy_html.scraper.requests.get")
def test_get_html_content_http_error(mock_get):
    """❌ Testa falha de requisição HTTP."""
    mock_get.return_value = MockResponse("Erro", status_code=404)
    with pytest.raises(Exception, match="❌ Falha ao acessar a URL"):
        get_html_content("https://exemplo.com")


# 🏃 **Execução dos testes**
if __name__ == "__main__":
    pytest.main(["-v", "tests/test_scraper.py"])
