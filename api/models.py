from django.db import models
import uuid

# Create your models here.

# class User():


class Case(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # investigation_officer = models.ForeignKey(User, on_delete=models.RESTRICT)
    name = models.CharField(max_length=50, blank=True, null=True)
    suspects = models.JSONField(blank=True, null=True)
    notes = models.CharField(max_length=256, blank=True, null=True)
    video_recording = models.FileField(upload_to="cases/videos_recs", blank=True)
    supporting_docs = models.FileField(
        upload_to="cases/supporting_docs", blank=True, null=True
    )
    objects_list = models.JSONField(blank=True, null=True)
    precaution_list = models.JSONField(blank=True, null=True)
    procedure_list = models.JSONField(blank=True, null=True)
    section_list = models.JSONField(blank=True, null=True)

    # location = models.JSONField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Evidence(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    precautions = models.CharField(max_length=256)
    procedure = models.CharField(max_length=256)
    case = models.ForeignKey(
        Case, related_name="evidences", on_delete=models.RESTRICT, blank=True
    )


class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=20)
    desc = models.CharField(max_length=100)
    cause = models.CharField(max_length=100)
    case = models.ForeignKey(
        Case, related_name="sections", on_delete=models.RESTRICT, blank=True
    )
