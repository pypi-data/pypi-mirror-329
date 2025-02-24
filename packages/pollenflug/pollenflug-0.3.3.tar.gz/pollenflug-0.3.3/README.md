# pollenflug
## CLI pollen/allergy calendar

[![Python package](https://github.com/BaderSZ/pollenflug/actions/workflows/python-package.yml/badge.svg?branch=master)](https://github.com/BaderSZ/pollenflug/actions/workflows/python-package.yml)

![Screenshot](https://raw.githubusercontent.com/BaderSZ/pollenflug/master/img/screenshot.png)

This script uses [Hexal's Pollenflugkalendar](https://allergie.hexal.de/pollenflug/vorhersage/) to fetch the predictions for the next week.

Currently, the intensity is printed as a numerical value between 0 and 3: 0 being none, 3 being severe.

pollenflug currently supports a configuration file as `~/.pollenflug.ini`, with an example configuration included in the repo

## License

The script is GPL-3.0

## Requirements
The requirements are available in `requirements.txt`. Install them:
```
	pip install -r requirements.txt
```

## INSTALL

The application is available on pip. Run the following command to install locally:
```
	pip install --user pollenflug
```
or globally, with `sudo` if needed:
```
	sudo pip install pollenflug
```

If you want to locally build and install this, then run:
```
	python3 setup.py build
	python3 setup.py install

```

## TODO
* Replace numbers with strings or emojis
* Add support for other countries
