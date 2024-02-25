from django.db import models
from django.shortcuts import render

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)

class Product(models.Model):
    title = models.CharField(max_length=200)
    keywords = models.TextField()

    def __str__(self):
        return self.title
def search(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query)
    products = Product.objects.filter(Q(title__icontains=query) | Q(keywords__icontains=query))

    context = {
        'users': users,
        'products': products,
        'query': query,
    }

    return render(request, 'search_results.html', context)