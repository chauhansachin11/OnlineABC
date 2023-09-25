from django import forms
from django.core.exceptions import ValidationError
from ABC.models import customer,retailer,books,customerContact,cardDetails
import re


class CardForm(forms.ModelForm):
    class Meta():
        model= cardDetails
        fields=['cardNumber','cvv','expiryDate','cardName','bankName','month','year','phoneNumber']

    phoneNumber = forms.CharField()
    month = forms.CharField()
    year = forms.CharField()

class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(BookForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['bookType'].required = False
        self.fields['novelType'].required = False
        self.fields['refType'].required = False
        self.fields['bookEdition'].required = False

    class Meta():
        model= books
        fields=['bookName','bookISBNcode','bookPublication','bookAuthor','bookEdition','bookPrice','bookType','refType','novelType','bookImage']
        widgets = {
            'bookImage' : forms.FileInput(attrs={'multiple': True})
        }
    bookType = forms.CharField()
    novelType = forms.CharField()
    refType= forms.CharField()


class CustomerUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(CustomerUpdateForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['customerName'].required = False
        self.fields['customerUserName'].required = False
        self.fields['password'].required = False
        self.fields['customerPhone'].required = False

    class Meta():
        model= customer
        fields=['customerName','customerUserName','password','customerPhone']

    customerPhone = forms.CharField()

    '''def clean_customerPhone(self):
        customerPhone=self.cleaned_data.get('customerPhone')
        if not( re.match(r'^[6-9]\d{9}$', customerPhone)):
            print "Mobile Number is not valid, Please insert 10 digit valid Mobile Number"
            raise forms.ValidationError("Mobile Number is not valid, Please insert 10 digit valid Mobile Number")
        return customerPhone'''

class RetailerUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(RetailerUpdateForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['retailerPriPhone'].required = False
        self.fields['retailerSecPhone'].required = False
        self.fields['retailerPassword'].required = False

    class Meta():
        model= retailer
        fields=['retailerPriPhone','retailerSecPhone','retailerPassword']

class RetailerAddressUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(RetailerAddressUpdateForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['shopAddress'].required = False
        self.fields['shopPincode'].required = False

    class Meta():
        model= retailer
        fields=['shopAddress','shopPincode']

class CustomerAddressUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(CustomerAddressUpdateForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['customerAddress'].required = False
        self.fields['customerPincode'].required = False

    class Meta():
        model= customerContact
        fields=['customerAddress','customerPincode']



class CustomerRegistration(forms.ModelForm):

    class Meta():

        model= customer
        fields=['customerName','customerUserName','customerEmailID','password']


    def clean_customerUserName(self):
        customerUserName=self.cleaned_data.get('customerUserName')
        customeremail = self.cleaned_data.get('customerEmailID')
        users=customer.objects.all()
        for i in users:
            if(i.customerUserName==customerUserName):
                print "User already exists, Please insert different UserName."
                raise forms.ValidationError("User already exists, Please insert different UserName.")
        return customerUserName


class RetailerRegistration(forms.ModelForm):

    class Meta():

        model= retailer
        fields=['shopID','shopName','retailerEmailID','retailerPriPhone','retailerPassword']

    def clean_shopID(self):

        shopID = self.cleaned_data.get('shopID')
        users=retailer.objects.all()
        for i in users:
            print i.shopID,shopID
            if(i.shopID==shopID):
                print "User already exists, Please insert different UserName."
                raise forms.ValidationError("User already exists, Please insert different UserName.")
        return shopID

    def clean_retailerPriPhone(self):
        retailerPriPhone=self.cleaned_data.get('retailerPriPhone')
        if not( re.match(r'^[6-9]\d{9}$', retailerPriPhone)):
            print "Mobile Number is not valid, Please insert 10 digit valid Mobile Number"
            raise forms.ValidationError("Mobile Number is not valid, Please insert 10 digit valid Mobile Number")
        return retailerPriPhone
