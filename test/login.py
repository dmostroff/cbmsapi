import http.client
import urllib.parse
import requests

baseUrl = 'http://localhost:8000'
baseHeader={"Content-Type": "application/json"}
loginParams = { "username": "dano", "password": "?Ch3$3d!"}

def GetUrl( apiPath):
    if isinstance(apiPath, str):
        url = '/'.join([baseUrl, apiPath, ''])
    elif isinstance(apiPath, list):
        url = '/'.join([baseUrl]+apiPath+[''])
    return url

def SetHeader( token):
    header = baseHeader
    header['Authorization'] = 'Bearer '+token['access']
    return header

def GetRequest( token, apiPath):
    url = GetUrl(apiPath)
    header = SetHeader(token)
    response = requests.get(url,headers=header)
    if 200 == response.status_code:
        return response.json()
    else:
        raise Exception("Status is {0}".format(response.status_code))

url = GetUrl('login')
response = requests.post(
    url,
    json=loginParams,
    headers=baseHeader )

token = None
if 200 == response.status_code:
    json_res = response.json()
    if 0 == json_res['rc']:
        user_data = json_res['data']
        token = user_data['token']

if 'access' in token:
    print( token['access'])
    data = GetRequest(token, ['cc', 'card'])
    print( data)
    data = GetRequest(token, ['cc', 'company'])
    print( data)
    # header = SetHeader(token)
    # url = GetUrl(['cc', 'card'])
    # re_path( 'adm/setting/(?P<adm_setting_id>[1-9][0-9]*)?/?$', admsetting.AdmSettingView.as_view()),
    # # Cc
    # re_path( 'cc/card/(?P<cc_card_id>[1-9][0-9]*)?/?$', cccard.CcCardView.as_view()),
    # re_path( 'cc/company/(?P<cc_company_id>[1-9][0-9]*)?/?$', cccompany.CcCompanyView.as_view()),

# conn = http.client.HTTPConnection("localhost", 8000)
# conn.putheader("Content-Type", "application/json")
# loginParams = urllib.parse.urlencode(loginData)
# conn.request("POST", "/login", loginParams)
# response = conn.getresponse()
# if response.status == 200:
#     userData = response.read()
#     print(userData)
