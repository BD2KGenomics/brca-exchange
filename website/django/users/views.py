import datetime
import hashlib
import json
import os
import random
import requests
from urllib.error import HTTPError
from django.core.mail import EmailMultiAlternatives
from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from django.views.decorators.cache import never_cache
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from mailchimp3 import MailChimp, mailchimpclient

from brca import settings, site_settings
from .models import MyUser, MailingListEmail

import logging


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def retrieve(request):
    user = request.user
    query = MyUser.objects.filter(email=user)
    data = list(query.values())[0]
    data["password"] = ''

    # get mailing list status (mailchimp uses md5 hashes of emails to identify subscribers)
    email = data["email"].lower().encode(encoding='utf-8')
    subscriber_hash = hashlib.md5(email).hexdigest()
    mc_client = MailChimp(mc_api=settings.MAILCHIMP_KEY, timeout=10.0)

    try:
        mc_user = client.lists.members.get(list_id=settings.MAILCHIMP_LIST, subscriber_hash=subscriber_hash)
        is_subscribed = (mc_user['status'] == 'pending' or mc_user['status'] == 'subscribed')
        response = JsonResponse({'user': data, 'mailinglist': is_subscribed})
        return response

    except mailchimpclient.MailChimpError as e:
        logging.error(repr(e))
        response = JsonResponse({'user': data, 'mailinglist': False})
        return response


@never_cache
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def update(request):
    user = MyUser.objects.filter(email=request.user)

    fields = user_fields(request)
    delete_image = request.POST.get('deleteImage', "false") == "true"
    fields['has_image'] = (user[0].has_image or fields['has_image']) and not delete_image

    del fields['email']
    if fields['password'] != '':
        u = user[0]
        u.set_password(fields['password'])
        u.save()
    del fields['password']

    try:
        user.update(**fields)
        if request.FILES:
            image = request.FILES["image"]
            if image is not None:
                save_picture(user[0].id, image)
    except Exception as e:
        logging.error(repr(e))
        return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': True})

def register(request):
    fields = user_fields(request)
    image = None
    if request.FILES:
        image = request.FILES["image"]

    # Check the CAPTCHA
    try:
        captcha = request.POST.get('captcha')
        post_data = {'secret': settings.CAPTCHA_SECRET,
                     'response': captcha}
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=post_data)
        content = json.loads(response.content.decode('utf-8'))
        response = {'success': content['success']}
    except HTTPError:
        logging.error(repr(HTTPError))
        return JsonResponse({'success': False, 'error': 'Wrong CAPTCHA'})

    # Create the user
    try:
        created_user = MyUser.objects.create_user(**fields)
        # Save the image under the user's id
        if image is not None:
            save_picture(created_user.id, image)

        created_user.is_active = False
        created_user.save()

        # Create and save activation key
        salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
        activation_key = hashlib.sha1((salt + created_user.email).encode('utf-8')).hexdigest()
        created_user.activation_key = activation_key
        created_user.save()

        # Sign up for mailchimp
        mc_client = MailChimp(mc_api=settings.MAILCHIMP_KEY, timeout=10.0)
        mc_client.lists.members.create(settings.MAILCHIMP_LIST, {
            'email_address': created_user.email,
            'status': 'subscribed',
            'merge_fields': {
                'FNAME': created_user.firstName,
                'LNAME': created_user.lastName,
            },
        })

        # Send activation email
        url = "{0}confirm/{1}".format(site_settings.URL_FRONTEND, activation_key)
        plaintext_email = get_template(os.path.join(settings.BASE_DIR, 'users', 'templates', 'registration_email.txt'))
        html_email = get_template(os.path.join(settings.BASE_DIR, 'users', 'templates', 'registration_email.html'))

        d = Context({'firstname': created_user.firstName, 'url': url})

        subject, from_email, to = 'BRCAExchange account confirmation', 'noreply@brcaexchange.org', created_user.email
        text_content = plaintext_email.render(d)
        html_content = html_email.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    except IntegrityError:
        logging.error(repr(IntegrityError))
        return JsonResponse({'success': False, 'error': 'This email address already exists'})

    except mailchimpclient.MailChimpError as e:
        logging.error(repr(e))

    return JsonResponse({'success': True})

