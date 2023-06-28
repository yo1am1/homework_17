from amazon.forms import ProductForm
from amazon.models import Product
import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def index(request):
    try:
        url = json.dumps(
            request.session.get("user")["userinfo"]["picture"], indent=4
        ).replace('"', "")
        context = {
            "session": request.session.get("user"),
            # "pretty": json.dumps(request.session.get("user")["userinfo"], indent=4),
            "nickname": request.session.get("user")["userinfo"]["nickname"],
            "email_varified": request.session.get("user")["userinfo"]["email_verified"],
            "email": request.session.get("user")["userinfo"]["email"],
            "picture": url,
        }
        return render(request, "index.html", context)
    except (Exception,):
        return render(request, "index.html")


def callback(request):
    try:
        token = oauth.auth0.authorize_access_token(request)
        request.session["user"] = token
        return redirect(request.build_absolute_uri(reverse("index")))
    except (Exception,) as e:
        return render(
            request,
            "error.html",
            context={
                "error": f"Access denied. Vallidate your email address and try again. {e}"
            },
        )


def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )


def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )


def add_image(request):
    form = ProductForm(request.POST, request.FILES)

    if request.method == "GET":
        form = ProductForm()
        return render(request, "images.html", {"form": form})

    if form.is_valid():
        form.save()
        return redirect(reverse(images))
    return render(request, "images.html", {"form": form})


def images(request):
    images_display = Product.objects.all()
    return render(request, "images_list.html", {"images": images_display})
