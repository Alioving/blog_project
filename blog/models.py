from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse
# python_2_unicode_compatible 装饰器用于兼容 python2

# python 中的一个类对应一个数据表格
@python_2_unicode_compatible
class Category(models.Model):
	name = models.CharField(max_length=100)
	'''
	Djangp 要求模型必须继承 models.Model 类。
	Category 只需要一个简单的分类名 name 就可以了。
	CharField 指定了分类名 name 的数据类型， CharField 是字符型，
	当然 Django 还为我们提供了多种其他的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。

	'''
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name
		
@python_2_unicode_compatible	
class Tag(models.Model):
	"""
	标签 Tag 也比较简单，和 Category 一样。
	一定要继承 models.Model 类！
	"""
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name
		
@python_2_unicode_compatible	
class Post(models.Model):
	"""
	文章的数据表稍微复杂点，主要是涉集的字段更多
	"""
	
	# 文章标题
	title=models.CharField(max_length=70)
	
	# 文章正文， 使用 TextField
	# 存储比较短的字符串可以使用 CharField， 利用 TextField 存储大段文本
	body = models.TextField()
	
	# 这两列分别表示文章的穿件时间和最后一次修改时间，存储时间的字段用 DateField 类型
	created_time = models.DateTimeField()
	modified_time = models.DateTimeField()
	
	# 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错
	# 指定了 blank=True 后就能够允许空值了
	excerpt=models.CharField(max_length=200,blank=True)
	
	# 这是分类与标签，分类与标签的模型已经定义在上面
	# 这里把文章对应的数据库表和分类、标签对应的数据库关联了起来，但关联方式有点不同。
	# 规定一篇文章只能对应一个分类，但一个分类下可以有多篇文章，因此使用ForeignKey，即一对多的关系
	# 对于标签来说，一篇文章可以有多个标签，一个标签也可以对应多篇文章吗，因此使用ManyToManyField，表明是多对多的关系
	# 同时规定文章可以没有标签，因此 tags 标签指定了 blank=True
	category = models.ForeignKey(Category)
	tags = models.ManyToManyField(Tag,blank=True)
	
	# 文章作者，这里 User 是从 django.contrib.auth.models 导入的
	# django.contrib.auth 是Django的内置应用，专门应用于处理网站用户的注册，登陆等流程，
	# User 是 Django 为我们写好的用户模型
	# 规定一篇文章只能有一个作者，而一个作者可以写多篇文章，因此是一对多的关联关系，和Category类似
	author = models.ForeignKey(User)
	def __str__(self):
		return self.title
		
	def get_absolute_url(self):
		return reverse('blog:detail', kwargs={'pk': self.pk})
		
	class Meta:
		ordering=['-created_time','title']
		