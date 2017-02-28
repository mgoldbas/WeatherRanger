from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from WeatherRangerProject.tempertaure import calculate_five_day_upper_lower, calculate_sixteen_day_upper_lower
import requests
import json

API_KEY = '8e662200ba6ef23c0cc1c12a3aeaf9e3'

URL_TEMPLATE = "http://api.openweathermap.org/data/2.5/weather?id={}&appid={}"

# Create your models here.

class City(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    five_day_avg = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    sixteen_day_avg = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    country = models.CharField(max_length=200, null=True)


    def __str__(self):
        return self.name

    def current_temperature(self):
        data = self.fetch_temperature()
        temperature = data['temperature']
        visability = data['visability']
        description = data['description']
        obj_data = {'temperature':temperature, 'visability':visability, 'description':description, 'city':self}
        temp_obj = TemperatureRange(**obj_data)
        temp_obj.save()
        pass

    def fetch_temperature(self):
        """
        go to weather site and fetch temperature, create City Temperature Model and reassign relationship
        :return:
        """

        def get_temperature(id):
            url = URL_TEMPLATE.format(str(id), API_KEY)
            response = requests.get(url)
            return json.loads(response.text)

        return get_temperature(self.id)



    def five_day_calculate(self):
        """
        calculate the average temperature for the next three days
        :return:
        """
        pass

    def sixteen_day_calculate(self):
        """
        calculate the average temperature for the next seven days
        :return:
        """
        pass

class CityTemperature(models.Model):
    """
    Model for storing historical city data
    """
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.DecimalField(decimal_places=2, max_digits=5)
    visability = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    date_created = models.DateField(auto_now=True) #TODO switch this to a datetime field


class TemperatureRange(models.Model):
    min_temperature = models.DecimalField(decimal_places=2, max_digits=5)
    max_temperature = models.DecimalField(decimal_places=2, max_digits=5)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_in_range = models.NullBooleanField(blank=True)
    is_in_five_day_range = models.NullBooleanField(blank=True)
    is_in_sixteen_day_range = models.NullBooleanField(blank=True)

    def check_current_range(self):
        """
        check to see if within current range
        :return:
        """
        temperature = 80
        if (self.max_temperature > temperature) and (self.min_temperature < temperature):
            self.is_in_range = True
        else:
            self.is_in_range = False

    def check_five_day_range(self):
        """
        check to see if three day moving average is within current range
        :return:
        """
        upper, lower = calculate_five_day_upper_lower(self.city.id)
        if (self.max_temperature < upper ) and (self.min_temperature > lower):
            self.is_in_five_day_range = True
        else:
            self.is_in_five_day_range = False
        pass

    def check_sixteen_day_range(self):
        """
        check to see if within current range
        :return:
        """
        upper, lower = calculate_sixteen_day_upper_lower(self.city.id)
        if (self.max_temperature < upper) and (self.min_temperature > lower):
            self.is_in_sixteen_day_range = True
            print(self.max_temperature)
            print(self.min_temperature)
            print(upper)
            print(lower)
        else:
            self.is_in_sixteen_day_range = False
        pass

    class Meta:
        ordering = ('city',)



admin.site.register([TemperatureRange, CityTemperature, City])