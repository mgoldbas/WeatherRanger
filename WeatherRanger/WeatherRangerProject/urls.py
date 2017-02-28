from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from WeatherRangerProject.views import EnterRangeView, DetailRangeView, CreateUserView, ListCityView

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', login_required(DetailRangeView.as_view()), name='detail_range'),
    url(r'^$', login_required(EnterRangeView.as_view(), login_url='/login/'), name='home'),

]
