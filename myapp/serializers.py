from rest_framework import serializers
from .models import MyModel  # 假设你有一个名为 MyModel 的模型

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'  # 或者指定具体的字段