def resend_activation(request):
    email = request.POST.get('email', '')
    user = MyUser.objects.filter(email = email)
    if not user:
        response = JsonResponse({'success': False, 'error': 'Email not found'})
        response['Access-Control-Allow-Origin'] = '*'
        return response;
    user = user[0]

    # resend activation email
    url = "{0}confirm/{1}".format(site_settings.URL_FRONTEND, user.activation_key)
    plaintext_email = get_template(os.path.join(settings.BASE_DIR, 'users', 'templates', 'registration_email.txt'))
    html_email = get_template(os.path.join(settings.BASE_DIR, 'users', 'templates', 'registration_email.html'))

    d = Context({'firstname': user.firstName, 'url': url})

    subject, from_email, to = 'BRCAExchange account confirmation', 'noreply@brcaexchange.org', user.email
    text_content = plaintext_email.render(d)
    html_content = html_email.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return JsonResponse({'success': True})

def confirm(request, activation_key):
    user = MyUser.objects.filter(activation_key=activation_key)
    if not user:
        response = JsonResponse({'success': False, 'error': 'Invalid activation key'})
        response['Access-Control-Allow-Origin'] = '*'
        return response
    user = user[0]
    user.is_active = True
    user.save()
    response = JsonResponse({'success': True})
    response['Access-Control-Allow-Origin'] = '*'
    return response


def password_reset(request):
    email = request.POST.get('email', '')
    user = MyUser.objects.filter(email=email)
    if not user:
        response = JsonResponse({'success': False, 'error': 'Email not found'})
        response['Access-Control-Allow-Origin'] = '*'
        return response
    user = user[0]

    # Create and save password reset token
    salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
    password_reset_token = hashlib.sha1((salt + user.email).encode('utf-8')).hexdigest()

    user.password_reset_token = password_reset_token
    email_duration_days = settings.PASSWORD_RESET_LINK_DURATION
    password_token_expires = timezone.now() + datetime.timedelta(email_duration_days)
    user.password_token_expires = password_token_expires
    user.save()

    # Send password reset email
    url = "{0}reset/{1}".format(site_settings.URL_FRONTEND, password_reset_token)
    plaintext_email = get_template(os.path.join(settings.BASE_DIR, 'users', 'templates', 'password_reset_email.txt'))
    html_email = get_template(os.path.join(settings.BASE_DIR, 'users', 'templates', 'password_reset_email.html'))
    d = Context({'firstname': user.firstName, 'url': url, 'hours': email_duration_days * 24})

    subject, from_email, to = 'BRCAExchange password reset', 'noreply@brcaexchange.org', user.email
    text_content = plaintext_email.render(d)
    html_content = html_email.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    response = JsonResponse({'success': True})
    response['Access-Control-Allow-Origin'] = '*'
    return response


def check_password_token(request, password_reset_token):
    user = MyUser.objects.filter(password_reset_token=password_reset_token)
    if not user or user[0].password_token_expires < timezone.now():
        response = JsonResponse({'invalid_token': True})
        response['Access-Control-Allow-Origin'] = '*'
        return response

    response = JsonResponse({'invalid_token': False})
    response['Access-Control-Allow-Origin'] = '*'
    return response


def update_password(request, password_reset_token):
    user = MyUser.objects.filter(password_reset_token=password_reset_token)
    if not user:
        response = JsonResponse({'success': False, 'invalid_token': True, 'error': 'Invalid link'})
        response['Access-Control-Allow-Origin'] = '*'
        return response
    user = user[0]

    if user.password_token_expires < timezone.now():
        response = JsonResponse({'success': False, 'invalid_token': True, 'error': 'Invalid link'})
        response['Access-Control-Allow-Origin'] = '*'
        return response

    password = request.POST.get('password', '')
    user.set_password(password)
    user.password_token_expires = timezone.now()
    user.save()
    response = JsonResponse({'success': True})
    response['Access-Control-Allow-Origin'] = '*'
    return response


