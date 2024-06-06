#!/bin/bash

# If any command fails, stop the script
set -e

load_env() {
    if [ -f .env ]; then
        export $(cat .env | xargs)
    fi
}

# Validate required environment variables
validate_env_variables() {
    local missing_vars=()
    for var in "$@"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done

    if [ ${#missing_vars[@]} -ne 0 ]; then
        echo "Missing required environment variables: ${missing_vars[*]}"
        exit 1
    fi
}

# List of required environment variables
# TODO: check env specific variables

# Constants
VENV=".venv"
PORT=8000         # Default port
ENV="development" # Default environment

display_help() {
    echo "Usage: $0 [option...] {start | deploy} [PORT]" >&2
    echo
    echo "   -h, --help                 display this help and exit"
    echo "   start [PORT] [env]         start the application on the specified port (default: 8000)"
    echo "                              env: development, production (default: development)"
    echo "   deploy                     deploy the application using Docker"
    echo
    exit 1
}

# CREATE venv if not exists
activate_venv() {
    if [ ! -d $VENV ]; then
        echo "Creating virtual environment... $VENV"
        python3 -m venv $VENV
    fi

    source $VENV/bin/activate
}

# install dependencies
install_dependencies() {
    echo "Installing dependencies..."
    pip install -r requirements.txt >/dev/null
    echo "Dependencies installed successfully."
}

# check which python and is in .venv
check_python() {
    echo "Checking python version..."
    echo "Python version: $(python3 --version)"
    if ! command -v python3 &>/dev/null; then
        echo "Python3 is not installed. Please install python3 and try again."
        echo "apt-get install python3"
        echo 'Exiting...'
        exit 1
    fi
}

# deploy the application using Docker
deploy() {
    echo "Building Docker image..."
    docker compose up --build -d
    echo "Docker image built successfully."
    # wait for the container to start
    sleep 5
    echo "Application is running on http://localhost:$PORT"
}

# stop the application
stop() {
    echo "Stopping the application..."
    docker compose down
    echo "Application stopped successfully."
}

# start the application
start() {
    if [ "$ENV" == "prod" ]; then
        echo "Running in production mode..."
        echo "Checking required environment variables..."
        required_env_vars=("ENV" "DATABASE_URL")
    fi
    validate_env_variables "${required_env_vars[@]}"
    echo "Starting the application..."
    python3 manage.py runserver 0.0.0.0:$PORT
}

COMMAND=""
# parse arguments
while [ $# -gt 0 ]; do
    case "$1" in
    -h | --help)
        display_help
        ;;
    start)
        COMMAND=$1
        shift
        if [ $# -gt 0 ]; then
            PORT=$1
            echo "Using port: $PORT"
            shift
        fi
        # parse environment
        if [ $# -gt 0 ]; then
            ENV=$1
            echo "Using environment: $ENV"
            shift
        fi
        ;;
    deploy)
        COMMAND=$1
        shift
        ;;
    stop)
        COMMAND=$1
        shift
        ;;

    *)
        echo "Error: Unknown option: $1" >&2
        display_help
        ;;
    esac
done

# Check if command is set
if [ -z "$COMMAND" ]; then
    echo "Error: Missing option" >&2
    display_help
fi

# Check if parameter is set too execute
case "$COMMAND" in
start)
    check_python
    activate_venv
    # env should be in ["dev", "prod"]
    if [ "$ENV" != "development" ] && [ "$ENV" != "production" ]; then
        echo "Invalid environment: $ENV. Valid environments are: development, production"
        exit 1
    fi
    install_dependencies
    start
    ;;
deploy)
    echo "Deploying..."
    deploy
    ;;

stop)
    stop
    ;;
*)
    echo "Error: Invalid option $COMMAND" >&2
    display_help
    ;;
esac
