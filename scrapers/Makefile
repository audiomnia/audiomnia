venv:
	python3 -m venv venv
	. venv/bin/activate; pip install wheel
	. venv/bin/activate; pip install -r requirements.txt

scrape: venv
	. venv/bin/activate; scrapy crawl macaulaylibrary -a MAX=150000 --loglevel WARNING
	gzip ../data/macaulaylibrary.geojson

clean:
	rm -rf venv
	find -iname "*.pyc" -delete

clear-cache:
	rm -rf .scrapy
