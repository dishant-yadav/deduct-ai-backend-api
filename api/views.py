from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.conf import settings


# Create your views here.
class PrecautionsView(APIView):
    def get(self, request):
        print(settings.VAR1)
        print(settings.VAR2)
        return Response("This is a sample text", status=HTTP_200_OK)
