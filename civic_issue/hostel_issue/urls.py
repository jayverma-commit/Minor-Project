from django.urls import path
from . import views 



urlpatterns = [



    path('',views.index,name='home'),
    path('login/',views.login_view,name='login'),
    path('signin/',views.signin,name='signin'),
    path('admindash/', views.admindash, name='admindash'),
    path('user/', views.user, name='user'),
    path('report/', views.report, name='report'),
    path('logout/', views.logout_view, name='logout'),
    path('update-status/<int:issue_id>/', views.update_issue_status, name='update_issue_status'),
    path('delete-issue/<int:issue_id>/', views.delete_issue, name='delete_issue'),




]