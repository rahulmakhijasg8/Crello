from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from.models import Columns,Workspace,Cards
from .serializers import ColumnSerializer,WorkspaceSerializer,CardSerializer
from rest_framework.response import Response
from rest_framework import status

class ColumnViewset(ModelViewSet):
    serializer_class = ColumnSerializer
    # queryset = Columns.objects.filter(id=self.kwargs['workspace_pk'].select_related('workspace').all()

    def get_serializer_context(self):
        #   print(self.kwargs['workspace_pk'])
          return {'id':self.kwargs['workspace_pk']}

    def get_queryset(self):
        queryset = Columns.objects.select_related('workspace').filter(workspace=self.kwargs['workspace_pk']).all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['workspace'] = Workspace.objects.filter(id=self.kwargs['workspace_pk'])[0]
        # print(serializer.validated_data['workspace'])
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
class WorkspaceViewset(ModelViewSet):
    serializer_class = WorkspaceSerializer
    
    def get_queryset(self):
        # print(self.request.user)
        queryset = Workspace.objects.filter(creator=self.request.user)
        return queryset
    
    def create(self, request, *args, **kwargs):
        # print(request.data)
        # request.data['creator'] = request.user
        # print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['creator'] = request.user
        # print(serializer.validated_data['creator'])
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['members'] = instance.members + ',' + serializer.validated_data['members']
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    

class CardViewset(ModelViewSet):
    serializer_class = CardSerializer
    queryset = Cards.objects.all()

    def get_serializer_context(self):
        #   print(self.kwargs['workspace_pk'])
          queryset = Columns.objects.filter(workspace = self.kwargs['workspace_pk']).values_list('id', flat=True)
          return {'queryset':queryset,'request':self.request.method}