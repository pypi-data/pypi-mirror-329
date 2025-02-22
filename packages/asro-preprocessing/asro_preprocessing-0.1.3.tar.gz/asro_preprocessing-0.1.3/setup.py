from setuptools import setup, find_packages

setup(
    name="asro_preprocessing",  # Nama library
    version="0.1.3",  # Versi library yang diperbarui
    description="Library untuk preprocessing teks bahasa Indonesia.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Asro",
    author_email="asro@raharja.info",
    url="https://github.com/asroharun6/asro_preprocessing",  # URL GitHub Anda
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "asro_preprocessing": [
            "data/stopwords.txt",
            "data/kamuskatabaku.xlsx",
            "data/news_dictionary.txt"  # Tambahkan path file baru
        ],
    },
    install_requires=[
        "pandas",
        "nltk",
        "openpyxl"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
