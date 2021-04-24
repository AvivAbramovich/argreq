build:
	make rst
	python -m build
install:
	pip install dist/*.whl
uninstall:
	pip uninstall -y argreq
clean:
	rm -rf dist build argreq.egg-info
upload:
	twine upload dist/*
test:
	pytest
rst:
	m2r --overwrite README.md