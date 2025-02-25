import re
from setuptools import setup, find_packages

# Leer el contenido del README
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Leer los requisitos
with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Obtener la versión desde __init__.py
with open("groovindb/__init__.py", "r") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

packages = [
    'groovindb',
    'groovindb.core',
    'groovindb.drivers',
    'groovindb.utils'
]

setup(
    name="groovindb",
    version=version,
    packages=find_packages(include=['groovindb*']),
    package_data={
        'groovindb': ['core/*.py', 'drivers/*.py', 'utils/*.py'],
    },
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "groovindb=groovindb.cli:cli",
        ],
    },
    author="Juan Manuel Panozzo Zenere",
    author_email="juanmanuel.panozzo@groovinads.com",
    description="ORM asíncrono para Python con interfaz similar a Prisma",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/groovinads/groovindb",
    project_urls={
        "Bug Tracker": "https://bitbucket.org/groovinads/groovindb/issues",
        "Documentation": "https://bitbucket.org/groovinads/groovindb/src/master/README.md",
        "Source Code": "https://bitbucket.org/groovinads/groovindb",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: AsyncIO",
    ],
    python_requires=">=3.8",
    keywords="database orm async postgresql mysql prisma",
    data_files=[
        ('', ['LICENSE', 'README.md', 'requirements.txt', 'CHANGELOG.md']),
    ],
) 