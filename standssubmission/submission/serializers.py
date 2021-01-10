from rest_framework import serializers
from review.models import Decision
from .models import Submission, Project, Theme, DigitalEdition, Contact


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ('theme', )


class ThemeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ('theme', 'description')


class ProjectSerializer(serializers.ModelSerializer):
    theme = ThemeSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ('name', 'description', 'theme', 'website')


class DigitalEditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalEdition
        fields = ('showcase', 'new_this_year', 'stand_website_code', 'stand_website_static')


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


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('name', 'email')


class ContactSubmissionSerializer(serializers.ModelSerializer):
    primary_contact = ContactSerializer(read_only=True)
    secondary_contact = ContactSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ('project', 'primary_contact', 'secondary_contact')


class ContactDecisionSerializer(serializers.ModelSerializer):
    submission = ContactSubmissionSerializer(read_only=True)

    class Meta:
        model = Decision
        fields = ('submission', )
