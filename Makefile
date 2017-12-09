wheel:
	@echo "Building python project..."
	@python setup.py bdist_wheel

# pipenv_lock:
# 	@echo "Building python project..."
# 	# @python setup.py bdist_wheel
# 	@python setup.py sdist

# docker: wheel
# 	sudo docker build -t holimetrix2/pythie-matching -f docker/Dockerfile .
# docker: pipenv_lock
# 	sudo docker build -t holimetrix2/pythie-matching -f docker/Dockerfile .

# run:
# 	docker run --rm -it holimetrix2/pythie-matching sh

pypi-register:
	python setup.py register -r hmx
	
pypi-upload: pypi-register
	python setup.py sdist upload -r hmx

# pip-install_pypi_tart.d-bi:
# 	pip install --extra-index-url https://tart.d-bi.fr/simple/ -e .

pip-install_pypi_localhost:
	pip install --extra-index-url http://localhost:8080/simple/ -e .

pipenv-lock:
	pipenv lock

pipenv-install_with_lock: pipenv-lock
	pipenv install --ignore-pipfile

clean:
	rm -rf build/ dist/

default: docker
