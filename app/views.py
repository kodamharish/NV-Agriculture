from unicodedata import category
from django.shortcuts import render, redirect, reverse, get_object_or_404
from pyparsing import empty
from .models import *
from .forms import *
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate

import requests
from .tokens import get_tokens_for_user
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

#<-----For check user is Admin, Visitor and Officer----->#
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_visitor(user):
    return user.groups.filter(name='VISITOR').exists()

def is_farmer(user):
    return user.groups.filter(name='FARMER').exists()

def is_mentor(user):
    return user.groups.filter(name='MENTOR').exists()
def is_officer(user):
    return user.groups.filter(name='OFFICER').exists()
def is_seller(user):
    return user.groups.filter(name='SELLER').exists()

#<-----LogOut For All----->#
def logout_view(request):
    logout(request)
    return redirect('/')

#<-------------------------------------------->#
#<---------------Admin Functions-------------->#
#<-------------------------------------------->#


#<-----Login For Admin----->#
def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.groups.filter(name='ADMIN'):
                    login(request,user)
                    return redirect('admin_home')
                else:
                    messages.success(request, 'Your account is not found in Admin..')
            else:
                messages.success(request, 'Your Username and Password is Wrong..')
    else:
         form = AdminLoginForm()           
    return render(request, 'admin/admin_login.html',{'form':form})


#<-----Home Page for Admin----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_home(request):
    return render(request, 'admin/admin_home.html')

#<-----Profile Page for Admin----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_profile(request):
    return render(request, 'admin/admin_profile.html')

#<-----Change password----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def change_password_admin(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('admin_home')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'admin/change_password_admin.html', {'form': form})

#<-----Admin Approvall for visitors----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_approve_visitor(request):
    visitors = Visitor.objects.all().filter(status=False)
    return render(request, 'admin/admin_approve_visitor.html',{'visitors':visitors})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def approve_visitor(request):
    visitor=get_object_or_404(Visitor, pk=request.GET.get('visitor_id'))
    visitor.status=True
    visitor.save()
    return redirect(reverse('admin_approve_visitor'))

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_visitor(request):
    visitor=get_object_or_404(Visitor, pk=request.GET.get('visitor_id'))
    user=User.objects.get(id=visitor.user_id)
    user.delete()
    visitor.delete()
    return redirect(reverse('admin_approve_visitor'))


#<-----Admin Approvall for farmers----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_approve_farmer(request):
    farmers = Farmer.objects.all().filter(status=False)
    return render(request, 'admin/admin_approve_farmer.html',{'farmers':farmers})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def approve_farmer(request):
    farmer=get_object_or_404(Farmer, pk=request.GET.get('farmer_id'))
    farmer.status=True
    farmer.save()
    return redirect(reverse('admin_approve_farmer'))

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_farmer(request):
    farmer=get_object_or_404(Farmer, pk=request.GET.get('farmer_id'))
    user=User.objects.get(id=farmer.user_id)
    user.delete()
    farmer.delete()
    return redirect(reverse('admin_approve_farmer'))

#<-----Admin Approvall for sellers----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_approve_seller(request):
    sellers = Seller.objects.all().filter(status=False)
    return render(request, 'admin/admin_approve_seller.html',{'sellers':sellers})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def detail_seller(request, id):
    sellers = Seller.objects.all().get(id=id)
    data={'sellers':sellers}
    return render(request, 'admin/detail_seller.html',data)

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def approve_seller(request):
    seller=get_object_or_404(Seller, pk=request.GET.get('seller_id'))
    seller.status=True
    seller.save()
    return redirect(reverse('admin_approve_seller'))

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_seller(request):
    seller=get_object_or_404(Seller, pk=request.GET.get('seller_id'))
    user=User.objects.get(id=seller.user_id)
    user.delete()
    seller.delete()
    return redirect(reverse('admin_approve_seller'))

#<-----Admin Approvall for officer----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_approve_officer(request):
    officers = Officer.objects.all().filter(status=False)
    return render(request, 'admin/admin_approve_officer.html',{'officers':officers})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def approve_officer(request):
    officer=get_object_or_404(Officer, pk=request.GET.get('officer_id'))
    officer.status=True
    officer.save()
    return redirect(reverse('admin_approve_officer'))

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_officer(request):
    officer=get_object_or_404(Officer, pk=request.GET.get('officer_id'))
    user=User.objects.get(id=officer.user_id)
    user.delete()
    officer.delete()
    return redirect('admin_approve_officer')

#<-----Admin add Admin----->#
def admin_add_admin(request):
    if request.method=='POST':
        form1=AdminUserForm(request.POST)
        form2=AdminExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_admin_group=Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('admin_active_admin')
    else:
        form1=AdminUserForm()
        form2=AdminExtraForm()
    return render(request, 'admin/admin_add_admin.html',{'form1':form1,'form2':form2})

#<-----Active Admin View for Admin----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_active_admin(request):
    admins = Admin.objects.all()
    return render(request, 'admin/admin_active_admin.html',{'admins':admins})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_admin_active(request):
    admin=get_object_or_404(Admin, pk=request.GET.get('admin_id'))
    user=User.objects.get(id=admin.user_id)
    user.delete()
    admin.delete()
    return redirect(reverse('admin_active_admin'))

