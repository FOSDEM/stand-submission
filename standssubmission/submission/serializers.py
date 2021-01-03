from rest_framework import serializers
from review.models import Decision
from .models import Submission, Project, Theme, DigitalEdition


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ('theme', )


class ProjectSerializer(serializers.ModelSerializer):
    theme = ThemeSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ('name', 'description', 'theme')


class DigitalEditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalEdition
        fields = ('showcase', 'new_this_year')


class SubmissionSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    digital_edition = DigitalEditionSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ('project', 'digital_edition')


class DecisionSerializer(serializers.ModelSerializer):
    submission = SubmissionSerializer(read_only=True)
    
    class Meta:
        model = Decision
        fields = ('submission', )
