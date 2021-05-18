from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from .models import Post,Like
# Create your views here.
from rest_framework.views import APIView
def AuctionSite(request):
    if request.user.is_authenticated:

        post= Post.objects.all()

        return render(request,'Post/allpostview.html',{'posts':post})
    else:
        return redirect('login')



def CreatePost(request):
    if request.user.is_authenticated:
        form = PostModelForm()
        print(request.POST)
        if 'submit_p_form' in request.POST:
            form=PostModelForm(request.POST,request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                instance.save()
                confirm = True
                form = PostModelForm()
                return redirect('Auctions:createpost')








        return render(request,'Post/CreatePost.html',{'form':form})
    else:
        return redirect('login')


class PostView(APIView):
    def get(self,request,*args,**kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.filter(pk=pk)
        comment=Comment.objects.filter(pk=pk)
        print(obj)
        return render(request,'Post/postview.html',{'obj':obj,})

@login_required
def like_unlike_post(request):
    print(request.POST.get('post_id'))
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(pk=post_id)
        profile = request.user
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'

            post_obj.save()
            like.save()


        return redirect('Auctions:postview',pk=post_id)