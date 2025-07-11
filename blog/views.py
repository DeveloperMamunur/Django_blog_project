from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Tag, Post
from django.utils import timezone

# Create your views here.
def home(request):
    return render(request, 'base.html')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'index.html')

# blog category views
@login_required(login_url='login')
def category_list(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            return redirect('category_list')
        if Category.objects.filter(name=name).exists():
            return redirect('category_list')
        if len(name) < 3:
            return redirect('category_list')
        if name == '':
            return redirect('category_list')
        category = Category.objects.create(name=name)
        category.save()
        return redirect('category_list')
    context = {
        'categories': categories
    }
    return render(request, 'post_category/category_list.html', context)

@login_required(login_url='login')
def category_update(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            return redirect('category_update', id=id)
        if len(name) < 3:
            return redirect('category_update', id=id)
        if name == '':
            return redirect('category_update', id=id)
        category.name = name
        category.save()
        return redirect('category_list')
    context = {
        'category': category,
    }
    return render(request, 'post_category/category_list.html', context)

@login_required(login_url='login')
def category_delete(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('category_list')


@login_required(login_url='login')
def category_inactive(request, id):
    category = get_object_or_404(Category, id=id)
    category.active = False
    category.save()
    return redirect('category_list')

@login_required(login_url='login')
def category_active(request, id):
    category = get_object_or_404(Category, id=id)
    category.active = True
    category.save()
    return redirect('category_list')

# blog tags views
@login_required(login_url='login')
def tags_list(request):
    tags = Tag.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            return redirect('tags_list')
        if Tag.objects.filter(name=name).exists():
            return redirect('tags_list')
        if len(name) < 3:
            return redirect('tags_list')
        if name == '':
            return redirect('tags_list')
        tag = Tag.objects.create(name=name)
        tag.save()
        return redirect('tags_list')

    context = {
        'tags': tags
    }

    return render(request, 'post_tags/tags_list.html', context)

@login_required(login_url='login')
def tags_update(request, id):
    tag = get_object_or_404(Tag, id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            return redirect('tags_update', id=id)
        if len(name) < 3:
            return redirect('tags_update', id=id)
        if name == '':
            return redirect('tags_update', id=id)
        tag.name = name
        tag.save()
        return redirect('tags_list')

    context = {
        'tag': tag,
    }

    return render(request, 'post_tags/tags_list.html', context)

@login_required(login_url='login')
def tags_delete(request, id):
    tag = get_object_or_404(Tag, id=id)
    tag.delete()
    return redirect('tags_list')

@login_required(login_url='login')
def tags_inactive(request, id):
    tag = get_object_or_404(Tag, id=id)
    tag.active = False
    tag.save()
    return redirect('tags_list')

@login_required(login_url='login')
def tags_active(request, id):
    tag = get_object_or_404(Tag, id=id)
    tag.active = True
    tag.save()
    return redirect('tags_list')   

# blog post views
@login_required(login_url='login')
def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'post/post_list.html', context)
 
@login_required(login_url='login')
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        tag_ids = request.POST.getlist('tags')
        image = request.FILES.get('image')
        meta_title = request.POST.get('meta_title')
        meta_description = request.POST.get('meta_description')
        meta_keywords = request.POST.get('meta_keywords')
        author = request.user
        
        if Post.objects.filter(title=title).exists():
            return redirect('post_create')
        
        if len(title) < 3:
            return redirect('post_create')
        
        if title == '':
            return redirect('post_create')

        category = Category.objects.get(id=category_id)

        post = Post.objects.create(
            title=title,
            description=description,
            category=category,
            image=image,
            meta_title=meta_title,
            meta_description=meta_description,
            meta_keywords=meta_keywords,
            author=author
        )
        post.tags.set(tag_ids)
        post.save()
        return redirect('post_list')
    else:
        categories = Category.objects.all()
        tags = Tag.objects.all()
    
        context = {
            'categories': categories,
            'tags': tags,
        }
    return render(request, 'post/post_create.html', context)

@login_required(login_url='login')
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        tag_ids = request.POST.getlist('tags')
        image = request.FILES.get('image')
        meta_title = request.POST.get('meta_title')
        meta_description = request.POST.get('meta_description')
        meta_keywords = request.POST.get('meta_keywords')
        author = request.user
        
        if not title or len(title) < 3 or \
           Post.objects.exclude(id=post.id).filter(title=title).exists():
            return redirect('post_update', id=id)

        category = Category.objects.get(id=category_id)

        if image:
            if post.image and post.image.name != image.name:
                post.image.delete(save=False)  # delete old image from storage
            post.image = image

        post.title = title
        post.description = description
        post.category = category
        post.meta_title = meta_title
        post.meta_description = meta_description
        post.meta_keywords = meta_keywords
        post.author = author
        post.save()
        post.tags.set(tag_ids)
        post.save()
        return redirect('post_list')
    else:
        categories = Category.objects.all()
        tags = Tag.objects.all()
    
        context = {
            'post': post,
            'categories': categories,
            'tags': tags,
        }
        return render(request, 'post/post_edit.html', context) 

@login_required(login_url='login')
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('post_list')

@login_required(login_url='login')
def post_inactive(request, id):
    post = get_object_or_404(Post, id=id)
    post.is_active = False
    post.save()
    return redirect('post_list')

@login_required(login_url='login')
def post_active(request, id):
    post = get_object_or_404(Post, id=id)
    post.is_active = True
    post.save()
    return redirect('post_list')

@login_required(login_url='login')
def post_details(request, id):
    post = get_object_or_404(Post, id=id)
    post.views_count += 1
    post.save(update_fields=['views_count'])
    context = {
        'post': post,
    }
    return render(request, 'post/post_details.html', context)

@login_required(login_url='login')
def post_active_details(request, id):
    post = get_object_or_404(Post, id=id)
    post.is_active = True
    post.save()
    return redirect('post_details', id=id)

@login_required(login_url='login')
def post_inactive_details(request, id):
    post = get_object_or_404(Post, id=id)
    post.is_active = False
    post.save()
    return redirect('post_details', id=id)

@login_required(login_url='login')
def post_delete_details(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('post_list')

@login_required(login_url='login')
def post_published(request, id):
    post = get_object_or_404(Post, id=id)
    if post.is_active == False:
        return redirect('post_details', id=id)
    post.published_at = timezone.now()
    post.published_by = request.user
    post.save()
    return redirect('post_details', id=id)

@login_required(login_url='login')
def post_unpublished(request, id):
    post = get_object_or_404(Post, id=id)
    post.published_at = None
    post.published_by = None
    post.save()
    return redirect('post_details', id=id)