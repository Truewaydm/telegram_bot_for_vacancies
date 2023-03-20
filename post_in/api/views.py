from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from notes.models import Note
from api.serializers import NoteSerializer, ThinNoteSerializer
from rest_framework.views import APIView
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin)
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet


class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwags):
        notes = Note.objects.all()
        context = {'request': request}
        serializer = ThinNoteSerializer(notes, many=True, context=context)
        return Response(serializer.data)

# class NoteListView(ListCreateAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer
#
#     def list(self, request, *args, **kwags):
#         notes = Note.objects.all()
#         context = {'request': request}
#         serializer = ThinNoteSerializer(notes, many=True, context=context)
#         return Response(serializer.data)
#
#
# class NoteDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer

# class NoteListView(ListModelMixin, CreateModelMixin, GenericAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer
#
#     def get(self, request, *args, **kwargs):
#         self.serializer_class = ThinNoteSerializer
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class NoteDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# class NoteListView(APIView):
#     """
#     List all snippets, or create a new snippet.
#      """
#
#     def get(self, request, format=None):
#         notes = Note.objects.all()
#         context = {'request': request}
#         serializer = ThinNoteSerializer(notes, many=True, context=context)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = NoteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class NoteDetailView(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#
#     def get_object(self, pk):
#         try:
#             return Note.objects.get(pk=pk)
#         except Note.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         note = self.get_object(pk)
#         serializer = NoteSerializer(note)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         note = self.get_object(pk)
#         serializer = NoteSerializer(note, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         note = self.get_object(pk)
#         note.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def notes_list(request, format=None):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         notes = Note.objects.all()
#         serializer = NoteSerializer(notes, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = NoteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def notes_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         note = Note.objects.get(pk=pk)
#     except Note.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = NoteSerializer(note)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = NoteSerializer(note, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         note.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
