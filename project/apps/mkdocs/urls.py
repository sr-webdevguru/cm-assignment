from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

doc_url = patterns('',
                   url(r'^oAuth/$', login_required(TemplateView.as_view(template_name='oAuth/index.html'))),
                   url(r'^Authentication/$',
                       login_required(TemplateView.as_view(template_name='Authentication/index.html'))),
                   url(r'^$', login_required(TemplateView.as_view(template_name='index.html'))),
                   )
