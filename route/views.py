from django.shortcuts import render
from rest_framework import generics, status
from .models import Route
from .serializers import routeSerializer, createRouteSerializer, updateRouteSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .mapUtils import *

# Create your views here.

"""
Jun Zhou
2022/4/6
"""
class RounteView(generics.ListAPIView):
    queryset = Route.objects.all()
    serializer_class = routeSerializer


class CreateRouteView(APIView):
    serializer_class = createRouteSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            code = serializer.data.get('code')
            addrs = serializer.data.get('addrs')
            geo_codes = get_geocodes_from_addrs(addrs)
            res = get_map_url_distance(geo_codes)

            route = Route.objects.create(
                code=code, geo_codes=geo_codes, addrs=addrs, image_url=res[0], total_dist = res[1], total_time = res[2])
            
            return Response(routeSerializer(route).data, status=status.HTTP_200_OK)

class UpdateRouteView(APIView):
    serializer_class = updateRouteSerializer

    def patch(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id = serializer.data.get('id')
            code = serializer.data.get('code')
            addrs = serializer.data.get('addrs')
            geo_codes = get_geocodes_from_addrs(addrs)

            queryset = Route.objects.filter(id = id)
            if not queryset.exists():
                return Response({'msg': 'Route not found'}, status=status.HTTP_404_NOT_FOUND)
            route = queryset[0]

            res = get_map_url_distance(geo_codes)

            route.code = code
            route.geo_codes = geo_codes
            route.addrs = addrs
            route.total_dist = res[1]
            route.image_url = res[0]
            route.total_time = res[2]
            route.save()
            
            return Response(routeSerializer(route).data, status=status.HTTP_200_OK)

