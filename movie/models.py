from django.db import models
from accounts.models import User

class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=300)
    movie_id=models.IntegerField()
    description=models.TextField()
    release_date=models.DateTimeField(blank=True,null=True)
    movie_type=models.CharField(max_length=300,default=None)
    genre=models.CharField(max_length=300,blank=True,null=True)
    poster=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} - {self.movie.title}"