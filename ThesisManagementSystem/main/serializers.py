# from django.contrib.auth import get_user_model

from rest_framework import serializers
from main.models import StudentsInfo


class StudentInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentsInfo
        fields = (
            'id',
            'name',
            'father_name',
            'last_name',
            'graduation_year',
            'department',
            'monograph_title',
            'monograph_language',
            'monograph_file',
            'source_code_files',
        )
