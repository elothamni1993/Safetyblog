from flaskblog import create_app
import os
from dotenv import load_dotenv
import sys
import os
from whitenoise import WhiteNoise

# Ensure the current working directory is in the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flaskblog import create_app



app = create_app()
# Print SECRET_KEY after app initialization

app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')

load_dotenv()  # Load environment variables from .env
with app.app_context():
    print(f"SECRET_KEY: {app.config['SECRET_KEY']}")


if __name__ == '__main__':
    app.run(debug=True)
