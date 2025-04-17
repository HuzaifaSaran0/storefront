from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Collection

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory', 'collection_title', 'inventory_status', 'edit_link']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update']
    search_fields = ['title', 'description']
    ordering = ['-last_update']  # latest products at the top
    list_per_page = 20  # pagination in admin

    # Custom column to show collection title (to avoid N+1 query)
    def collection_title(self, product):
        return product.collection.title
    collection_title.admin_order_field = 'collection'  # make it sortable
    collection_title.short_description = 'Collection'

    # Computed field for inventory status
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "OK"
    inventory_status.short_description = 'Stock Status'

    # Link to the edit page (optional but fun!)
    def edit_link(self, product):
        return format_html('<a href="{}">Edit</a>', f'/admin/store/product/{product.id}/change/')
    edit_link.short_description = 'Edit Product'


# the next step to show these models in the admin site is to register them
# admin.site.register(Product)
# admin.site.register(Collection)
# admin.site.register(Customer)
# admin.site.register(Order)
# admin.site.register(OrderItem)
# admin.site.register(Address)
# admin.site.register(Cart)