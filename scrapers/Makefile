setup:
	mkdir -p data
	python3 -m venv venv
	. venv/bin/activate; pip install wheel
	. venv/bin/activate; pip install -r requirements.txt

scrape: setup
	. venv/bin/activate; scrapy crawl macaulaylibrary -o data/macaulaylibrary.jl

clean:
	rm -rf venv
	find -iname "*.pyc" -delete
