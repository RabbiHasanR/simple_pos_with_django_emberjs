from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json

from .serializers import ProductSerializer
from .models import Product


@api_view(['POST']) 
@permission_classes([IsAuthenticated]) 
def product_create_view(request,*args,**kwargs):
    request.data['user']=request.user.id
    serializer=ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        print(request.user)
        serializer.save()
        print(serializer.data)
        return Response(serializer.data,status=201)
    return Response({},status=400)
@api_view(['GET'])
def product_list_view(request,*args,**kwargs):
    qs=Product.objects.all()
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
@permission_classes([IsAuthenticated]) 
def product_delete_view(request,product_id,*args,**kwargs):
    qs=Product.objects.filter(id=product_id)
    if not qs.exists():
        return Response({},status=404)
    qs=qs.filter(user=request.user)
    if not qs.exists():
        return Response({'message':'You can not delete this!'},status=401)
    obj=qs.first()
    obj.delete()
    return Response({'message':'Tweet removed!'},status=200)

@api_view(['PUT'])
@permission_classes([IsAuthenticated]) 
def product_update_view(request,product_id,*args,**kwarg):
    user=request.user.id
    request.data['user']=user
    product_object=Product.objects.filter(id=product_id,user=user)
    if not product_object.exists():
        return Response({},status=404)
    serializer = ProductSerializer(product_object.first(),data=request.data) 
    if serializer.is_valid(): 
        serializer.save() 
        return Response(serializer.data,status=200) 
    return Response(serializer.errors,status=400)
