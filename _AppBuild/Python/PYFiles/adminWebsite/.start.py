from flask import Flask

app = Flask(__name__, instance_relative_config=True)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
