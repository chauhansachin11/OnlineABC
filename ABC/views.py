# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# EMail extensions
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from django.contrib import messages
from django.shortcuts import render, HttpResponse,  HttpResponseRedirect
from models import customer,retailer,customerContact,cardDetails,customerPayments,books,novelType,bookType,refBooks,subject
from .forms import CustomerRegistration,BookForm,RetailerRegistration,CustomerUpdateForm,CustomerAddressUpdateForm,CardForm,RetailerUpdateForm,RetailerAddressUpdateForm
import random
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.files.storage import FileSystemStorage
import os
from django.contrib.auth.decorators import login_required




def customerObjectsGet(sessionVarible):
    customerObject=customer.objects.get(customerEmailID=sessionVarible)
    return customerObject

def retailerObjectsGet(sessionVarible):
    retailerObject=retailer.objects.get(retailerEmailID=sessionVarible)
    return retailerObject

def sessionIsAvailable(sessionVarible):
    if(sessionVarible!=None) or (sessionVarible!=""):
        return True
    else:
        return False

def logout(request):
    allbooks=books.objects.all()
    try:
        if( sessionIsAvailable(request.session['customerEmailID'])==True):
            print "session",request.session['customerEmailID']
            del request.session['customerEmailID']
            print "session deleted "
            return render(request,'ABC/index.html',{'books':allbooks})
        else:
            return render(request,'ABC/index.html',{'books':allbooks})
    except KeyError:
            return render(request,'ABC/index.html',{'books':allbooks})

def index(request):
    allbooks=books.objects.all()
    return render(request,'ABC/index.html',{'books':allbooks})

def about(request):
       return render(request,'ABC/about.html')

def faq(request):
       return render(request,'ABC/faq.html')

def myprofile(request):
    form = {}
    if 'updateCustomerDetails' in request.POST:
        updateCustomerDetails(request)
    elif 'updateCustomerAddress' in request.POST:
        updateCustomerAddress(request)
    elif 'addcardDetails' in request.POST:
        addcardDetails(request)
    elif 'delete_card' in request.POST:
        delete_card(request)

    if(sessionIsAvailable(request.session['customerEmailID'])==True):
            user=customerObjectsGet(request.session['customerEmailID'])
            usercontact=customerContact.objects.filter(customerID = user.id).values()[0]
            if(cardDetails.objects.filter(customercardID = user.id).values()):
                cards=cardDetails.objects.filter(customercardID = user.id).values()
            else:
                cards={}

    return render(request,'ABC/myprofile.html',{'user':user,'usercontact':usercontact,'cards':cards})


def loginTest(request):
       if 'loginForm' in request.POST:
            return (login(request))
       elif 'customerRegistrationForm' in request.POST:
            return (customerRegistration(request))
       elif 'retailerRegistrationForm' in request.POST:
            return (retailerRegistration(request))
       elif 'resetPasswordForm' in request.POST:
            return (forgotPassword(request))
       else:
            return render(request,'ABC/TestLogin.html')

def editRetailerProfile(request):
    form = {}
    if 'updateRetailerDetails' in request.POST:
        updateRetailerDetails(request)
    elif 'updateRetailerAddress' in request.POST:
        updateRetailerAddress(request)

    if(sessionIsAvailable(request.session['retailerEmailID'])==True):
            user=retailerObjectsGet(request.session['retailerEmailID'])

    return render(request,'ABC/retailerProfileEdit.html',{'user':user})

def addBooks(request):
    allbooks = {}

    if 'addNewBooks' in request.POST:
        print("In ADD BOOKS")
        addNewBooks(request)

    if 'deleteBooks' in request.POST:
        deleteBooks(request)

    if 'updateBooks' in request.POST:
        updateBooks(request)

    if(sessionIsAvailable(request.session['retailerEmailID'])==True):
            user=retailerObjectsGet(request.session['retailerEmailID'])
            allbooks=books.objects.filter(bookRetailer = user.id).values()

    return render(request,'ABC/addBooks.html',{'user':user,'books':allbooks})

