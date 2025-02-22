from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Кастомный обработчик ошибок, который логирует их и возвращает структурированный ответ.
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'error': response.data,
            'status_code': response.status_code,
        }
        response.data = custom_response_data

    else:
        logger.error(f"Unhandled exception: {str(exc)}")
        return Response(
            {'error': 'Internal Server Error',
             'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
