from blog.models import Category


menu = [{'title': 'Добавить статью', 'url_name': 'addpage'},]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.all()
        context['menu'] = menu
        context['cats'] = cats
        if 'cats_selected' not in context:
            context['cats_selected'] = 0
        return context
