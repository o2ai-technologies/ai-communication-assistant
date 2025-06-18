#!/bin/bash

# Define the original entrypoint script of the base image
ORIGINAL_ENTRYPOINT="/storage/entrypoint.sh"

# Check if the container is meant to run in debug mode
if [ "$DEBUG_MODE" = "true" ]; then
    ### DEBUG MODE ###
    echo "DEBUG_MODE is enabled. Bypassing original entrypoint to start with debugpy."

    # These are the arguments passed from your Dockerfile's CMD
    # e.g., ["langgraph_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
    ARGS=("$@")

    # This makes the script robust. If the Docker CMD accidentally includes "uvicorn"
    # as the first argument, we remove it before passing the rest to our command.
    if [ "${ARGS[0]}" = "uvicorn" ]; then
      echo "Found 'uvicorn' in CMD, removing it to avoid duplication."
      # This 'shift's the arguments, so ARGS becomes ("langgraph_api.main:app", ...)
      unset ARGS[0]
    fi

    echo "Starting debugpy on 0.0.0.0:${DEBUG_PORT}, which will launch uvicorn."

    echo "ARGS ---------- $ARGS"
    echo "@ --------------- $@"
    echo "PORT --------------- $PORT"
    echo "RELOAD --------------- $RELOAD"

    # We use 'exec' to replace this script with the python debugger process.
    # The debugger (-m debugpy) will then launch the application module (-m uvicorn)
    # with the correct application arguments (the remaining parts of "${ARGS[@]}").
    exec python -m debugpy \
        --listen 0.0.0.0:${DEBUG_PORT} \
        --wait-for-client \
        -m uvicorn langgraph_api.server:app --log-config /api/logging.json --host 0.0.0.0 --port 8000 --no-access-log

else
    ### NORMAL MODE ###
    echo "DEBUG_MODE is not enabled. Running the original entrypoint."
    # If not in debug mode, just run the original entrypoint script
    # and pass along all the arguments from the Dockerfile's CMD.
    exec "$ORIGINAL_ENTRYPOINT" "$@"
fi