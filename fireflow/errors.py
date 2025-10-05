from flask import jsonify


def register_errorhandlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not found'}), 404


    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({'error': 'Bad request', 'message': str(e)}), 400


    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': 'Server error'}), 500