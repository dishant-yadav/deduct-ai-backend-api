from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.permissions import AllowAny
from .models import Case
from .serializers import CaseSerializer
from .utils import get_objects_from_video
from django.http import Http404
import requests


# Create your views here.


class TestView(APIView):

    def get(self, request):
        return Response({"message": "This is a test view"}, status=HTTP_200_OK)


class CreateCase(APIView):

    def post(self, request):
        video = request.FILES["video_recording"]
        case = Case.objects.create(video_recording=video)

        file_path = "./media/" + str(case.video_recording)
        objects = get_objects_from_video(file_path)
        case.objects_list = objects

        case.save()
        case_serializer = CaseSerializer(case)

        print("Final Objects", objects)
        return Response(case_serializer.data, status=HTTP_201_CREATED)


class EvidencePrecautionProcedureView(APIView):

    def get_object(self, pk):
        try:
            return Case.objects.get(pk=pk)
        except Case.DoesNotExist:
            raise Http404

    def get_precaution(self, query):
        BASE_URL = f"http://localhost:5000/api/precautions/{query}"
        print("Precaution API Call for", query)
        resp = requests.get(BASE_URL)
        resp_json = resp.json()
        # print(resp_json)
        return resp_json["precautions"]["response"]

    def get_procedure(self, query):
        BASE_URL = f"http://localhost:5000/api/procedures/{query}"
        print("Procedure API Call for", query)
        resp = requests.get(BASE_URL)
        resp_json = resp.json()
        # print(resp_json)
        return resp_json["procedures"]["response"]

    def get(self, request, pk):
        case = self.get_object(pk)
        name = request.data["name"]
        objects = request.data["objects"]

        precautions = []
        procedures = []

        for object in objects:
            precaution = self.get_precaution(object)
            precautions.append({"name": object, "precautions": precaution})

        for object in objects:
            procedure = self.get_procedure(object)
            procedures.append({"name": object, "procedures": procedure})

        case.name = name
        case.objects_list = objects
        case.precaution_list = precautions
        case.procedure_list = procedures
        case.save()
        case_serializer = CaseSerializer(case)

        return Response(case_serializer.data, status=HTTP_200_OK)


class CaseSectionView(APIView):

    def get_object(self, pk):
        try:
            return Case.objects.get(pk=pk)
        except Case.DoesNotExist:
            raise Http404

    def get_section(self, query):
        BASE_URL = f"http://localhost:5000/api/sections/{query}"
        print("Section API Call for", query)
        resp = requests.get(BASE_URL)
        resp_json = resp.json()
        # print(resp_json)
        return resp_json["sections"]["response"]

    def get(self, request, pk):
        case = self.get_object(pk)
        notes = request.data["notes"]
        case.notes = notes
        objects = case.objects_list

        sections = []

        for object in objects:
            section = self.get_section(object)
            sections.append({"name": object, "sections": section})

        case.section_list = sections

        case.save()

        case_serializer = CaseSerializer(case)

        return Response(case_serializer.data, status=HTTP_200_OK)


class SuspectSupportingDocView(APIView):

    def get_object(self, pk):
        try:
            return Case.objects.get(pk=pk)
        except Case.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        case = self.get_object(pk)
        suspects = request.data["suspects"]
        if len(request.FILES):
            docs = request.FILES["supporting_docs"]
            case.supporting_docs = docs

        case.suspects = suspects

        case.save()

        case_serializer = CaseSerializer(case)

        return Response(case_serializer.data, status=HTTP_200_OK)


# class CaseViewSet(ModelViewSet):
#     queryset = Case.objects.all()
#     serializer_class = CaseSerializer
#     permission_classes = [AllowAny]
#     http_method_names = ["get", "list", "post", "patch"]
