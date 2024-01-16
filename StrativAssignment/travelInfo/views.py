from rest_framework import generics
from .models import District
from .serializers import DistrictSerializer
from Helper import  forecasts, avgTemp
from itertools import islice
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta

class DistrictListCreateView(generics.ListCreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class GetAvgForecast(APIView):
    serializer_class = DistrictSerializer

    def get(self, request, *args, **kwargs):
        districts = District.objects.all()
        coolest_districts = {}

        current_date = datetime.now()
        date_after_seven_days = current_date + timedelta(days=7)
        current_date=current_date.strftime('%Y-%m-%d')
        formatted_date = date_after_seven_days.strftime('%Y-%m-%d')
        
        for district in districts:
            
            each_district_temp = forecasts.getForecasts(district.lat, district.long, f"{current_date}T00:00", f"{formatted_date}T00:00")
            coolest_districts[district.name] = avgTemp.getAvgTemp(each_district_temp)
            
        sorted_dict_asc = dict(sorted(coolest_districts.items(), key=lambda item: item[1]))
        top_n_items = dict(islice(sorted_dict_asc.items(), 10))

        return Response({'coolest_districts': top_n_items})
    
class TravelDecision(APIView):
    
    def post(self, request, *args, **kwargs):

            
            friend_location = District.objects.get(name=request.data['friend_location'])
            destination_location = District.objects.get(name=request.data['destination'])
            travel_date = datetime.strptime(request.data['travel_date'], '%Y-%m-%d')
            formatted_date = travel_date.strftime("%Y-%m-%d")

            friend_forecast = forecasts.getForecasts(friend_location.lat,friend_location.long,f"{formatted_date}T20:00",f"{formatted_date}T20:00")
            destination_forecast = forecasts.getForecasts(destination_location.lat,destination_location.long,f"{formatted_date}T20:00",f"{formatted_date}T20:00")

            decision = "Recommended" if destination_forecast['temperature_2m'].iloc[0] > friend_forecast['temperature_2m'].iloc[0] else "Not Recommended"
            
            return Response({'decision': decision,'friend_forecast':friend_forecast,'destination_forecast':destination_forecast})
        

