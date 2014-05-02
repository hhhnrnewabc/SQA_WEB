from django.test import TestCase

from baseuser.models import BaseUser, UserManager

class BaseUserTestCase(TestCase):
    def setUp(self):
        BaseUser.objects.create_superuser(email="XX@yy.com", password="1234")
        BaseUser.objects.create_staff(email="YY@yy.com", password="1234")
        BaseUser.objects.create_user(email="ZZ@yy.com", password="1234")



    def test_creat_user(self):
        """Animals that can speak are correctly identified"""
        XX = BaseUser.objects.get(email="XX@yy.com")
        YY = BaseUser.objects.get(email="YY@yy.com")
        ZZ = BaseUser.objects.get(email="ZZ@yy.com")

        self.assertEqual(XX.get_short_name(), 'XX@yy.com')
        self.assertEqual(YY.get_short_name(), 'YY@yy.com')
        self.assertEqual(ZZ.get_short_name(), 'ZZ@yy.com')

        self.assertEqual(XX.is_active, True)
        self.assertEqual(YY.is_active, True)
        self.assertEqual(ZZ.is_active, True)

        self.assertEqual(XX.is_staff, True)
        self.assertEqual(YY.is_staff, True)
        self.assertEqual(ZZ.is_staff, False)

        self.assertEqual(XX.is_superuser, True)
        self.assertEqual(YY.is_superuser, False)
        self.assertEqual(ZZ.is_superuser, False)


        self.assertEqual(ZZ.get_full_name(), 'ZZ@yy.com')


    def test_sent_email(self):
        ZZ = BaseUser.objects.get(email="ZZ@yy.com")
        YY = BaseUser.objects.get(email="YY@yy.com")
        XX = BaseUser.objects.get(email="XX@yy.com")

        subject = 'subject'
        message = 'message'
        
        self.assertEqual(XX.email_user(subject, message), "sent to XX@yy.com subject message")
        self.assertEqual(YY.email_user(subject, message), "sent to YY@yy.com subject message")
        self.assertEqual(ZZ.email_user(subject, message), "sent to ZZ@yy.com subject message")


    def test_creat_user_with_no_input_email(self):
        kargs = {'password':"1234",}
        self.assertRaisesRegex(ValueError,"The given email must be set", 
            BaseUser.objects.create_user, **kargs)