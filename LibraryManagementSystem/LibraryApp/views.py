from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from . forms import *
from . models import *
from LibraryManagementSystem import settings
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q
from django.db.models import F
# Create your views here.

def home(request):
    k = AddBook.objects.all()
    return render(request,'html/home.html',{'s':k})

def blank(request):
    return render(request,'html/blank.html')

def about(request):
    return render(request,'html/about.html')

def contact(request):
    return render(request,'html/contact.html')

def register(request):
    if request.method == "POST":
        g = UsrForm(request.POST)
        if g.is_valid():
            user = g.save(commit=False)
            user.set_password(g.cleaned_data['password'])
            user.save()
            return redirect('/lgo')
    else:
        g = UsrForm()

    return render(request,'html/register.html',{'t':g})

def profile(request):
    w = User.objects.get(id=request.user.id)
    if request.method == "POST":
        t=ProfileForm(request.POST,request.FILES)
        y=UserupdationForm(request.POST,instance=w)
        if t.is_valid() and y.is_valid():
            k=t.save(commit=False)
            k.usd_id = request.user.id
            w.has_stregister = 1
            w.save()
            y.save()
            k.save()
            return redirect('/')

    t=ProfileForm
    y=UserupdationForm(instance=w)
    return render(request,'html/student_profile.html',{'q':y,'r':t})
@login_required
def viewprofile(request):
    # s = User.objects.get(id=request.user.id)
    t = Profile.objects.all()
    return render(request,'html/viewprofile.html',{'r':t})

@login_required
def editprofile(request):
    student = Profile.objects.get(usd=request.user)
    alert = False

    if request.method == "POST":
        email = request.POST.get('email', '')
        mobileno = request.POST.get('mobileno', '')
        branch = request.POST.get('branch', '')
        sec = request.POST.get('sec', '')
        sid = request.POST.get('sid', '')
        if email:
            student.usd.email = email
        if mobileno:
            student.mobileno = mobileno
        if branch:
            student.branch = branch
        if sec:
            student.sec = sec
        if sid:
            student.usd.sid = sid

        # Save the updated student profile
        student.usd.save()
        student.save()
        alert = True
        return render(request, "html/editprofile.html", {'alert':alert})
    return render(request,'html/editprofile.html')


def addbook(request):
    if request.method == "POST":
        qa = AddBookForm(request.POST)
        if qa.is_valid():
            w = qa.save(commit=False)
            w.bstatus=True
            w.save()
            return redirect('/viewbook')

    qa = AddBookForm()
    return render(request,'html/addbook.html',{'y':qa})

def viewbook(request):
    books = AddBook.objects.all()
    return render(request,'html/viewbook.html',{'books':books})

@login_required
def deletebook(request,myid):
    book = AddBook.objects.filter(id=myid)
    if request.method == "POST":
        book.delete()
        return redirect("/viewbook")
    return render(request,"html/deletebook.html",{'h':book})

@login_required
def viewstudents(request):
    profile_students = Profile.objects.all() 
    user_students = User.objects.filter(role_type = '1')
    students = list(list(profile_students) + list(user_students))
    return render(request, "html/viewstudents.html", {'students':profile_students})


