import datetime

from django.http import (
    HttpRequest,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    StreamingHttpResponse,
)
from django.utils.translation import gettext_lazy as _
from django.views import View

from .builders import BlobResponseBuilder
from .models import FileModel


class MediaView(View):
    def get(self, request: HttpRequest, path: str):
        if not path:
            return HttpResponseBadRequest(_("Invalid file path."))

        if file_record := FileModel.objects.filter(file=path).first():
            if not (request.user and request.user.is_staff) and not file_record.check_auth(request):
                return HttpResponseBadRequest(_("Invalid file path."))
        else:
            file_record = FileModel(file=path, uploaded_at=datetime.datetime.now())

        return self.serve_file(file_record)

    def serve_file(self, file_record: FileModel, chunk_size: int = 8192):
        def file_iterator():
            with file_record.file.open("rb") as file_obj:
                while chunk := file_obj.read(chunk_size):
                    yield chunk

        try:
            response = StreamingHttpResponse(file_iterator())
            return BlobResponseBuilder.build_response(file_record, response)
        except FileNotFoundError:
            return HttpResponseBadRequest(_("Invalid file path."))
