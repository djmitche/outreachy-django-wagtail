# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-01-19 18:23
from __future__ import unicode_literals

from django.db import migrations
import datetime

# For the Dec 2018 to Mar 2018 round:
# Internship starts: Dec 4
# Initial feedback due: Dec 19 (2 weeks + 1 day from start of internship)
# Midpoint feedback due: Jan 30 (8 weeks + 1 day from start of internship)
# So if the initial feedback is delayed because an intern started late,
# we add 6 weeks to the initial feedback due date to get the mid-point feedback due date
def update_intern_selections(apps, schema_editor):
    InternSelection = apps.get_model('home.InternSelection')
    interns = InternSelection.objects.all()
    for i in interns:
        round_initial_feedback = i.project.project_round.participating_round.initialfeedback
        custom_initial_feedback = i.initial_feedback_due

        if round_initial_feedback == custom_initial_feedback:
            i.midpoint_feedback_due = i.project.project_round.participating_round.midfeedback
        else:
            i.midpoint_feedback_due = i.initial_feedback_due + datetime.timedelta(days=7*6)
        i.midpoint_feedback_opens = i.midpoint_feedback_due - datetime.timedelta(days=7)
        i.save()

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0136_auto_20190119_1822'),
    ]

    operations = [
        migrations.RunPython(update_intern_selections, reverse_code=migrations.RunPython.noop),
    ]