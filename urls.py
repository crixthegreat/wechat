#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2021/2/10 13:18:33

import makepoem

DEFAULT_MSG = ('欢迎来谈心，请使用关键词\n' + 
        '【二次元】来一张二次元美图\n' +
        #'【买家秀】送你一张淘宝买家秀\n' +
        '【汉子】来一张汉子图\n' +
        '【妹子】来一张妹子图\n' +
        #'【说一句】跟你聊一句\n' +
        '【舔狗】来一段舔舔的日记\n' +
        #'【撩我】轻轻撩你一下\n' +
        '【鸡汤】来一口毒鸡汤，爽\n' +
        '【来一句】聊一句正经话\n' + 
        '【来首诗】欣赏一首暴力机器诗'
        )

URL = {
        'comic':{'url':'https://acg.yanwz.cn/api.php', 'type':'img', 'trigger':'二次元'},
        #'taobao_show':{'url':'https://api.66mz8.com/api/rand.tbimg.php?format=jpg', 'type':'img', 'trigger':'买家秀'},
        'male':{'url':'https://api.66mz8.com/api/rand.portrait.php?type=%E7%94%B7&format=jpg', 'type':'img', 'trigger':'汉子'},
        'female':{'url':'https://api.66mz8.com/api/rand.portrait.php?type=%E5%A5%B3&format=jpg', 'type':'img', 'trigger':'妹子'},
        #'one_sentence':{'url':'https://api.ixiaowai.cn/api/ylapi.php','type':'txt', 'trigger':'说一句'},
        'tian_dog':{'url':'https://api.ixiaowai.cn/tgrj/index.php','type':'txt', 'trigger':'舔狗'},
        #'dirty_words':{'url':'https://api.66mz8.com/api/sweet.php?format=json','type':'json', 'keyword':'sweet', 'trigger':'撩我'},
        'poison_soup':{'url':'http://api.lkblog.net/ws/api.php', 'type':'json', 'keyword':'data', 'trigger':'鸡汤'}, 
        'hitokoto':{'url':'https://v1.hitokoto.cn/', 'type':'json', 'keyword':'hitokoto', 'trigger':'来一句'}, 
        'poem':{'url':'', 'type':'txt_event', 'keyword':makepoem.make_poem, 'trigger':'来首诗'}, 
        }

triggers = [item['trigger'] for key, item in URL.items()]
#print(triggers)
