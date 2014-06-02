from django.test import TestCase
from baseuser.models import BaseUser, UserManager
from django.core import mail


class BaseUserModelTestCase(TestCase):
    def setUp(self):
        # set defalut lang to English
        from django.utils.translation import activate
        activate('en-us')

        BaseUser.objects.create_superuser(email="XX@yy.com", password="1234")
        BaseUser.objects.create_staff(email="YY@yy.com", password="1234")
        BaseUser.objects.create_user(email="ZZ@yy.com", password="1234")

    def test_create_user(self):
        """test base user is active/staff/superuser?"""
        XX = BaseUser.objects.get(email="XX@yy.com")
        YY = BaseUser.objects.get(email="YY@yy.com")
        ZZ = BaseUser.objects.get(email="ZZ@yy.com")

        self.assertEqual(XX.get_short_name(), 'XX@yy.com')
        self.assertEqual(YY.get_short_name(), 'YY@yy.com')
        self.assertEqual(ZZ.get_short_name(), 'ZZ@yy.com')

        self.assertEqual(XX.is_active, True)
        self.assertEqual(YY.is_active, True)
        self.assertEqual(ZZ.is_active, False)

        self.assertEqual(XX.is_staff, True)
        self.assertEqual(YY.is_staff, True)
        self.assertEqual(ZZ.is_staff, False)

        self.assertEqual(XX.is_superuser, True)
        self.assertEqual(YY.is_superuser, False)
        self.assertEqual(ZZ.is_superuser, False)

        self.assertEqual(ZZ.get_full_name(), 'ZZ@yy.com')
        self.assertEqual(ZZ.get_email(), 'ZZ@yy.com')
        self.assertEqual(ZZ.__str__(), 'ZZ@yy.com')

    def test_sent_email(self):
        ZZ = BaseUser.objects.get(email="ZZ@yy.com")
        YY = BaseUser.objects.get(email="YY@yy.com")
        XX = BaseUser.objects.get(email="XX@yy.com")

        subject = 'subject'
        message = 'message'

        XX.email_user(subject, message)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, subject)
        self.assertEqual(mail.outbox[0].body, message)
        self.assertEqual(mail.outbox[0].to, [XX.email])

        YY.email_user(subject, message)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].subject, subject)
        self.assertEqual(mail.outbox[1].body, message)
        self.assertEqual(mail.outbox[1].to, [YY.email])

        ZZ.email_user(subject, message)
        self.assertEqual(len(mail.outbox), 3)
        self.assertEqual(mail.outbox[2].subject, subject)
        self.assertEqual(mail.outbox[2].body, message)
        self.assertEqual(mail.outbox[2].to, [ZZ.email])

    def test_create_user_with_no_input_email(self):
        kargs = {'password': "1234", }
        self.assertRaisesRegex(ValueError, "The given email must be set",
            BaseUser.objects.create_user, **kargs)
