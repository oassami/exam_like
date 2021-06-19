from django.urls import path
from . import views

urlpatterns = [
    path('', views.snacks),
    path('add', views.add_snack),
    path('delete/<int:snack_id>', views.delete_snack),
    path('<int:snack_id>', views.display_snack),
    path('user/<int:user_id>', views.user_profile),
    path('user/edit', views.user_edit),
]
