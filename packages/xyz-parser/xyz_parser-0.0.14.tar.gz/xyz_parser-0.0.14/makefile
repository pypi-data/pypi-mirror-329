.PHONY: upload commit

commit:
	git add makefile readme.md pyproject.toml src/xyz_parser/__init__.py
	git commit

upload:
	git push
	cd dist; rm *
	python -m build
	python -m pip install --upgrade twine
	python -m twine upload --repository pypi dist/*
