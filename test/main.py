import time
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    # Let's add a variable to inspect
    message = "Hello from inside the Docker container!"
    print(message) # This will print to the container logs
    
    # Add a breakpoint on the next line
    return f"<h1>{message}</h1>"

if __name__ == "__main__":
    # Important: host='0.0.0.0' makes it accessible outside the container
    app.run(host='0.0.0.0', port=5000, debug=False)
