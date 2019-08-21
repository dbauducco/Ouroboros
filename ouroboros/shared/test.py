import datetime
import os
import shutil
from unittest import mock

from django import test
from django.test import override_settings
from django.core import files
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template.loader import render_to_string
from django.utils import html, timezone

from hacker import models as hacker_models

TEST_RESUME_DIR = "test_resume_dir"

@override_settings(MEDIA_ROOT=TEST_RESUME_DIR)
class SharedTestCase(test.TestCase):
    def setUp(self):
        self.email = "dummy@tamu.edu"
        self.password = "dummypwd"
        self.first_name = "Kennedy"
        self.last_name = "Doe"

        self.hacker = hacker_models.Hacker(
            email=self.email,
            password=self.password,
            is_active=True,
        )
        self.hacker.set_password(self.password)
        self.hacker.save()

        self.email2 = "dummy2@tamu.edu"
        self.password2 = "bigdummypwd"
        self.first_name2 = "John"
        self.last_name2 = "Doe"

        self.hacker2 = hacker_models.Hacker.objects.create_superuser(
            email=self.email2,
            password=self.password2,
        )

        self.resume = SimpleUploadedFile("resume.pdf", b"dummy")
        self.resume_file_data = {"resume": self.resume}

        self.application_fields = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "major": "Computer Science",
            "gender": "M",
            "classification": "Fr",
            "grad_year": "Other",
            "num_hackathons_attended": 0,
            "hacker": self.hacker,
            "race": ["NA"],
            "extra_links": "A",
            "programming_joke": "B",
            "unlimited_resource": "C",
            "cool_prize": "D",
            "adult": True,
            "previous_attendant": False,
            "additional_accommodations": "E",
            "mlh_coc": True,
            **self.resume_file_data,
        }

        self.updated_application_fields = dict(**self.application_fields)
        self.updated_application_fields["major"] = "Accounting"
        self.resume2 = SimpleUploadedFile("resume2.pdf", b"dummy2")
        self.updated_application_fields["resume"] = self.resume2

    def create_active_wave(self):
        start = timezone.now() - timezone.timedelta(days=1)
        end = start + timezone.timedelta(days=30)

        self.wave1 = hacker_models.Wave(start=start, end=end)
        self.wave1.save()

    def assertEmailBodiesEqual(self, template_name, context, email):
        html_output = render_to_string(template_name, context)
        stripped = html.strip_tags(html_output)
        self.assertEqual(email.body, stripped)

    def tearDown(self):
        shutil.rmtree(TEST_RESUME_DIR, ignore_errors=True)
