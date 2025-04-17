from django.shortcuts import render
from store.models import Product, Customer
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q # For complex queries for OR operations



def say_hello(request):
    # product = Product.objects.filter(pk=0).first() # This will return None if no product is found
    # count = Product.objects.count()
    # query_set = Product.objects.filter(unit_price__gt=20) # Here __gt is a lookup filter that filters the products with unit_price greater than 20
    # query_set = Product.objects.filter(unit_price__range=(20, 30)) # Here __range is a lookup filter that filters the products with unit_price between 20 and 30
    # query_set = Product.objects.filter(title__icontains='coffee') # Here __icontains is a lookup filter that filters the products with title containing 'coffee'
    # query_set = Customer.objects.filter(email__icontains='.com') # Here __icontains is a lookup filter that filters the products with title containing 'coffee'
    # query_set = Customer.objects.filter(email__icontains='.com') # Here __icontains is a lookup filter that filters the products with title containing 'coffee'
    query_set = Product.objects.filter(Q(unit_price__gt=20) | ~Q(collection_id=1)) # Here Q is used to perform OR operations in the query
    # try:
    #     product = Product.objects.get(pk=1)
    
    # except ObjectDoesNotExist:
    #     pass


    # for product in query_set:
    #     print(product)
    return render(request, 'hello.html', {'name': 'Mosh', 'products': list(query_set)})
