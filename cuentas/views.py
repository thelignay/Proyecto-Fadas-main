from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render


def _style_form_fields(form):
    for field in form.fields.values():
        existing_classes = field.widget.attrs.get('class', '')
        classes = f"{existing_classes} form-control".strip()
        field.widget.attrs['class'] = classes
    return form


def landing(request):
    return render(request, 'cuentas/landing.html')


@login_required
def home(request):
    return render(request, 'cuentas/dashboard.html')


def signin(request):
    next_url = request.POST.get('next') or request.GET.get('next', '')
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        _style_form_fields(form)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            redirect_to = request.POST.get('next') or request.GET.get('next')
            return redirect(redirect_to or 'dashboard')
    else:
        form = AuthenticationForm(request)
        _style_form_fields(form)

    return render(request, 'cuentas/signin.html', {
        'form': form,
        'next': next_url,
    })


def signout(request):
    auth_logout(request)
    return redirect('landing')


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        _style_form_fields(form)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
        _style_form_fields(form)

    return render(request, 'cuentas/signup.html', {
        'form': form,
    })
