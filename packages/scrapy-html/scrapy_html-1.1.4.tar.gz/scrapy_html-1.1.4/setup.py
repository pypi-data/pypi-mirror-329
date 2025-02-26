from setuptools import setup, find_packages

setup(
    name="scrapy_html",
    version="1.1.4",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0",
        "lxml>=4.9.0"
    ],
    author="Roberto Lima",
    author_email="robertolima.izphera@gmail.com",
    description="🌐 Um scraper que retorna o HTML completo de uma URL, tags, classes e atributos usando BeautifulSoup",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/robertolima-dev/scrapy-html",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "scrapy_html=scrapy_html.scraper:get_html_content",
        ],
    },
    python_requires=">=3.6",
    tests_require=["pytest>=7.0.0"],
)
