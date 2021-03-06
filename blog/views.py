from django.shortcuts import render, get_object_or_404
from .models import Tag,Category,Post
# Create your views here.
from django.http import HttpResponse
import  markdown
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.db.models import Q


#def index(request):
#	return render(request,'blog/index.html',context={'title':'我的博客首页',
#							'welcome':'欢迎访问我的博客首页'})
#	post_list=Post.objects.all().order_by('-created_time')
#	return render(request,'blog/index.html',context={'post_list':post_list})
# 把上面的视图函数改造成类视图函数
def search(request):
  q = request.GET.get('q')
  error_msg = ''

  if not q:
    error_msg = "请输入关键词"
    return render(request, 'blog/index.html', {'error_msg': error_msg})

  post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
  return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})
  

class IndexView(ListView):
  model=Post
  template_name='blog/index.html'
  context_object_name='post_list'
  paginate_by=5

  def get_context_data(self,**kwargs):
    context=super().get_context_data(**kwargs)

    paginator=context.get('paginator')
    page=context.get('page_obj')
    is_paginated=context.get('is_paginated')

    pagination_data=self.pagination_data(paginator,page,is_paginated)

    context.update(pagination_data)
    return context

  def pagination_data(self,paginator,page,is_paginated):
    if not is_paginated:
      return {}

    left={}
    right={}
    left_has_more=False
    right_has_more=False
    first=False
    last=False
    page_number=page.number
    total_pages=paginator.num_pages
    page_range=paginator.page_range

    if page_number==1:
      right=page_range[page_number:page_number+2]

      if right[-1]<total_pages-1:
        right_has_more=True

      if right[-1]<total_pages:
        last=True

    elif page_number==total_pages:
      left=page_range[(page_number-3) if (page_number-3)>0 else 0:page_number-1]

      if left[0]>2:
        left_has_more=True

      if left[0]>1:
        first=True

    else:
      left=page_range[(page_number-3) if (page_number-3)>0 else 0:page_number-1]
      rifht=page_range[page_number:page_number+2]

      if right[-1]<total_pages-1:
        right_has_more=True

      if right[-1]<total_pages:
        last=True

      if left[0]>2:
        left_has_more=True

      if left[0]>1:
        first=True

    data={
      'left':left,
      'right':right,
      'left_has_more':left_has_more,
      'right_has_more':right_has_more,
      'first':first,
      'last':last,
    }

    return data




	
#def detail(request,pk):
#	post = get_object_or_404(Post,pk=pk)
#	post.body = markdown.markdown(post.body,
#									extensions=[
#										'markdown.extensions.extra',
###									])
#return render(request,'blog/detail.html', context={'post':post})
	

# def detail(request, pk):

#     post = get_object_or_404(Post, pk=pk)
#     post.increase_views()
#     post.body = markdown.markdown(post.body,
#                                   extensions=[
#                                       'markdown.extensions.extra',
#                                       'markdown.extensions.codehilite',
#                                       'markdown.extensions.toc',
#                                   ])
#     # 记得在顶部导入 CommentForm
#     form = CommentForm()
#     # 获取这篇 post 下的全部评论
#     comment_list = post.comment_set.all()

#     # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
#     context = {'post': post,
#                'form': form,
#                'comment_list': comment_list
#                }
#     return render(request, 'blog/detail.html', context=context)
# 将上面的detail视图函数改造成DetailVIew视图函数
class PostDetailView(DetailView):
  model=Post
  template_name='blog/detail.html'
  context_object_name='post'

  def get(self,request,*args,**kwargs):
  # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
  # get 方法返回的是一个 HttpResponse 实例
  # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
  # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
    response=super(PostDetailView,self).get(request,*args,**kwargs)

    # 将文章阅读量+1
    # 注意self.object 的值就是被访问的文章post
    self.object.increase_views()

    # 视图必须返回一个HttpResponse对象
    return response

  def get_object(self,queryset=None):
    # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
    post=super(PostDetailView,self).get_object(queryset=None)
    md=markdown.Markdown(extensions=['markdown.extensions.extra','markdown.extensions.codehilite',TocExtension(slugify=slugify),])
    post.body=md.convert(post.body)
    post.toc=md.toc
    return post

  def get_context_data(self,**kwargs):
    # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
    # 还要把评论表单、post 下的评论列表传递给模板。
    context=super(PostDetailView,self).get_context_data(**kwargs)
    form=CommentForm()
    comment_list=self.object.comment_set.all()
    context.update({
      'form':form,
      'comment_list':comment_list
      })

    return context


	

#def category(request,pk):
#	cate=get_object_or_404(Category,pk=pk)
#	post_list=Post.objects.filter(category=cate).order_by('-created_time')
#	return render(request,'blog/index.html',context={'post_list':post_list})
# 将上面的category视图函数改造成类视图函数
class CategoryView(IndexView):
  def get_queryset(self):
    cate=get_object_or_404(Category,pk=self.kwargs.get('pk'))
    return super(CategoryView,self).get_queryset().filter(category=cate)

# 归档
#def archives(request,year,month):
 # post_list=Post.objects.filter(created_time__year=year,
 #                 created_time__month=month,
 #                 ).order_by('-created_time')               
 # return render(request, 'blog/index.html', context={'post_list': post_list})
  
# 将上面的archives视图函数改造成类视图函数
class ArchivesView(IndexView):
  def get_query(self):
    return super(ArchivesView,self).get_queryset().filter(created_time__year=year,created_time__month=month,)


class TagView(ListView):
  model=Post
  template_name='blog/index.html'
  context_object_name='post_list'

  def get_queryset(self):
    tag=get_object_or_404(Tag,pk=self.kwargs.get('pk'))
    return super(TagView,self).get_queryset().filter(tags=tag)
