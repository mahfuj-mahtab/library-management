from django.urls import path,include

import apps.user.urls
import apps.book.urls
urlpatterns = [
    path("users/", include(apps.user.urls)), 
    path("books/", include(apps.book.urls)), 

]