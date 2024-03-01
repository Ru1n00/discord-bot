from django.urls import path
from api.views import QuoteListAPIView, GetQuoteAPIView, GetQuoteBYAuthor

urlpatterns = [
    path('', QuoteListAPIView.as_view()),
    path('author/<str:author>', GetQuoteBYAuthor.as_view()),
    path('author/<str:author>/category/<str:category>', GetQuoteAPIView.as_view()),
]
