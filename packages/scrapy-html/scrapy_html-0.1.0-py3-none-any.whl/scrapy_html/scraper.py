import requests
from bs4 import BeautifulSoup


def get_html_content(url: str) -> str:
    """
    🔎 Obtém todo o conteúdo HTML de uma URL usando BeautifulSoup.

    Args:
        url (str): A URL da página a ser raspada.

    Returns:
        str: Conteúdo HTML formatado da página.

    Raises:
        Exception: Se a URL for inválida ou não puder ser acessada.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # ⚡ Garante resposta 200 OK
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.prettify()  # Retorna HTML bonito e legível
    except Exception as e:
        raise Exception(f"❌ Erro ao acessar a URL: {url}. Detalhe: {str(e)}")
