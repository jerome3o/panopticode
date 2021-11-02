cd analysis

NAME=analysis
TAGS=0.0.1

docker build . -t jerome3o/$NAME:$TAGS
docker push jerome3o/$NAME:$TAGS

cd ..