@login_required
def changepassword(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "html/changepassword.html", {'alert':alert})
            else:
                currpasswrong = True
                return render(request, "html/changepassword.html", {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, "html/changepassword.html")
#student requesting for book
@login_required
def bookview(request,v):
    m=AddBook.objects.get(id=v)
    isexist = BookRequest.objects.filter(book=m,requested_by=request.user).exists()
    requested_books_count = BookRequest.objects.filter(requested_by=request.user).count()
    if request.method == 'POST':
        if isexist:
            messages.warning(request,'!!!...OOPS!!! Multiple Requests not allowed...!!!')
            return redirect('/requestedbooks')
        elif m.ncopies<=0:
            messages.warning(request,'!!!...SORRY OUT OF STOCK...!!!')
            return redirect('/requestedbooks')
        elif requested_books_count >=4:
            messages.warning(request,'!!!...!!..OOPS!!! Maximum Requests reached...!!!')
            return redirect('/requestedbooks')
        else:
            reqbk = BookRequest(book = m,requested_by=request.user,requested_by_student = request.user)
            reqbk.save()
            messages.success(request,'!!...BookRequested Successfully...!!')
            return redirect('/requestedbooks')
    return render(request,'html/bookview.html',{'bookview':m})

def total_fine(book_fine):
    t = 0
    for i in book_fine:
        t += i.fine_amount
    return t


def requestedbooks(request):
    d = BookRequest.objects.filter(requested_by = request.user)
    aprove = BookRequest.objects.filter(requested_by = request.user,status_to_approve = 'Approved')
    book_fine = BookRequest.objects.filter(
        requested_by_student=request.user,
        status_to_approve='Approved',
        return_status='Returned'
    )
    approved_books = BookRequest.objects.filter(
        requested_by_student=request.user,
        status_to_approve='Approved'
    )
    all_books_returned = all(book.return_status == 'Returned' for book in approved_books)

    total = total_fine(book_fine)
    return render(request,'html/requestedbooks.html',{'book_requests' : d})




# accept requests...


def approverequests(request,requestid):
    bkrequest = BookRequest.objects.get(id = requestid)
    if bkrequest.book.ncopies > 0:
        bkrequest.status_to_approve="Approved"
        bkrequest.approved_date = timezone.now()
        due_date = bkrequest.approved_date+timedelta(days=14)
        bkrequest.due_date = due_date
        book = bkrequest.book
        AddBook.objects.filter(id = book.id).update(ncopies=F('ncopies')-1)
        bkrequest.save()
        subject = '!!!!..Book Request Approved...!!!'
        message = f"\nDear Student"
        message += f"\nName : {bkrequest.requested_by_student}\nPin Number : {bkrequest.requested_by_student.sid}"
        message += f"\nYour requested book  '{bkrequest.book.bname}' has been approved.\n"
        message += f"\nApproved Date: {bkrequest.approved_date}\n"
        message += f"\nDue Date: {due_date}\n"
        message += f"\nPlease make sure to return the book ,with in the due date ,otherwise you will be imposed of fine "
        message += f"\nDon't Reply...."
        recipient = bkrequest.requested_by.email

        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
        messages.success(request,'Approved Successfully')
    else:
        messages.warning(request,'Out Of Stock...') 
    return render(request,'html/approvedrequests.html')

def allrequests(request):
    p = BookRequest.objects.filter(status_to_approve = 'Pending')
    return render(request,'html/allrequests.html',{'pending':p})


#librarian reject requests
def rejectrequests(request,requestid):
    bkrequest = BookRequest.objects.get(id = requestid)
    bkrequest.status_to_approve = 'Rejected'
    bkrequest.save()
    subject = '!!!...Book Request Rejected...!!!'
    m = f"\nDear Student"
    m+= f"\nname : {bkrequest.requested_by_student}\npin : {bkrequest.requested_by_student.sid}"
    m+= f"\nYour book request for '{bkrequest.book.bname}' has been rejected.Due to the Shortage of books(The book u requested that is under out of stock)"
    recipient = bkrequest.requested_by.email
    send_mail(subject, m, settings.EMAIL_HOST_USER, [recipient])
    messages.warning(request,'!!..Rejected Successfully..!!')   
    return redirect('/allrequests')


#student cancel request
def cancelrequest(request,bk):
    book_fine = BookRequest.objects.filter(
        requested_by_student=request.user,
        status_to_approve='Approved',
        return_status='Returned'
    )
    money = total_fine(book_fine)
    if request.method == "POST":
        book_request = BookRequest.objects.get(id = bk)
       
        if book_request.status_to_approve != 'Approved':
            book_request.delete()
            messages.success(request, 'Book request cancelled successfully.')
        elif money == 0 and book_request.return_status == 'Returned':
            book_request.delete()
            messages.success(request,'Book Submited..')
        else:
            messages.warning(request,'Not Possible Action')    
        
    return redirect('/requestedbooks')

# return book to library by sstudent

def returnbook(request,bkid):
    bkrequest = get_object_or_404(BookRequest,id=bkid)
    if request.method == 'POST':
        if bkrequest.return_status == 'Returned':
            messages.warning(request,'Already Returned')
        elif bkrequest.return_status == 'Pending':
            bkrequest.return_status='Returned'
            book = bkrequest.book
            AddBook.objects.filter(id=book.id).update(ncopies=F('ncopies')+1)
            bkrequest.return_date = timezone.now()
            bkrequest.save()
            due_date = bkrequest.due_date
            actual_return_date = bkrequest.return_date
            fine_amount = 0
            if actual_return_date > due_date:
                days_late = (actual_return_date - due_date).days
                fine_amount = days_late * 5
            bkrequest.fine_amount = fine_amount
            bkrequest.save()
            messages.success(request,'Book returned Successfully')
        else:
            messages.info(request,'Book must Approved First')
    return redirect('/stapprovedbooks')

def stapprovedbooks(request):
    d = BookRequest.objects.filter(requested_by = request.user)
    aprove = BookRequest.objects.filter(requested_by = request.user,status_to_approve = 'Approved')
    book_fine = BookRequest.objects.filter(
        requested_by_student=request.user,
        status_to_approve='Approved',
        return_status='Returned'
    )
    approved_books = BookRequest.objects.filter(
        requested_by_student=request.user,
        status_to_approve='Approved'
    )
    all_books_returned = all(book.return_status == 'Returned' for book in approved_books)

    total = total_fine(book_fine)
    return render(request,'html/stapprovedbooks.html',{'book_approved' : aprove})

def lbapprovedbooks(request):
    ap = BookRequest.objects.filter(Q(status_to_approve='Approved') & Q(return_status='Pending'))
    return render(request,'html/lbapprovedbooks.html',{'approvedbooks':ap})

#pay fine