def user_fields(request):
    image = None
    if request.FILES:
        image = request.FILES["image"]
    has_image = (image is not None)
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    firstName = request.POST.get('firstName', '')
    lastName = request.POST.get('lastName', '')
    title = request.POST.get('title', '')
    role = request.POST.get('role', MyUser.ROLE_OTHER)
    role_other = request.POST.get('role_other', '')
    institution = request.POST.get('institution', '')
    city = request.POST.get('city', '')
    state = request.POST.get('state', '')
    country = request.POST.get('country', '')
    latitude = request.POST.get('latitude', '')
    longitude = request.POST.get('longitude', '')
    phone_number = request.POST.get('phone_number', '')
    hide_number = (request.POST.get('hide_number', "true") == "true")
    hide_email = (request.POST.get('hide_email', "true") == "true")

    return {'role': role, 'role_other': role_other, 'city': city, 'country': country, 'latitude': latitude, 'longitude': longitude,
            'email': email, 'firstName': firstName, 'has_image': has_image, 'hide_email': hide_email,
            'hide_number': hide_number, 'institution': institution,
            'lastName': lastName, 'password': password, 'phone_number': phone_number, 'state': state, 'title': title}


def save_picture(filename, image):
    path = os.path.join(settings.MEDIA_ROOT, str(filename))
    fd = open(path, 'wb')
    for chunk in image.chunks():
        fd.write(chunk)
    fd.close()


def users(request):
    page_num = int(request.GET.get('page_num', '0'))
    page_size = int(request.GET.get('page_size', '0'))
    search = request.GET.get('search', '')
    roles = request.GET.getlist('roles[]')

    query = MyUser.objects.filter(is_approved=True)
    if roles:
        query = query.filter(role__in=roles)

    search_query = Q()
    for term in search.split():
        search_query &= ( Q(firstName__icontains=term) | Q(lastName__icontains=term)
                        | Q(institution__icontains=term) | Q(role_other__icontains=term)
                        | Q(city__icontains=term) | Q(state__icontains=term) | Q(country__icontains=term)
                        )
    query = query.filter(search_query)

    whitelist = ['id','email','firstName','lastName','title','role','role_other','institution','city','state','country','phone_number','hide_number','hide_email','is_active','is_admin','has_image','is_approved']

    count = query.count()

    start = page_num * page_size
    end = start + page_size
    data = list(query[start:end].values(*whitelist))


    for user in data:
        if user['hide_email']:
            user['email'] = ""
        if user['hide_number']:
            user['phone_number'] = ""

    response = JsonResponse({'data': data, 'count': count})
    response['Access-Control-Allow-Origin'] = '*'
    return response

def user_locations(request):
    search = request.GET.get('search', '')
    roles = request.GET.getlist('roles[]')
    query = MyUser.objects.filter(is_approved=True)
    if roles:
        query = query.filter(role__in=roles)

    search_query = Q()
    for term in search.split():
        search_query &= ( Q(firstName__icontains=term) | Q(lastName__icontains=term)
                        | Q(institution__icontains=term) | Q(role_other__icontains=term)
                        | Q(city__icontains=term) | Q(state__icontains=term) | Q(country__icontains=term)
                        )
    query = query.filter(search_query)

    fields = ['id', 'firstName', 'lastName', 'title', 'role', 'role_other', 'institution', 'city', 'state', 'country', 'latitude', 'longitude', 'has_image']
    response = JsonResponse({'data': list(query.values(*fields))})
    response['Access-Control-Allow-Origin'] = '*'
    return response
