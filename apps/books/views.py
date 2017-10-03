from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from models import User, Book, Review
def index(request):
    return render(request, 'books/index.html')
def home(request):
    context = {
    'review': Book.objects.reviews.last()
    }
    print context
    return render(request, 'books/home.html', context)
def book(request):
    return render(request, 'books/book.html')
def user(request):
    return render(request, 'books/user.html')
def register(request):
    errors = User.objects.basic_validator(request.POST)
    entered = User.objects.filter(email=request.POST['email'])
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        if entered.count() > 0:
            messages.error(request, "email already taken", extra_tags="email")
            return redirect('/')
        else:
            new = User.objects.create(name = request.POST['name'], alias = request.POST['alias'], email = request.POST['email'], password = hashed_pw)
            request.session['name'] = new.name
            request.session['id'] = new.id
            return redirect('/books')
def login(request):
    entered = User.objects.filter(email=request.POST['email'])
    if entered.count() > 0:
        entered = entered.first()
        if bcrypt.checkpw(request.POST['password'].encode(), entered.password.encode()) == True:
            request.session['name'] = entered.name
            request.session['id'] = entered.id
            return redirect('/books')
        else:
            messages.error(request, "Please check password or register", extra_tags="email")
            return redirect('/')
    else:
        messages.error(request, "Please check email or register", extra_tags="email")
        return redirect('/')
def review(request):
    if request.method == 'POST':
        try:
            new_book = Book.objects.create(title = request.POST['title'], author = request.POST['new_author'])
        except:
            new_book = Book.objects.create(title = request.POST['title'], author = request.POST['author'])
        Review.objects.create(content = request.POST['review'], rating = request.POST['rating'], user=User.objects.get(id=request.session['id']), book= Book.objects.get(id=new_book.id))
        return redirect('/books')
    else:
        context = {
        'book': Book.objects.all()
        }
        print context
        return render(request, 'books/review.html', context)
