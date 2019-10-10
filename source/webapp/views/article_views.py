from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView
from django.views import View
from webapp.models import Article, Comment
from webapp.forms import ArticleForm, CommentForm
from webapp.views.base_views import DetailView, CreateView, DeleteView


class ArticleIndexView(ListView):
    template_name = 'article/index.html'
    context_object_name = 'articles'
    model = Article
    ordering = ['-created_at']
    paginate_by = 4
    paginate_orphans = 1


class ArticleView(DetailView):
    template_name = 'article/article.html'
    model = Article
    context_key = 'article'

# class ArticleView(DetailView):
#     template_name = 'article/article.html'
#     model = Article
#     context_object_name = 'article'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = CommentForm()
#         article = context['article']
#         comments = article.comments.order_by('-created_at')
#         # self.paginate_comments_to_context(comments, context)
#         return context

    # def paginate_comments_to_context(self, comments, context):
    #     paginator = Paginator(comments, 3, 0)
    #     page_number = self.request.GET.get('page', 1)
    #     page = paginator.get_page(page_number)
    #     context['paginator'] = paginator
    #     context['page_obj'] = page
    #     context['comments'] = page.object_list
    #     context['is_paginated'] = page.has_other_pages()


class ArticleCreateView(CreateView):
    model = Article
    template_name = 'article/create.html'
    form_class = ArticleForm

    def get_redirect_url(self):
        return reverse('article_view', kwargs={'pk': self.object.pk})


class ArticleEditView(UpdateView):
    model = Article
    template_name = 'article/update.html'
    form_class = ArticleForm
    context_object_name = 'article'

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.pk})


class ArticleDeleteView(DeleteView):
    template_name = 'article/delete.html'
    model = Article
    context_key = 'article'
    redirect_url = reverse_lazy('index')

    # def get(self, request, *args, **kwargs):
    #     article_pk = kwargs.get('pk')
    #     article = get_object_or_404(Article, pk=article_pk)
    #     return render(request, 'article/delete.html', context={'article': article})
    #
    # def post(self, *args, **kwargs):
    #     article_pk = kwargs.get('pk')
    #     article = get_object_or_404(Article, pk=article_pk)
    #     article.delete()
    #     return redirect('index')


class ArticleCommentView(TemplateView):
    template_name = 'article_comments/article_comments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_pk = kwargs.get('pk')
        context['article'] = get_object_or_404(Article, pk=article_pk)
        article = context['article']
        context['comments'] = article.comments.order_by('-created_at')
        return context


class ArticleCommentCreateView(View):

    def post(self, request, *args, **kwargs):
        article_pk = kwargs.get('pk')
        article_id = get_object_or_404(Article, pk=article_pk)
        author = request.POST.get('author')
        text = request.POST.get('text')
        comment = Comment.objects.create(
            author=author,
            text=text,
            article=article_id
        )
        return redirect('article_comment', pk=comment.article.pk)
