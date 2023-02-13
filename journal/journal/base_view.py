import functools
import traceback
from django.db import transaction

from django.http.response import JsonResponse

JSON_PARAMS = {
    'ensure_ascii': False
}


def return_response(json_obj, status=200):
    return JsonResponse(json_obj, status=status, safe=not isinstance(json_obj, list),
                        json_dumps_params=JSON_PARAMS)


def error(exception):
    res = {'message': str(exception), 
           'traceback': traceback.format_exc()}
    return return_response(res, 400)


def baseView(function):
    @functools.wraps(function)
    def inner(request, *args, **kwargs):
        try:
            with transaction.atomic():
                return function(request, *args, **kwargs)
        except Exception as e:
            return error(e)

    return inner
