from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from quote.models import Quote, Category
from django.shortcuts import get_object_or_404
from api.serializers import QuoteSerializer
from DiscordBot import quote_perser

class QuoteListAPIView(APIView, IsAuthenticated):
    serializer_class = QuoteSerializer
    model = Quote
    def get(self, request):
        queryset = Quote.objects.select_related('category')
        # queryset = Quote.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class GetQuoteAPIView(APIView, IsAuthenticated):
    serializer_class = QuoteSerializer
    model = Quote
    def get(self, request, author, category):
        print('getting')
        category_obj = Category.objects.filter(name=category).first()
        if category_obj is None:
            category_obj = Category.objects.create(name=category.capitalize())
        queryset = Quote.objects.filter(author__icontains=author, category=category_obj)
        if len(queryset) == 0:
            quote = quote_perser.get_quote_by_author_and_category(author, category_obj.name)
            print(quote)
            if "Sorry, I couldn't find" not in quote['quote']:
                quote = Quote.objects.create(author=quote['author'].title(), quote=quote['quote'], category=category_obj)
                queryset = Quote.objects.filter(author__icontains=author, category=category_obj)
            else:
                print(Response({'quote': 'Sorry, I couldn\'t find any quotes by this author.', 'author':'Najrubindro'}))
                return Response({'quote': 'Sorry, I couldn\'t find any quotes by this author.', 'author':'Najrubindro'})


        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class GetQuoteBYAuthor(APIView, IsAuthenticated):
    serializer_class = QuoteSerializer
    model = Quote
    def get(self, request, author):
        print('getting')
        queryset = Quote.objects.filter(author__icontains=author)
        print(queryset, 'queryset')
        if len(queryset) == 0:
            quote = quote_perser.get_quote_by_author(author)
            print(quote, 'qutoe ----')
            if "Sorry, I couldn't find" not in quote['quote']:
                quote = Quote.objects.create(author=quote['author'], quote=quote['quote'])
                queryset = Quote.objects.filter(author__icontains=author)
            else:
                print('in else')
                return Response({'quote': 'Sorry, I couldn\'t find any quotes by this author.', 'author':'Najrubindro'})



        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class GetQuoteByCategory(APIView, IsAuthenticated):
    serializer_class = QuoteSerializer
    model = Quote
    def get(self, request, category):
        print('getting')
        queryset = Quote.objects.select_related('category').filter(category__name=category)
        print(queryset, 'queryset')
        if len(queryset) == 0:
            return Response({'quote': 'Sorry, I couldn\'t find any quotes by this author.', 'author':'Najrubindro'})


        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
