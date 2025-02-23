import json
from functools import wraps
from Osdental.InternalHttp.Request import CustomRequest
from Osdental.InternalHttp.Response import CustomResponse
from Osdental.Exception.ControlledException import OSDException, RedisException
from Osdental.Utils.Util import Util
from Osdental.Utils.Code import APP_ERROR

def handle_audit_and_exception(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            _, info = args[:2] 
            request = info.context.get('request')
            headers = info.context.get('headers')
            if request:
                CustomRequest(request)

            response = await func(*args, **kwargs)
            CustomResponse(content=json.dumps(response), headers=headers)
            return response

        except OSDException as e:
            OSDException(message=e.message, error=e.error, status_code=e.status_code, headers=headers)
            CustomResponse(content=None, status_code=e.status_code, headers=headers)
            return Util.response(status=e.status_code, message=e.error, data=None)

        except Exception as e:
            CustomResponse(content=None, status_code=APP_ERROR, headers=headers)
            return Util.response(status=APP_ERROR, message=str(e), data=None)

    return wrapper