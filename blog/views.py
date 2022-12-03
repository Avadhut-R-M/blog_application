from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import ShareForm
from django.core.mail import send_mail
from django.conf import settings
from .serializers import BlogSerilaizer

from .models import Blog, Comment, Like

@login_required(login_url='/login')
def blog_list(request):
    data = request.GET
    page_no = data.get('page', 1)
    blogs = Blog.objects.all()

    paginator = Paginator(blogs, 5)

    try:
        paginated_blogs = paginator.page(page_no)
    except PageNotAnInteger:
        paginated_blogs = paginator.page(1)
        page_no = 1
    except EmptyPage:
        paginated_blogs = paginator.page(paginator.num_pages)
        page_no = paginator.num_pages

    pages = {'next':False, 'prev':False, 'total':paginator.num_pages, 'now':page_no}

    if paginated_blogs.has_next():
        pages['next'] = True
        pages['next_page_no'] = int(page_no) + 1
    if paginated_blogs.has_previous():
        pages['prev'] = True
        pages['previous_page_no'] = int(page_no) - 1

    return render(request, 'home.html', context={'paginated_blogs':paginated_blogs, 'pages':pages})


@login_required(login_url='/login')
def blog_detail(request, id):
    blog = Blog.objects.filter(id=id).last()
    ser = BlogSerilaizer(blog)
    data = ser.data
    # print(data)

    if not blog:
        return redirect('/home')

    return render(request, 'detail.html', context={'blog':data})

@login_required(login_url='/login')
def share_blog(request, id):
    user = request.user
    form = ShareForm
    blog = Blog.objects.filter(id=id).last()
    if not blog:
        return redirect('/home')

    if request.method == 'GET':
        return render(request,  'share_blog.html', context={'form': form, 'blog':blog})

    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            comments = form.cleaned_data['comments']

            msg = f'hi {name},\n'
            msg += comments
            msg += f'\n check this blog sent by - {user.email}\n\n'
            msg += f'{settings.CURRENT_HOST}/blog/{id}'

            send_mail(
            subject= 'Check this Blog',
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
            )

        return redirect('/blog/{}'.format(id))

@login_required(login_url='/login')
def comment(request):
    text= request.POST.get('text')
    user = request.user
    root_node_type = request.POST.get('root_node_type')
    root_node_id = request.POST.get('root_node_id')

    Comment.objects.create(
        text = text,
        root_node_type=root_node_type,
        root_node_id = root_node_id,
        writter = user
    )

    return redirect('/blog/{}'.format(root_node_id))

@login_required(login_url='/login')
def like(request):
    user = request.user
    root_node_type = request.GET.get('root_node_type')
    root_node_id = request.GET.get('root_node_id')
    like = request.GET.get('like')

    if like == '-1':
        like_obj = Like.objects.filter(root_node_type=root_node_type, 
            owner=user,root_node_id=root_node_id, status = True)
        like_obj.update(status = False)

    if like == '1':
        like_obj = Like.objects.create(root_node_type=root_node_type, 
            owner=user,root_node_id=root_node_id, status = True)
    
    return redirect('/blog/{}'.format(root_node_id))
    

