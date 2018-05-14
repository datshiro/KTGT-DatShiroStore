import json

from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import model_to_dict


@receiver(user_logged_in, sender=User)
def update_session(request, user, **kwargs):
    # print("Save session")
    # data = serializers.serialize("json", [user])
    # # data = model_to_dict(User, exclude=['groups'])
    # print(data)
    request.session['user_id'] = user.id
    request.session['username'] = user.get_full_name()