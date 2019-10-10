from django import forms
from webapp.models import Article, Comment
from django.forms import widgets


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['created_at', 'updated_at']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['created_at', 'updated_at']


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']

#
# class ArticleForm(forms.Form):
#     title = forms.CharField(max_length=200, required=True, label='Title')
#     author = forms.CharField(max_length=40, required=True, label='Author')
#     text = forms.CharField(max_length=3000, required=True, label='Text',
#                            widget=widgets.Textarea)
#     category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Category',
#                                       empty_label=None)
#
#
# class CommentForm(forms.Form):
#     article = forms.ModelChoiceField(queryset=Article.objects.all(), required=True, label='Article')
#     text = forms.CharField(max_length=400, required=True, label='Text', widget=widgets.Textarea)
#     author = forms.CharField(max_length=40, required=False, label='Author', initial='Anonym')
#
