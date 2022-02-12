from unicodedata import name
from django.shortcuts import get_object_or_404, render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serialisers import CategorySerializer, ProductSerializer
from .models import Product, Category
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
'''Список продуктов по определнной карточке'''
class  ProductViewSet(ModelViewSet):
    def list(self, request):
        card_name=request.GET.get("card", "")
        card=Category.objects.filter(depth=4).filter(name=card_name)
        try:
            card=card.values()[0]
        except IndexError:
            return Response('No card', status=status.HTTP_404_NOT_FOUND)
        products=Product.objects.filter(card__name=card['name'])
        result={
            'products':[]
        }
        for product in products:
            result['products'].append(product.name)
        return Response(result, status=status.HTTP_200_OK)
        


'''Список категорий'''
class CategoryViewSet(ModelViewSet):
    queryset= Category.objects.filter(depth=1)
    serializer_class = CategorySerializer
    
    

''' Список всех карточек товаров категории (секции, группы, подгруппы) '''
class SubCategoryViewSet(ModelViewSet):
    
    def list(self, request):
        category_name=request.GET.get("category", "")   
        result={'cards':[]}
        #category=Category.objects.filter(name=category_name)
        categorys=get_object_or_404(Category,name=category_name)
        categorys=categorys.get_descendants()
        for category in categorys:
            if category.get_depth()==4:
                result['cards'].append(category.name)

        return Response(result, status=status.HTTP_200_OK)


    
'''Детальная информация о карточке по ее названию'''
class DetailCardViewSet(ModelViewSet):
    
    def list(self, request):
    
        card_name=request.GET.get("card", "")
        card=Category.objects.filter(depth=4).filter(name=card_name)
      
        result={
            'card_name':[],
            'scopes': [],
            'diametrs':[],
            'lengths':[],
            'colors':[],
            'images':[],
            'main_image':[],
        }
        print(card)
        try:
            card=card.values()[0]
        except IndexError:
            return Response('No card', status=status.HTTP_404_NOT_FOUND)
        result['card_name'].append(card['name'])
        products=Product.objects.filter(card__name=card['name'])
        for product in products:
            if product.scope not in  result['scopes']:
                result['scopes'].append(product.scope)
            
            if product.diametr not in  result['diametrs']:
                result['diametrs'].append(product.diametr)
            
            if product.length not in  result['lengths']:
                result['lengths'].append(product.length)
            
            if product.color not in  result['colors']:
                result['colors'].append(product.color)

            if product.picture.url not in  result['images']:
                result['images'].append(product.picture.url)

        result['main_image'].append(products[0].picture.url)   
        return Response(result, status=status.HTTP_200_OK)


        
       

