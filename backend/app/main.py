from flask import jsonify

class App:
    def __init__(self, app):
        self.app = app
        @app.get("/api/health")
        def healthCheck():
            return jsonify('Think different Academy'), 200
