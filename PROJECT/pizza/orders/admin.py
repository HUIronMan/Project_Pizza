from django.contrib import admin

from .models import MenuPizza, MenuTopping

# Register your models here.
admin.site.register(MenuPizza)
admin.site.register(MenuTopping)
