from django.contrib import admin
from django.urls import include, path
from sentiment import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('callback/', include([
        path('sentiment/', include([
            path('new/', views.SentimentCallback.as_view()),
        ])),
    ])),
    path('sentiment/', include([
        path('', views.SentimentList.as_view()),
        path('<int:pk>/', views.SentimentDetail.as_view()),
        path('new/', views.SentimentCreate.as_view())
    ]))
]
