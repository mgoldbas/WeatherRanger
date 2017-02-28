from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView, ListView, DetailView, DeleteView
from datetime import datetime, timedelta
from WeatherRangerProject.forms import TemperatureRangeForm, CreateUserForm
from WeatherRangerProject.models import TemperatureRange, City
from WeatherRangerProject.tempertaure import get_temperature_simple


# Create your views here.



class EnterRangeView(FormView, ListView):
    form_class = TemperatureRangeForm
    template_name = 'list.html'
    context_object_name = 'temperature_range'
    model = TemperatureRange
    success_url = '/weather/'
    paginate_by = 10

    def get_queryset(self):
        query_set = super(EnterRangeView, self).get_queryset()
        return query_set.filter(user=self.request.user)


    def form_valid(self, form, **kwargs):
        form_obj = form.save(commit=False)
        form_obj.user_id = str(self.request.user.id)
        form_obj.save()
        return super(EnterRangeView, self).form_valid(form)

    def get_paginator(self, queryset, per_page, orphans=0,
                      allow_empty_first_page=True, **kwargs):

        query_set = super(EnterRangeView, self).get_paginator(queryset, per_page, orphans=0
                                                            , allow_empty_first_page=True, **kwargs)
        for range in query_set.object_list:
            range.current_temperature = get_temperature_simple(range.city.id)
            range.check_five_day_range()
            range.check_sixteen_day_range()
        return query_set



class DetailRangeView(DetailView):
    model = TemperatureRange
    template_name = 'form.html'


class ListCityView(ListView):
    model = City
    paginate_by = 10
    template_name = 'list_city.html'
    context_object_name = 'cities'



    def get_paginator(self, queryset, per_page, orphans=0,
                      allow_empty_first_page=True, **kwargs):

        query_set = super(ListCityView, self).get_paginator(queryset, per_page, orphans=0
                                                            , allow_empty_first_page=True, **kwargs)
        for city in query_set.object_list:
            city.current_temperature = get_temperature_simple(city.id)
        return query_set




class CreateUserView(FormView):
    form_class = CreateUserForm
    success_url = '/'
    template_name = 'form.html'

    def form_valid(self, form):
        form.save()
        user = User.objects.get(date_joined=datetime.now() - timedelta(seconds=.1))[0]
        login(user)
        return super(CreateUserView, self).form_valid(form)

