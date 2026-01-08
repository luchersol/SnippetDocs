from setuptools import setup, find_packages

setup(
    name='snippet_docs',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,  # Incluye templates
    install_requires=[
        'Jinja2',
    ],
    entry_points={
        'console_scripts': [
            'generate-snippet-docs=snippet_docs.generate:main',
        ],
    },
    package_data={
        'snippet_docs': ['templates/*.html'],
    },
    python_requires='>=3.7',
    description='Generador de documentación estática tipo Javadoc para snippets',
)
