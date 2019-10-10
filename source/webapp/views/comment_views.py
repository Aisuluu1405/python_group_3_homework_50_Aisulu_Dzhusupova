from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import ListView, UpdateView
from django.views import View
from webapp.models import Comment
from webapp.forms import CommentForm
from webapp.views.base_views import CreateView, DeleteView


class CommentIndexView(ListView):
    template_name = 'comments/index.html'
    context_object_name = 'comments'
    model = Comment
    ordering = ['-created_at']
    paginate_by = 6
    paginate_orphans = 1


class CommentCreateView(CreateView):
    model = Comment
    template_name = 'comments/create.html'
    form_class = CommentForm

    def get_redirect_url(self):
        return reverse('comment_index')


class CommentEditView(UpdateView):
    model = Comment
    template_name = 'comments/update.html'
    form_class = CommentForm
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse('comment_index')


class CommentDeleteView(DeleteView):
    model = Comment
    confirm_deletion = False

    def get_redirect_url(self):
        return reverse('article_view', kwargs={'pk': self.object.article.pk})

#
# class CommentEditView(View):
#
#     def get(self, request, *args, **kwargs):
#         comment_pk = kwargs.get('pk')
#         comment = get_object_or_404(Comment, pk=comment_pk)
#         form = CommentForm(data={
#             'article': comment.article_id,
#             'text': comment.text,
#             'author': comment.author
#             })
#         return render(request, 'comments/update.html', context={'form': form, 'comment': comment})
#
#     def post(self, request, *args, **kwargs):
#         form = CommentForm(data=request.POST)
#         comment_pk = kwargs.get('pk')
#         comment = get_object_or_404(Comment, pk=comment_pk)
#         if form.is_valid():
#             data = form.cleaned_data
#             comment.text = data['text']
#             comment.author = data['author']
#             comment.save()
#             return redirect('comment_index')
#         else:
#             return render(request, 'comments/update.html', context={'form': form, 'comment': comment})
#
#
# class CommentDeleteView(View):
#
#     def get(self, request, *args, **kwargs):
#         comment_pk = kwargs.get('pk')
#         comment = get_object_or_404(Comment, pk=comment_pk)
#         return render(request, 'comments/delete.html', context={'comment': comment})
#
#     def post(self, request, *args, **kwargs):
#         comment_pk = kwargs.get('pk')
#         comment = get_object_or_404(Comment, pk=comment_pk)
#         comment.delete()
#         return redirect('comment_index')


