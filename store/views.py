
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from store.models import Book, BookCopy, BookRating


from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import datetime
from store import forms




# Create your views here.


def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    desired_book = get_object_or_404(Book,id=bid)
    
    count = BookCopy.objects.filter(Q(book=desired_book) & Q(status=True)).count()
    issued = False
    if request.user.is_authenticated:
        user_book_copies = request.user.borrower.all() 
        for bc in user_book_copies:
            if bc.book == desired_book:
                issued = True
                break
        
    
   
    context = {
        'book': desired_book, # set this to an instance of the required book
        'num_available': count,
        'issued': issued # set this to the number of copies of the book available, or 0 if the book isn't available
    }
    # START YOUR CODE HERE
    
    
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    get_data = request.GET
    print(get_data,"hello")
    if(len(get_data)>0):
        
        required_books=Book.objects.filter(title__icontains=get_data['title'],author__icontains=get_data['author'],genre__icontains=get_data['genre'])
        print(get_data.get('title'),get_data['title'])
    else:
        required_books=Book.objects.all()
    
    
    context = {
    'books':required_books, # set this to the list of required books upon filtering using the GET parameters
    }                          # (i.e. the book search feature will also be implemented in this view)
                            # (i.e. the book search feature will also be implemented in this view)
        
        

    
    
    
    
    
    
    # queryset = Book.objects.all()
    # print(queryset,"hello")
   

    # START YOUR CODE HERE
    
    
    return render(request, template_name, context=context)

@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
     
    issued_books = request.user.borrower.all()
    context = {
        'books': issued_books,
    }
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    # START YOUR CODE HERE
    


    return render(request, template_name, context=context)

@csrf_exempt
@login_required
def loanBookView(request):
    book_id = request.POST.get('bid')
    count = BookCopy.objects.filter(Q(book=Book.objects.get(id=book_id)) & Q(status=True)).count()



    if count>0:
        book_copy = BookCopy.objects.filter(Q(book=Book.objects.get(id=book_id)) & Q(status=True))[0]
        print(book_copy.id)
        book_copy.status = False
        book_copy.borrow_date = datetime.date.today()
        book_copy.borrower = request.user
        book_copy.save()
        msg = 'success'
    else:
        msg = 'failure'

    response_data = {
        'message': msg,
    }
    
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE
     # get the book id from post data


    return JsonResponse(response_data)

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 
@csrf_exempt
@login_required
def returnBookView(request):
    
    bookcopy_id = request.POST.get('bid')
    bookcopy = get_object_or_404(BookCopy,id=bookcopy_id)
    bookcopy.borrower = None
    bookcopy.borrow_date = None
    bookcopy.status = True
    bookcopy.save()
    print(request.POST)
    msg = 'success'

    response_data={
        'message': msg
    }

    return JsonResponse(response_data)

def rateBook(request,bid):
    if request.method == 'POST':
        form = forms.RatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data.get('rating')
            ratings_by_user =request.user.rating_by.all()
            print(ratings_by_user,'hellllsaldlasldlasldl')
            if ratings_by_user.count() > 0:
                rating_object = ratings_by_user[0]
                rating_object.rating = rating
                rating_object.save()
            else:    
                book_rating = BookRating.objects.create(book=Book.objects.get(id=bid), rating_by = request.user, rating = rating)
            book=Book.objects.get(id=bid)
            all_BookRating_objects = BookRating.objects.all()
            total_ratings = all_BookRating_objects.count()
            sum_of_ratings = 0
            for obj in all_BookRating_objects:
                sum_of_ratings = sum_of_ratings + obj.rating
            book.rating = sum_of_ratings/total_ratings
            book.save()
            
            
            str_url = '/book/' + str(bid) +'/'
            return redirect(str_url)
    else:
        form = forms.RatingForm()
    book_title = Book.objects.get(id=bid).title
    context = {
        'form': form,
        'title': book_title
    }

    return render(request,'store/rate.html',context)            
            





      

    


