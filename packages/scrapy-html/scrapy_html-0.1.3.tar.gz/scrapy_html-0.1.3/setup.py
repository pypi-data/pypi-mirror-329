from setuptools import setup, find_packages

setup(
    name="scrapy_html",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0"
    ],
    author="Roberto Lima",
    author_email="robertolima.izphera@gmail.com",
    description="🌐 Um simples scraper que retorna o HTML completo de uma URL usando BeautifulSoup",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/robertolima-dev/scrapy-html",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
