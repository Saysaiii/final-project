from django.test import TestCase
from .models import Project

class ProjectModelTest(TestCase):
    def test_str_method(self):
        project = Project(title="Test", description="A test project")
        self.assertEqual(str(project), "Test")
