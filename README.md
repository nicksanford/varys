# Varys

## Dependencies
1. install python 2.7.13
2. sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev li
bffi-dev libssl-dev
3. install a virtualenv & source the virtualenv
4. pip install -r requirements.txt
5. update varys/settings.py to have the correct database creds
6. make

## Usage
Run the project with `cd varys && make`
If your page is not returning results you can debug it with the shell
`scrapy shell 'http://quotes.toscrape.com/page/1/'`
