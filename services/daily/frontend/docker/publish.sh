SCRIPT_DIR="$(realpath "$(dirname "${BASH_SOURCE[0]}")")"

(
    cd $SCRIPT_DIR/..
    docker build -t jerome3o/daily-frontend .
    docker push jerome3o/daily-frontend
)
