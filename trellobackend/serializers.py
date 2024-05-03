from rest_framework import serializers
from .models import Columns,Workspace,Cards


class ColumnSerializer(serializers.ModelSerializer):
    wpk = None
    class Meta:
        model = Columns
        fields = ['id','name','workspace']

    # workspace = serializers.PrimaryKeyRelatedField(queryset=Workspace.objects.filter(id=1))

    def get_fields(self):
        fields = super().get_fields()
        pk = self.context.get('id')

        fields['workspace'] = serializers.PrimaryKeyRelatedField(queryset=Workspace.objects.filter(id=pk))

        return fields

    def create(self, validated_data):
        # print(self.context.get('id'))
        return super().create(validated_data)
    
    


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['name','members']

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = ['title','description','column']

    def create(self, validated_data):
        # print(self.context['request'])
        return super().create(validated_data)
    
    def get_fields(self):
        fields = super().get_fields()
        columns = self.context.get('queryset')

        if self.context.get('request') == 'POST':
            fields['column'] = serializers.StringRelatedField()
        fields['column'] = serializers.PrimaryKeyRelatedField(queryset = Columns.objects.filter(id__in=columns))

        return fields