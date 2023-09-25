from django.conf.urls import url
from . import views




urlpatterns=[
    url(r'^$',views.index),
    url(r'^index/',views.index),
    url(r'^shop/',views.shop),
    url(r'^retailerProfile/',views.retailerProfile),
    url(r'^TestLogin/',views.loginTest),
    url(r'^about/',views.about),
    url(r'^products/',views.products),
    url(r'^product_single/$',views.product_single),
    url(r'^faq/',views.faq),
    url(r'^privacy/',views.privacy),
    url(r'^terms-conditions/',views.terms),
    url(r'^ships/',views.ships),
    url(r'^myprofile/',views.myprofile),
    url(r'^logout/',views.logout),
    url(r'^resetpassword/',views.resetpassword),
    url(r'^editRetailerProfile/',views.editRetailerProfile),
    url(r'^addBooks/',views.addBooks),

]
