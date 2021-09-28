cd scraper

NAME=bankscraper
TAGS=0.0.1

docker build . -t $NAME:$TAGS

cd ..