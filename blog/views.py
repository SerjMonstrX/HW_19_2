from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from blog.models import BlogPost


class BlogCreateView(CreateView):
    model = BlogPost
    fields = ('title', 'post_content', 'preview',)
    success_url = reverse_lazy('blog:list')

    # def form_valid(self, form):
    #     # Генерация уникального слага
    #     form.instance.slug = unique_slug_generator(form.cleaned_data['title'])
    #     return super().form_valid(form)


class BlogListView(ListView):
    model = BlogPost