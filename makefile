.PHONY:build
build:
	jupyter-book build .

.PHONY:publish
publish:
	ghp-import -n -p -f _build/html

.PHONY:convert
convert:
	jupyter-book myst init