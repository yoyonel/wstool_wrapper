wheel:
	@echo "Building python project..."
	@python setup.py bdist_wheel

pypi-register:
	python setup.py register -r hmx
	
pypi-upload: pypi-register
	python setup.py sdist upload -r hmx

pip-install_pypi_localhost:
	pip install --extra-index-url http://localhost:8080/simple/ -e .

pipenv-lock:
	pipenv lock

pipenv-install_with_lock: pipenv-lock
	pipenv install --ignore-pipfile

clean:
	rm -rf build/ dist/

default: wheel