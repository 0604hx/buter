import os

from app.server import create_app

env = os.getenv('FLASK_CONFIG') or 'default'
app, config = create_app(env)

if __name__ == '__main__':
    app.run(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        debug=config.DEBUG
    )
