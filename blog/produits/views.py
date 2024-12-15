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
from users.models import User  # Replace 'myproject' with your project folder name if needed

from .forms import AchatForm

import paypalrestsdk
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Produit, User, Achat
from .forms import AchatForm
import json
from django.db.models import Count 



# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # 'sandbox' or 'live'
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})




def add_achat(request, produit_reference):
    produit = get_object_or_404(Produit, reference=produit_reference)

    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if user is not authenticated

    user = request.user  # The logged-in user, who will be the client

    if request.method == 'POST':
        form = AchatForm(request.POST)  # No need to pass client here, it will be set in the view
        if form.is_valid():
            achat = form.save(commit=False)
            achat.produit = produit  # Set the product
            achat.client = user  # Set the logged-in user (client)
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

            return redirect('payment_error')  # If PayPal is not selected or fails

    else:
        form = AchatForm()

    return render(request, 'add_achat.html', {'form': form, 'produit': produit, 'user': user})




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
        # Annotate products with the count of related 'Achats'
        queryset = Produit.objects.annotate(total_achats=Count('achats'))

        # Filter by category if specified
        categorie = self.request.GET.get('categorie')
        if categorie:
            queryset = queryset.filter(categorie=categorie)

        # Search by name if a search term is provided
        search_term = self.request.GET.get('search')
        if search_term:
            queryset = queryset.filter(nom__icontains=search_term)  # Case-insensitive search

        # Sorting by price or number of purchases
        sort_order = self.request.GET.get('sort')
        if sort_order == 'price_asc':
            queryset = queryset.order_by('prix')
        elif sort_order == 'price_desc':
            queryset = queryset.order_by('-prix')
        elif sort_order == 'achats_asc':
            queryset = queryset.order_by('total_achats')
        elif sort_order == 'achats_desc':
            queryset = queryset.order_by('-total_achats')

        return queryset



# Détail d'un produit
class ProduitDetailView(DetailView):
    model = Produit
    template_name = 'produit_detail.html'

    def get_object(self, queryset=None):
        # Retrieve the product using its reference
        reference = self.kwargs['reference']
        return get_object_or_404(Produit, reference=reference)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produit = self.get_object()

        # Count the number of 'Achats' related to this product
        total_achats = produit.achats.count()
        
        # Add the count to the context
        context['total_achats'] = total_achats
        return context

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