#<-----Active Visitor View for Admin----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_active_visitor(request):
    visitors = Visitor.objects.all().filter(status=True)
    return render(request, 'admin/admin_active_visitor.html',{'visitors':visitors})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_visitor_active(request):
    visitor=get_object_or_404(Visitor, pk=request.GET.get('visitor_id'))
    user=User.objects.get(id=visitor.user_id)
    user.delete()
    visitor.delete()
    return redirect(reverse('admin_active_visitor'))

#<-----Active Farmer View for Admin----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_active_farmer(request):
    farmers = Farmer.objects.all().filter(status=True)
    return render(request, 'admin/admin_active_farmer.html',{'farmers':farmers})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_farmer_active(request):
    farmer=get_object_or_404(Farmer, pk=request.GET.get('farmer_id'))
    user=User.objects.get(id=farmer.user_id)
    user.delete()
    farmer.delete()
    return redirect(reverse('admin_active_farmer'))

#<-----Active Seller View for Admin----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_active_seller(request):
    sellers = Seller.objects.all().filter(status=True)
    return render(request, 'admin/admin_active_seller.html',{'sellers':sellers})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def detail_active_seller(request, id):
    products=''
    sellers = Seller.objects.all().get(id=id)
    products = Product.objects.all().filter(seller=id,status=True)
    data={'sellers':sellers,'products':products}
    return render(request, 'admin/detail_active_seller.html',data)

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_seller_active(request):
    seller=get_object_or_404(Seller, pk=request.GET.get('seller_id'))
    user=User.objects.get(id=seller.user_id)
    user.delete()
    seller.delete()
    return redirect(reverse('admin_active_seller'))

#<-----Active Officer View for Admin----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_active_officer(request):
    officers = Officer.objects.all().filter(status=True)
    return render(request, 'admin/admin_active_officer.html',{'officers':officers})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_officer_active(request):
    officer=get_object_or_404(Officer, pk=request.GET.get('officer_id'))
    user=User.objects.get(id=officer.user_id)
    user.delete()
    officer.delete()
    return redirect(reverse('admin_active_officer'))

#<-----Admin active product page----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_product(request):
    products = Product.objects.all().filter(status=True)
    return render(request, 'admin/admin_product.html',{'products':products})

#<-----admin Detail view of product----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def detail_product_admin(request, id):
    products = Product.objects.all().get(id=id)
    return render(request, 'admin/detail_product_admin.html',{'products':products})

#<-----Admin active product page----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_request_product(request):
    products = Product.objects.all().filter(status=False)
    return render(request, 'admin/admin_request_product.html',{'products':products})

#<-----admin Detail view of product----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def detail_request_product_admin(request, id):
    products = Product.objects.all().get(id=id)
    return render(request, 'admin/detail_request_product_admin.html',{'products':products})

#<-----Admin approve product----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def product_approve(request):
    product=get_object_or_404(Product, pk=request.GET.get('product_id'))
    product.status=True
    product.save()
    return redirect(reverse('admin_request_product'))

#<-----admin delete product----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def product_delete(request):
    product=get_object_or_404(Product, pk=request.GET.get('product_id'))
    product.delete()
    return redirect(reverse('admin_request_product'))

#<-----admin inactive product----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def inactive(request):
    product=get_object_or_404(Product, pk=request.GET.get('product_id'))
    product.activity=False
    product.save()
    return redirect(reverse('admin_product'))

#<-----admin active product----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def active(request):
    product=get_object_or_404(Product, pk=request.GET.get('product_id'))
    product.activity=True
    product.save()
    return redirect(reverse('admin_product'))

#<-----admin delete approved product----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def approve_product_delete(request):
    product=get_object_or_404(Product, pk=request.GET.get('product_id'))
    product.delete()
    return redirect(reverse('admin_product'))

#<---------------------------------------------->#
#<---------------Visitor Functions-------------->#
#<---------------------------------------------->#

#<-----Signup For Visitor----->#
def visitor_signup(request):
    if request.method=='POST':
        form1=VisitorUserForm(request.POST)
        form2=VisitorExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_visitor_group=Group.objects.get_or_create(name='VISITOR')
            my_visitor_group[0].user_set.add(user)

            messages.success(request, 'Request send for approval, Try Login after 24 Hours..')

            return HttpResponseRedirect('/')
    else:
        form1=VisitorUserForm()
        form2=VisitorExtraForm()
    return render(request, 'visitor/visitor_signup.html',{'form1':form1,'form2':form2})





#<-----APIs----->#

