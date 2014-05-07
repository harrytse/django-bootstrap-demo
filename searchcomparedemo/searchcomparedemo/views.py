#coding=utf-8

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import encoding

import urllib2
import simplejson

from forms import DefaultForm,SearchForm, ShopSearchForm

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

    return render_to_response('happytimes.html', {'form': form, 'total':total, 'result': final_result, 'lat':lat, 'lng':lng }, context_instance=RequestContext(request))

def replace_query(head,tail,substr,oristr):
    idx1 = oristr.find(head)
    print idx1
    idx2 = oristr.find(tail,idx1,len(oristr))

    print idx2
    return oristr[:idx1]+substr+oristr[idx2+1:]


def search(request):
    
    result = ''
    final_result = ''
    stat=''
    total='0'
    alg = ''
    lat='31.218816'
    lng='121.416603'
    reallatlng = ''
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['query']
            lat = form.cleaned_data['lat']
            lng = form.cleaned_data['lng']
            print url
            tranformurl = "http://api.gpsspg.com/convert/latlng/?oid=9&key=FFDAE45D94A3DA29DE4CB6838048D18F&from=1&to=0&latlng=%s,%s" %(lat,lng)
            latlngresult = urllib2.urlopen(encoding.smart_str(tranformurl)).read()
            latlngresultjson = simplejson.loads(latlngresult)
            print latlngresult
            reallat = latlngresultjson['result'][0]['lat']
            reallng = latlngresultjson['result'][0]['lng']
            reallatlng = '纬度：'+str(reallat)+" 经度："+str(reallng)
            if url.startswith("http://") is False:
                url = "http://192.168.5.149:4053/search/shop?"+url
            geoLatLng = 'geo(poi,'+str(reallng)+':'+str(reallat)+",1000)"
            distLatLng = 'dist(poi,'+str(reallng)+':'+str(reallat)+")"
            url = replace_query('geo(', ')', geoLatLng, url)
            url = replace_query('dist(', ')', distLatLng, url)

            print url
            result = urllib2.urlopen(encoding.smart_str(url)).read()
            if result != '':
                all_result = simplejson.loads(result)
                final_result = all_result['records']
                #print final_result
                alg = all_result['otherinfo']['algversion']
                total = simplejson.loads(result)['totalhits']
    else:
        form = SearchForm()

    return render_to_response('searchdemo.html', {'form': form, 'total':total, 'result': final_result, 'lat':lat, 'lng':lng, 'alg':alg, 'reallatlng':reallatlng}, context_instance=RequestContext(request))

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


def shopsearch(request):

    result = ''
    final_result = ''
    stat=''
    total='0'
    alg = ''
    lat='31.218816'
    lng='121.416603'
    if request.method == 'POST':
        form = ShopSearchForm(request.POST)
        if form.is_valid():
            lat = form.cleaned_data['lat']
            lng = form.cleaned_data['lng']
            category = form.cleaned_data['category']
            radius = form.cleaned_data['radius']
            q_w = form.cleaned_data['quality']
            d_w = form.cleaned_data['dist']
            url = createShopQuery(lat, lng, category, radius, q_w, d_w)
            print url
            result = urllib2.urlopen(encoding.smart_str(url)).read()
            if result != '':
                all_result = simplejson.loads(result)
                final_result = all_result['records']
                #print final_result
                alg = all_result['otherinfo']['algversion']
                total = simplejson.loads(result)['totalhits']
    else:
        form = ShopSearchForm()

    return render_to_response('shopsearchdemo.html', {'form': form, 'total':total, 'result': final_result, 'lat':lat, 'lng':lng, 'alg':alg}, context_instance=RequestContext(request))


def createShopQuery(lat, lng, category='10', radius='1000', baseWeight='7', distWeight='3', businessWeight='0.3', localClickWeight='0', wifiWeight='0', sort='shopnewlocal', interval='100'):
    if category!='0':
        cate = 'term(categoryids,%s),' % category
    else:
        cate = ''
    query = 'http://192.168.5.149:4053/search/shop?query=%sgeo(gpoi,%s:%s,%s)' \
            '&sort=desc(%s)&limit=0,100&fl=shopid,shopname,shoppower,address,avgprice,maincategoryname,dist(gpoi,%s:%s),' \
            'defaultpic&info=app:PointShopSearch,platform:MAPI,recordscoredetail:true,interval:%s,' \
            'debug:true,localClick:%s,dist:%s,base:%s' \
            % (cate,lng,lat,radius,sort,lng,lat,interval,localClickWeight,distWeight,baseWeight)
    return query