from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json

from .serializers import CustomerSerializer
from .models import Customer


@api_view(['POST']) #http method the client =POST
#@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated]) 
def customer_create_view(request,*args,**kwargs):
    request.data['user']=request.user.id
    serializer=CustomerSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        print(request.user)
        serializer.save()
        print(serializer.data)
        return Response(serializer.data,status=201)
    return Response({},status=400)
@api_view(['GET'])
def customer_list_view(request,*args,**kwargs):
    qs=Customer.objects.all()
    serialize=CustomerSerializer(qs,many=True)
    return Response(serialize.data,status=200)

@api_view(['GET'])
def customer_details_view(request,customer_id,*args,**kwargs):
    qs=Customer.objects.filter(id=customer_id)
    if not qs.exists():
        return Response({},status=404)
    obj=qs.first()
    serialize=CustomerSerializer(obj)
    return Response(serialize.data,status=200)

@api_view(['DELETE','POST'])
@permission_classes([IsAuthenticated]) 
def customer_delete_view(request,customer_id,*args,**kwargs):
    qs=Customer.objects.filter(id=customer_id)
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
def customer_update_view(request,customer_id,*args,**kwarg):
    user=request.user.id
    request.data['user']=user
    customer_object=Customer.objects.filter(id=customer_id,user=user)
    if not customer_object.exists():
        return Response({},status=404)
    serializer = CustomerSerializer(customer_object.first(),data=request.data) 
    if serializer.is_valid(): 
        serializer.save() 
        return Response(serializer.data,status=200) 
    return Response(serializer.errors,status=400)
