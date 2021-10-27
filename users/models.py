from django.db               import models

class User(models.Model):
    name       = models.CharField(max_length = 20)
    password    = models.CharField(max_length = 200)
    email      = models.EmailField(max_length = 50, unique = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
        
    class Meta:
        db_table = 'users'