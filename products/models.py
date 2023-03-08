from django.db import models


class Hashtag(models.Model):
    title = models.CharField(max_length=55)

    def __str__(self):
        return self.title


class Products(models.Model):
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=155)
    price = models.FloatField()
    description = models.TextField()
    rate = models.FloatField(default=0.0)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.CharField(max_length=355)
    product = models.ForeignKey(Products, on_delete=models.CASCADE,
                             related_name="Reviews")
    created_date = models.DateField(auto_now_add=True)