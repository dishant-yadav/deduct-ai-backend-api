from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from .models import Case
from .serializers import CaseSerializer
from .utils import get_objects_from_video
from django.http import Http404
from .utils import get_results_from_query
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

    def post(self, request, pk):
        case = self.get_object(pk)
        name = request.data["name"]
        objects = request.data["objects"]

        evidence_details = []

        for object in objects:
            precaution = get_results_from_query("precautions", object)
            procedure = get_results_from_query("procedures", object)
            evidence_details.append(
                {"name": object, "precautions": precaution, "procedures": procedure}
            )

        case.name = name
        case.objects_list = objects
        case.evdience_detail_list = evidence_details
        case.save()
        case_serializer = CaseSerializer(case)

        return Response(case_serializer.data, status=HTTP_200_OK)


class CaseSectionView(APIView):

    def get_object(self, pk):
        try:
            return Case.objects.get(pk=pk)
        except Case.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        case = self.get_object(pk)
        notes = request.data["notes"]
        case.notes = notes
        objects = case.objects_list
        objects_len = len(objects)
        query_string = ""
        if objects_len == 1:
            query_string = objects[0]
        else:
            for i in range(objects_len):
                if i != len(objects) - 1:
                    query_string += objects[i]
                else:
                    query_string += " and " + objects[i]

        sections = get_results_from_query("sections", query_string)

        # to fetch sections for individual object
        # for object in objects:
        #     section = self.get_section(object)
        #     sections.append({"name": object, "sections": section})

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

    def post(self, request, pk):
        case = self.get_object(pk)
        suspects = request.data["suspects"]
        suspects = request.data["section_list"]
        # sections save in section list with formatting
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
