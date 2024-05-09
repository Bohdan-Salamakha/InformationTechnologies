from django.http import JsonResponse

from lab4.exceptions import UncheckedException, CustomException


class CustomExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @staticmethod
    def process_exception(request, exception):
        if isinstance(exception, CustomException):
            return JsonResponse({"error": str(exception)}, status=400)
        elif isinstance(exception, UncheckedException):
            return JsonResponse({"error": str(exception)}, status=500)
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)
