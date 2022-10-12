from django.db import models


class Order(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    owner = models.ForeignKey(
        'auth.User', related_name='orders', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('created',)
        
    def __str__(self):
        return self.title
    