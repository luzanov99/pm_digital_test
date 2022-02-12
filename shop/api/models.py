from django.db import models
from treebeard.mp_tree import MP_Node

class Category(MP_Node):
    name=models.CharField(max_length=100)
    discription=models.TextField(blank=True)
    node_order_by = ['name']

    def __str__(self):
        return f"{self.name}"


class Product(MP_Node):
    name = models.CharField(max_length=100)
    discription = models.TextField()
    scope=models.CharField(max_length=100)
    diametr=models.FloatField()
    length=models.IntegerField()
    color=models.CharField(max_length=100)
    picture=models.ImageField(upload_to="media/api")
    node_order_by = ['name']
    card=models.ForeignKey(Category,on_delete=models.CASCADE, blank=True, null=True)


# Create your models here.
