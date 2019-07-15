from django.urls import reverse
from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin
from crm import models
from django.conf import settings

class AuthMiddleware ( MiddlewareMixin ):
    def process_request(self, request):
        if request.path_info in [reverse ( "login" ), reverse ( "reg" )]:
            return
        if request.path_info.startswith ( "/admin/" ):
            return
        pk= request.session.get("u_id")
        user = models.UserProfile.objects.filter(pk=pk).first()
        if not user:
            return render(request, "login.html")
        request.user_obj = user