from django.contrib.auth.hashers import check_password

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):  # Using Django's password checking
                tokens = get_tokens_for_user(user)
                return Response(tokens, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        




class TokenRefreshView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh = request.data.get('refresh')
        if refresh:
            try:
                token = RefreshToken(refresh)
                return Response({
                    'access': str(token.access_token),
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)





class TokenVerifyView(APIView):
    
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get('token')
        if token:
            try:
                # Attempt to validate as an AccessToken first
                AccessToken(token)
                return Response(status=status.HTTP_200_OK)
            except Exception:
                try:
                    # If it fails, try validating as a RefreshToken
                    RefreshToken(token)
                    return Response(status=status.HTTP_200_OK)
                except Exception:
                    return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

#<-----Signup For Farmer----->#
def farmer_signup(request):
    if request.method=='POST':
        form1=FarmerUserForm(request.POST)
        form2=FarmerExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_farmer_group=Group.objects.get_or_create(name='FARMER')
            my_farmer_group[0].user_set.add(user)

            messages.success(request, 'Request send for approval, Try Login after 24 Hours..')

            return HttpResponseRedirect('/')
    else:
        form1=FarmerUserForm()
        form2=FarmerExtraForm()
    return render(request, 'farmer/farmer_signup.html',{'form1':form1,'form2':form2})


BASE_API_URL = 'http://127.0.0.1:8100/'


#<-----Login For Farmer----->#
def farmer_login_error(request):
    if request.method == 'POST':
        form = FarmerLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            data = {'username': username,'password': password,}
            response = requests.post(f'{BASE_API_URL}api/login/', data=data)
            
            

            if response.status_code == 200 and user.groups.filter(name='FARMER'):
                # Assuming the response contains the access token in JSON format
                token_data = response.json()
                access_token = token_data.get('access')
                print(access_token,'login access_token ')

                if access_token:
                    # Store the access token in the session
                    request.session['access_token'] = access_token
                    print("Access token stored, redirecting to farmer_home...")

                    messages.success(request, 'Logged in successfully!')
                    
                    return redirect('farmer_home')

                    #return redirect(reverse('farmer_home'))
                else:
                    messages.error(request, 'Login failed: Access token not found.')
            else:
                messages.error(request, 'Login failed: {}'.format(response.json().get('message', 'Invalid credentials')))
    else:
         form = FarmerLoginForm()           
    return render(request, 'farmer/farmer_login.html',{'form':form})




def farmer_login(request):
    if request.method == 'POST':
        form = FarmerLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            data = {'username': username, 'password': password}
            response = requests.post(f'{BASE_API_URL}api/login/', data=data)

            #print(user,'user')

            if response.status_code == 200 :
                token_data = response.json()
                access_token = token_data.get('access')

                if user:
                    if user.groups.filter(name='FARMER'):
                        if Farmer.objects.all().filter(user_id=user.id,status=True):
                            if access_token:
                                #request.session['access_token'] = access_token
                                # Ignore the 'next' parameter and force redirection to 'mentor_home'
                                #return render(request,'farmer/farmer_home.html')
                                login(request,user)
                                #print(access_token,'access_token')
                                messages.success(request, 'Logged in successfully!')
                                return redirect('farmer_home')

                            else:
                                messages.error(request, 'Login failed: Access token not found.')
                            login(request,user)
                            return redirect('farmer_home')
                        else:
                          messages.success(request, 'Your Request is in process, please wait for Approval..') 
                    else:
                        messages.success(request, 'Your account is not found in Farmer..')
                else:
                   messages.success(request, 'Your Username and Password is Wrong..')   
            else:
                messages.error(request, 'Login failed: {}'.format(response.json().get('message', 'Invalid credentials')))
    else:
        form = FarmerLoginForm()

    return render(request, 'farmer/farmer_login.html', {'form': form})

#<-----Login For Farmer----->#
def farmer_login_old(request):
    if request.method == 'POST':
        form = FarmerLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            
            
            if user:
                if user.groups.filter(name='FARMER'):
                    if Farmer.objects.all().filter(user_id=user.id,status=True):
                        login(request,user)
                        return redirect('farmer_home')
                    else:
                       messages.success(request, 'Your Request is in process, please wait for Approval..') 
                else:
                    messages.success(request, 'Your account is not found in Visitor..')
            else:
                messages.success(request, 'Your Username and Password is Wrong..')

            
    else:
         form = FarmerLoginForm()           
    return render(request, 'farmer/farmer_login.html',{'form':form})



#<-----Signup For Mentor----->#
def mentor_signup(request):
    if request.method=='POST':
        form1=MentorUserForm(request.POST)
        form2=MentorExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_mentor_group=Group.objects.get_or_create(name='MENTOR')
            my_mentor_group[0].user_set.add(user)

            messages.success(request, 'Request send for approval, Try Login after 24 Hours..')

            return HttpResponseRedirect('/')
    else:
        form1=MentorUserForm()
        form2=MentorExtraForm()
    return render(request, 'mentor/mentor_signup.html',{'form1':form1,'form2':form2})




#<-----Login For Mentor----->#
def mentor_login(request):
    if request.method == 'POST':
        form = MentorLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            data = {'username': username, 'password': password}
            response = requests.post(f'{BASE_API_URL}api/login/', data=data)
            if response.status_code == 200 :
                token_data = response.json()
                access_token = token_data.get('access')
                print(access_token,'acess_token')
                if user:
                    if user.groups.filter(name='MENTOR'):
                        if Mentor.objects.all().filter(user_id=user.id,status=True):
                            if access_token:

                                login(request,user)
                                return redirect('mentor_home')
                            else:
                                messages.error(request, 'Login failed: Access token not found.')
                        else:
                         messages.success(request, 'Your Request is in process, please wait for Approval..') 
                    else:
                        messages.success(request, 'Your account is not found in Mentor..')
                else:
                    messages.success(request, 'Your Username and Password is Wrong..')
            else:
               messages.error(request, 'Login failed: {}'.format(response.json().get('message', 'Invalid credentials')))    
    else:
         form = MentorLoginForm()           
    return render(request, 'mentor/mentor_login.html',{'form':form})


def mentor_login_old(request):
    if request.method == 'POST':
        form = MentorLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.groups.filter(name='MENTOR'):
                    if Mentor.objects.all().filter(user_id=user.id,status=True):
                        login(request,user)
                        return redirect('mentor_home')
                    else:
                       messages.success(request, 'Your Request is in process, please wait for Approval..') 
                else:
                    messages.success(request, 'Your account is not found in Visitor..')
            else:
                messages.success(request, 'Your Username and Password is Wrong..')
    else:
         form = MentorLoginForm()           
    return render(request, 'mentor/mentor_login.html',{'form':form})

#<-----Login For Visitor----->#
def visitor_login(request):
    if request.method == 'POST':
        form = VisitorLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.groups.filter(name='VISITOR'):
                    if Visitor.objects.all().filter(user_id=user.id,status=True):
                        login(request,user)
                        return redirect('visitor_home')
                    else:
                       messages.success(request, 'Your Request is in process, please wait for Approval..') 
                else:
                    messages.success(request, 'Your account is not found in Visitor..')
            else:
                messages.success(request, 'Your Username and Password is Wrong..')
    else:
         form = VisitorLoginForm()           
    return render(request, 'visitor/visitor_login.html',{'form':form})

#<-----Home Page for Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_home(request):
    return render(request, 'visitor/visitor_home.html')


#<-----Home Page for Farmer----->#
@login_required(login_url='farmer_login')
@user_passes_test(is_farmer)
def farmer_home_old(request):
    return render(request, 'farmer/farmer_home.html')


from django.shortcuts import render
from .models import PH
from collections import defaultdict
import json

@login_required(login_url='farmer_login')
@user_passes_test(is_farmer)
def farmer_home(request):
    # Fetch all pH data from the database
    ph_data = PH.objects.all()

    # Group data by date and time
    data_by_date = defaultdict(list)
    timestamps_by_date = defaultdict(list)

    for entry in ph_data:
        date_str = entry.time_stamp.strftime('%Y-%m-%d')
        time_str = entry.time_stamp.strftime('%H:%M')
        data_by_date[date_str].append(float(entry.ph_value))
        timestamps_by_date[date_str].append(time_str)

    # Prepare the data to be used in JavaScript
    chart_data = {
        'data_by_date': data_by_date,
        'timestamps_by_date': timestamps_by_date,
    }
    
    context = {
        'chart_data': json.dumps(chart_data),
        'default_date': next(iter(data_by_date)) if data_by_date else ''
    }

    return render(request, 'farmer/farmer_home.html', context)



#<-----Home Page for Mentor----->#
@login_required(login_url='mentor_login')
@user_passes_test(is_mentor)
def mentor_home(request):
    return render(request, 'mentor/mentor_home.html')

#<-----Profile Page for Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_profile(request):
    return render(request, 'visitor/visitor_profile.html')

#<-----Change password----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def change_password_visitor(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('visitor_home')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'visitor/change_password_visitor.html', {'form': form})

#<-----Add soil By Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_add_soil(request):
    if request.method=='POST':
        form=SoilAddForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.save()

            messages.success(request, 'Your Contibution send for Verification, If detail is genuine it may reflect in Soil after 24 Hours..')

            return HttpResponseRedirect('visitor_home')
    else:
        form=SoilAddForm()
    return render(request, 'visitor/visitor_add_soil.html',{'form':form})

def load_regions(request):
    district_id = request.GET.get('district_id')
    regions = Region.objects.filter(district_id=district_id).all()
    return render(request, 'dropdown_list_region.html', {'regions':regions})

#<-----Find Soil for Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_find_soil(request):
    soils = None
    if request.method == 'POST':
        form = FindSoilForm(request.POST)
        if form.is_valid():
            district = request.POST['district']
            soils = SoilLocationDetail.objects.all().filter(district=district, status=True)
    else:
        form = FindSoilForm()
    return render(request, 'visitor/visitor_find_soil.html',{'form':form,'soils':soils})

#<-----Find Soil Detail for Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_find_soil_detail(request):
    soils = None
    if request.method == 'POST':
        form = FindSoilDetailForm(request.POST)
        if form.is_valid():
            soil = request.POST['soil']
            soils = SoilDetail.objects.all().filter(soil=soil)
    else:
        form = FindSoilDetailForm()
    return render(request, 'visitor/visitor_find_soil_detail.html',{'form':form,'soils':soils})

#<-----Find Rainfall for Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_find_rainfall(request):
    rainfalls = None
    if request.method == 'POST':
        form = FindRainfallForm(request.POST)
        if form.is_valid():
            district = request.POST['district']
            rainfalls = RainfallDetail.objects.all().order_by('year').filter(district=district)
    else:
        form = FindRainfallForm()
    return render(request, 'visitor/visitor_find_rainfall.html',{'form':form,'rainfalls':rainfalls})

#<-----Find Crop for Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_find_crop(request):
    result=''

    if request.method == 'POST':
        form = FindCropForm(request.POST)
            
        nitrogen = request.POST['nitrogen']
        phosphorus = request.POST['phosphorus']
        potassium = request.POST['potassium']
        temperature = request.POST['temperature']
        humidity = request.POST['humidity']
        ph = request.POST['ph']
        rainfall = request.POST['rainfall']

        df = pd.read_csv("Mechine Learning\Crop_recommendation.csv")

        features = df[['N', 'P','K','temperature', 'humidity', 'ph', 'rainfall']]
        target = df['label']
        #features = df[['temperature', 'humidity', 'ph', 'rainfall']]
        labels = df['label']

        # Initialzing empty lists to append all model's name and corresponding name
        acc = []
        model = []

        # Splitting into train and test data
        Xtrain, Xtest, Ytrain, Ytest = train_test_split(features,target,test_size = 0.2,random_state =2)

        RF = RandomForestClassifier(n_estimators=20, random_state=0)
        RF.fit(Xtrain.values,Ytrain.values)

        predicted_values = RF.predict(Xtest.values)

        x = metrics.accuracy_score(Ytest, predicted_values)
        acc.append(x)
        model.append('RF')

        data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
        prediction = RF.predict(data)
        result = "The predicted crop is "+ str(prediction).replace("'","")[1:-1]

    else:
        form=FindCropForm()
    return render(request, 'visitor/visitor_find_crop.html',{'form':form,'result':result})

#<-----Request seed by Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_get_seed(request):
    if request.method=='POST':
        form=RequestSeedForm(request.POST)
        if form.is_valid():
            
            username = request.user.username
            name = request.user.visitor.get_name
            email = request.user.visitor.email
            district = str(request.user.visitor.district)
            gender = request.user.visitor.gender
            address = request.POST.get('address')
            crop = request.POST.get('crop')
            quantity = request.POST.get('quantity')

            req=RequestSeed.objects.create(username=username, name=name, email=email, district=district, gender=gender, address=address, crop=crop, quantity=quantity)
            req.save()
            
            messages.success(request, 'Your application in process it may take some time..')

            return HttpResponseRedirect('visitor_home')
    else:
        form=RequestSeedForm()
    return render(request, 'visitor/visitor_get_seed.html',{'form':form})

#<-----Request seed by Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_get_fertilizer(request):
    if request.method=='POST':
        form=RequestFertilizerForm(request.POST)
        if form.is_valid():
            
            username = request.user.username
            name = request.user.visitor.get_name
            email = request.user.visitor.email
            district = str(request.user.visitor.district)
            gender = request.user.visitor.gender
            address = request.POST.get('address')
            fertilizer = request.POST.get('fertilizer')
            quantity = request.POST.get('quantity')

            req=RequestFertilizer.objects.create(username=username, name=name, email=email, district=district, gender=gender, address=address, fertilizer=fertilizer, quantity=quantity)
            req.save()
            
            messages.success(request, 'Your application in process it may take some time..')

            return HttpResponseRedirect('visitor_home')
    else:
        form=RequestFertilizerForm()
    return render(request, 'visitor/visitor_get_fertilizer.html',{'form':form})

#<-----Application for seed request view by Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_seed_request(request):
    username=request.user.username
    seeds = RequestSeed.objects.all().filter(username=username)
    return render(request, 'visitor/visitor_seed_request.html',{'seeds':seeds})

#<-----Application for fertilizer request view by Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_fertilizer_request(request):
    username=request.user.username
    ferts = RequestFertilizer.objects.all().filter(username=username)
    return render(request, 'visitor/visitor_fertilizer_request.html',{'ferts':ferts})

#<-----Visitor Virtual Market Home----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_market_home(request):
    seller = Seller.objects.all().filter(status=True)
    visitor = request.user.visitor
    cart_count = Cart.objects.all().filter(visitor=visitor).count()
    order_count = Order.objects.all().filter(visitor=visitor, payment=False).count()
    pay_count = Order.objects.all().filter(visitor=visitor, payment=True).count()
    return render(request, 'visitor/visitor_market_home.html',{'seller':seller,'cart_count':cart_count,'order_count':order_count,'pay_count':pay_count})

#<-----Visitor Virtual Market Search----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def search(request):
    search=''
    product=''
    if request.method=='POST':
        search = request.POST.get('search')
        product = Product.objects.all().filter(status=True,activity=True,product_name=search)
    return render(request, 'visitor/search.html',{'search':search,'product':product})

#<-----Visitor Virtual Market Vegitable category----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def vegetable_cat(request):
    veg = Product.objects.all().filter(status=True,activity=True,category="Vegetable")
    return render(request, 'visitor/vegetable_cat.html',{'veg':veg})

#<-----Visitor Virtual Market Fruits category----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def fruit_cat(request):
    fru = Product.objects.all().filter(status=True,activity=True,category="Fruit")
    return render(request, 'visitor/fruit_cat.html',{'fru':fru})

#<-----Visitor Virtual Market Seeds category----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def seed_cat(request):
    seed = Product.objects.all().filter(status=True,activity=True,category="Seed")
    return render(request, 'visitor/seed_cat.html',{'seed':seed})

#<-----Visitor Virtual Market Bio Fertilizer category----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def bio_cat(request):
    bio = Product.objects.all().filter(status=True,activity=True,category="Bio Fertilizer")
    return render(request, 'visitor/bio_cat.html',{'bio':bio})

#<-----Visitor Virtual Market Nuts category----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def nut_cat(request):
    nut = Product.objects.all().filter(status=True,activity=True,category="Nuts")
    return render(request, 'visitor/nut_cat.html',{'nut':nut})

#<-----Visitor Virtual Market Spices category----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def spices_cat(request):
    spi = Product.objects.all().filter(status=True,activity=True,category="Spices")
    return render(request, 'visitor/spices_cat.html',{'spi':spi})

#<-----Visitor Detail view of product----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def view_product_visitor(request, id):
    visitor = request.user.visitor
    products = Product.objects.all().get(id=id)
    cart = Cart.objects.all().filter(visitor=visitor).first()
    return render(request, 'visitor/view_product_visitor.html',{'products':products,'cart':cart})

#<-----add to cart----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def add_cart(request, id):
    product = Product.objects.all().get(id=id)
    visitor = request.user.visitor
    req=Cart.objects.create(product=product, visitor=visitor)
    req.save()
    return redirect(reverse('visitor_market_home'))

#<-----cart view----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def cart(request):
    visitor = request.user.visitor
    cart = Cart.objects.all().filter(visitor=visitor)
    return render(request, 'visitor/cart.html',{'cart':cart})

#<-----delete cart----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def delete_cart(request):
    cart=get_object_or_404(Cart, pk=request.GET.get('cart_id'))
    cart.delete()
    return redirect(reverse('cart'))

#<-----Order page----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_order(request, id):
    product = Product.objects.all().get(id=id)
    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            product = Product.objects.all().get(id=id)
            visitor = request.user.visitor
            address = request.POST.get('address')
            quantity = request.POST.get('quantity')
            req=Order.objects.create(product=product, visitor=visitor, address=address, quantity=quantity)
            req.save()
            cart = Cart.objects.all().filter(product=id)
            if cart is not empty:
                cart.delete()
            return redirect('pending_order')
    else:
        form=OrderForm()
    return render(request, 'visitor/visitor_order.html',{'product':product, 'form':form})

#<-----Order confirm page----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_order_confirm(request, id):
    order = Order.objects.all().get(id=id)
    if request.method=='POST':
        order = Order.objects.all().get(id=id)
        name = request.POST.get('cardname')
        card_number = request.POST.get('cardnumber')
        month = request.POST.get('month')
        year = request.POST.get('year')
        cvv_number = request.POST.get('cvv')
        amount = int(order.quantity) * int(order.product.price) + 25
        req = Pay.objects.create(order=order, name=name, card_number=card_number, month=month, year=year, cvv_number=cvv_number, amount=amount)
        req.save()
        order.payment=True
        order.save()
        return redirect('your_order')
    return render(request, 'visitor/visitor_order_confirm.html',{'order':order})

#<-----cart view----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def pending_order(request):
    visitor = request.user.visitor
    order = Order.objects.all().filter(visitor=visitor, payment=False)
    return render(request, 'visitor/pending_order.html',{'order':order})

#<-----Remove order from pending order----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def remove_order(request):
    order=get_object_or_404(Order, pk=request.GET.get('order_id'))
    order.delete()
    return redirect(reverse('pending_order'))

#<-----View your order----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def your_order(request):
    visitor=request.user.visitor
    order = Order.objects.all().filter(visitor=visitor, payment=True)
    pay = Pay.objects.all().filter(order__in=order)
    zippedList = zip(order, pay)
    return render(request, 'visitor/your_order.html',{'zippedList':zippedList})

#<-----Cancel order----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def cancel_order(request):
    order=get_object_or_404(Order, pk=request.GET.get('order_id'))
    order.order=False
    order.save()
    return redirect(reverse('your_order'))

@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_view_seller(request, id):
    products=''
    sellers = Seller.objects.all().get(id=id)
    products = Product.objects.all().filter(seller=id,status=True)
    data={'sellers':sellers,'products':products}
    return render(request, 'visitor/visitor_view_seller.html',data)

#<---------------------------------------------->#
#<---------------Officer Functions-------------->#
#<---------------------------------------------->#

#<-----Signup For Officer----->#
def officer_signup(request):
    if request.method=='POST':
        form1=OfficerUserForm(request.POST)
        form2=OfficerExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_visitor_group=Group.objects.get_or_create(name='OFFICER')
            my_visitor_group[0].user_set.add(user)

            messages.success(request, 'Request send for approval, Try Login after 24 Hours..')

            return HttpResponseRedirect('/')
    else:
        form1=OfficerUserForm()
        form2=OfficerExtraForm()
    return render(request, 'officer/officer_signup.html',{'form1':form1,'form2':form2})

#<-----Login For Officer----->#
def officer_login(request):
    if request.method == 'POST':
        form = OfficerLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.groups.filter(name='OFFICER'):
                    if Officer.objects.all().filter(user_id=user.id,status=True):
                        login(request,user)
                        return redirect('officer_home')
                    else:
                       messages.success(request, 'Your Request is in processing, please wait for Approval..') 
                else:
                    messages.success(request, 'Your account is not found..')
            else:
                messages.success(request, 'Invalid Username and Password..')
    else:
         form = OfficerLoginForm()           
    return render(request, 'officer/officer_login.html',{'form':form})

#<-----Home Page for Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_home(request):
    return render(request, 'officer/officer_home.html')

#<-----Profile Page for Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_profile(request):
    return render(request, 'officer/officer_profile.html')

#<-----Change password----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def change_password_officer(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('officer_home')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'officer/change_password_officer.html', {'form': form})

#<-----Active Soils View for Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_active_soil(request):
    soils = SoilLocationDetail.objects.all().filter(status=True)
    return render(request, 'officer/officer_active_soil.html',{'soils':soils})

@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def delete_soil_active(request):
    soil=get_object_or_404(SoilLocationDetail, pk=request.GET.get('soil_id'))
    soil.delete()
    return redirect(reverse('officer_active_soil'))

#<-----Add soil By Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_add_soil(request):
    if request.method=='POST':
        form=SoilAddForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.status=True
            user.save()

            messages.success(request, 'Locations Soil Details Added Sucssesfully..')

            return HttpResponseRedirect('officer_active_soil')
    else:
        form=SoilAddForm()
    return render(request, 'officer/officer_add_soil.html',{'form':form})

#<-----Active Detail of Soil View for Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_active_soil_detail(request):
    soils = SoilDetail.objects.all()
    return render(request, 'officer/officer_active_soil_detail.html',{'soils':soils})

@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def delete_soil_detail_active(request):
    soil=get_object_or_404(SoilDetail, pk=request.GET.get('soil_id'))
    soil.delete()
    return redirect(reverse('officer_active_soil_detail'))

#<-----Add soil Detail By Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_add_soil_detail(request):
    if request.method=='POST':
        form=SoilDetailAddForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.save()

            messages.success(request, 'Soil Detail Save Sucssesfully..')

            return HttpResponseRedirect('officer_active_soil_detail')
    else:
        form=SoilDetailAddForm()
    return render(request, 'officer/officer_add_soil_detail.html',{'form':form})

#<-----Active Detail of Rainfall View for Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_active_rainfall(request):
    rainfalls = RainfallDetail.objects.all()
    return render(request, 'officer/officer_active_rainfall.html',{'rainfalls':rainfalls})

@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def delete_rainfall_active(request):
    rainfall=get_object_or_404(RainfallDetail, pk=request.GET.get('rainfall_id'))
    rainfall.delete()
    return redirect(reverse('officer_active_rainfall'))

#<-----Add Rainfall Detail By Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_add_rainfall(request):
    if request.method=='POST':
        form=RainfallDetailAddForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.save()

            messages.success(request, 'Rainfall Detail Save Sucssesfully..')

            return HttpResponseRedirect('officer_active_rainfall')
    else:
        form=RainfallDetailAddForm()
    return render(request, 'officer/officer_add_rainfall.html',{'form':form})

#<-----Request for seed View for Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_seed_request(request):
    seeds = RequestSeed.objects.all().filter(reject=False, approve=False)
    return render(request, 'officer/officer_seed_request.html',{'seeds':seeds})

@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def reject_seed_request(request):
    seed=get_object_or_404(RequestSeed, pk=request.GET.get('seed_id'))
    seed.reject=True
    seed.approve=False
    seed.save()
    return redirect(reverse('officer_seed_request'))

@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def approve_seed_request(request):
    seed=get_object_or_404(RequestSeed, pk=request.GET.get('seed_id'))
    seed.reject=False
    seed.approve=True
    seed.save()
    return redirect(reverse('officer_seed_request'))

#<-----Approved seed request for seed for officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_approve_seed_request(request):
    seeds = RequestSeed.objects.all().filter(reject=False, approve=True)
    return render(request, 'officer/officer_approve_seed_request.html',{'seeds':seeds})

#<-----Rejected seed request for seed for officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_reject_seed_request(request):
    seeds = RequestSeed.objects.all().filter(reject=True, approve=False)
    return render(request, 'officer/officer_reject_seed_request.html',{'seeds':seeds})

#<-----Request for fertilizer View for Officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_fertilizer_request(request):
    ferts = RequestFertilizer.objects.all().filter(reject=False, approve=False)
    return render(request, 'officer/officer_fertilizer_request.html',{'ferts':ferts})

@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def reject_fertilizer_request(request):
    fertilizer=get_object_or_404(RequestFertilizer, pk=request.GET.get('fertilizer_id'))
    fertilizer.reject=True
    fertilizer.approve=False
    fertilizer.save()
    return redirect(reverse('officer_fertilizer_request'))

@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def approve_fertilizer_request(request):
    fertilizer=get_object_or_404(RequestFertilizer, pk=request.GET.get('fertilizer_id'))
    fertilizer.reject=False
    fertilizer.approve=True
    fertilizer.save()
    return redirect(reverse('officer_fertilizer_request'))

#<-----Approved fertilizer request for seed for officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_approve_fertilizer_request(request):
    ferts = RequestFertilizer.objects.all().filter(reject=False, approve=True)
    return render(request, 'officer/officer_approve_fertilizer_request.html',{'ferts':ferts})

#<-----Rejected fertilizer request for seed for officer----->#
@login_required(login_url='officer_login')
@user_passes_test(is_officer)
def officer_reject_fertilizer_request(request):
    ferts = RequestFertilizer.objects.all().filter(reject=True, approve=False)
    return render(request, 'officer/officer_reject_fertilizer_request.html',{'ferts':ferts})

#<--------------------------------------------->#
#<---------------Seller Functions-------------->#
#<--------------------------------------------->#

#<-----Signup For Seller----->#
def seller_signup(request):
    if request.method=='POST':
        form1=SellerUserForm(request.POST)
        form2=SellerExtraForm(request.POST,request.FILES)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_seller_group=Group.objects.get_or_create(name='SELLER')
            my_seller_group[0].user_set.add(user)

            messages.success(request, 'Request send for process, please wait for Approval..')

            return HttpResponseRedirect('/')
    else:
        form1=SellerUserForm()
        form2=SellerExtraForm()
    return render(request, 'seller/seller_signup.html',{'form1':form1,'form2':form2})

#<-----Login For Seller----->#
def seller_login(request):
    if request.method == 'POST':
        form = SellerLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.groups.filter(name='SELLER'):
                    if Seller.objects.all().filter(user_id=user.id,status=True):
                        login(request,user)
                        return redirect('seller_home')
                    else:
                       messages.success(request, 'Your Request is in process, please wait for Approval..') 
                else:
                    messages.success(request, 'Your account is not found in Seller..')
            else:
                messages.success(request, 'Your Username and Password is Wrong..')
    else:
         form = VisitorLoginForm()           
    return render(request, 'seller/seller_login.html',{'form':form})

#<-----Home Page for Seller----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def seller_home(request):
    return render(request, 'seller/seller_home.html')

#<-----Profile Page for Seller----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def seller_profile(request):
    return render(request, 'seller/seller_profile.html')

#<-----Change password----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def change_password_seller(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('seller_home')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'seller/change_password_seller.html', {'form': form})

#<-----Seller product page----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def product(request):
    products = Product.objects.all().filter(seller=request.user.seller.id)
    return render(request, 'seller/product.html',{'products':products})

#<-----Detail view of product----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def detail_product_seller(request, id):
    products = Product.objects.all().get(id=id)
    if request.method=='POST':
        form=EditPriceForm(request.POST)
        if form.is_valid():
            obj = Product.objects.all().get(id=id)
            obj.price = request.POST.get('price')
            obj.save()

            return HttpResponseRedirect('detail_product_seller')
    else:
        form=EditPriceForm()
    return render(request, 'seller/detail_product_seller.html',{'products':products,'form':form})

#<-----Seller add new product page----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def add_product(request):
    if request.method=='POST':
        form=ProductAddForm(request.POST, request.FILES)
        if form.is_valid():
            
            product_name = request.POST.get('product_name')
            describe = request.POST.get('describe')
            image_1 = request.FILES.get('image_1')
            image_2 = request.FILES.get('image_2')
            image_3 = request.FILES.get('image_3')
            image_4 = request.FILES.get('image_4')
            seller = str(request.user.seller.id)
            category=request.POST.get('category')
            price = request.POST.get('price')
            price_per_quantity = request.POST.get('price_per_quantity')

            req=Product.objects.create(product_name=product_name, describe=describe, image_1=image_1, image_2=image_2, image_3=image_3, image_4=image_4, seller_id = seller, category=category, price=price, price_per_quantity=price_per_quantity)
            req.save()

            return HttpResponseRedirect('seller_home')
    else:
        form=ProductAddForm()
    return render(request, 'seller/add_product.html',{'form':form})

#<-----Make out of stock----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def outofstock(request):
    product=get_object_or_404(Product, pk=request.GET.get('product_id'))
    product.stock=False
    product.save()
    return redirect(reverse('product'))

#<-----Make out of stock----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def instock(request):
    product=get_object_or_404(Product, pk=request.GET.get('product_id'))
    product.stock=True
    product.save()
    return redirect(reverse('product'))

#<-----Delete product----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def delete_product_seller(request):
    product=get_object_or_404(Product, pk=request.GET.get('product_id'))
    product.delete()
    return redirect(reverse('product'))

#<-----new order page----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def new_order_seller(request):
    orders = Order.objects.all().filter(payment=True, shipped=False, order=True)
    return render(request, 'seller/new_order_seller.html',{'orders':orders})

#<-----detail new order seller----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def detail_new_order_seller(request, id):
    order = Order.objects.all().get(id=id)
    pay = Pay.objects.all().get(order_id=order)
    return render(request, 'seller/detail_new_order_seller.html',{'order':order,'pay':pay})

#<-----Package Shipped----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def shipped_package(request):
    order=get_object_or_404(Order, pk=request.GET.get('order_id'))
    order.shipped=True
    order.save()
    return redirect(reverse('new_order_seller'))

#<-----Shipped Order----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def shipped_order_seller(request):
    orders = Order.objects.all().filter(payment=True, shipped=True, order=True)
    pay = Pay.objects.all().filter(order__in=orders)
    zippedList = zip(orders, pay)
    return render(request, 'seller/shipped_order_seller.html',{'zippedList':zippedList})

#<-----Package Shipped----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def delivered_order(request):
    order=get_object_or_404(Order, pk=request.GET.get('order_id'))
    order.shipped=False
    order.delivered=True
    order.order=False
    order.save()
    return redirect(reverse('shipped_order_seller'))

#<-----Delivered Order----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def delivered_order_seller(request):
    orders = Order.objects.all().filter(payment=True, delivered=True, order=False)
    pay = Pay.objects.all().filter(order__in=orders)
    zippedList = zip(orders, pay)
    return render(request, 'seller/delivered_order_seller.html',{'zippedList':zippedList})

#<-----Canceled Order----->#
@login_required(login_url='seller_login')
@user_passes_test(is_seller)
def canceled_order_seller(request):
    orders = Order.objects.all().filter(payment=True, delivered=False, order=False)
    pay = Pay.objects.all().filter(order__in=orders)
    zippedList = zip(orders, pay)
    return render(request, 'seller/canceled_order_seller.html',{'zippedList':zippedList})





from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from .models import Admin, District
from django.contrib import messages

def test(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        district_id = request.POST.get('district')

        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        
        if len(username) < 8:
            messages.error(request, 'Username length must be greater than 8 characters.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif len(password) < 8:
            messages.error(request, 'Password length must be greater than 8 characters.')
        elif not any(char.isdigit() for char in password):
            messages.error(request, 'Password must contain at least one digit.')
        elif not any(char in special_characters for char in password):
            messages.error(request, 'Password must contain at least one special character.')
        else:
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()
            
            admin = Admin(user=user, email=email, gender=gender, district=District.objects.get(id=district_id))
            admin.save()

            my_admin_group, created = Group.objects.get_or_create(name='ADMIN')
            my_admin_group.user_set.add(user)

            messages.success(request, 'Admin added successfully.')
            return HttpResponseRedirect('admin_active_admin')
    
    #gender_choices = Admin.GENDER_CHOICES
    districts = District.objects.all()

    context = {
        #'gender_choices': gender_choices,
        'districts': districts
    }

    return render(request, 'test.html', context)




def logout(request):
    request.session.flush()  # Clear the session data
    messages.success(request, 'You have been logged out successfully!')
    return redirect('farmer_login')





