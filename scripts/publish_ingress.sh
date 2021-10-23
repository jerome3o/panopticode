cd ingress

NAME=ingress
TAGS=0.0.4

docker build . -t jerome3o/$NAME:$TAGS
docker push jerome3o/$NAME:$TAGS

cd ..