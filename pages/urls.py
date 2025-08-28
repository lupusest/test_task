from django.urls import path
from .views import PageListView, PageDetailView

urlpatterns = [
    # Путь для списка страниц теперь '' (корень относительно /api/v1/pages/)
    path('', PageListView.as_view(), name='page-list'),
    
    # Путь для детальной страницы теперь просто <int:pk>
    path('<int:pk>/', PageDetailView.as_view(), name='page-detail'),
]
