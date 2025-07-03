from fastapi import status
from starlette.responses import JSONResponse

class AppExceptionCase(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, code: str = None):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = {
            "message": message,
        }
        if code:
            self.context["code"] = code

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code={self.status_code} - context={self.context}>"
        )


async def app_exception_handler(request, exc: AppExceptionCase):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "app_exception": exc.exception_case,
            "context": exc.context,
        },
    )
