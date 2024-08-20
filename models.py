from django.db import models
from django.contrib.auth.models import User

# Модель Author
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = sum(post.rating * 3 for post in self.post_set.all())
        comments_rating = sum(comment.rating for post in self.post_set.all() for comment in post.comment_set.all())
        author_comments_rating = sum(comment.rating for comment in Comment.objects.filter(user=self.user))
        self.rating = posts_rating + comments_rating + author_comments_rating
        self.save()

# Модель Category
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

# Модель Post
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    POST_TYPE_CHOICES = [
        ('article', 'Article'),
        ('news', 'News')
    ]
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...' if len(self.text) > 124 else self.text

# Модель PostCategory
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

# Модель Comment
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()