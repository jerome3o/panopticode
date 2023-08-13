cd ingress

NAME=ingress
TAGS=0.0.7

docker build . -t jerome3o/$NAME:$TAGS
docker push jerome3o/$NAME:$TAGS

cd ..