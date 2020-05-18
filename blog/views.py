from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Post , User
from django.views.generic import TemplateView
from .forms import NewpostForm
from django.utils import timezone
from datetime import datetime

class HomePage(TemplateView):
	def get(self, request):
		posts= Post.objects.filter(create_date__lte=timezone.now()).order_by('create_date')
		return render(request, 'blog/front.html', {'alldata':posts})


class Perma(TemplateView):
	def get(self,request, pk):
		obj= get_object_or_404(Post, pk=pk)
		return render(request, "blog/perma.html",{'post':obj})
		

class NewPost(TemplateView):
	def get(self,request):
		bg=NewpostForm(request.GET)
		return render(request,"blog/newpost.html",)

	def post(self, request):
		bg=NewpostForm(request.POST)
		if bg.is_valid():
			title= bg.cleaned_data['title']
			content=bg.cleaned_data['content']
			p=Post(title= title, content=content)
			p.save()
			return redirect(reverse('blog:onepost',args=(p.pk,)))

		else:
			title= bg.cleaned_data['title']
			content=bg.cleaned_data['content']
			print(bg.errors)
			return render(request, 'blog/newpost.html',{'title': title, 'content':content})
