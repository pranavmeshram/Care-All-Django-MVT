from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.contrib.auth import get_user_model
from accounts.models import User
from care_all.models import Elder, Youngster

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
    # print("***********GETTING HERE********************")
    # print(sender)
    # print(instance)
    # print(instance.role)
    # print(created)
    # print(created)
    if created:
        print("***********GETTING INSIDE CREATED BLOCK********************")
        if instance.role == 'Elder':
            print("User is an Elder")
            print(instance)
            print(instance.username)
            Elder.objects.create(user=instance)
        else:
            print("user is youngster")
            print(instance)
            Youngster.objects.create(user=instance)

