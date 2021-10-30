from django.db               import models

class BulletinBoard(models.Model):
    author      = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='bulletin_board')
    title       = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
        
    class Meta:
        db_table = 'bulletin_boards'
