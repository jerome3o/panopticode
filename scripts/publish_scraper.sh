cd scraper

NAME=bankscraper
TAGS=0.0.1

docker buildx build --platform=linux/arm64 . -t jerome3o/$NAME:$TAGS-arm
docker push jerome3o/$NAME:$TAGS-arm

cd .. 