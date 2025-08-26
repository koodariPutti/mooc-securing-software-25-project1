from django.urls import path

from .views import login_view, logout_view, index, xss, transfer, confirm, csrf_attack, sqli, idor_profile, clickjack_attack

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('', index, name='index'),

    # Flaw 1: XSS
    path('xss/', xss, name='xss'),
    
    # Flaw 2: CSRF
    path("transfer/", transfer, name="transfer"),
    path("confirm/", confirm, name="confirm"),
    path("attacker/csrf/", csrf_attack, name="csrf_attack"),

    # Flaw 3: SQL Injection
    path("sqli/", sqli, name="sqli"),

    # Flaw 4: IDOR
    path("idor/", idor_profile, name="idor_profile"),

    # Flaw 5: Clickjacking
    path("attacker/clickjack/", clickjack_attack, name="clickjack_attack"),

]
