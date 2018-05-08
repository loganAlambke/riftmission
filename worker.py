from django.shortcuts import render
from django.http import HttpResponse
import django
django.setup()
from django.shortcuts import render
from django.views import View
from rift_missions.forms import missionForm
from rift_missions.models import Input
import requests
import psycopg2
import psycopg2.extras
from datetime import datetime
from django.core import serializers
from ratelimit.mixins import RatelimitMixin
import datetime
import os





class blob():


    threading.Timer(3600, db_update).start()
    summoners = Input.objects.all().values_list('account_id','summoner_id','region')
    summoners = summoners

    def update(x):
        api_key = apikey
        account_id =  x[0]
        summoner_id = x[1]
        region = x[2]
        item_dict ={}
        all_kills = []
        url = "https://" + region + ".api.riotgames.com/lol/match/v3/matchlists/by-account/" + str(
            account_id) + "?endTime=1521401934000&beginTime=1520969934000" + "&api_key=" + api_key
        json = (requests.get(url)).json()
        response = requests.get(url)

        if response.status_code != 200:
            pass


        else:
            gidlist = []
            for each in json['matches']:
                if each['champion'] == 202:
                    gidlist.append(str(each['gameId']))

                else:
                    pass

        for each in gidlist:
            url = "https://" + region + ".api.riotgames.com/lol/match/v3/matches/" + each + "?api_key=" + api_key
            response = requests.get(url)
            if response.status_code != 200:
                pass

            else:
                # url = "https://" + region + ".api.riotgames.com/lol/match/v3/matches/" + each + "?api_key=" + api_key
                json = (requests.get(url)).json()
                participantIdentities = json['participantIdentities']
                for each in participantIdentities:
                    if each['player']['summonerId'] == int(summoner_id):
                        participantId = each['participantId']
                for each in json['participants']:
                    if each['participantId'] == participantId:
                        kills = each['stats']['kills']
                        all_kills.append(kills)
                        items = [each['stats']['item0'], each['stats']['item1'], each['stats']['item2'],each['stats']['item3'],each['stats']['item4'], each['stats']['item5'], each['stats']['item6']]
                        item_dict[kills] = items


        if all_kills:
            top_kill = max(all_kills)
            print(top_kill)
            items = item_dict[top_kill]
            item0 = str(items[0])
            item1 = str(items[1])
            item2 = str(items[2])
            item3 = str(items[3])
            item4 = str(items[4])
            item5 = str(items[5])
            item6 = str(items[6])
            update = Input.objects.filter(summoner_id=summoner_id).update(top_kill=top_kill, item0=item0, item1=item1,
                                                                          item2=item2, item3=item3, item4=item4,
                                                                          item5=item5, item6=item6)

        else:
            pass




        result = x
        return(result)

    start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = executor.map(update, summoners)

    end = time.time()
    print('time to finish:')
    print(end-start)
    print(result)





blob()