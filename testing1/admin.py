from django.contrib import admin
from django.utils.html import format_html
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'unit_price', 'description']
    list_editable = ['unit_price', 'color']
    list_filter = ['name', 'unit_price', 'color']
    search_fields = ['name']
    # ordering = ['-last_update']  # latest products at the top
    list_per_page = 20  # pagination in admin

    # Custom column to show collection title (to avoid N+1 query)
    def car_name(self, product):
        return product.name
    # collection_title.admin_order_field = 'collection'  # make it sortable
    # collection_title.short_description = 'Collection'

    # Computed field for inventory status
    # def inventory_status(self, product):
    #     if product.inventory < 10:
    #         return "Low"
    #     return "OK"
    # inventory_status.short_description = 'Stock Status'

    # Link to the edit page (optional but fun!)
    # deSption = 'Edit Product'
