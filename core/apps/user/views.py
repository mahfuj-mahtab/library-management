from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import logout,authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import *
from apps.book.serializers import *
from apps.book.models import *
from django.shortcuts import get_object_or_404
from apps.author.models import *

class RegisterView(APIView):
    def post(self,request):
        serializers = UserRegistrationSerializer(data = request.data)
        if(serializers.is_valid()):
            serializers.save()
            return Response({'message' : "Registrations Done"},status = 201)
        else:
            return Response({"error" : serializers.errors},status = status.HTTP_403_FORBIDDEN)
        
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and Password cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Assuming email is used as the username for authentication
        user = authenticate(request, username=email.split("@")[0], password=password)
        is_admin = False
        if user is not None:
            if user.is_staff or user.is_superuser:
                is_admin = True
            refresh = RefreshToken.for_user(user)
            login(request,user)
            data = {
                'refresh' : str(refresh),
                'access' : str(refresh.access_token),
                'data' : UserSerializer(user).data,
                "is_admin" : is_admin,

             
                               
            }
            return Response({"message": data}, status=status.HTTP_200_OK)
        else:
           
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        logout(request)
        return Response({"message" : "Logout"},status = 200)
    
class AdminCheckBorrowedBooks(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        data = []
        borrowed_books = BorrowBook.objects.filter(status = 'APPROVED')
        due_borrowed = BorrowBook.objects.filter(status = 'HOLD')
        
        data = {
            "borrowed_books" : BookBorrowSerializer(borrowed_books,many = True).data,
            "due_borrowed" : BookBorrowSerializer(due_borrowed,many = True).data
        }
        return Response({"data" : data}, status = 200)
class AdminCreateBook(APIView):
    permission_classes = [IsAdminUser]
    def post(self,request):
        if not request.user.has_perm('books.add_book'):
            return Response({"error" : "Permission Deinied"}, status = 403)
        author = get_object_or_404(Author, pk = request.data['author'])
        serializers = BookSerializer(data = request.data)
        if(serializers.is_valid()):
            serializers.save(author = author)
            return Response({'message' : 'Successfully Book Added'},status = 201)
        else:
            return Response({'error' : serializers.errors},status = status.HTTP_403_FORBIDDEN)

# class to fetch book info, update it and delete it
class AdminSingleBook(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request,b_id):
        if not request.user.has_perm('books.view_book'):
            return Response({"error" : "Permission Deinied"}, status = 403)
        book = get_object_or_404(Book,id = b_id)
        return Response({'data' : BookSerializer(book).data},status = 201)
    
    def put(self,request,b_id):
        if not request.user.has_perm('books.edit_book'):
            return Response({"error" : "Permission Deinied"}, status = 403)
        book = get_object_or_404(Book,id = b_id)
        author = get_object_or_404(Author,id = request.data['author'])
        serializers = BookSerializer(book,data = request.data,partial = True)
        if(serializers.is_valid()):
            serializers.save(author = author)
            return Response({'message' : 'Successfully Book Edited'},status = 201)
        else:
            return Response({'error' : serializers.errors},status = status.HTTP_403_FORBIDDEN)
    
    def delete(self,request,b_id):
        if not request.user.has_perm('books.delete_book'):
            return Response({"error" : "Permission Deinied"}, status = 403)
        book = get_object_or_404(Book,id = b_id)
        book.delete()
        return Response({'message' : 'Successfully Book Deleted'},status = 201)



class UserBookBorrow(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = request.user
        book = get_object_or_404(Book,id = request.data['book'])
        already_borrowed = BorrowBook.objects.filter(book = book, user = user,status = 'APPROVED').exists()
        if(already_borrowed):
            return Response({"error": "sorry you have already taken this book"},status = status.HTTP_403_FORBIDDEN)

        borrowed_books = BorrowBook.objects.filter(user = user,status = 'APPROVED')
        borrow_limit = BorrowLimit.objects.filter().first()
        print(borrow_limit)
        if(len(borrowed_books) >= borrow_limit.limit):
            return Response({"error": "sorry your book borrowing limit exceded"},status = status.HTTP_403_FORBIDDEN)
        if(book.available_copies <= 0 ):
            return Response({"error": "sorry Book Not Available"},status = status.HTTP_403_FORBIDDEN)

        serializers = BookBorrowSerializer(data = request.data)
        if(serializers.is_valid()):
            serializers.save(book = book, user = user)
           
            return Response({'message' : 'Successfully Book Borrowed'},status = 201)
        else:
            return Response({'error' : serializers.errors},status = status.HTTP_403_FORBIDDEN)



class UserBookReturn(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = request.user
        book = get_object_or_404(Book,id = request.data['book'])
        try:
            already_borrowed = BorrowBook.objects.get(book = book, user = user,status = 'APPROVED')
        except BorrowBook.DoesNotExist:
            return Response({"error": "sorry you have not taken this book"},status = status.HTTP_403_FORBIDDEN)
             

        serializers = BookBorrowSerializer(already_borrowed,data = request.data,partial = True)
        if(serializers.is_valid()):
            serializers.save(book = book, user = user)
            book.available_copies+=1
            book.save()
            return Response({'message' : 'Successfully Book Returned'},status = 201)
        else:
            return Response({'error' : serializers.errors},status = status.HTTP_403_FORBIDDEN)
            
       

