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



#def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")

apikey = "RGAPI-07c20519-f4e8-41e4-a661-41de24ddb41b"

class Homeview(View):
	template_name = 'rift_missions/index.html'
	template_name1 = 'rift_missions/confirmation.html'
	form_class = missionForm

	apikey = "RGAPI-07c20519-f4e8-41e4-a661-41de24ddb41b"
	
    



	def get(self, request):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})


	def post(self, request):
	    form = self.form_class(request.POST)
	    if form.is_valid():

	        #text = form.cleaned_data['username']
	        apikey = "RGAPI-07c20519-f4e8-41e4-a661-41de24ddb41b"
	        username = str(form.cleaned_data['username'])
	        
	        region = form.cleaned_data['region']
	        api_key = apikey
	        item_dict = {}
	        all_kills = []
	        
	        
	        # Get summoner id using player's name


	        url = "https://" + region + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + username + "?api_key=" + api_key
	        response = requests.get(url)
	        
	        if response.status_code == 403:
	            return(self.template_name)
	        if response.status_code != 200:
	            return render(
	                request,
	                self.template_name,
	                {'form': form}
	            )
	        else:
	            json = (requests.get(url)).json()
	            summoner_id = json['id']
	            account_id = json['accountId']
	            


	            url = "https://" + region + ".api.riotgames.com/lol/match/v3/matchlists/by-account/" + str(account_id) + "?api_key=" + api_key
	            
	            json = (requests.get(url)).json()
	            response = requests.get(url)
	            
	            if response.status_code != 200:
	                return render(
	                    request,
	                    self.template_name1,
	                    {'form': form}
	                )
	            else:
	                gidlist = []
	                for each in json['matches']:
	                    if each['champion'] == 202:
	                        gidlist.append(str(each['gameId']))
	                    else:
	                        top_kill = 0
	                        item0 = 0
	                        item1 = 0
	                        item2 = 0
	                        item3 = 0
	                        item4 = 0
	                        item5 = 0
	                        item6 = 0
	               


	            # get game data with gameID. First match summ ID with player ID in game to get played ID stats
	            for each in gidlist:
	                url = "https://" + region + ".api.riotgames.com/lol/match/v3/matches/" + each + "?api_key=" + api_key
	                json = (requests.get(url)).json()
	                response = requests.get(url)
	            
	                if response.status_code != 200:
	                    return render(
	                        request,
	                        self.template_name,
	                        {'form': form}
	                    )
	                else:
	                    participantIdentities = json['participantIdentities']
	                    for each in participantIdentities:
	                        if each['player']['summonerId'] == summoner_id:
	                            participantId = each['participantId']
	                    for each in json['participants']:
	                        if each['participantId'] == participantId:
	                            kills = each['stats']['kills']
	                            all_kills.append(kills)
	                            items = [each['stats']['item0'], each['stats']['item1'], each['stats']['item2'], each['stats']['item3'],
	                                     each['stats']['item4'], each['stats']['item5'], each['stats']['item6']]

	                            item_dict[kills] = items

	        if all_kills:
	            top_kill = max(all_kills)
	            items = item_dict[top_kill]
	            item0 = str(items[0])
	            item1 = str(items[1])
	            item2 = str(items[2])
	            item3 = str(items[3])
	            item4 = str(items[4])
	            item5 = str(items[5])
	            item6 = str(items[6])
	            

	            try:
	                conn = psycopg2.connect(dbname='rift_missions', user='postgres', host='localhost', password='battery1')
	                print('opened success')
	            except:
	                print(datetime.now(), 'unable to connect')
	                return
	            else:
	                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	            # write data to db

	            cur.execute('''INSERT INTO rift_missions_input(username, summoner_id, account_id, top_kill, region, item0, item1, item2, item3, item4, item5, item6)
	                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (
	            username, summoner_id, account_id, top_kill, region, item0, item1, item2, item3, item4, item5,
	            item6))

	            conn.commit()
	            cur.close()
	            conn.close()

	            # return HttpResponseRedirect('/mission/')
	            args = {'form': form, 'username': username, 'account_id': account_id, 'summoner_id': summoner_id,
	                    'top_kill': top_kill, 'region': region, }
	            #return template saying they have been entered
	            return render(request, self.template_name1, args)

	        else:
	            top_kill = 0
	            try:
	                conn = psycopg2.connect(dbname='rift_missions', user='postgres', host='localhost', password='battery1')
	                print('opened success')
	            except:
	                print(datetime.now(), 'unable to connect')
	                return
	            else:
	                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	                # write data to db

	            cur.execute('''INSERT INTO rift_missions_input(username, summoner_id, account_id, top_kill, region, item0, item1, item2, item3, item4, item5, item6)
	                                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (
	                username, summoner_id, account_id, top_kill, region, item0, item1, item2, item3, item4, item5,
	                item6))

	            conn.commit()
	            cur.close()
	            conn.close()

	            # return HttpResponseRedirect('/mission/')
	            args = {'form': form, 'username': username, 'account_id': account_id, 'summoner_id': summoner_id,
	                    'top_kill': top_kill, 'region': region, }
	            return render(request, self.template_name1, args)



	                # open db


	    else:
	        return render(
	            request,
	            self.template_name,
	            {'form': form}
	        )



def highscores(request):
	poop = Input.objects.order_by('-top_kill')[:25]

	names = serializers.serialize('python', poop, fields=('username'))
	kills = serializers.serialize('python', poop, fields=('top_kill'))
	item0 = serializers.serialize('python', poop, fields=('item0'))
	item1 = serializers.serialize('python', poop, fields=('item1'))
	item2 = serializers.serialize('python', poop, fields=('item2'))
	item3 = serializers.serialize('python', poop, fields=('item3'))
	item4 = serializers.serialize('python', poop, fields=('item4'))
	item5 = serializers.serialize('python', poop, fields=('item5'))
	item6 = serializers.serialize('python', poop, fields=('item6'))

	# 'item0': item0

	args = {'kills': kills, 'names': names, 'item0': item0, 'item1': item1, 'item2': item2, 'item3': item3,
	        'item4': item4, 'item5': item5, 'item6': item6}

	return render(request, 'rift_missions/highscores.html', args)


def missions(request):
	return render(request, 'rift_missions/missions.html')

def home(request):
	return render(request, 'rift_missions/home.html')


def permission_denied(request):
	response = render_to_response(
	    'errors/403.html'
	)

	return HttpResponseNotFound(response.content)


def custom_403(request, exception):
	return render(request, 'rift_missions/403.html', {}, status=403)

def custom_500(request):
	return render(request, 'rift_missions/500.html', {}, status=500)
