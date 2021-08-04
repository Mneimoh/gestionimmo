from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from main.models import User
from django.contrib.auth import get_user_model

# Create your views here.

# def get_queryset(self):
#     """
#     Return the list of items for this view.

#     The return value must be an iterable and may be an instance of
#     `QuerySet` in which case `QuerySet` specific behavior will be enabled.
#     """
#     if self.queryset is not None:
#         queryset = self.queryset
#         if isinstance(queryset, QuerySet):
#             queryset = queryset.all()
#     elif self.model is not None:
#         queryset = self.model._default_manager.all()
#     else:
#         raise ImproperlyConfigured(
#             "%(cls)s is missing a QuerySet. Define "
#             "%(cls)s.model, %(cls)s.queryset, or override "
#             "%(cls)s.get_queryset()." % {
#                 'cls': self.__class__.__name__
#             }
#         )
#     ordering = self.get_ordering()
#     if ordering:
#         if isinstance(ordering, str):
#             ordering = (ordering,)
#         queryset = queryset.order_by(*ordering)

#     return queryset

@login_required
def change_list_view(request):
      if(request.user.is_staff):
            print('-------------------------------------')
            print('----------Making a request -----------')
            print('-----------------------------------')
            User = get_user_model()
            users = User.objects.filter(is_admin = True)   
            print(users)       
            return render(request, '/templates/admin/change_list.html', { 'title': 'Espace vente'})
            return HttpResponse('Youu came knocking')
      else:
            return redirect(f"/login?next=/admin/")