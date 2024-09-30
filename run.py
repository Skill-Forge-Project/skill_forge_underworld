import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    debug_port = os.getenv("DEBUG_PORT", 5001)  # Set default port to 5001 if DEBUG_PORT is not set
    app.run(host="localhost", port=debug_port, debug=True)