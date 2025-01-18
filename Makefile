format:
    black .
	autopep8 --in-place --aggressive --recursive .
    isort .
    flake8 .