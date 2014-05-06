#coding=utf-8

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import encoding

import urllib2
import simplejson

from forms import DefaultForm,SearchForm

def welcome(request):
    return render_to_response('list.html')

def happy(request):

    result = ''
    final_result = ''
    stat=''
    total='0'
    lat='31.218816'
    lng='121.416603'
    if request.method == 'POST':
        form = DefaultForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            clienttype = form.cleaned_data['clienttype']
            postype = form.cleaned_data['postype']
            sorttype = form.cleaned_data['sorttype']
            lng = form.cleaned_data['lng']
            lat = form.cleaned_data['lat']
            distance = form.cleaned_data['distance']


            if keyword != '' or distance != '':
                url = createQuery(keyword, sorttype, clienttype, postype, lng, lat, distance)
                result = urllib2.urlopen(encoding.smart_str(url)).read()
                if result != '':

                    final_result = simplejson.loads(result)['records']
                    total = simplejson.loads(result)['totalhits']
    else:
        form = DefaultForm()

    return render_to_response('happytimes.html', {'form': form, 'total':total, 'result': final_result, 'lat':lat, 'lng':lng}, context_instance=RequestContext(request))


def search(request):
    
    result = ''
    final_result = ''
    stat=''
    total='0'
    alg = ''
    lat='31.218816'
    lng='121.416603'
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['query']
            lat = form.cleaned_data['lat']
            lng = form.cleaned_data['lng']
            print url
            if url.startswith("http://") is False:
                url = "http://192.168.5.149:4053/search/shop?"+url

            result = urllib2.urlopen(encoding.smart_str(url)).read()
            if result != '':
                all_result = simplejson.loads(result)
                final_result = all_result['records']
                print final_result
                alg = all_result['otherinfo']['algversion']
                total = simplejson.loads(result)['totalhits']
    else:
        form = SearchForm()

    return render_to_response('searchdemo.html', {'form': form, 'total':total, 'result': final_result, 'lat':lat, 'lng':lng, 'alg':alg}, context_instance=RequestContext(request))

def createQuery(keyword, sorttype, clienttype, postype, lng, lat, distance):
    keywordquery = ''
    gaodequery = ''
    if keyword != '':
        st = encoding.smart_unicode( keyword, 'utf8' )
        keywordquery = "keyword(searchkeyword,%s)," % (st)
        

    if clienttype == 'gaode':
        gaodequery = "term(clienttype,126),"
    query="query=%s%sgeo(%s,%s:%s,%s)" % (keywordquery,gaodequery,postype,lng,lat,distance)

    notquery=''
    if clienttype == 'dianping':
        notquery='&notquery=term(clienttype,126)'
    
    
    sort="&sort=desc(%s)" % (sorttype)
    if sorttype == 'dist':
        sort="&sort=asc(dist(%s,%s:%s))" % (postype,lng,lat)

    fl="&fl=defaultpic,avgprice,fulladdress,phone,shopid,shoppower,shopname,branchname,address,district,dist(%s,%s:%s)" % (postype,lng,lat)
    limitinfo="&limit=0,100&info=app:WechatNearbyCheckinSearch,platform:OPENAPI,queryid:test" 
    url='http://10.2.2.52:4163/search/shopwx?'
    url+=query
    url+= "%s%s%s%s" % (notquery,sort,fl,limitinfo)
    return url
