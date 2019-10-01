from django.views.generic import View
from django.shortcuts import render, redirect


# class ListView(TemplateView):
#     model = None
#     context_key = 'objects'
#
#     def get_context_data(self, **kwargs):
#         context = super(). get_context_data(**kwargs)
#         context[self.context_key] = self.model.get_objects.all()
#
#         return context


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

