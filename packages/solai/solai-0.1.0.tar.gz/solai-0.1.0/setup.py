from setuptools import setup, find_packages

# Read README.md if it exists
long_description = 'A CLI assistant powered by OpenAI'
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except:
    pass

setup(
    name="solai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'click>=8.0.0',
        'python-dotenv>=1.0.0',
        'openai>=1.0.0',
        'rich>=10.0.0',
    ],
    entry_points={
        'console_scripts': [
            'sol=solai.app:main',
        ],
    },
    author="Jon Caraveo",
    author_email="jon@ziavision.com",
    description="A CLI assistant powered by OpenAI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/caraveo/solai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    keywords="cli, assistant, openai, gpt, command-line",
) 