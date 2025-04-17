from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Car
from .serializers import CarSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ViewSet, ModelViewSet, GenericViewSet

class firstViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

# class first(ListCreateAPIView):
#     queryset = Car.objects.all()
#     serializer_class = CarSerializer


    # def get(self, request):
    #     cars = Car.objects.all()
    #     serializer = CarSerializer(cars, many=True)
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = CarSerializer(data=request.data) # This will deserialize the data
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     # print(serializer.validated_data) # This will print the deserialized validated data
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)        
    
# class first_details(RetrieveUpdateDestroyAPIView):
#     queryset = Car.objects.all()
#     serializer_class = CarSerializer
    # lookup_field = 'id'
        # self.car = car # This will assign the car object to the class variable
    # def get(self, request, id):
    #     car = get_object_or_404(Car, pk=id)
    #     serializer = CarSerializer(car) # This will serialize the product object
    #     return Response(serializer.data)
    
    # def post(self, request, id):
    #     car = get_object_or_404(Car, pk=id)
    #     serializer = CarSerializer(car,data=request.data) # This will deserialize the data
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     # print(serializer.validated_data) # This will print the deserialized validated data
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def put(self, request, id):
    #     car = get_object_or_404(Car, pk=id)
    #     serializer = CarSerializer(car, data=request.data) # This will deserialize the data
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)

    # def delete(self, request, id):
    #     car = get_object_or_404(Car, pk=id)
    #     car.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)




# Create your views here.
# @api_view(['GET', 'POST'])
# def first(request):
#     if request.method == 'GET':
#         cars = Car.objects.all()
#         serializer = CarSerializer(cars, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CarSerializer(data=request.data) # This will deserialize the data
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # print(serializer.validated_data) # This will print the deserialized validated data
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# def first_details(request, id):
#     car = get_object_or_404(Car, pk=id)
#     if request.method == 'GET':
#         serializer = CarSerializer(car) # This will serialize the product object
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CarSerializer(car, data=request.data) # This will deserialize the data
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # print(serializer.validated_data) # This will print the deserialized validated data
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     elif request.method == 'PUT':
#         serializer = CarSerializer(car, data=request.data) # This will deserialize the data
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         car.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    