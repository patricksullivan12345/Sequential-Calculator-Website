from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from users.models import Profile

def createProfile(sender, instance, created, **kwargs):
    print('Create profile signal triggered')
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.first_name,
            email=user.email,
            name=user.first_name,
        )

def updateUser(sender, instance, created, **kwargs):
    print('Update profile signal triggered')
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

def deleteUser(sender, instance, **kwargs):
    print('Delete profile signal triggered')
    try:
        user = instance.user
        user.delete()
    except:
        pass

post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)