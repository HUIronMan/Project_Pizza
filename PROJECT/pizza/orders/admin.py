from django.contrib import admin

from .models import MenuPizza, MenuTopping, MenuSize

# Register your models here.
admin.site.register(MenuPizza)
admin.site.register(MenuSize)
admin.site.register(MenuTopping)
