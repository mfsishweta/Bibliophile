from django.utils import timezone
import random
import string
from datetime import datetime, timedelta

from django.utils import timezone

from apps.coreauth.models import OTPAuthentication
from apps.users.models import User
from common.utils.email_util import EmailHandler


class OTPGenerator:
    @staticmethod
    def generate(length_of_otp):
        otp = ''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=length_of_otp))
        return otp


class OTPAuthenticationRecordGenerator:
    def get_otp_from_authentication_record(self, user_id):
        otp = self._get_saved_otp_from_db(user_id)
        if otp:
            return otp
        return self._create_otp(user_id)

    def _get_saved_otp_from_db(self, user):
        otp_query_set = OTPAuthentication.objects.filter(user=user)
        if not otp_query_set:
            return None
        otp_record = otp_query_set.first()
        if otp_record.expire_at < timezone.now():
            return None
        return otp_record.otp

    def _create_otp(self, user_id):
        # TODO: get OTP length,TTL(live duration) from settings.py
        otp = OTPGenerator.generate(5)
        current_datetime = timezone.now()
        expire_at = current_datetime + timedelta(minutes=5)
        user = User.objects.get(id=user_id)
        OTPAuthentication.objects.create(user=user, otp=otp, expire_at=expire_at)
        return otp

    def validate_otp(self, user, user_otp):
        existing_otp = self._get_saved_otp_from_db(user)
        is_valid = existing_otp == user_otp
        print(existing_otp,'***',user_otp)
        if is_valid:
            self._expire_current_otp(user)
        return is_valid

    def _expire_current_otp(self, user):
        otp_record = OTPAuthentication.objects.filter(user=user).first()
        otp_record.expire_at = datetime.now()
        otp_record.save(update_fields=['expire_at'])


class EmailSender:
    def __init__(self):
        self._email_handler = EmailHandler()
        self.sender_email = 'mfsi.shweta.mishra@gmail.com'

    def create_and_send_email(self, user_id):
        otp = OTPAuthenticationRecordGenerator().get_otp_from_authentication_record(user_id)
        plain_msg = self._get_email_text(otp)
        recipient_email = User.objects.get(id=user_id).email
        self._email_handler.send_message(self.sender_email, 'Bibliophile_OTP_verification',
                                         [recipient_email], plain_msg)

    def _get_email_text(self, otp):
        return f"Your OTP verification code is {otp}"
