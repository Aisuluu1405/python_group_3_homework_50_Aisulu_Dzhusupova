from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import TemplateView
from django.views import View
from webapp.models import Article, Comment

from webapp.forms import ArticleForm, CommentForm


class ArticleIndexView(TemplateView):
    template_name = 'article/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
        return context


class ArticleView(TemplateView):
    template_name = 'article/article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_pk = kwargs.get('pk')
        context['article'] = get_object_or_404(Article, pk=article_pk)
        return context


class FormView(View):
    template_name = None

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = self.get_form(request.POST)
        if form.is_valid():
            self.form_valid(form)
            url = self.get_url()
            return redirect(url)
        else:
            return render(request, self.template_name, context={'form': form})

    def get_form(self, data=None):
        raise NotImplementedError

    def form_valid(self, form):
        raise NotImplementedError

    def get_url(self):
        raise NotImplementedError


class ArticleCreateView(FormView):
    template_name = 'article/create.html'

    def get_form(self, data=None):
        return ArticleForm(data=data)

    def form_valid(self, form):
        data = form.cleaned_data
        self.article = Article.objects.create(
            title=data['title'],
            author=data['author'],
            text=data['text'],
            category=data['category']
        )

    def get_url(self):
        return reverse('article_view', kwargs={'pk': self.article.pk})


class ArticleEditView(View):

    def get(self, request, *args, **kwargs):
        article_pk= kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)
        form = ArticleForm(data={
            'title': article.title,
            'author': article.author,
            'text': article.text,
            })
        return render(request, 'article/update.html', context={'form': form, 'article': article})

    def post(self, request, *args, **kwargs):
        article_pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            article.title = data['title']
            article.author = data['author']
            article.text = data['text']
            article.save()
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'article/update.html', context={'form': form, 'article': article})


class ArticleDeleteView(View):

    def get(self, request, *args, **kwargs):
        article_pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)
        return render(request, 'article/delete.html', context={'article': article})

    def post(self, *args, **kwargs):
        article_pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)
        article.delete()
        return redirect('index')


class CommentIndexView(TemplateView):
    template_name = 'comments/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all().order_by('-created_at')
        return context


class CommentCreateView(FormView):
    template_name = 'comments/create.html'

    def get_form(self, data=None):
        return CommentForm(data=data)

    def form_valid(self, form):
        data = form.cleaned_data
        self.comment = Comment.objects.create(
            article=data['article'],
            text=data['text'],
            author=data['author'],
        )

    def get_url(self):
        return reverse('comment_index')


class CommentEditView(View):

    def get(self, request, *args, **kwargs):
        comment_pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=comment_pk)
        form = CommentForm(data={
            'article': comment.article_id,
            'text': comment.text,
            'author': comment.author
            })
        return render(request, 'comments/update.html', context={'form': form, 'comment': comment})

    def post(self, request, *args, **kwargs):
        form = CommentForm(data=request.POST)
        comment_pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=comment_pk)
        if form.is_valid():
            data = form.cleaned_data
            comment.text = data['text']
            comment.author = data['author']
            comment.save()
            return redirect('comment_index')
        else:
            return render(request, 'comments/update.html', context={'form': form, 'comment': comment})


class CommentDeleteView(View):

    def get(self, request, *args, **kwargs):
        comment_pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=comment_pk)
        return render(request, 'comments/delete.html', context={'comment': comment})

    def post(self, request, *args, **kwargs):
        comment_pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
        return redirect('comment_index')


class ArticleCommentView(TemplateView):
    template_name = 'article_comments/article_comments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_pk = kwargs.get('pk')
        context['article'] = get_object_or_404(Article, pk=article_pk)
        context['comments'] = context['article'].comments.order_by('-created_at')

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
