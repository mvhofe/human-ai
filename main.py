import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory

from src.routes.humanizer_api import humanizer_bp

# Import the NLTK resource downloader
from src.humanizer_logic.download_resources import download_nltk_resources_for_app

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'a_very_secret_key_for_humanizer_app'

app.register_blueprint(humanizer_bp, url_prefix='/api')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "Welcome to the Text Humanizer API. No frontend index.html found.", 200

if __name__ == '__main__':
    print("Checking/Downloading NLTK resources for the web app...")
    # This will use the Python interpreter running this script.
    # Ensure this script is run with the venv's python when starting the app.
    download_nltk_resources_for_app()
    print("NLTK resource check complete.")
    
    app.run(host='0.0.0.0', port=5000, debug=False) # debug=False for more production-like testing before deployment

