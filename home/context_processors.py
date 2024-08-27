# context_processors.py
from auths.models import Account

def user_count(request):
    return {
        'user_count': Account.objects.count(),
    }
