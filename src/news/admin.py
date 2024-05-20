from django.contrib import admin

# Register your models here.


from .models import newsBit

@admin.register(newsBit)
class newsBitAdmin(admin.ModelAdmin):
    list_display = ("category", "title", "publication_date")