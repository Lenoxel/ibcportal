from django.shortcuts import render, get_object_or_404
from .models import Post, Video, Schedule, Donate, STATUS_CHOICES
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q
from .forms import DonateForm
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic.base import RedirectView
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from pagseguro import PagSeguro
from paypal.standard.forms import PayPalPaymentsForm, PayPalSharedSecretEncryptedPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED, ST_PP_DECLINED, ST_PP_FAILED, ST_PP_EXPIRED
from paypal.standard.ipn.signals import valid_ipn_received
from . import auxiliar_functions

def home(request):
    posts = Post.objects.filter(Q(published_date__lte=timezone.now()) | Q(published_date__isnull=True)).order_by('-published_date')[0:4]
    
    videos = Video.objects.order_by('-registering_date')[0:3]

    one_week_after_period = datetime.today() + timedelta(days=7)

    meetings = Schedule.objects.filter(
        Q(
            Q(start_date__gte=timezone.now()) |
            Q(
                Q(end_date__isnull=False),
                Q(end_date__gte=timezone.now())
            )
        ), Q(start_date__lte=one_week_after_period)
       
    ).order_by('start_date')

    for meeting in meetings:
        if meeting.title == 'Geral':
            if meeting.organizing_group is not None:
                meeting.formatted_title = 'Programação - ' + meeting.organizing_group.name
            else:
               meeting.formatted_title = auxiliar_functions.meeting_types.get(meeting.title) 
        else:
            meeting.formatted_title = auxiliar_functions.meeting_types.get(meeting.title)

    form = DonateForm()

    # video_ids = ""

    # for video in videos:
    #     video_ids += video.youtube_video_code + ","
    # video_ids = video_ids[0:len(video_ids)-1]

    # Utilizar a requisição abaixo para incrementar informações nos vídeos
    # my_request = auxiliar_functions.youtube_request(video_ids)

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
        post.views_count += 1
        post.save()
    context = {
        'post': post
    }
    return render(request, 'core/post_detail.html', context)

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

                # Update possible pending payments with the the same email
                pending_payments = Donate.objects.filter(donor_email=donor_email, payment_status='pending', donate_type=donate_Type)
                for payment in pending_payments:
                    payment.payment_status = 'excluded'

                Donate.objects.bulk_update(pending_payments, ['payment_status'])

                donate = Donate()
                donate.initialize_object(donate_object)
                donate.save()

                pagseguro_donate = Donate.objects.earliest('-id')

                pg = pagseguro_donate.pagseguro()

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
                'payment_option': 'paypal',
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

            paypal_dict['notify_url']  = request.build_absolute_uri(
                reverse('paypal-ipn')
            )

            form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
            # form = PayPalSharedSecretEncryptedPaymentsForm(initial=paypal_dict, button_type="subscribe")
            return HttpResponse(form.render())


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
            donate.pagseguro_paypal_update_status(status)
    return HttpResponse('OK')    

def paypal_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        if ipn_obj.receiver_email == settings.PAYPAL_EMAIL:
            try:
                donate = Donate.objects.get(pk=ipn_obj.invoice)
                donate.pagseguro_paypal_update_status('3')
            except ObjectDoesNotExist:
                pass
    elif ipn_obj.payment_status == ST_PP_DECLINED or ipn_obj.payment_status == ST_PP_FAILED or ipn_obj.payment_status == ST_PP_EXPIRED:
        try:
            donate = Donate.objects.get(pk=ipn_obj.invoice)
            donate.pagseguro_paypal_update_status('7')
        except ObjectDoesNotExist:
            pass

valid_ipn_received.connect(paypal_notification)
