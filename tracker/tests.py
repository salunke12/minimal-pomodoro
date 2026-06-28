import json
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Task, PomodoroSession

class PomodoroModelTests(TestCase):
    def test_task_creation(self):
        task = Task.objects.create(name="Study Django")
        self.assertEqual(str(task), "Study Django")

    def test_session_creation(self):
        task = Task.objects.create(name="Coding Session")
        session = PomodoroSession.objects.create(
            task=task,
            task_label=task.name,
            session_type="WORK",
            duration_minutes=25,
            completed_successfully=True
        )
        self.assertIn("Coding Session (Work Session) - Completed", str(session))
        self.assertEqual(session.task, task)


class PomodoroViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.task = Task.objects.create(name="Write Code")
        self.timer_page_url = reverse("timer_page")
        self.save_session_url = reverse("save_session")
        self.task_api_url = reverse("task_api")
        self.stats_api_url = reverse("stats_api")

    def test_timer_page(self):
        response = self.client.get(self.timer_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tracker/index.html")

    def test_save_session_post_valid(self):
        payload = {
            "label": "Write Code",
            "type": "WORK",
            "minutes": 25,
            "completed": True
        }
        response = self.client.post(
            self.save_session_url,
            json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "saved")
        self.assertEqual(data["task_label"], "Write Code")
        
        # Verify DB entry
        self.assertEqual(PomodoroSession.objects.count(), 1)
        session = PomodoroSession.objects.first()
        self.assertEqual(session.task_label, "Write Code")
        self.assertEqual(session.session_type, "WORK")
        self.assertTrue(session.completed_successfully)
        self.assertEqual(session.task, self.task)

    def test_save_session_invalid_method(self):
        response = self.client.get(self.save_session_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "POST requests only"})

    def test_task_api_get(self):
        response = self.client.get(self.task_api_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["tasks"]), 1)
        self.assertEqual(data["tasks"][0]["name"], "Write Code")

    def test_task_api_post(self):
        payload = {"name": "Refactoring"}
        response = self.client.post(
            self.task_api_url,
            json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.get(name="Refactoring").name, "Refactoring")

    def test_stats_api(self):
        # Create some sessions
        PomodoroSession.objects.create(
            task=self.task,
            task_label=self.task.name,
            session_type="WORK",
            duration_minutes=25,
            completed_successfully=True
        )
        PomodoroSession.objects.create(
            task=self.task,
            task_label=self.task.name,
            session_type="SHORT_BREAK",
            duration_minutes=5,
            completed_successfully=True
        )
        
        response = self.client.get(self.stats_api_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_focus_minutes"], 25)
        self.assertEqual(data["total_completed_sessions"], 1)
        self.assertEqual(data["task_distribution"]["labels"], ["Write Code"])
        self.assertEqual(data["task_distribution"]["values"], [25])
        self.assertEqual(data["session_breakdown"]["WORK"], 1)
        self.assertEqual(data["session_breakdown"]["SHORT_BREAK"], 1)
