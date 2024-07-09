from django.contrib import admin
from .models import Category,Product,Adresse,User,Subcategory

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=('username','password','telephone')
admin.site.register(User,UserAdmin)
#
class ProductAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'stock', 'categorie', 'sous_categorie', 'utilisateur')
    list_filter = ('categorie', 'utilisateur')
    search_fields = ('nom', 'description')

    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'description', 'photo')
        }),
        ('Détails du produit', {
            'fields': ('prix', 'stock', 'categorie', 'sous_categorie', 'utilisateur')
        }),
    )
admin.site.register(Product, ProductAdmin)


#
class AdresseAdmin(admin.ModelAdmin):
    list_display=('ville','quartier','repere','contact','utilisateur')
admin.site.register(Adresse,AdresseAdmin)
#

class SubcategoryInline(admin.TabularInline):  # Vous pouvez utiliser StackedInline pour un affichage différent
    model = Subcategory
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
    inlines = [SubcategoryInline]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory)  # Si vous souhaitez également une entrée distincte pour les sous-catégories