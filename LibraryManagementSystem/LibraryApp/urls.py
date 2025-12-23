from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="hm"),
    path('abt/', views.about, name="abt"),
    path('cnt/', views.contact, name="cnt"),

    path('reg/', views.register, name='reg'),

    path(
        'lgo/',
        auth_views.LoginView.as_view(
            template_name="html/login.html",
            redirect_authenticated_user=True
        ),
        name='lgo'
    ),

    path(
        'lgt/',
        auth_views.LogoutView.as_view(next_page='lgo'),
        name='lgt'
    ),

    path('profile/', views.profile, name='profile'),
    path('blank/', views.blank, name="blank"),
    path('viewprofile/', views.viewprofile, name="viewprofile"),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('changepassword/', views.changepassword, name="changepassword"),
    path('addbook/', views.addbook, name="addbook"),
    path("deletebook/<int:myid>/", views.deletebook, name="deletebook"),
    path('viewbook/', views.viewbook, name="viewbook"),
    path('viewstudents/', views.viewstudents, name="viewstudents"),
    path('bookview/<int:v>/', views.bookview, name='bookview'),
    path('requestedbooks/', views.requestedbooks, name='requestedbooks'),
    path('allrequests/', views.allrequests, name='allrequests'),
    path('approverequests/<int:requestid>/', views.approverequests, name='approverequests'),
    path('rejectrequests/<int:requestid>/', views.rejectrequests, name='rejectrequests'),
    path('cancelrequest/<int:bk>/', views.cancelrequest, name='cancelrequest'),
    path('returnbook/<int:bkid>/', views.returnbook, name='returnbook'),
    path('stapprovedbooks/', views.stapprovedbooks, name='stapprovedbooks'),
    path('lbapprovedbooks/', views.lbapprovedbooks, name='lbapprovedbooks'),
]
