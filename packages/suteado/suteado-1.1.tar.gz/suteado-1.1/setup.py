from setuptools import setup

DESCRIPTION = 'm.kuku.luで使える捨てアドぽいぽいの非公式API'
NAME = 'suteado'
AUTHOR = 'mily'
AUTHOR_EMAIL = 'goshoahiru0323@gmail.com'
URL = 'https://github.com/milypy/suteado/'
LICENSE = 'MIT'
DOWNLOAD_URL = URL
VERSION = '1.01'
PYTHON_REQUIRES = '>=3.1'
INSTALL_REQUIRES = [
    'requests'
]
PACKAGES = [
    'suteado'
]
KEYWORDS = 'suteadopoipoi suteado mail freemail'
CLASSIFIERS=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.1'
]
with open('README.md', 'r', encoding='utf-8') as fp:
    readme = fp.read()
LONG_DESCRIPTION = readme
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    url=URL,
    download_url=URL,
    packages=PACKAGES,
    classifiers=CLASSIFIERS,
    license=LICENSE,
    keywords=KEYWORDS,
    install_requires=INSTALL_REQUIRES
)