from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



from .models import Task


# Create your views here.
class CustomLoginView(LoginView):
    #overrice lai ten template su dung mac dinh
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    # Dia chi tra ve khi thanh cong
    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterFage(FormView):
    # Overrice ten template mac dinh
    template_name ='base/register.html'
    #Su dung form userceation form
    form_class = UserCreationForm
    redirect_authenticated_user = True
    # Dia chi dan toi khi thanh cong
    success_url = reverse_lazy('tasks')
    #Kiem tra hop le cua du lieu nhap vao
    def form_valid(self, form):
        # neu hop le thi luu vao database
        user =form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterFage,self).form_valid(form)
    # Kiem tra neu da co dang nhap roi thi truy cap vao trang task
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(RegisterFage,self).get(*args,**kwargs)




class TaskList(LoginRequiredMixin,ListView):
    model = Task
    # Overrice lai ten cua object, mac dinh se la oject_list
    context_object_name = 'tasks'
    fields = '__all__'
    # get data cua moi user
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        #Dem task chua thuc hien
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input =self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']= context['tasks'].filter(title__icontains=search_input)
        context['search-input'] =search_input
        return context



class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    # Overrice ten template mac dinh
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    #xuat cac truong ra form , su dung Model Form
    fields = ['title','description','complete']
    # Dia chi dan toi khi thanh cong
    success_url = reverse_lazy('tasks')
    #Tao kiem tra form hop le, khi tao se tu dong tao cho user do
    def form_valid(self, form):
        form.instance.user =self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    # xuat cac truong ra form , su dung Model Form
    fields = ['title','description','complete']
    # Dia chi dan toi khi thanh cong
    success_url = reverse_lazy('tasks')



class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    # Overrice lai ten cua object
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