def login(request):
    a={}
    flag=1
    print(request.get_host())
    if request.method=='POST':
            emailid=request.POST.get('emailID')
            passwd=request.POST.get('password')
            customers=customer.objects.all()
            retailers=retailer.objects.all()
            for i in customers:
                    if(i.customerEmailID==emailid and i.password==passwd):
                        a={'name': i.customerName}
                        request.session['customerEmailID'] = emailid
                        print "session created",request.session['customerEmailID']
                        if(sessionIsAvailable(request.session['customerEmailID'])==True):
                                customerDetail=customerObjectsGet(request.session['customerEmailID'])
                                allbooks=books.objects.all()
                                result = "Recommendes books"
                                #print "customerDetail username:",customerDetail.customerEmailID,customerDetail.customerUserName
                        return render (request,'ABC/shop.html',{'a':a,'books':allbooks,'result':result})
                        #return shop(request)

            for j in retailers:
                    if(j.retailerEmailID==emailid and j.retailerPassword==passwd):
                        a={'name': j.shopName}
                        form = {}

                        request.session['retailerEmailID'] = emailid
                        if(sessionIsAvailable(request.session['retailerEmailID'])==True):
                                user=retailerObjectsGet(request.session['retailerEmailID'])
                                print "session created",request.session['retailerEmailID']
                        return render(request,'ABC/retailerProfile.html',{'user':user})
            flag=0
    if(flag==0):
        messages.error(request,"Enter Valid Credentials")
        return render(request,'ABC/TestLogin.html')


def customerRegistration(request):
    a={}
    args={}
    flag=1
    if request.method=='POST':

        customer_registration=CustomerRegistration(request.POST)

        print "valid or not",customer_registration.is_valid()
        if customer_registration.is_valid():
             # Fething The data From forms fields
            customerName=customer_registration.cleaned_data['customerName']
            a={'name': customerName}
            customerUserName=customer_registration.cleaned_data['customerUserName']
            customerEmailID=customer_registration.cleaned_data['customerEmailID']
            password=customer_registration.cleaned_data['password']
            customerdetails=customer.objects.create(customerName=customerName,customerUserName=customerUserName,customerEmailID=customerEmailID,password=password)
            customercontact=customerContact.objects.create(customerID=customerdetails)
            return render(request,'ABC/TestLogin.html',{'a':a})
        else:
            flag=0
            customer_registration=CustomerRegistration()
            args['customer_registration']= customer_registration

    if(flag==0):
        messages.error(request,"An account with credentials already exists.Please use another username or email id")
        return render(request,'ABC/TestLogin.html',args)

def retailerRegistration(request):
    a={}
    args={}
    flag=1
    if request.method=='POST':
        retailer_registration=RetailerRegistration(request.POST)
        if retailer_registration.is_valid():
             # Fething The data From forms fields
            shopID=retailer_registration.cleaned_data['shopID']
            shopName=retailer_registration.cleaned_data['shopName']
            a={'name': shopName}
            retailerEmailID=retailer_registration.cleaned_data['retailerEmailID']
            retailerPriPhone=retailer_registration.cleaned_data['retailerPriPhone']
            retailerPassword=retailer_registration.cleaned_data['retailerPassword']
            retailerdetails=retailer.objects.create(shopID=shopID,shopName=shopName,retailerEmailID=retailerEmailID,retailerPriPhone=retailerPriPhone,retailerPassword=retailerPassword)
            return render(request,'ABC/TestLogin.html',{'a':a})
        else:
            flag=0
            retailer_registration=RetailerRegistration()
            args['retailer_registration']= retailer_registration

    if(flag==0):
        messages.error(request,"An account with credentials already exists.Please use another username or email id")
        return render(request,'ABC/TestLogin.html',args)

def updateCustomerDetails(request):
    a={}
    args={}
    flag=1
    if request.method=='POST':
        print "\nIn Updation part\n"
        user=customerObjectsGet(request.session['customerEmailID'])
        usercontact=customerContact.objects.get(customerID = user.id)
        customer_form=CustomerUpdateForm(request.POST)
        if customer_form.is_valid():
             # Fething The data From forms fields
            customerName=customer_form.cleaned_data['customerName'] if customer_form.cleaned_data['customerName'] else user.customerName
            customerUserName=customer_form.cleaned_data['customerUserName'] if customer_form.cleaned_data['customerUserName'] else user.customerUserName
            password=customer_form.cleaned_data['password'] if customer_form.cleaned_data['password'] else user.password

            customerPhone=customer_form.cleaned_data['customerPhone'] if customer_form.cleaned_data['customerPhone'] else usercontact.customerPhone

            customer.objects.filter(id = user.id).update(customerName=customerName,customerUserName=customerUserName,password=password)
            customerContact.objects.filter(customerID = user.id).update(customerPhone=customerPhone)


