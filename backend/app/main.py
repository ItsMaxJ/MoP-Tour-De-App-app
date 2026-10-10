from flask import jsonify

class App:
    def __init__(self, app):
        self.app = app
        @app.get("/api/v1/health")
        def healthCheck():
            return jsonify({'status': 'ok'}), 200
