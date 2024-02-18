from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.permissions import AllowAny
from .models import Case
from .serializers import CaseSerializer
import random
from .utils import get_objects_from_video
from django.core.files.storage import FileSystemStorage


import os
from django.conf import settings

# Create your views here.


def TestView(request):
    return Response({"message": "This is a test view"}, status=HTTP_201_CREATED)


class FileUploadView(APIView):

    # def get(self, request):

    def post(self, request):
        video = request.FILES["video_recording"]
        random_no = str(random.randint(0, 100))
        case = Case.objects.create(name="Case " + random_no, video_recording=video)
        case.save()
        case_serializer = CaseSerializer(case)
        file_path = "./media/" + str(case.video_recording)

        objects = get_objects_from_video(file_path)
        response_dict = case_serializer.data
        response_dict.update({"objects": objects})
        print("Final Objects", objects)
        return Response(response_dict, status=HTTP_201_CREATED)


class CaseViewSet(ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get", "list", "post", "patch"]

    # def create():


# deduct_ai / media / cases / videos_recs / SIGNUPPAGE_cnsJOR2.webm
