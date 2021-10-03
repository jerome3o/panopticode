cd ingress

NAME=bankingress
TAGS=0.0.1

docker build . -t $NAME:$TAGS

cd ..