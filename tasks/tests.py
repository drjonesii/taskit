from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Task, Category
from django.urls import reverse

class TaskModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Test Category')
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            category=self.category,
            due_date='2025-01-01T00:00:00Z',
            priority='High',
            completed=False,
            votes=0
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        self.assertEqual(self.task.category.name, 'Test Category')
        self.assertEqual(str(self.task.due_date), '2025-01-01 00:00:00+00:00')
        self.assertEqual(self.task.priority, 'High')
        self.assertFalse(self.task.completed)
        self.assertEqual(self.task.votes, 0)

class TaskViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Test Category')
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            category=self.category,
            due_date='2025-01-01T00:00:00Z',
            priority='High',
            completed=False,
            votes=0
        )

    def test_home_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_list_view(self):
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_add_view(self):
        response = self.client.post('/tasks/add/', {
            'title': 'New Task',
            'description': 'New Description',
            'category': self.category.id,
            'due_date': '2025-01-01T00:00:00Z',
            'priority': 'Medium',
            'completed': False
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 2)

    def test_task_edit_view(self):
        response = self.client.post(f'/tasks/edit/{self.task.id}/', {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'category': self.category.id,
            'due_date': '2025-01-01T00:00:00Z',
            'priority': 'Low',
            'completed': 'on'  # Ensure the completed field is set to True
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.description, 'Updated Description')
        self.assertEqual(self.task.priority, 'Low')
        self.assertTrue(self.task.completed)

    def test_task_delete_view(self):
        response = self.client.post(f'/tasks/delete/{self.task.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)

    def test_vote_task_view(self):
        response = self.client.post(f'/tasks/vote/{self.task.id}/')
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.votes, 1)
