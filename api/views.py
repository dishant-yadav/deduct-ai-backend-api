from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.permissions import AllowAny
from .models import Case
from .serializers import CaseSerializer
import random
from django.http import JsonResponse

# import os
# from django.conf import settings
# Create your views here.


def TestView(request):
    return JsonResponse({"message": "This is a test view"}, status=HTTP_201_CREATED)


class FileUploadView(APIView):

    # def get(self, request):

    def post(self, request):
        video = request.FILES["video_recording"]
        random_no = str(random.randint(0, 100))
        case = Case.objects.create(name="Case " + random_no, video_recording=video)
        caseSerializer = CaseSerializer(case)
        print(video.file)
        case.save()
        return Response(caseSerializer.data, status=HTTP_201_CREATED)


class CaseViewSet(ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get", "list", "post", "patch"]

    # def create():
