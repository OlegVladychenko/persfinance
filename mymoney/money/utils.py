from money.models import Currencies

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        return context

def get_main_currencie():
    return Currencies.objects.filter(code='980')