from django.utils.deprecation import MiddlewareMixin

from user.models import User


class UserMiddle(MiddlewareMixin):

    def process_request(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(pk=user_id).first()
            request.user = user