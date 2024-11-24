from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Produit
from .forms import ProduitForm  # Vous devrez créer ce formulaire
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Produit, Achat
from .models import Achat
from .forms import AchatForm

from django.shortcuts import render, redirect
from users.models import Client  # Replace 'myproject' with your project folder name if needed

from .forms import AchatForm

import paypalrestsdk
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Produit, Client, Achat
from .forms import AchatForm
import json
import stripe


# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # 'sandbox' or 'live'
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

stripe.api_key = settings.STRIPE_SECRET_KEY  # Set your Stripe secret key here


def add_achat(request, produit_reference):
    produit = get_object_or_404(Produit, reference=produit_reference)

    # Retrieve and decode user_info cookie
    user_info_cookie = request.COOKIES.get('user_info', None)
    
    if user_info_cookie is None:
        return redirect('produit_list')  # Redirect to login page if cookie is missing
    
    try:
        # Decode the URL-encoded string and parse the JSON
        user_info = json.loads(user_info_cookie.replace('%22', '"').replace('%2C', ',').replace('%3A', ':'))
        
        # Extract username from the decoded user_info object
        client_username = user_info.get('username', None)

        if client_username is None:
            return redirect('produit_list')  # Redirect to login page if username is not found in the cookie

        # Retrieve client using the username
        client = get_object_or_404(Client, username=client_username)

    except (json.JSONDecodeError, KeyError) as e:
        # Handle errors in decoding or if the expected keys are not present
        print(f"Error decoding cookie: {e}")
        return redirect('produit_list')  # Redirect to login page if there is an issue with the cookie

    if request.method == 'POST':
        form = AchatForm(request.POST, client=client, produit=produit)  # Pass client and produit to the form
        if form.is_valid():
            achat = form.save(commit=False)
            achat.produit = produit  # Set the product
            achat.client = client  # Set the client (from cookies)
            achat.save()

            # Get the selected payment method
            payment_method = request.POST.get('payment_method')

            if payment_method == 'paypal':
                # Set up PayPal payment
                payment = create_paypal_payment(achat)
                if payment:
                    # Redirect to PayPal for approval
                    for link in payment.links:
                        if link.rel == "approval_url":
                            approval_url = link.href
                            return redirect(approval_url)

            elif payment_method == 'stripe':
                # Set up Stripe payment
                try:
                    charge = stripe.Charge.create(
                        amount=int(achat.total_prix * 100),   # Stripe expects the amount in cents
                        currency="usd",  # or your desired currency
                        description=f"Payment for {achat.produit.nom}",
                        source=request.POST['stripeToken'],  # You'll send this from the frontend
                    )
                    if charge.status == "succeeded":
                        # Payment succeeded, mark the achat as paid or do necessary actions
                        achat.status = "paid"
                        achat.save()
                        return redirect('payment_success')  # Redirect to a success page
                except stripe.error.StripeError as e:
                    # Handle Stripe error (e.g., invalid card)
                    print(f"Stripe error: {e}")
                    return redirect('payment_error')  # Redirect to an error page if payment fails

            return redirect('payment_error')  # If neither PayPal nor Stripe is selected

    else:
        form = AchatForm(client=client, produit=produit)  # Pass client and produit to the form

    return render(request, 'add_achat.html', {'form': form, 'produit': produit})



def create_paypal_payment(achat):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [{
            "amount": {
                "total": str(achat.produit.prix),
                "currency": "EUR"
            },
            "description": f"Achat for {achat.produit.nom}"
        }],
        "redirect_urls": {
            "return_url": "http://localhost:8000/produit/execute",
            "cancel_url": "http://localhost:8000/produit/cancel"
        }
    })
    if payment.create():
        return payment
    else:
        raise Exception(payment.error)

def execute_payment(request, achat_id):
    """Execute the PayPal payment after the user approves it."""
    achat = get_object_or_404(Achat, id=achat_id)
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    # Execute the payment
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Payment executed successfully
        # Update the purchase status in your database
        achat.payment_status = 'completed'
        achat.save()
        return redirect('payment_success')  # Redirect to a success page
    else:
        # Payment failed
        return redirect('payment_error')  # Redirect to an error page
def payment_success(request):
    return render(request, 'payment_success.html')

def payment_error(request):
    return render(request, 'payment_error.html')



def fitness_home(request):
    return render(request, 'index.html')

# Liste des produits
class ProduitListView(ListView):
    model = Produit
    template_name = 'produit_list.html'
    context_object_name = 'produits'

    def get_queryset(self):
        queryset = Produit.objects.all()
        
        # Filter by category if specified
        categorie = self.request.GET.get('categorie')
        if categorie:
            queryset = queryset.filter(categorie=categorie)
        
        # Search by name if a search term is provided
        search_term = self.request.GET.get('search')
        if search_term:
            queryset = queryset.filter(nom__icontains=search_term)  # Case-insensitive search
        
        # Sorting by price if specified
        sort_order = self.request.GET.get('sort')
        if sort_order == 'price_asc':
            queryset = queryset.order_by('prix')
        elif sort_order == 'price_desc':
            queryset = queryset.order_by('-prix')
        
        return queryset



# Détail d'un produit
class ProduitDetailView(DetailView):
    model = Produit
    template_name = 'produit_detail.html'

    def get_object(self, queryset=None):
        # You can override the get_object method to look up the product using its reference
        reference = self.kwargs['reference']  # reference from the URL
        return get_object_or_404(Produit, reference=reference)

# Création d'un produit
class ProduitCreateView(CreateView):
    model = Produit
    form_class = ProduitForm
    template_name = 'produit_form.html'
    success_url = reverse_lazy('produit_list')

# Mise à jour d'un produit
class ProduitUpdateView(UpdateView):
    model = Produit
    form_class = ProduitForm
    template_name = 'produit_form.html'
    success_url = reverse_lazy('produit_list')

# Suppression d'un produit
class ProduitDeleteView(DeleteView):
    model = Produit
    template_name = 'produit_confirm_delete.html'
    success_url = reverse_lazy('produit_list')

