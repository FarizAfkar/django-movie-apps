import os
import time
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from datetime import date
from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

def path_and_rename(instance, filename):
    upload_to = date.today().strftime('poster/%Y/%m/%d/')
    name = os.path.splitext(os.path.basename(filename))[0]
    ext = os.path.splitext(filename)[1]
    timestamp = int(time.time())
    filename = f'{name}-{timestamp}{ext}'
    return os.path.join(upload_to, filename)

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    try:
        if not User.objects.filter(is_superuser=True).exists():
            # Create a superuser if one doesn't exist
            User.objects.create_superuser(
                username=os.getenv('SUPER_USER'),
                email=os.getenv('SUPER_EMAIL'),
                password=os.getenv('SUPER_PASS'),
                is_staff=True
            )
            print("Superuser created successfully.")
        else:
            print("Superuser already exists.")
    except Exception as e:
        print(f"Error creating superuser: {e}")

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Genre(models.Model):
    """Model for storing genre details."""
    name = models.CharField(max_length=100)  # e.g. 'Action', 'Comedy', 'Drama'

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'genre'


class MPAA_Rating(models.Model):
    """Model to store MPAA ratings."""
    type_mpaa = models.CharField(max_length=10)  # e.g. 'PG', 'M18', 'R21'
    label = models.CharField(max_length=100, null=True, blank=True)  # Description for the rating (e.g. "Some Violence")

    def __str__(self):
        return f'{self.type_mpaa}: {self.label}'

    class Meta:
        managed = True
        db_table = 'mpaa_rating'


class Movie(models.Model):
    """Model for storing movie details."""
    name = models.CharField(max_length=255)  # Name of the movie
    description = models.TextField()  # Description of the movie
    imgPath = models.ImageField(upload_to=path_and_rename)  # Path to the image file
    duration = models.IntegerField()  # Duration in minutes
    language = models.CharField(max_length=100)  # Language of the movie
    userRating = models.DecimalField(max_digits=2, decimal_places=1)  # User Rating (e.g. 4.0)
    mpaaRating = models.ForeignKey(MPAA_Rating, models.DO_NOTHING)  # Foreign key to MPAA Rating

    class Meta:
        managed = True
        db_table = 'movie'

class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, models.DO_NOTHING)
    genre = models.ForeignKey(Genre, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'movie_genre'
        unique_together = (('movie', 'genre'),)
