from jose import jws
from django.http import HttpResponse
import datetime
from django.contrib.auth import authenticate

def create_jwt(request):
    user_email = request.POST['user_email']
    password = request.POST['password']
    expiry = datetime.date.today()
    token = jws.sign(
        {'user_email' : user_email,
         'expiry' : expiry}
        , 'seKre8', algorithm = 'HS256')

    return HttpResponse(token)