from imit import app

if __name__ == "__main__":
    app.run(host=app.config['LISTEN_HOST'], port=app.config['LISTEN_PORT'])
