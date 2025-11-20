#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemical_equipment.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='agamarora').exists():
    User.objects.create_superuser('agamarora', 'agam@example.com', '12345678')
    print("User 'agamarora' created successfully!")
else:
    print("User 'agamarora' already exists.")
