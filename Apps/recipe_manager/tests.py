from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Recipe


class RecipeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser1', password='12345')
        self.user = User.objects.create_user(username='testuser2', password='12345')
        Recipe.objects.create(name="kombucha", owner=self.user)
        Recipe.objects.create(name="sourdough", owner=self.user)

    def test_name_correctly_set(self):
        kombucha = Recipe.objects.get(name="kombucha")
        sourdough = Recipe.objects.get(name="sourdough")
        self.assertEqual(kombucha.name, 'kombucha')
        self.assertEqual(sourdough.name, 'sourdough')

    def test_work_duration_calculated_correctly(self):
        delta = timedelta(minutes=30)
        kombucha = Recipe.objects.get(name="kombucha")
        kombucha.create_process(name="process 1", work_duration=delta)
        kombucha.create_process(name="process 2", work_duration=delta)
        self.assertEqual(kombucha.get_total_work_duration(), delta * 2)

    def test_wait_duration_calculated_correctly(self):
        delta = timedelta(minutes=30)
        kombucha = Recipe.objects.get(name="kombucha")
        kombucha.create_process(name="process 1", wait_duration=delta)
        kombucha.create_process(name="process 2", wait_duration=delta)
        self.assertEqual(kombucha.get_total_wait_duration(), delta * 2)

    def test_processes_added(self):
        kombucha = Recipe.objects.get(name="kombucha")
        process_count = len(kombucha.get_processes())
        kombucha.create_process(name="process 1")
        kombucha.create_process(name="process 2")
        self.assertEqual(len(kombucha.get_processes()), process_count + 2)

    def test_processes_ingredients_added(self):
        kombucha = Recipe.objects.get(name="kombucha")
        p = kombucha.create_process(name="process 1")
        count = len(p.get_ingredients())
        p.create_recipe_ingredient(name="ingredient 1", amount=5, unit="ml")
        self.assertEqual(len(p.get_ingredients()), count + 1)

    def test_processes_schedule_added(self):
        kombucha = Recipe.objects.get(name="kombucha")
        p = kombucha.create_process(name="process 1")
        count = len(p.get_process_schedule())
        p.create_schedule(executed_once=False)
        self.assertEqual(len(p.get_process_schedule()), count + 1)

    def test_processes_process_step_added(self):
        kombucha = Recipe.objects.get(name="kombucha")
        p = kombucha.create_process(name="process 1")
        count = len(p.get_process_steps())
        p.create_process_step(text="process step 1", index=0)
        self.assertEqual(len(p.get_process_steps()), count + 1)

    def test_processes_utensil_added(self):
        kombucha = Recipe.objects.get(name="kombucha")
        p = kombucha.create_process(name="process 1")
        count = len(p.get_utensils())
        p.create_utensil(name="utensil 1")
        self.assertEqual(len(p.get_utensils()), count + 1)
