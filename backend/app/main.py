from flask import jsonify

class App:
    def __init__(self, app):
        self.app = app
        @app.get("/api/health")
        def health_check():
            return jsonify('200'), 200
