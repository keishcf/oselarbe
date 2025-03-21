# Generated by Django 5.0.4 on 2024-04-27 11:28

from django.db import migrations
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import get_user_model as User
from django.contrib.contenttypes.models import ContentType
import accounts.models as accounts_models
import business.models as business_models


def create_permissions_and_groups(app, schema_editor):
    # Create Groups
    business_group, created = Group.objects.get_or_create(name="business")
    personal_group, created = Group.objects.get_or_create(name="personal")

    # Define Permissions
    can_review_business = Permission.objects.create(
        codename="can_review_business",
        name="Can review business",
        content_type=ContentType.objects.get_for_model(business_models.BusinessReview),
    )
    can_ask_question = Permission.objects.create(
        codename="can_ask_question",
        name="Can ask question",
        content_type=ContentType.objects.get_for_model(business_models.BusinessQuestions),
    )
    can_answer_question = Permission.objects.create(
        codename="can_answer_question",
        name="Can answer question",
        content_type=ContentType.objects.get_for_model(business_models.BusinessAnswer),
    )
    can_thumbsup_review = Permission.objects.create(
        codename="can_thumbsup_review",
        name="Can thumbsup review",
        content_type=ContentType.objects.get_for_model(business_models.ReviewThumbsUp),
    )
    can_reply_review = Permission.objects.create(
        codename="can_reply_review",
        name="Can reply review",
        content_type=ContentType.objects.get_for_model(business_models.ReplyReview),
    )
    can_create_edit_short_message = Permission.objects.create(
        codename="can_create_short_message",
        name="Can create short message",
        content_type=ContentType.objects.get_for_model(business_models.BusinessShortMessage),
    )
    

    business_group.permissions.add(
        can_create_edit_short_message, can_reply_review, can_answer_question
    )
    personal_group.permissions.add(can_ask_question, can_review_business, can_thumbsup_review)


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_permissions_and_groups),
    ]
