# DeepL Paradox
> Tool to use DeepL Pro on Paradox localisation file

## Requirements

You need a [DeepL API key](https://www.deepl.com/pro.html#developer)

## Installation

Download or clone this repository.

### Python
I recommend you to install a Python environment with conda or virtualenv.

For example with conda, 
[download and install miniconda](https://docs.conda.io/en/latest/miniconda.html)

Create a conda environment
```
conda create -n deepl_paradox python=3.7
```

Activate the conda environment
```
activate deepl_paradox
```

Install the packages with the following commands
```
conda install tqdm requests
```

### DeepL

Put your [DeepL API key](https://www.deepl.com/pro.html#developer) in a file
named _DeepL_key_ at the root of this repository.

## Usage

Activate the conda environment
```
activate deepl_paradox
```

To translate the file _D:\Documents\Commune_de_France_l_english.yml_ execute in the repository
directory the command

```
python translate_paradox_file.py "D:\Documents\Commune_de_France" DeepL_key
```

## License

Tasking manager stats is released under the [MIT License](http://www.opensource.org/licenses/MIT).
