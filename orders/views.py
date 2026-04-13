import requests
from django.shortcuts import render
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order


# =========================
# EMAIL FUNCTION (EMAILJS - FIXED)
# =========================
def send_email_emailjs(username, email):
    url = "https://api.emailjs.com/api/v1.0/email/send"

    data = {
        "service_id": "service_qpxmye3",
        "template_id": "template_sbfxt4k",
        "user_id": "dTg30LRsgHc73QEbb",
        "accessToken":"BYWukhpvsHy79pgMQpZek",
        "template_params": {
            "username": username,
            "email": email
        }
    }

    try:
        response = requests.post(url, json=data)
        print("Email Status:", response.status_code)
        print("Email Response:", response.text)
    except Exception as e:
        print("Email Error:", e)


# =========================
# REGISTER
# =========================
def register(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()

        # empty check
        if not username or not password or not email:
            messages.error(request, "All fields are required ❌")
            return render(request, "register.html")

        # user exists check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists ❌")
            return render(request, "register.html")

        # create user
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
        except IntegrityError:
            messages.error(request, "Username already exists ❌")
            return render(request, "register.html")

        # send email (EMAILJS)
        send_email_emailjs(username, email)

        messages.success(request, "Registered Successfully ✅ Check your email 📧")
        return redirect('/login/')

    return render(request, "register.html")


# =========================
# LANDING
# =========================
def landing(request):
    return render(request, 'landing.html')


# =========================
# MENU
# =========================
@login_required
def menu(request):
    return render(request, 'menu.html')


# =========================
# BILLING
# =========================
@login_required
def billing(request):
    if request.method == 'POST':
        items = request.POST.getlist('items')

        total = 0
        for item in items:
            if "Waffle" in item:
                total += 120
            else:
                total += 60

        gst = total * 0.05
        discount = total * 0.10 if total > 200 else 0
        final = total + gst - discount
        request.session['final_amount'] = final
        request.session.modified = True

        Order.objects.create(
            user=request.user,
            items=", ".join(items),
            total=total,
            gst=gst,
            discount=discount,
            final_amount=final
        )

        return render(request, 'billing.html', {
            'items': items,
            'total': total,
            'gst': gst,
            'discount': discount,
            'final': final
        })

    return redirect('menu')

def payment(request):
    amount = request.GET.get('amount')

    print("AMOUNT FROM URL:", amount)   # 🔥 DEBUG

    return render(request, 'payment.html', {'amount': amount})



def fail(request):
    return render(request, 'fail.html')

def help_page(request):
    return render(request, 'help.html')

def cart(request):
    return render(request, 'cart.html')
# =========================
# SUCCESS
# =========================
@login_required
def success(request):
    return render(request, 'success.html')