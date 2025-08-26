from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Account
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.db import connection
from django.contrib.auth.hashers import check_password


def login_view(request):
    if request.method == "GET":
        return render(request, "pages/login.html")
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is None:
        return HttpResponse("Invalid credentials", status=401)
    login(request, user)
    return redirect("/")

def logout_view(request):
    logout(request)
    return redirect("/")

def index(request):
    return render(request, "pages/index.html")

# Flaw 1: XSS vulnerable
def xss(request):
    name = request.GET.get("name", "")
    return HttpResponse(f"<h1>Hello {name}</h1>")

# Flaw 1: XSS fix
#def xss_fix(request):
#    name = request.GET.get("name", "")
#    return render(request, "pages/xss.html", {"name": name})


# Flaw 2: CSRF vulnerable
def csrf_attack(request):
    return render(request, "pages/csrf.html")


def transfer(request):
	request.session['to'] = request.GET.get('to')
	request.session['amount'] = int(request.GET.get('amount'))
	return render(request, 'pages/confirm.html')

def confirm(request):
	money = request.session['amount']
	sendTo = User.objects.get(username=request.session['to'])

	request.user.account.balance -= money
	sendTo.account.balance += money

	request.user.account.save()
	sendTo.account.save()

	return redirect('/')

# Flaw 2: CSRF fix
#def transfer(request):
#	if request.method != "POST":
#		return HttpResponse("Invalid method", status=405)
#	request.session['sendTo'] = request.POST.get('sendTo')
#	request.session['money'] = int(request.POST.get('money'))
#	return render(request, 'pages/confirm.html')
#
#@csrf_protect
#def confirm(request):
#    if request.method != "POST":
#        return HttpResponse("Invalid method", status=405)
#
#    money = request.session['money']
#    sendTo = User.objects.get(username=request.session['sendTo'])
#
#    request.user.account.balance -= money
#    sendTo.account.balance += money
#    request.user.account.save()
#    sendTo.account.save()
#
#    return redirect('/')


# Flaw 3: SQL Injection vulnerable
def sqli(request):
    q = request.GET.get("q", "")
    sql = f"SELECT username FROM auth_user WHERE username = '{q}'"

    with connection.cursor() as cur:
        cur.execute(sql)
        rows = [r[0] for r in cur.fetchall()]

    return JsonResponse({"executed_sql": sql, "results": rows})

# Flaw 3: SQL Injection fix
#def sqli(request):
#    q = request.GET.get("q")
#    if not q: return HttpResponseBadRequest("Usage: /sqli/?q=<username>")
#    sql = "SELECT username FROM auth_user WHERE username = %s"
#    with connection.cursor() as cur:
#        cur.execute(sql, [q])
#        return JsonResponse({"executed_sql": sql, "params": [q],
#                             "results": [r[0] for r in cur.fetchall()]})


# Flaw 4: IDOR vulnerable
def idor_profile(request):
    user_id = request.GET.get("user_id")
    if not user_id:
        return HttpResponseBadRequest("Usage: /idor/?user_id=<id>")
    try:
        u = User.objects.get(id=user_id)
        return JsonResponse({
            "username": u.username,
            "balance": u.account.balance,
        })
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)

# Flaw 4: IDOR fix
#def idor_profile(request):
#    u = request.user
#    if not u.is_authenticated:
#        return HttpResponse("Not authenticated", status=401)
#    return JsonResponse({
#        "username": u.username,
#        "balance": u.account.balance,
#    })


# Flaw 5: Clickjacking vulnerable
def clickjack_attack(request):
    return render(request, "pages/clickjack.html")
