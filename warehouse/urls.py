from django.urls import path

from warehouse.views import PhoneCreateView, ColorCreateView, BrandCreateView, PhoneListAPIView

app_name = 'phone'
urlpatterns = [
    path('api/phones/', PhoneListAPIView.as_view(), name='api-phones'),

    path('', PhoneCreateView.as_view(), name='add'),
    path('add-color/', ColorCreateView.as_view(), name='color_add'),
    path('add-brand/', BrandCreateView.as_view(), name='brand_add'),
]
