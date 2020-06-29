# coding=utf-8
# auther：Liul5
# date：9/16/2019 3:53 PM
# tools：PyCharm
# Python：3.7.3

from werkzeug.exceptions import HTTPException
from flask import jsonify, make_response
from resources import basic_auth, token_auth


def register_errors(app):
    # @app.errorhandler(401)
    @app.errorhandler(HTTPException)
    def error_handler(error):
        """
        Standard Error Handler
        """
        if isinstance(error, HTTPException):
            return jsonify({
                'description': error.description,
                'name': error.name,
                'statusCode': error.code,
            }), error.code
        else:
            return jsonify({
                'statusCode': 500,
                'name': 'Internal Server Error',
                'description': 'An unknown error has occurred'
            }), 500

    @basic_auth.error_handler
    @token_auth.error_handler
    def unauthorized():
        return make_response(jsonify({'statusCode': 401, 'name': 'UNAUTHORIZED', 'description': 'Unauthorized access'}),
                             401)


# from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, NotFound
# from werkzeug.exceptions import MethodNotAllowed, InternalServerError, BadGateway

# class BaseError(Exception):
#     """Base Error Class"""
#
#     def __init__(self, except_obj):
#         Exception.__init__(self)
#         self.code = except_obj.code
#         self.message = except_obj.description
#
#     def to_dict(self):
#         return {
#             'code': self.code,
#             'message': self.message,
#         }

# errors = {
#     400: BaseError(BadRequest).to_dict(),
#     401: BaseError(Unauthorized).to_dict(),
#     403: BaseError(Forbidden).to_dict(),
#     404: BaseError(NotFound(description="just a test")).to_dict(),  # 自定义message
#     405: BaseError(MethodNotAllowed).to_dict(),
#     500: BaseError(InternalServerError).to_dict(),
#     502: BaseError(BadGateway).to_dict(),
# }
#
#
# def register_errors(app):
#     @app.errorhandler(400)
#     @app.errorhandler(401)
#     @app.errorhandler(403)
#     @app.errorhandler(404)
#     @app.errorhandler(500)
#     @app.errorhandler(502)
#     def handle_error(error):
#         return errors.get(error.code)

