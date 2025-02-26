from setuptools import setup, find_packages

setup(
    name="ai_guard_dbp",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "presidio-analyzer",
        "transformers",
        "bert-score",
        "rouge-score",
        "pandas",
    ],
    description='A module for applying evaluation metrics and guardrails to queries and generated responses.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Dipak Balram Patil",
    author_email="verulikar@gmail.com",
        classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)