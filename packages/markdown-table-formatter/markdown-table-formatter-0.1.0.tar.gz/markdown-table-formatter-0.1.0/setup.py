from setuptools import setup, find_packages

setup(
    name="markdown-table-formatter",
    version="0.1.0",
    description="A tool to format Markdown tables by aligning columns.",
    author="Tabib",
    author_email="pytabib@gmail.com",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'markdown-table-formatter=markdown_table_formatter:main',
        ],
    },
    url="https://github.com/pyTabib/Markdown_Table_Formatter",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
