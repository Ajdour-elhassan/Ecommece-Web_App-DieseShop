from django.contrib import admin
from . models import Category , Product , OrderItem , Order

class CategoryAdmin(admin.ModelAdmin) :
    list_display = ["name" , "slug" ]
    prepopulated_fields = {'slug':('name',)}
    list_per_page = 5

admin.site.register(Category , CategoryAdmin)
class ProductAdmin(admin.ModelAdmin) :
    list_display = ["name" , "price" , "stock" , "available" , "created_date" , "updated"]
    list_editable = ['price' , 'stock' , 'available']
    prepopulated_fields = {'slug':('name',)}
    list_per_page = 5

admin.site.register(Product , ProductAdmin)

class OrderItemAdmdin(admin.TabularInline):
    model = OrderItem
    fieldsets = [
        ('Product' , {'fields': ['product'],}),
        ('Quantity' , {'fields': ['quantity'],}),
        ('Price' , {'fields': ['price'],}),
    ]
    readonly_fields = ['product', 'quantity' , 'price']

@admin.register(Order)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id' , 'billingName' , 'emailAddress' , 'created']
    list_display_link = ('id' , 'billingName')
    search_fields = ['id' , 'billingName' , 'emailAddress']
    readonly_fields = [ 'id' ,
                        'token' ,
                        'emailAddress' ,
                        'created' ,
                        'billingName' ,
                        'billingAddress1' ,
                        'billingCity' ,
                        'billingPostcode' ,
                        'billingCountry ',
                        'shippingName' ,
                        'shippingAddress1',
                        'shippingCity',
                        'shippingPostcode ' ,
                        'shippingCountry'
                    ]

    fieldsets  = [
        ('ORDER INFORMATION', {'fields': ['id','token','total','created']}),

        ('BILLING INFORMATION', {'fields': ['billingName','billingAddress1','billingCity ' ,
        'billingPostcode ' , 'billingCountry ','shippingName']}),

        ('SHIPPING INFORMATION', {'fields': [ 'shippingName' , 'shippingAddress1','shippingCity','shippingPostcode ' , 'shippingCountry']}),
    ]

    InLines = [
        OrderItemAdmdin,
    ]

    def has_delete_permession(self, request , obj=None) :
        return False

    def has_add_permission(self, request):
       return False
        

