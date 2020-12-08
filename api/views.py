from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, permissions, status, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, ID, Entities, COAModel
from django.db import IntegrityError
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from api.serializers import *
from api.utils import TokenGenerator
# from mysite import settings
from random import randint


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LoginAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request, *args, **kwargs):
        email = request.data['email']
        user = User.objects.get(email=email)

        if not user:
            return Response(dict(detail="Please register"), status=404)
        else:
            phone_verification = user.is_phone_verified
            # if user.is_active is False:
            #     return Response(dict(detail="Please verify your email address"), status=401)
            if phone_verification is False:
                return Response(dict(detail="Please verify your phone number"), status=201)
            if user.is_active:
                MyTokenObtainPairView()


class UserInfoAPIView(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = request.user
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.email = request.data['email']
        user.save()
        user.phone_number = request.data['phone_number']
        phone_verification_url = '%s/login/phone_verification?uid=%s&token=%s' % (request.build_absolute_uri('/')[:-1],
                                                                                  urlsafe_base64_encode(force_bytes(user.pk)),
                                                                                  TokenGenerator().make_token(user))
        user.save()
        try:
            name = user.first_name + ' ' + user.last_name
            message = render_to_string('emails/phone_verification.html', {
                'name': name,
                'phone_verification_url': phone_verification_url,
            })
            email = EmailMessage(
                'Phone verification', message, to=[user.email]
            )
            email.send()
        except Exception:
            pass
        return Response(data=self.get_serializer(user).data)

    def patch(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserSingUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Some fields are missing',
                'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        try:
            num = randint(100000, 999999)
            user = User.objects.create(email=data['email'], first_name=data['first_name'], username=data['email'],
                                       last_name=data['last_name'], is_active=True, email_verification_code=num)
            user.set_password(data['password'])
            user.save()
        except IntegrityError as e:
            return Response({
                'message': 'Email already exists.',
                'errors': {'email': 'Email already exists.'}
                 }, status=status.HTTP_400_BAD_REQUEST)

        # email_verification_url = '%s/login/email_verification?uid=%s&token=%s' % (request.build_absolute_uri('/')[:-1],
        #                                                                           urlsafe_base64_encode(force_bytes(user.pk)),
        #                                                                           TokenGenerator().make_token(user))

        try:
            name = user.first_name + ' ' + user.last_name
            message = render_to_string('emails/email_verification.html', {
                'name': name,
                'email_verification_code': num,
            })
            email = EmailMessage(
                'Email verification', message, to=[user.email]
            )
            email.send()
        except Exception:
            pass

        return Response(data=UserSerializer(user).data, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request):
        email = request.data['email']
        code = request.data['code']
        user = User.objects.get(email=email)

        if user.email_verification_code == code:
            user.is_active = True
            user.save()
            return Response(dict(detail="Email address verified successfully"), status=201)
        return Response(dict(detail='The provided email did not match'), status=200)


class ResendEmailView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request):
        email = request.data['email']
        user = User.objects.get(email=email)

        if user:
            num = randint(100000, 999999)
            user.email_verification_code = num
            user.save()

            try:
                name = user.first_name + ' ' + user.last_name
                message = render_to_string('emails/email_verification.html', {
                    'name': name,
                    'email_verification_code': num,
                })
                email = EmailMessage(
                    'Email Verification', message, to=[user.email]
                )
                email.send()
            except Exception:
                pass
            return Response(dict(detail="Resend email verification code done successfully."), status=201)
        return Response(dict(detail='The provided email did not match'), status=200)


class ResendPhoneView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request):
        phone_number = request.data['phone_number']
        user = User.objects.get(phone_number=phone_number)

        if user:
            num = randint(100000, 999999)
            user.email_verification_code = num
            user.save()

            try:
                name = user.first_name + ' ' + user.last_name
                message = render_to_string('emails/email_verification.html', {
                    'name': name,
                    'email_verification_code': num,
                })
                email = EmailMessage(
                    'Email Verification', message, to=[user.email]
                )
                email.send()
            except Exception:
                pass
            return Response(dict(detail="Resend email verification code done successfully."), status=201)
        return Response(dict(detail='The provided email did not match'), status=200)


class ResetPasswordAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request, *args, **kwargs):
        email = request.data['email']
        user = User.objects.get(username=email)
        if user:
            password_reset_url = '%s/login/reset_password?uid=%s&token=%s' % (request.build_absolute_uri('/')[:-1],
                                                                             urlsafe_base64_encode(force_bytes(user.pk)),
                                                                             TokenGenerator().make_token(user))

            try:
                name = user.first_name + ' ' + user.last_name
                message = render_to_string('emails/reset_password.html', {
                    'name': name,
                    'password_set_url': password_reset_url,
                })
                email = EmailMessage(
                    'Please reset your password.', message, to=[user.email]
                )
                email.send()
            except Exception:
                pass
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CreatePasswordAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(request.data['uid']))
            user = User.objects.get(pk=uid)
            if user is None or not TokenGenerator().check_token(user, request.data['token']):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                user.set_password(request.data['password'])
                user.is_active = True
                user.save()
            except IntegrityError:
                return Response({
                    'password': 'Password already exists.',
                    'errors': {'password': 'Password already exists.'}
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        # admin_id = request.user.profile.admin_id
        # select_users = User.objects.filter(profile__admin_id=admin_id)
        users = User.objects.order_by('-date_joined')
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):
        serializer = CreateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Some fields are missing',
                'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        try:
            user = User.objects.create(username=data['email'], email=data['email'], first_name=data['first_name'],
                                       last_name=data['last_name'], is_active=False, phone_number=data['phone_number'],)
        except IntegrityError:
            return Response({
                'message': 'Email already exists.',
                'errors': {'email': 'Email already exists.'}
                 }, status=status.HTTP_400_BAD_REQUEST)

        password_set_url = '%s/login/create_password?uid=%s&token=%s' % (request.build_absolute_uri('/')[:-1],
                                                                         urlsafe_base64_encode(force_bytes(user.pk)),
                                                                         TokenGenerator().make_token(user))

        return Response(data=UserSerializer(user).data, status=status.HTTP_201_CREATED)

    @staticmethod
    def update(request, pk=None):
        user = User.objects.get(pk=pk)
        try:
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.email = request.data['email']
            user.username = request.data['email']
            user.save()
        except IntegrityError:
            return Response({
                'message': 'Email already exists.',
                'errors': {'email': 'Email already exists.'}
            }, status=status.HTTP_400_BAD_REQUEST)

        # user.profile.phone_number = request.data['phone_number']
        # user.profile.user_role = int(request.data['user_role'])
        # user.profile.save()
        return Response(data=UserSerializer(user).data, status=status.HTTP_200_OK)

    @staticmethod
    def destroy(request, pk=None):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IDViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        ids = ID.objects.order_by('-updated_at')
        serializer = IDSerializer(ids, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):
        serializer = CreateIDSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Some fields are missing',
                'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        roles = []
        for index in data['id_role']:
            id_role = index['label']
            roles.append(id_role)
        ids = ID.objects.create(id_name=data['id_name'], id_type=data['id_type'], id_role=roles,
                                info=data['id_info'], status=data['status'])

        return Response(data=IDSerializer(ids).data, status=status.HTTP_201_CREATED)

    @staticmethod
    def update(request, pk=None):
        sel_id = ID.objects.get(pk=pk)

        sel_id.id_name = request.data['id_name']
        sel_id.id_type = request.data['id_type']
        sel_id.id_info = request.data['id_info']
        sel_id.status = request.data['status']

        roles = []
        for index in request.data['id_role']:
            id_role = index['label']
            roles.append(id_role)
        sel_id.id_role = roles
        sel_id.save()

        return Response(data=IDSerializer(sel_id).data, status=status.HTTP_200_OK)

    @staticmethod
    def destroy(request, pk=None):
        ids = ID.objects.get(pk=pk)
        ids.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EntityViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        entities = Entities.objects.order_by('-start_date')
        serializer = EntitySerializer(entities, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):
        serializer = CreateEntitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Some fields are missing',
                'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        entities = Entities.objects.create(entity_id=data['entity_id'], entity_type=data['entity_type'],
                                           entity_name=data['entity_name'])

        return Response(data=EntitySerializer(entities).data, status=status.HTTP_201_CREATED)

    @staticmethod
    def update(request, pk=None):
        sel_entity = Entities.objects.get(pk=pk)

        sel_entity.entity_id = request.data['entity_id']
        sel_entity.entity_name = request.data['entity_name']
        sel_entity.entity_type = request.data['entity_type']

        sel_entity.save()

        return Response(data=EntitySerializer(sel_entity).data, status=status.HTTP_200_OK)

    @staticmethod
    def destroy(request, pk=None):
        entity = Entities.objects.get(pk=pk)
        entity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ModelViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        model = COAModel.objects.order_by('-model_name')
        serializer = ModelSerializer(model, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):
        serializer = CreateModelSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Some fields are missing',
                'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        model = COAModel.objects.create(model_name=data['model_name'], status=data['status'])

        return Response(data=ModelSerializer(model).data, status=status.HTTP_201_CREATED)

    @staticmethod
    def update(request, pk=None):
        sel_model = COAModel.objects.get(pk=pk)

        sel_model.model_name = request.data['model_name']
        sel_model.status = request.data['status']

        sel_model.save()

        return Response(data=ModelSerializer(sel_model).data, status=status.HTTP_200_OK)

    @staticmethod
    def destroy(request, pk=None):
        model = COAModel.objects.get(pk=pk)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        accounts = COAModel.objects.order_by('-account_id')
        serializer = AccountSerializer(accounts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):
        serializer = CreateAccountSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Some fields are missing',
                'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        account = Accounts.objects.create(
            account_id=data['account_id'], description=data['description'], info=data['info'],
            account_type=data['account_type'], sub_type=data['sub_type'], activity=data['activity'])

        return Response(data=AccountSerializer(account).data, status=status.HTTP_201_CREATED)

    @staticmethod
    def update(request, pk=None):
        sel_account = Accounts.objects.get(pk=pk)

        sel_account.account_id = request.data['account_id']
        sel_account.description = request.data['description']
        sel_account.info = request.data['info']
        sel_account.account_type = request.data['account_type']
        sel_account.sub_type = request.data['sub_type']
        sel_account.activity = request.data['activity']

        sel_account.save()

        return Response(data=AccountSerializer(sel_account).data, status=status.HTTP_200_OK)

    @staticmethod
    def destroy(request, pk=None):
        account = Accounts.objects.get(pk=pk)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JournalViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        journals = Journals.objects.order_by('-created_at')
        serializer = JournalSerializer(journals, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):
        serializer = CreateJournalSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Some fields are missing',
                'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        journal = Journals.objects.create(journal_id=data['journal_id'], journal_name=data['journal_name'],
                                          info=data['info'], avail_entities=data['avail_entities'])

        return Response(data=JournalSerializer(journal).data, status=status.HTTP_201_CREATED)

    @staticmethod
    def update(request, pk=None):
        sel_journal = Journals.objects.get(pk=pk)

        sel_journal.journal_id = request.data['journal_id']
        sel_journal.journal_name = request.data['journal_name']
        sel_journal.info = request.data['info']
        sel_journal.avail_entities = request.data['avail_entities']

        sel_journal.save()

        return Response(data=JournalSerializer(sel_journal).data, status=status.HTTP_200_OK)

    @staticmethod
    def destroy(request, pk=None):
        journal = Journals.objects.get(pk=pk)
        journal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlanViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        plans = Plans.objects.order_by('-created_at')
        serializer = PlanSerializer(plans, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):
        serializer = CreatePlanSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Some fields are missing',
                'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        plan = Plans.objects.create(plan_id=data['plan_id'], type=data['type'], total=data['total'],
                                    info=data['info'], rows=data['rows'], year=data['year'])

        return Response(data=PlanSerializer(plan).data, status=status.HTTP_201_CREATED)

    @staticmethod
    def update(request, pk=None):
        sel_plan = Plans.objects.get(pk=pk)

        sel_plan.plan_id = request.data['plan_id']
        sel_plan.type = request.data['type']
        sel_plan.info = request.data['info']
        sel_plan.rows = request.data['rows']
        sel_plan.total = request.data['total']
        sel_plan.year = request.data['year']

        sel_plan.save()

        return Response(data=PlanSerializer(sel_plan).data, status=status.HTTP_200_OK)

    @staticmethod
    def destroy(request, pk=None):
        plan = Plans.objects.get(pk=pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
