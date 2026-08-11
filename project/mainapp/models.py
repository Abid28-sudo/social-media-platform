from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    text = models.TextField(blank = True)
    image = models.ImageField(upload_to ='post_image/', blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} : {self.text[:30]}'    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE)        
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} on {self.post.id}: {self.text[:30]}'

class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')        
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        unique_together = ('post','user')

class Follow(models.Model):
    follower = models.ForeignKey(User,related_name='following',on_delete= models.CASCADE)
    following = models.ForeignKey(User,related_name='followers',on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        unique_together = ('follower' , 'following')