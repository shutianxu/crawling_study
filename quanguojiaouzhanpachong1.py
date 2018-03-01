"""
quanghuojiayouzhandizhi
"""
import pandas as pd
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import math
import json
import urllib

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 偏心率平方

url2 = "&key=FBOBZ-VODWU-C7SVF-B2BDI-UK3JE-YBFUS&output=jsonp&pf=jsapi&ref=jsapi&cb=qq.maps._svcb3.geocoder0"
url1 = "http://apis.map.qq.com/jsapi?qt=geoc&addr="
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}


class Geocoding:
    def __init__(self, api_key):
        self.api_key = api_key

    def geocode(self, address):
        """
        利用高德geocoding服务解析地址获取位置坐标
        :param address:需要解析的地址
        :return:
        """
        geocoding = {'s': 'rsv3',
                     'key': self.api_key,
                     'city': '全国',
                     'address': address}
        geocoding = urllib.parse.urlencode(geocoding)
        ret = urllib.request.urlopen("%s?%s" % ("http://restapi.amap.com/v3/geocode/geo", geocoding))

        if ret.getcode() == 200:
            res = ret.read()
            json_obj = json.loads(res)
            if json_obj['status'] == '1' and int(json_obj['count']) >= 1:
                geocodes = json_obj['geocodes'][0]
                lng = float(geocodes.get('location').split(',')[0])
                lat = float(geocodes.get('location').split(',')[1])
                return [lng, lat]
            else:
                return None
        else:
            return None


def gcj02_to_bd09(lng, lat):
    """
    火星坐标系(GCJ-02)转百度坐标系(BD-09)
    谷歌、高德——>百度
    :param lng:火星坐标经度
    :param lat:火星坐标纬度
    :return:
    """
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lng, bd_lat]


def bd09_to_gcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    :param bd_lat:百度坐标纬度
    :param bd_lon:百度坐标经度
    :return:转换后的坐标列表形式
    """
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return [gg_lng, gg_lat]


def wgs84_to_gcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:
    """
    if out_of_china(lng, lat):  # 判断是否在国内
        return lng, lat
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]


def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return lng, lat
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def bd09_to_wgs84(bd_lon, bd_lat):
    lon, lat = bd09_to_gcj02(bd_lon, bd_lat)
    return gcj02_to_wgs84(lon, lat)


def wgs84_to_bd09(lon, lat):
    lon, lat = wgs84_to_gcj02(lon, lat)
    return gcj02_to_bd09(lon, lat)


def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)










def get_one_page(url):
    try:
        response = requests.get(url,headers = headers)
        if response.status_code ==200:
            return response.text
        return None
    except RequestException:
        return None


def parse_page_jiayouzhan_wangdian(html):
        try:
            soup = BeautifulSoup(html,'html5lib')
            lls1 = soup.select('body div.left-module.fl div.w730m.w730m02.net-panel a.blue.more')

            for x in lls1:
               jiayouzhan_wangdian.append(x.get('href'))       
        except:
            pass    
        
def parse_page_page(html):
        try:
            soup = BeautifulSoup(html,'html5lib')
            lls1 = soup.select('div.left-module.fl div.left-panel-part.net-count span.red')

            for x in lls1:
                page.append(math.ceil(float(x.get_text().strip())/30.0))    
        except:
            pass    
    
    
def parse_page(html):
        try:
            soup = BeautifulSoup(html,'html5lib')
            lls1 = soup.select('div.left-module.fl div.w730m.w730m02.net-panel div.text.w575.fl a')
            lls2 = soup.select('div.left-module.fl div.w730m.w730m02.net-panel div.text.w575.fl p')
            lls3 = soup.select('div.crumbsBox div.fl a.red')
            
            
            for x in lls1:
                name.append(x.get_text().strip())
                
            for y in lls2:
                address.append(y.get_text().strip())
                
                for z in lls3:
                    city.append(z.get_text().strip())
        except:
            pass        


#爬加油站地址
jiayouzhan_wangdian=[]
page = []
address = []
name = []
city =[]
for i in range(32):
    url = 'https://energy.cngold.org/jyzwd_'+str(i+2)+'.htm'
    html = get_one_page(url)
    parse_page_jiayouzhan_wangdian(html)
    
url = 'https://energy.cngold.org/jyzwd_405.htm'
html = get_one_page(url)
parse_page_jiayouzhan_wangdian(html)
url = 'https://energy.cngold.org/jyzwd_441.htm'
html = get_one_page(url)
parse_page_jiayouzhan_wangdian(html)


for j in range(len(jiayouzhan_wangdian)):
    html = get_one_page(jiayouzhan_wangdian[j])
    parse_page_page(html)
    url_1 = jiayouzhan_wangdian[j][:-4]
    for i in range(page[j]):
        url = url_1 + '_p' + str(i+1) + '.htm'
        html = get_one_page(url)
        parse_page(html)
        
print(len(name))
print(len(address))
print(len(city))



#通过地址查询经纬度坐标
nam = []
add=[]
point_lng=[]
point_lat=[]
cit = []
for line in range(len(address)):
    
    url = url1 + address[line] + url2    
    try:
        response = requests.get(url,headers = headers)
              
        result = response.text[51:-1]
        #print(result) #获取解析的数据
        result1 = json.loads(result)  #生成字典
        pointx = result1['detail']['pointx']
        pointy = result1['detail']['pointy']
        nam.append(name[line])
        add.append(address[line])
        point_lng.append(pointx)
        point_lat.append(pointy) 
        cit.append(city[line])
        print(address[line])
# =============================================================================
#         #写文件
#         lin = line + '\t' + str(pointx) + '\t' + str(pointy) + '\n'
#         print(lin)
#         with open(r'D:\document\crawling\jiayouzhandizhi.txt','a',encoding='utf-8') as f:
#             f.write(lin)
# =============================================================================
            
            
    except:
        print('pase_error!')




#坐标转化
new_point_lng = []
new_point_lat = []
code = []
for lng,lat in zip(point_lng,point_lat):
    lng = float(lng)
    lat = float(lat)
    new_lng,new_lat = gcj02_to_wgs84(lng,lat)
    new_point_lng.append(new_lng)
    new_point_lat.append(new_lat)
    print(new_lng)
    print(new_lat)

for i in range(len(add)):
    code.append(i)


g = Geocoding('API_KEY')

print(len(name))
print(len(add))
print(len(new_point_lng))
print(len(new_point_lat))
print(len(code))
print(len(city))


df = pd.DataFrame({ 
                    'name' : nam,
                    'address' : add,
                    'WGS84_point_lng' : new_point_lng,
                    'WGS84_point_lat' : new_point_lat,
                    'code' : code,
                    'city' : cit

                         })

    
df.to_csv('D:\document\crawling\quanguojiayouzhandizhi_new.csv')    


