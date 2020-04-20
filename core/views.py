from django.shortcuts import render, get_object_or_404
from .models import Post, Video, Schedule, Donate, STATUS_CHOICES
from django.utils import timezone
from django.db.models import Q
from .models import PostView
from .forms import DonateForm
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic.base import RedirectView
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from pagseguro import PagSeguro
from paypal.standard.forms import PayPalPaymentsForm

def home(request):
    posts = Post.objects.filter(Q(published_date__lte=timezone.now()) | Q(published_date__isnull=True)).order_by('-published_date')[0:4]
    videos = Video.objects.order_by('-registering_date')[0:3]
    meetings = Schedule.objects.filter(
        Q(start_date__gte=timezone.now()) | 
        Q(
            Q(end_date__isnull=False),
            end_date__lt=timezone.now()
        )
    )
    form = DonateForm()
    context = {
        'posts': posts,
        'meetings': meetings,
        'videos': videos,
        'form': form
    }
    return render(request, 'core/home.html', context)

def posts(request):
    posts = Post.objects.filter(Q(published_date__lte=timezone.now()) | Q(published_date__isnull=True)).order_by('-published_date')
    context = {
        'posts': posts
    }
    return render(request, 'core/posts.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post is not None:
        post_view, create = PostView.objects.get_or_create(post=post)
        if post_view:
            post_view.views_count += 1
            post_view.save()
    context = {
        'post': post
    }
    return render(request, 'core/post_detail.html', context)

def about(request):
    # SAI QUE É TUA, GABRIEL!
    return render(request, 'core/about.html')

class DonateViewPagseguro(RedirectView):
    def get_redirect_url(self):
        if self.request.POST:
            form = DonateForm(self.request.POST)

            if form.is_valid():
                donor_name = form.cleaned_data['donor_name']
                donor_email = form.cleaned_data['donor_email']
                donate_Type = form.data['donate_Type']
                amount = form.cleaned_data['amount']
                
                donate_object = {
                    'donor_name': donor_name,
                    'donor_email': donor_email,
                    'donate_Type': donate_Type,
                    'payment_option': 'pagseguro',
                    'amount': amount
                }

                # Update probably pending payments by the the same email
                pending_payments = Donate.objects.filter(donor_email=donor_email, payment_status='pending', donate_type=donate_Type)
                for payment in pending_payments:
                    payment.payment_status = 'excluded'

                Donate.objects.bulk_update(pending_payments, ['payment_status'])

                donate = Donate()
                donate.initialize_object(donate_object)
                donate.save()

                pagseguro_donate = Donate.objects.earliest('-id')

                pg = pagseguro_donate.pagseguro()

                # pg.redirect_url = "http://meusite.com/obrigado"

                pg.redirect_url = self.request.build_absolute_uri(
                    reverse('done_payment')
                )

                pg.notification_url  = self.request.build_absolute_uri(
                    reverse('pagseguro_notification')
                )

                response = pg.checkout()
                return response.payment_url

def donateViewPayPal(request):   
    if request.POST:
        form = DonateForm(request.POST)

        if form.is_valid():
            donor_name = form.cleaned_data['donor_name']
            donor_email = form.cleaned_data['donor_email']
            donate_Type = form.data['donate_Type']
            amount = form.cleaned_data['amount']
            
            donate_object = {
                'donor_name': donor_name,
                'donor_email': donor_email,
                'donate_Type': donate_Type,
                'payment_option': 'pagseguro',
                'amount': amount
            }

            # Update probably pending payments by the the same email
            pending_payments = Donate.objects.filter(donor_email=donor_email, payment_status='pending', donate_type=donate_Type)
            for payment in pending_payments:
                payment.payment_status = 'excluded'

            Donate.objects.bulk_update(pending_payments, ['payment_status'])   

            donate = Donate()
            donate.initialize_object(donate_object)
            donate.save()

            paypal_donate = Donate.objects.earliest('-id')

            paypal_dict = paypal_donate.paypal()

            paypal_dict['return'] = request.build_absolute_uri(
                reverse('done_payment')
            )

            paypal_dict['cancel_return']  = request.build_absolute_uri(
                reverse('home')
            )

            form = PayPalPaymentsForm(initial=paypal_dict)
            context = {"form": form}
            return render(request, "core/payment.html", context)


def done_payment(request):
    return render(request, 'core/done_payment.html')

@csrf_exempt
def pagseguro_notification(request):
    notification_code = request.POST.get('notificationCode', None)
    if notification_code:
        pg = PagSeguro(
            email=settings.PAGSEGURO_EMAIL, 
            token=settings.PAGSEGURO_TOKEN,
            config={'sandbox': settings.PAGSEGURO_SANDBOX}
        )

        notification_data = pg.check_notification(notification_code)
        status = notification_data.status
        reference = notification_data.reference
        try:
            donate = Donate.objects.get(pk=reference)
        except ObjectDoesNotExist:
            pass
        else:
            donate.pagseguro_update_status(status)
    return HttpResponse('OK')    