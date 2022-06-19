
class HitTracker:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from web.models import HitCount
        if request.user.is_authenticated:  
            HitCount.objects.create(
                page = request.path,
                user = request.user
            )
        return self.get_response(request)