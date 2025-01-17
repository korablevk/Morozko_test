from django.contrib import admin

from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    ordering = ('name',)

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('name',),
        }


class ProductImageInline(admin.TabularInline):
    """
    Inline отображение изображений для продукта.
    """
    model = ProductImage
    extra = 1  # Количество дополнительных пустых полей для загрузки
    fields = ('image',)
    readonly_fields = ('uploaded_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'price', 'discount', 'quantity', 'available', 'created_at', 'updated_at')
    list_filter = ('available', 'discount', 'created_at', 'updated_at')
    search_fields = ('title', 'brand', 'description')
    ordering = ('title',)
    inlines = [ProductImageInline]  # Inline изображения для продукта

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('title',),
        }
