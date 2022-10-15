import json

from django.db.models.query_utils import Q

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from main.models import StudentsInfo
from main.serializers import StudentInfoSerializer
from main.plagiarism_detector import check_plagiarism


class getRecords(viewsets.GenericViewSet, 
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin):

    permission_classes = (IsAuthenticated,)
    queryset = StudentsInfo.objects.all().order_by('created_at')
    serializer_class = StudentInfoSerializer


class addRecord(viewsets.GenericViewSet, 
                mixins.CreateModelMixin):
    
    permission_classes = (IsAuthenticated,)
    queryset = StudentsInfo.objects.all()
    serializer_class = StudentInfoSerializer

    def create(self, request, *arg, **kwargs):

        target = request.data['monograph_file']
        
        monographs = []
        monographs.append(target)

        ##### CHECKING ONLY THE SAME DEPARTMENT MONOGRAPHS #####

        students = StudentsInfo.objects.filter(monograph_language=request.data['monograph_language'],
                                                department=request.data['department'])
        
        for student in list(students):
            temp = student.monograph_file.path
            monographs.append(temp)

        plagiarism_result = check_plagiarism(target=target, monographs_list=monographs)

        ##### IF PLAGIARISM NOT FOUND IN SAME DEPARTMENTS BELOW CHECKS ALL DEPARTMENT MONOGRAPHS EXCEPT THE MONOGRAPHS WHICH IS CHECKED BEFORE #####

        if len(plagiarism_result) == 0:
            students = StudentsInfo.objects.filter(monograph_language=request.data['monograph_language']).exclude(department=request.data['department'])
        
            monographs.clear()
            monographs.append(target)

            for student in list(students):
                temp = student.monograph_file.path
                monographs.append(temp)

            plagiarism_result = check_plagiarism(target=target, monographs_list=monographs)
        
        if len(plagiarism_result) == 0:
            print('no pal detected') 
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers=self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            
            details = {'target_file': str(plagiarism_result[0][0]),
                        'similar with': plagiarism_result[0][1],
                        'similarity score': plagiarism_result[0][2]}
            json.dumps(details)
            return Response(details, status=status.HTTP_400_BAD_REQUEST)


    def perform_create(self, serializer):
        serializer.save()