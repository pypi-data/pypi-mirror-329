from setuptools import setup, find_packages

setup(
    name="laonlp-spellchecker",
    version="0.1.9",
    packages=find_packages(),
    install_requires=["symspellpy"],
    author="Khonepaseuth SOUNAKHEN",
    author_email="khonepaserth@fe-nuol.edu.la",
    description="A Lao NLP library for spell-checking",
    long_description=open("readme.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Monaliza14xx/laonlp_spellchecker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    package_data={
        'laonlp_spellchecker': ['lao_words_with_freq.txt'],  # Include the dictionary file in the package
    },
)