def updateCustomerAddress(request):
    a={}
    args={}
    flag=1
    if request.method=='POST':
        user=customerObjectsGet(request.session['customerEmailID'])
        usercontact=customerContact.objects.get(customerID = user.id)
        customer_form=CustomerAddressUpdateForm(request.POST)
        if customer_form.is_valid():
             # Fething The data From forms fields
            customerAddress=customer_form.cleaned_data['customerAddress'] if customer_form.cleaned_data['customerAddress'] else usercontact.customerAddress
            customerPincode=customer_form.cleaned_data['customerPincode'] if customer_form.cleaned_data['customerPincode'] else usercontact.customerPincode

            customerContact.objects.filter(customerID = user.id).update(customerAddress=customerAddress,customerPincode=customerPincode)


def addcardDetails(request):

    if request.method=='POST':
        user=customerObjectsGet(request.session['customerEmailID'])
        card_form=CardForm(request.POST)
        #print "card_form->",card_form
        if card_form.is_valid():
             # Fething The data From forms fields
            cardNumber=card_form.cleaned_data['cardNumber']
            cvv=card_form.cleaned_data['cvv']
            expiryDate=card_form.cleaned_data['expiryDate']
            cardName=card_form.cleaned_data['cardName']
            bankName=card_form.cleaned_data['bankName']
            phoneNumber=card_form.cleaned_data['phoneNumber']

            carddetails=cardDetails.objects.create(cardNumber=cardNumber,cvv=cvv,expiryDate=expiryDate,cardName=cardName,bankName=bankName,customercardID=user)
            customerpayments=customerPayments.objects.create(paymentMethod='Card',detailID=carddetails,customerNo=user,phoneNumber=phoneNumber)


def delete_card(request):
    if request.method=='POST':
        cardID=request.POST.get('cardID')
        print "\ncardID",cardID
        customerPayments.objects.filter(detailID=cardID).delete()
        cardDetails.objects.filter(id=cardID).delete()

def deleteBooks(request):
    if request.method=='POST':
        bookID=request.POST.get('bookID')
        book=books.objects.get(id = bookID)
        os.remove("media/" + str(book.bookImage))
        books.objects.filter(id=bookID).delete()

def updateBooks(request):
    if request.method=='POST':
        bookID=request.POST.get('bookID')
        bookPrice=request.POST.get('bookPrice')
        print "\nIN updateBooks",bookID,bookPrice
        books.objects.filter(id = bookID).update(bookPrice=bookPrice)


def updateRetailerDetails(request):
    a={}
    args={}
    flag=1
    if request.method=='POST':
        print "\nIn Updation part\n"
        user=retailerObjectsGet(request.session['retailerEmailID'])
        retailer_form=RetailerUpdateForm(request.POST)
        if retailer_form.is_valid():
             # Fething The data From forms fields
            retailerPriPhone=retailer_form.cleaned_data['retailerPriPhone'] if retailer_form.cleaned_data['retailerPriPhone'] else user.retailerPriPhone
            retailerSecPhone=retailer_form.cleaned_data['retailerSecPhone'] if retailer_form.cleaned_data['retailerSecPhone'] else user.retailerSecPhone
            retailerPassword=retailer_form.cleaned_data['retailerPassword'] if retailer_form.cleaned_data['retailerPassword'] else user.retailerPassword

            retailer.objects.filter(id = user.id).update(retailerPriPhone=retailerPriPhone,retailerSecPhone=retailerSecPhone,retailerPassword=retailerPassword)


def updateRetailerAddress(request):
    a={}
    args={}
    flag=1
    if request.method=='POST':
        user=retailerObjectsGet(request.session['retailerEmailID'])
        retailer_form=RetailerAddressUpdateForm(request.POST)
        if retailer_form.is_valid():
             # Fething The data From forms fields
            shopAddress=retailer_form.cleaned_data['shopAddress'] if retailer_form.cleaned_data['shopAddress'] else user.shopAddress
            shopPincode=retailer_form.cleaned_data['shopPincode'] if retailer_form.cleaned_data['shopPincode'] else user.shopPincode

            retailer.objects.filter(id=user.id).update(shopAddress=shopAddress,shopPincode=shopPincode)

