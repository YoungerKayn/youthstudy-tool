import requests,json,time
import urllib.parse

#如不使用github actions，请删除下方注释并手动设定xLitemallToken或mid
#xLitemallToken=""
#mid=
apiHeaders = {
  'Host': 'tuanapi.12355.net',
  'Connection': 'keep-alive',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Origin': 'https://tuan.12355.net',
  'User-Agent': 'MicroMessenger',
  'X-Requested-With': 'com.tencent.mm',
  'Sec-Fetch-Site': 'same-site',
  'Sec-Fetch-Mode': 'cors',
  'Referer': 'https://tuan.12355.net/wechat/view/YouthLearning/page.html',
  'Accept-Encoding': 'gzip, deflate',
  'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}
youthstudyHeaders = {
        'Host': 'youthstudy.12355.net',
        'Connection': 'keep-alive',
        'Content-Length': '134',
        'Origin': 'https://youthstudy.12355.net',
        'X-Litemall-Token': '',
        'X-Litemall-IdentiFication': 'young',
        'User-Agent': 'MicroMessenger',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'X-Requested-With': 'com.tencent.mm',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://youthstudy.12355.net/h5/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
headers = {
    'Host': 'youthstudy.12355.net',
    'Connection': 'keep-alive',
    'X-Litemall-Token': '',
    'X-Litemall-IdentiFication': 'young',
    'User-Agent': 'MicroMessenger',
    'Accept': '*/*',
    'Origin': 'https://youthstudy.12355.net',
    'X-Requested-With': 'com.tencent.mm',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://youthstudy.12355.net/h5/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}
#检查xLitemallToken或mid
if ('xLitemallToken' in locals().keys()) == True:
    pass
elif ('mid' in locals().keys()) == True:
    #将mid转换为xLitemallToken
    payload="sign="+urllib.parse.quote((json.loads(requests.get('https://tuanapi.12355.net/questionnaire/getYouthLearningUrl?mid='+str(mid),headers=apiHeaders).text))['youthLearningUrl'].replace('https://youthstudy.12355.net/h5/#/?sign=',''))
    rp=json.loads((requests.post('https://youthstudy.12355.net/apih5/api/user/get',headers=youthstudyHeaders,data=payload)).text)
    xLitemallToken=rp["data"]["entity"]["token"]
else:
    exit('+===========================+\n| mid或xLitemallToken未定义！ |\n+===========================+')
headers['X-Litemall-Token']=xLitemallToken

#获取积分、徽章
class GetProfile:
    profile_dist=json.loads(requests.get('https://youthstudy.12355.net/saomah5/api/myself/get',headers=headers).text)
    if profile_dist['errmsg'] == '成功':
        def score():
            return(GetProfile.profile_dist['data']['entity']['score'])
        def medal():
            return(GetProfile.profile_dist['data']['entity']['medal']['name'])

if __name__ == '__main__':#防止import的时候被执行
    # 获取时间戳
    t = int(round(time.time()* 1000))

    score=GetProfile.score()#获取打卡前积分，用于后续计算
    # (广东)每日签到
    print("开始签到:")
    mark = requests.get('https://youthstudy.12355.net/saomah5/api/young/mark/add', headers=headers)
    msg=json.loads(mark.text).get('msg')
    print(msg)

    # 青年大学习打卡
    # 获得最新学习章节
    latest = requests.get('https://youthstudy.12355.net/saomah5/api/young/chapter/new', headers=headers)

    chapterId=json.loads(latest.text).get('data').get('entity').get('id')
    updateDate=json.loads(latest.text).get('data').get('entity').get('updateDate')
    name=json.loads(latest.text).get('data').get('entity').get('name')

    data = {
        'chapterId': chapterId,
    }
    # 打卡
    print("打卡最新一期青年大学习:")
    saveHistory = requests.post('https://youthstudy.12355.net/saomah5/api/young/course/chapter/saveHistory', headers=headers, data=data)
    #print(saveHistory.text)

    print("更新日期:",updateDate,"名称:",name,"打卡状态:",json.loads(saveHistory.text).get('msg'))

    #学习频道-我要答题”
    #获得题目
    print("\n刷题:")
    getList = requests.get('https://youthstudy.12355.net/saomah5/api/question/list', headers=headers)
    #print(getList.text)
    questionlist=json.loads(getList.text).get("data").get("list")
    submit_output=''
    for questions in questionlist:
        #print(questions['id'])
        json_data = {
        'dataId': questions['id'],
        'commitDetails': [
            {
                'questionId': '1510063654195441665',
                'answer': '2,3,4',
                'active': True,
                'questionType': 1,
            },
            {
                'questionId': '1510063654187053058',
                'answer': '2,4',
                'active': True,
                'questionType': 1,
            },
            {
                'questionId': '1510063654203830274',
                'answer': '1,2,4',
                'active': True,
                'questionType': 1,
            },
            {
                'questionId': '1510063654208024578',
                'answer': '1,2,4',
                'active': True,
                'questionType': 1,
            },
            {
                'questionId': '1510063654191247361',
                'answer': '1,3',
                'active': True,
                'questionType': 1,
            },
        ],
        }
        #刷题
        submit = requests.post('https://youthstudy.12355.net/saomah5/api/question/submit/question', headers=headers, json=json_data)
        print(json.loads(submit.text).get('msg'),end="")
        submit_output=submit_output+json.loads(submit.text).get('msg')

    #学习频道-广东共青团原创专区
    params = {
        'channelId': '1457968754882572290',
        'time': t,
    }
    getarticle = requests.get('https://youthstudy.12355.net/saomah5/api/article/get/channel/article', params=params, headers=headers)
    articleslist = json.loads(getarticle.text).get("data").get("entity").get("articlesList")
    print("\n刷文章:")
    addScore_output=''
    availableArticles=0
    for articles in articleslist:
        if articles['scoreStatus'] == False:
            params = {
                'id': articles['id'],
            }
            addScore = requests.get('https://youthstudy.12355.net/saomah5/api/article/addScore', params=params, headers=headers)
            print(json.loads(addScore.text).get('msg'),end="")
            addScore_output=addScore_output+json.loads(addScore.text).get('msg')
            availableArticles+=1
    if availableArticles==0:
        print("无可供学习文章")
        addScore_output=addScore_output+"无可供学习文章"
    output={}
    output['title']=name+'签到'+json.loads(saveHistory.text).get('msg')
    output['result']="更新日期:"+updateDate+"\n名称:"+name+"\n打卡状态:"+json.loads(saveHistory.text).get('msg')+"\n刷题：\n"+submit_output+"\n刷文章：\n"+addScore_output
    output['score']=score
    with open('result.txt','a',encoding='utf8') as new_file:
        new_file.write(str(output))