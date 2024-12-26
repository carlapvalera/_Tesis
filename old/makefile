.PHONY: prod
prod: test
	cd src && quarto render

.PHONY: test
test:
	python -m doctest lib/utils.py

.PHONY: demo
demo:
	streamlit run demo.py

.PHONY: publish
publish: prod
	cp -r src/_book/* build/
	cd build && git add . && git commit -a -m "build" && git push

.PHONY: zip
zip:
	git archive -o source.zip HEAD .

.PHONY: preview
preview:
	cd src && quarto preview

.PHONY: preview-pdf
preview-pdf:
	cd src && quarto preview --to pdf

.PHONY: html
html:
	cd src && quarto render --to html

.PHONY: pdf
pdf:
	cd src && quarto render --to pdf

.PHONY: epub
epub:
	cd src && quarto render --to epub

.PHONY: install-deps-linux
install-deps-linux:
	sudo apt install librsvg2-bin tinytex