def addNewBooks(request):
    if request.method=='POST':
        user=retailerObjectsGet(request.session['retailerEmailID'])
        book_form=BookForm(request.POST, request.FILES)
        print "\n\nbook_form->",book_form.is_valid()
        print "\nform_error->",book_form.errors
        #bookImage = request.FILES['bookImage'].file.read()
        if book_form.is_valid():
             # Fething The data From forms fields
            bookName=book_form.cleaned_data['bookName']
            bookISBNcode=book_form.cleaned_data['bookISBNcode']
            bookPublication=book_form.cleaned_data['bookPublication']
            bookAuthor=book_form.cleaned_data['bookAuthor']
            bookEdition=book_form.cleaned_data['bookEdition'] if book_form.cleaned_data['bookEdition'] else 0
            bookPrice=book_form.cleaned_data['bookPrice']
            booktype=book_form.cleaned_data['bookType']
            if(booktype == 'novel'):
                novelname=book_form.cleaned_data['novelType']
                novel=novelType.objects.get(novelType = novelname)
                bookTypeID=bookType.objects.get(typeName = novel.id)
            elif(booktype == 'refBook'):
                refType=book_form.cleaned_data['refType']
                sub=refBooks.objects.get(subject = refType)
                bookTypeID=bookType.objects.get(typeName = sub.id)
            bookImage = request.FILES['bookImage']
            #fs = FileSystemStorage()
            #filename = fs.save(bookImage.name, bookImage)
            print "bookimage->",bookImage
            bookdetails=books.objects.create(bookName=bookName,bookISBNcode=bookISBNcode,bookPublication=bookPublication,bookAuthor=bookAuthor,bookEdition=bookEdition,bookPrice=bookPrice,bookTypeID=bookTypeID,bookImage=bookImage,bookRetailer=user)


def privacy(request):
    return render(request,'ABC/privacy-policy.html')

def products(request):
    return render(request,'ABC/products.html')

def product_single(request):
    book_id=request.GET.get('book_id')
    singlebook = books.objects.filter(id = book_id).values()[0]
    print singlebook
    return render(request,'ABC/product-single.html',{'book':singlebook})


def terms(request):
    return render(request,'ABC/terms-conditions.html')

def ships(request):
    return render(request,'ABC/shipping.html')

def shop(request):
    if 'searchBooks' in request.POST:
        searchText=request.POST.get('searchText')
        book_byAuthor=books.objects.filter(bookAuthor__icontains=searchText)
        book_byName=books.objects.filter(bookName__icontains=searchText)
        book_byPublication=books.objects.filter(bookPublication__icontains=searchText)
        allbooks = book_byAuthor | book_byName | book_byPublication
        result = "Search Result" if allbooks else "No Result Found"
    elif(sessionIsAvailable(request.session['retailerEmailID'])==True):
        allbooks=books.objects.all()
        result = "Recommendes books"
    return render(request,'ABC/shop.html',{'books':allbooks,'result':result})


def generateOtp():
    otp = random.randrange(1, 999999, 1)
    return otp

def forgotPassword(request):
    flag=1
    subject = 'Reset your password'
    recipient=request.POST.get('email')
    customers=customer.objects.all()
    retailers=retailer.objects.all()
    for i in customers:
            if(i.customerEmailID==recipient):
                otp =generateOtp()
                html_content = render_to_string('ABC/resetpassword.html', {'varname':'value', 'otp': otp, 'reciever': recipient}) # render with dynamic value
                text_content = strip_tags(html_content)

                email_from = settings.EMAIL_HOST_USER

                recipient_list= [recipient,]
                a={'name': recipient}
                msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
                msg.attach_alternative(html_content, "text/html")
                if(msg.send()):
                    flag=0
                    changePassword(recipient,str(otp))
                    return render (request,'ABC/TestLogin.html')
                else:
                    print("error sending email")
    for j in retailers:
                if(j.retailerEmailID==recipient):
                    otp =generateOtp()
                    html_content = render_to_string('ABC/resetpassword.html', {'varname':'value', 'otp': otp, 'reciever': recipient}) # render with dynamic value
                    text_content = strip_tags(html_content)

                    email_from = settings.EMAIL_HOST_USER

                    recipient_list= [recipient,]
                    a={'name': recipient}
                    msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
                    msg.attach_alternative(html_content, "text/html")
                    if(msg.send()):
                        flag=0
                        changePassword(recipient,str(otp))
                        return render (request,'ABC/TestLogin.html')

                    else:
                        print("error sending email")

    if(flag==1):
        messages.error(request,"Enter Valid Credentials")
        return render(request,'ABC/TestLogin.html')
    else:
        return render(request,'ABC/TestLogin.html')

def retailerProfile(request):
    if(sessionIsAvailable(request.session['retailerEmailID'])==True):
            user=retailerObjectsGet(request.session['retailerEmailID'])

    return render(request,'ABC/retailerProfile.html',{'user':user})

def changePassword(email,otp):
        user=customerObjectsGet(email)
        customer.objects.filter(id = user.id).update(password=otp)

def resetpassword(request):
    return render (request,'ABC/resetpassword.html')
