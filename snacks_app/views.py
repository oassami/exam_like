from django.shortcuts import render, redirect
from django.db.models import Count
from . models import *
from django.contrib import messages
import bcrypt

def snacks(request):
  if 'logged_in' not in request.session: 
    return redirect('/')
  context = {
    'all_snacks': Snack.objects.annotate(Count('likes')).order_by('likes__count').reverse()
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
  this_snack = Snack.objects.create(
    title=request.POST['title'], 
    description=request.POST['description'], 
    creator=this_user
    )
  this_snack.likes.add(this_user)
  this_snack.dislikes.remove(this_user)
  del request.session['title']
  del request.session['description']
  return redirect('/snacks')

def delete_snack(request, snack_id):
  this_snack = Snack.objects.get(id=snack_id)
  if this_snack.creator.id == request.session['user_id']:
    this_snack.delete()
  return redirect('/snacks')

def display_snack(request, snack_id):
  logged_user = User.objects.get(id=request.session['user_id'])
  this_snack = Snack.objects.get(id=snack_id)
  users_like = this_snack.likes.all()
  users_dislike = this_snack.dislikes.all()
  logged_user_like = False
  logged_user_dislike = False
  if logged_user in users_like:
    logged_user_like = True
  if logged_user in users_dislike:
    logged_user_dislike = True
  context = {
    'this_snack': this_snack,
    'users_like': users_like,
    'users_dislike': users_dislike,
    'logged_user_like': logged_user_like,
    'logged_user_dislike': logged_user_dislike,
  }
  return render(request, 'snack_disp.html', context)

def user_profile(request, user_id):
  this_user = User.objects.get(id=user_id)
  this_user_snacks = this_user.snacks.all()
  user_likes = this_user.liked_snacks.all()
  user_dislikes = this_user.disliked_snacks.all()
  context = {
    'this_user': this_user,
    'user_snacks': this_user_snacks,
    'user_likes': user_likes,
    'user_dislikes': user_dislikes,
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

def like_snack(request, snack_id):
  this_user = User.objects.get(id=request.session['user_id'])
  this_snack = Snack.objects.get(id=snack_id)
  this_snack.likes.add(this_user)
  this_snack.dislikes.remove(this_user)
  return redirect(f'/snacks/{snack_id}')

def dislike_snack(request, snack_id):
  this_user = User.objects.get(id=request.session['user_id'])
  this_snack = Snack.objects.get(id=snack_id)
  this_snack.likes.remove(this_user)
  this_snack.dislikes.add(this_user)
  return redirect(f'/snacks/{snack_id}')
