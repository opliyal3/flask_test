from app.tasks import task_blue
from flask import Flask

app = Flask(__name__)
app.register_blueprint(task_blue)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)  # pragma: no cover
