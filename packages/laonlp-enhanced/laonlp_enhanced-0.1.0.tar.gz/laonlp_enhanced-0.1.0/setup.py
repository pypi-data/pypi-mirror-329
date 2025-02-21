from setuptools import setup, find_packages

setup(
    name="laonlp-enhanced",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "laonlp>=1.0.0",  # Adjust version as needed
        "transformers>=4.0.0",
        "tokenizers>=0.10.0"
    ],
    include_package_data=True,
    package_data={"laonlp_enhanced": ["lao_tokenizer.json", "dictionary.txt", "stopwords.txt"]},
    description="Enhanced Lao NLP tokenizer, compatible with laonlp POS tagging",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Savath Saypadith",
    author_email="mr.saypadith@gmail.com",
    url="https://github.com/saypadith/laonlp-enhanced",  # Optional
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)