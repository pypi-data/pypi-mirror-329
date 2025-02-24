from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.authentication import get_authorization_header
from rest_framework.views import exception_handler
from rest_framework import pagination
from rest_framework.permissions import BasePermission
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed


class BasePermission(BasePermission):
    pass


class Response(Response):
    pass


class JSONRenderer(JSONRenderer):
    pass


class MultiPartParser(MultiPartParser):
    pass


class NotFound(NotFound):
    pass


class ListAPIView(ListAPIView):
    pass


class APIView(APIView):
    pass


class ModelSerializer(ModelSerializer):
    pass


class Serializer(Serializer):
    pass


class Request(Request):
    pass


class AuthenticationFailed(AuthenticationFailed):
    pass


status = status
serializers = serializers
get_authorization_header = get_authorization_header
exception_handler = exception_handler
pagination = pagination
