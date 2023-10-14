from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def testView(req):
    return HttpResponse("<p>test</p>")
