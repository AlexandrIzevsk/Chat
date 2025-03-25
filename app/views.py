from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from . models import Customer, Chat
from . forms import CustomerForm
from django.views.generic import UpdateView, ListView
from rest_framework import viewsets, permissions, status
from django.contrib.auth.models import User
from rest_framework.response import Response
from . import models
from . import forms
from . import serializers


class Profile(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'profile.html'
    success_url = '/chats/'

    def get_object(self, queryset=None):
        return self.request.user


class ListChats(ListView):
    form_class = forms.MessageForm
    template_name = 'chats.html'
    context_object_name = 'chats'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        user = self.request.user
        return Chat.objects.filter(members__user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.request.user
        customer = models.Customer.objects.get(user=self.request.user)
        context['customer'] = customer
        context['form'] = self.form_class
        print(context)
        return context


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChatViewSet(viewsets.ModelViewSet):
    queryset = models.Chat.objects.all()
    serializer_class = serializers.ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        customer = Customer.objects.get(user=user)
        return queryset.filter(members__in=[customer])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.members.clear()
        m = instance.message_set.all()
        m.delete()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        chat_id = self.request.query_params.get('chat_id', None)
        if chat_id and models.Chat.objects.filter(pk=chat_id).exists():
            if models.Chat.objects.get(pk=chat_id).members.contains(request.user) or request.user.is_superuser:
                serializer = self.serializer_class(self.queryset.filter(chat__id=chat_id, deleted=False), many=True, context={'request': request})
                data = serializer.data
                return Response(data)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        chat_id = pk
        if chat_id and models.Chat.objects.filter(pk=chat_id).exists():
            if models.Chat.objects.get(pk=chat_id).members.contains(request.user) or request.user.is_superuser:
                serializer = self.serializer_class(self.queryset.filter(chat__id=chat_id, deleted=False), many=True, context={'request': request})
                data = serializer.data
                return Response(data)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author_id == request.user.id:
            instance.deleted = True
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = forms.CustomerForm
    template_name = 'profile.html'
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user