setup:
	python3 -m venv venv
	. venv/bin/activate; pip install -r requirements.txt

scrape: setup
	. venv/bin/activate; scrapy crawl macaulaylibrary

clean:
	rm -rf venv
	find -iname "*.pyc" -delete
