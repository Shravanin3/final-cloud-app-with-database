import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from onlinecourse.models import Course, Lesson, Question, Choice, Instructor, Learner, Enrollment
from django.utils.timezone import now

# 1. Superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin12345')
    print("Created superuser admin")

# 2. Regular test user
user, created = User.objects.get_or_create(
    username='shravani',
    defaults={'first_name': 'Shravani', 'last_name': 'N', 'email': 'shravani@example.com'}
)
if created:
    user.set_password('pass12345')
    user.save()
    print("Created user shravani")

# 3. Instructor
instructor_user, _ = User.objects.get_or_create(
    username='instructor1',
    defaults={'first_name': 'Yan', 'last_name': 'Luo', 'email': 'yan@example.com'}
)
if not instructor_user.has_usable_password():
    instructor_user.set_password('pass12345')
    instructor_user.save()

instructor, _ = Instructor.objects.get_or_create(
    user=instructor_user,
    defaults={'full_time': True, 'total_learners': 1500}
)

# 4. Course
course, _ = Course.objects.get_or_create(
    name='Cloud Application Development with Django',
    defaults={
        'description': 'Learn full-stack web application development using Django, SQLite, and cloud deployment.',
        'pub_date': now().date(),
        'total_enrollment': 1
    }
)
course.instructors.add(instructor)

# 5. Lessons
lesson1, _ = Lesson.objects.get_or_create(
    title='Introduction to Cloud Applications and Django Architecture',
    course=course,
    defaults={
        'order': 0,
        'content': 'Django is an open-source web application framework written in Python that follows the model-template-views (MTV) architectural pattern.'
    }
)

lesson2, _ = Lesson.objects.get_or_create(
    title='Django Models, ORM and Database Migrations',
    course=course,
    defaults={
        'order': 1,
        'content': 'Django provides an Object-Relational Mapper (ORM) that enables Python developers to interact with relational databases seamlessly.'
    }
)

# 6. Questions & Choices
q1, _ = Question.objects.get_or_create(
    course=course,
    question_text='Which Python file is primarily used to define database models in a Django application?',
    defaults={
        'lesson': lesson2,
        'grade': 50
    }
)
Choice.objects.get_or_create(question=q1, choice_text='models.py', defaults={'is_correct': True})
Choice.objects.get_or_create(question=q1, choice_text='views.py', defaults={'is_correct': False})
Choice.objects.get_or_create(question=q1, choice_text='urls.py', defaults={'is_correct': False})
Choice.objects.get_or_create(question=q1, choice_text='settings.py', defaults={'is_correct': False})

q2, _ = Question.objects.get_or_create(
    course=course,
    question_text='Which Django CLI management command executes SQL statements to apply database migrations?',
    defaults={
        'lesson': lesson2,
        'grade': 50
    }
)
Choice.objects.get_or_create(question=q2, choice_text='python manage.py migrate', defaults={'is_correct': True})
Choice.objects.get_or_create(question=q2, choice_text='python manage.py makemigrations', defaults={'is_correct': False})
Choice.objects.get_or_create(question=q2, choice_text='python manage.py runserver', defaults={'is_correct': False})
Choice.objects.get_or_create(question=q2, choice_text='python manage.py createsuperuser', defaults={'is_correct': False})

# 7. Enrollment for shravani
Enrollment.objects.get_or_create(
    user=user,
    course=course,
    defaults={'mode': 'honor', 'rating': 5.0}
)

print("Database seeded successfully!")
