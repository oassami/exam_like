from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
import bcrypt

def snacks(request):
  if 'logged_in' not in request.session: 
    return redirect('/')
  context = {
    'all_snacks': Snack.objects.all(),
  }
  return render(request, 'snacks.html', context)

def add_snack(request):
  request.session['title'] = request.POST['title']
  request.session['description'] = request.POST['description']
  errors = Snack.objects.addValidation(request.POST)
  if errors:
      for key, value in errors.items():
          messages.error(request, value)
      return redirect('/snacks')
  this_user = User.objects.get(id=request.session['user_id'])
  this_idea = Snack.objects.create(
    title=request.POST['title'], 
    description=request.POST['description'], 
    creator=this_user
    )
  del request.session['title']
  del request.session['description']
  return redirect('/snacks')

def delete_snack(request, snack_id):
  this_snack = Snack.objects.get(id=snack_id)
  if this_snack.creator.id == request.session['user_id']:
    this_snack.delete()
  return redirect('/snacks')

def display_snack(request, snack_id):
  context = {
    'this_snack': Snack.objects.get(id=snack_id),
  }
  return render(request, 'snack_disp.html', context)

def user_profile(request, user_id):
  this_user = User.objects.get(id=user_id)
  this_user_snacks = User.objects.get(id=this_user.id).snacks.all()
  count_snacks = this_user_snacks.count()
  context = {
    'this_user': this_user,
    'user_snacks': this_user_snacks,
    'count_snacks': count_snacks,
  }
  return render(request, 'user.html', context)

def user_edit(request):
  user = User.objects.get(id=request.session['user_id'])
  if request.method == 'GET':
    context={
      'this_user': user,
    }
    return render(request, 'user_edit.html', context)
  else:
    errors = User.objects.editValidator(request.POST, user)
    if errors:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect('/snacks/user/edit')
    if request.POST['first_name']:
      user.first_name = request.POST['first_name']
    if request.POST['last_name']:
      user.last_name = request.POST['last_name']
    if request.POST['email']:
      user.email = request.POST['email']
      request.session['email'] = user.email
    if request.POST['new_password']:
      user.password = bcrypt.hashpw(request.POST['new_password'].encode(), bcrypt.gensalt()).decode()
    user.save()
  return redirect(f'/snacks/user/{user.id}')

