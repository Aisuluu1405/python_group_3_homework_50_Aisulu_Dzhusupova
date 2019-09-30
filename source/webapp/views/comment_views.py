from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import TemplateView
from django.views import View
from webapp.models import Comment

from webapp.forms import CommentForm

class CommentIndexView(TemplateView):
    template_name = 'comments/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all().order_by('-created_at')
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


