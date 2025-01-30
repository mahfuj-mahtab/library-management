from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # Login
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Refresh token
    path("login/", LoginView.as_view(), name="logout"),  # login
    path("logout/", LogoutView.as_view(), name="logout"),  # Logout
    path("register/", RegisterView.as_view(), name="register"),  # Register new user

    # user book borrow url 
    path("borrow/book/", UserBookBorrow.as_view(), name="UserBookBorrow"),  # User Book Borrow url
    path("return/book/", UserBookReturn.as_view(), name="UserBookReturn"),  # User Book return url

    # admin panel 
    path("admin/create/book/", AdminCreateBook.as_view(), name="AdminCreateBook"),  #admin create book url
    path("admin/single/book/<int:b_id>/", AdminSingleBook.as_view(), name="AdminSingleBook"),  #admin single book url for get put and delete
]