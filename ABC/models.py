# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime
# Create your models here.

'''class userProfile(models.Model):
        user = models.OneToOneField(User)
        description = models.CharField(max_length=100, default='')
        city = models.CharField(max_length=100, default='')
        url = models.URLField(default='')
        phone = models.IntegerField(default=0)
        state = models.CharField(max_length=100, default='')'''

class customer(models.Model):
        customerName = models.CharField(max_length=100, default='')
        customerUserName = models.CharField(max_length=100, default='')
        customerEmailID = models.EmailField(max_length=100, default='')
        password = models.CharField(max_length=32, default='')

        def __str__(self):
            return '%s %s' % (self.customerEmailID, self.password)

class customerContact(models.Model):
        customerPhone = models.CharField(max_length=10, default='0')
        customerAddress = models.CharField(max_length=200, default='')
        customerPincode = models.IntegerField(max_length=6, default=0)
        customerID = models.ForeignKey(customer, related_name='custID', on_delete=models.CASCADE)

class retailer(models.Model):
        shopID = models.IntegerField(default=0)
        shopName = models.CharField(max_length=100, default='')
        shopAddress = models.CharField(max_length=200, default='')
        shopPincode = models.IntegerField(max_length=6, default=0)
        retailerEmailID = models.EmailField(max_length=100, default='')
        retailerPriPhone = models.CharField(max_length=10,default='0')
        retailerSecPhone = models.CharField(max_length=10,default='0')
        retailerPassword = models.CharField(max_length=32, default='')

class year(models.Model):
        year = models.IntegerField(max_length=1, default=0)
        semester = models.IntegerField(max_length=1, default=0)


class subject(models.Model):
        subject=models.CharField(max_length=50, default='')

class courseType(models.Model):
        courseName=models.CharField(max_length=100, default='')
        YearID=models.ForeignKey(year, related_name= 'yearID', on_delete=models.CASCADE)

class course(models.Model):
        stream=models.CharField(max_length=50, default='')
        courseTypeID=models.ForeignKey(courseType, related_name='courseTypeID', on_delete=models.CASCADE)
        subjectID=models.ForeignKey(subject, related_name='subjectID', on_delete=models.CASCADE)

        class Meta:
            unique_together= ('courseTypeID','subjectID')

class textBooks(models.Model):
        semester=models.IntegerField(default=0)
        courseID=models.ForeignKey(course, related_name='courseID', on_delete=models.CASCADE)

class novelType(models.Model):
        novelType=models.CharField(max_length=50, default='')

class refBooks(models.Model):
        subject=models.CharField(max_length=50, default='')
        
class bookType(models.Model):
        typeName=models.ForeignKey('textBooks', on_delete=models.CASCADE)
        typeName=models.ForeignKey('refBooks', on_delete=models.CASCADE)
        typeName=models.ForeignKey('novelType', on_delete=models.CASCADE)

class books(models.Model):
        bookName = models.CharField(max_length=100, default='')
        bookISBNcode = models.CharField(max_length=100, default='')
        bookPublication = models.CharField(max_length=100, default='')
        bookAuthor = models.CharField(max_length=100, default='')
        bookEdition = models.IntegerField(max_length=2, default=0)
        bookPrice = models.FloatField(null=True, blank=True, default=None)
        bookTypeID= models.ForeignKey(bookType, related_name='bookTypeID', on_delete=models.CASCADE)
        bookImage = models.FileField(upload_to="images/", null=True, blank=True)
        bookRetailer= models.ForeignKey(retailer, related_name='bookretailer', on_delete=models.CASCADE)


class bookReview(models.Model):
        ratings=models.FloatField(default=None)
        booksID=models.ForeignKey(books, related_name='booksID', on_delete=models.CASCADE)

class bookComments(models.Model):
        comments=models.CharField(max_length=5000, default='')
        booksId=models.ForeignKey(books, related_name='booksId', on_delete=models.CASCADE)
        customerId=models.ForeignKey(customer, related_name='customerId', on_delete=models.CASCADE)
        class Meta:
            unique_together = ('booksId','customerId')

class wishlist(models.Model):
        bookId=models.ForeignKey(books, related_name='bookId', on_delete=models.CASCADE)
        customersId=models.ForeignKey(customer, related_name='customersId', on_delete=models.CASCADE)
        class Meta:
            unique_together = ('bookId','customersId')

class cardDetails(models.Model):
        cardNumber=models.CharField(max_length=16, default=0)
        cvv=models.IntegerField(max_length=3, default=0)
        expiryDate= models.CharField(max_length=10,default='')
        cardName=models.CharField(max_length=50, default='')
        bankName=models.CharField(max_length=50, default='')
        customercardID = models.ForeignKey(customer, related_name='custcardID', on_delete=models.CASCADE)


class customerPayments(models.Model):
        paymentMethod=models.CharField(max_length=100,default=None)
        detailID=models.ForeignKey(cardDetails,related_name='detailID', on_delete=models.CASCADE)
        customerNo=models.ForeignKey(customer, related_name='customerNo', on_delete=models.CASCADE)
        phoneNumber=models.CharField(max_length=10,default='0')
        class Meta:
            unique_together = ('detailID','customerNo')

class deliveryBoy(models.Model):
        address=models.CharField(max_length=400,default='')
        deliveryBoyName=models.CharField(max_length=100,default='')
        adhaarNumber=models.IntegerField(default=0)
        priMobileNumber=models.IntegerField(default=0)
        secMobileNumber=models.IntegerField(default=0)

class customerOrder(models.Model):
        status=models.CharField(max_length=20,default='')
        dateOfOrder=models.DateField(auto_now=False)
        dateOfDelivery=models.DateField(auto_now=False)
        deliveredDate=models.DateField(auto_now=False)
        quantity=models.IntegerField(default=0)
        totalPrice=models.FloatField(default=None)
        bookSeqID=models.ForeignKey(books,related_name='bookSeqID', on_delete=models.CASCADE)
        customerSeqID=models.ForeignKey(customer, related_name='customerSeqID', on_delete=models.CASCADE)

class orderTracking(models.Model):
        orderStatus=models.CharField(max_length=400,default='')
        statusDate=models.DateField(auto_now=False)
        orderNo=models.ForeignKey(customerOrder,related_name='orderNo', on_delete=models.CASCADE)
        deliveryBy=models.ForeignKey(deliveryBoy, related_name='deliveryBy', on_delete=models.CASCADE)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.retailer.id, filename)

class addNewBooks(models.Model):
        dateOfRequest=models.DateField(auto_now=False)
        requestFile=models.FileField(upload_to=user_directory_path)
        requestStatus=models.CharField(max_length=50,default='')
        retailerID=models.ForeignKey(retailer,related_name='retailerID',on_delete=models.CASCADE)

class customerComplaint(models.Model):
        dateOfComplaint=models.DateField(auto_now=False)
        complaintStatus=models.CharField(max_length=100, default='')
        desc=models.TextField()
        image=models.ImageField(upload_to='complaints/')

def create_profile(sender, **kwargs):
        if(kwargs['created']):
                user_profile= userProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
