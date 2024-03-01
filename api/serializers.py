from rest_framework import serializers
from quote.models import Quote

class QuoteSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    class Meta:
        model = Quote
        fields = ['id', 'author', 'quote', 'category']

