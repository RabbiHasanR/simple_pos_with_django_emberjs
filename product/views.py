from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Product
from .serializers import ProductSerializer

@api_view(['POST']) #http method the client =POST
def product_create_view(request,*args,**kwargs):
    serializer=ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data,status=201)
    return Response({},status=400)


@api_view(['GET'])
def product_list_view(request,*args,**kwargs):
    qs=Product.objects.all()
    # username=request.GET.get('username') # ?username=rabbi
    # if username!=None:
    #     qs=qs.filter(user__username__iexact=username)
    serialize=ProductSerializer(qs,many=True)
    return Response(serialize.data,status=200)


@api_view(['GET'])
def product_details_view(request,product_id,*args,**kwargs):
    qs=Product.objects.filter(id=product_id)
    if not qs.exists():
        return Response({},status=404)
    obj=qs.first()
    serialize=ProductSerializer(obj)
    return Response(serialize.data,status=200)

@api_view(['DELETE','POST'])
def product_delete_view(request,product_id,*args,**kwargs):
    qs=Product.objects.filter(id=product_id)
    if not qs.exists():
        return Response({},status=404)
    # qs=qs.filter(user=request.user)
    # if not qs.exists():
    #     return Response({'message':'You can not delete this!'},status=401)
    obj=qs.first()
    obj.delete()
    return Response({'message':'Product removed!'},status=200)
