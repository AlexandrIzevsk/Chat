from django.contrib import admin
from .models import Customer, Chat, ChatCustomer, Message


# class CustomerAdmin(admin.ModelAdmin):
#     # list_display = ('user', 'rating')
#     # list_filter = ('rating',)
#     # search_fields = ('user__username',)
#     # actions = [nulfy_rating]
#     model = Customer

admin.site.register(Customer)
admin.site.register(Chat)
admin.site.register(ChatCustomer)
admin.site.register(Message)
