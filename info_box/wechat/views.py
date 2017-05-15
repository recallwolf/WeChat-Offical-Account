#coding=utf-8

# Create your views here.
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import (TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage, ShortVideoMessage)

conf = WechatConf(
    token='wechatinfobox', 
    appid='wxfe5f1438b661e667', 
    appsecret='81eca465fa6fb0ad8968e418712fe25d', 
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='yzJY6Q5IhOlJmd9A28qS4Q1chANB9rkLTqirRTNbTTG'  # 如果传入此值则必须保证同时传入 token, appid
)

@csrf_exempt
def wechat(request):
    signature = request.GET.get('signature', '')
    timestamp = request.GET.get('timestamp', '')
    nonce = request.GET.get('nonce', '')
	

    wechat_instance = WechatBasic(conf=conf)
    # 验证微信公众平台的消息
    if wechat_instance.check_signature(signature!=signature, timestamp!=timestamp, nonce!=nonce):
        return HttpResponseBadRequest('Verify Failed')
    else:
        if request.method == 'GET':
           response = request.GET.get('echostr', 'error')
        else:
            try:
                wechat_instance.parse_data(request.body)
                message = wechat_instance.get_message()
            except ParseError:    
                return HttpResponseBadRequest('Invalid XML Data')
               

        response = wechat_instance.response_text(
        content=(
            '感谢您的关注！\n回复【help】查看支持的功能'
            '\n【<a href="http://www.rwnexus.site">我的博客</a>】'
            ))                                             
        if isinstance(message, TextMessage):
        # 当前会话内容
            content = message.content.strip()
            if content == 'help':
                reply_text = (
                    '目前支持的功能：\n1. 输入【博客】来查看我的博客\n'
                    '2. 回复【天气】来获取近几日天气情况\n'
                    '3. 回复【快递】来查询快递情况\n'
                    '还有更多功能正在开发中哦 ^_^\n'
                    '【<a href="http://www.rwnexus.site">我的博客</a>】'
                    )
            elif content == u'博客':
                reply_text = '我的博客地址是http://www.rwnexus.site'
            elif content == u'天气':
                reply_text = '天气功能还在开发中噢,亲可以先查看【<a href="http://www.rwnexus.site">我的博客</a>】'
            elif content == u'快递':
                reply_text = '快递功能还在开发中噢,亲可以先查看【<a href="http://www.rwnexus.site">我的博客</a>】'    
            else:
                reply_text = '功能还在开发中哦,亲可以提出您宝贵的意见' 

            response = wechat_instance.response_text(content=reply_text)
            
        return HttpResponse(response, content_type="application/xml")