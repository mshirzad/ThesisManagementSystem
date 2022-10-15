import os, uuid

from django.db import models
from django.core.exceptions import ValidationError


def file_path_generator_for_monographs(instance, filename):
    extension = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{extension}'

    return os.path.join(f'monographs/', filename)


def file_path_generator_for_source_code(instance, filename):
    extension = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{extension}'

    return os.path.join(f'source_codes/', filename)

def validate_monograph_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    # valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. <PDF files Only>')


def validate_source_code_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.zip', '.7z', '.rar']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. <zip, 7z, rar files Only>')


class StudentsInfo(models.Model):

    DEPARTMENT_CHOICES = (
        ('SE', 'Software Engineering'),
        ('IT', 'Information Technology'),
        ('IS', 'Information System')
    )

    LANGUAGE_CHOICES = (
        ('EN', 'English'),
        ('FA', 'Farsi'),
        ('PA', 'Pashto')        
    )

    YEAR_CHOICES = (
        # ('1380', '1380'), ('1381', '1381'),('1382', '1382'),('1383', '1383'),('1384', '1384'),('1385', '1385'),('1386', '1386'),
        # ('1387', '1387'),('1388', '1388'),('1389', '1389'),('1390', '1390'),('1391', '1391'),('1392', '1392'),('1393', '1393'),
        # ('1394', '1394'),('1395', '1395'),('1396', '1396'),('1397', '1397'),('1398', '1398'),
        ('1399', '1399'),('1400', '1400'),
        ('1401', '1401'),('1402', '1402'),('1403', '1403'),('1404', '1404'),('1405', '1405'),('1406', '1406'),('1407', '1407'),
        ('1408', '1408'),('1409', '1409'),('1410', '1410'),('1411', '1411'),('1412', '1412'),('1413', '1413'),('1414', '1414'),
        ('1415', '1415'),('1416', '1416'),('1417', '1417'),('1418', '1418'),('1419', '1419'),('1420', '1420'),('1421', '1421'),
        ('1422', '1422'),('1423', '1423'),('1424', '1424'),('1425', '1425')
    ) 
    
    id = models.CharField(primary_key=True, max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    graduation_year = models.CharField(max_length=4, choices=YEAR_CHOICES)
    department = models.CharField(max_length=2, choices=DEPARTMENT_CHOICES)
    monograph_title = models.CharField(max_length=255)
    monograph_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    monograph_file = models.FileField(upload_to=file_path_generator_for_monographs, validators= [validate_monograph_file_extension])
    source_code_files = models.FileField(null=True, blank=True, upload_to=file_path_generator_for_source_code, validators=[validate_source_code_file_extension])

    def __str__(self):
        return f'{self.name}, {self.father_name}, {self.monograph_title}, {self.monograph_file}'
    