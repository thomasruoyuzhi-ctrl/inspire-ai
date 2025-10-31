from flask import Flask, render_template
from routes.main import main_bp

app = Flask(__name__)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
     