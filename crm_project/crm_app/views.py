from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
def home(request):

    records=Record.objects.all()

    # check to see if logging in
    if request.method=='POST':
        Username = request.POST['Username']
        Password = request.POST['Password']
        
        # authenticate
        user = authenticate(request, username=Username, password=Password)
        if user is not None:
            login(request, user)
            messages.success(request, f'You are now logged in as {user.username}')
            return redirect('home')
        
        else:
            messages.success(request, 'There was an error while logging in')
            return redirect('home')

    else:        
        return render(request,'crm_app/home.html',{'records': records})

# def login_user(request):



def logout_user(request):
    logout(request)
    messages.success(request, f'You are now logged out')
    return redirect('home')
    

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            # authenticate and login
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {user.username}')
            return redirect('home')
        
    else:
        form = SignUpForm()
        return render(request,'crm_app/register.html',{'form': form})
    
    return render(request,'crm_app/register.html',{'form': form})



def customer_record(request,pk):
    if request.user.is_authenticated:
        # look up records
        customer_record=Record.objects.get(id=pk)
        return render(request,'crm_app/record.html',{'customer_record': customer_record})
    
    else:
        messages.success(request,'You must be logged in to view that page')
        return redirect('home')
    

def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = Record.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully...")
		return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')

def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save()
				messages.success(request, "Record Added...")
				return redirect('home')
		return render(request, 'crm_app/add_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')
      

def update_record(request,pk):
      if request.user.is_authenticated:
            current_record= Record.objects.get(id=pk)
            form = AddRecordForm(request.POST or None, instance=current_record)
            if form.is_valid():
                form.save()
                messages.success(request, "Record Has Been Updated!")
                return redirect('home')
            return render(request, 'crm_app/update_record.html', {'form':form})
      else:
            messages.success(request, "You Must Be Logged In...")
            return redirect('home')