from slinn.http_response import HttpResponse
import json


class HttpJSONResponse(HttpResponse):
    def __init__(self, **payload: dict):
        self.data = payload['__data'] if '__data' in payload.keys() else None
        self.status = payload['__status'] if '__status' in payload.keys() else '200 OK'
        self.content_type = payload['__content_type'] if '__content_type' in payload.keys() else 'text/plain'
        if '__data' in payload: 
            del payload['__data']
        if '__status' in payload:
            del payload['__status']
        if '__content_type' in payload:
            del payload['__content_type']
        super().__init__(payload=json.dumps(payload), data=self.data, status=self.status, content_type=self.content_type)
