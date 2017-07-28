import re
import json

text = '<link rel="alternate" type="application/vnd.wap.xhtml+xml" media="handheld" href="http://xw.qq.com/c/news/20170727054126"><script type="text/javascript">' \
       'ARTICLE_INFO = window.ARTICLE_INFO || {' \
       'site:\'news\', ' \
       'site_cname:\'新闻\',\
        site_url:\'http://news.qq.com\',\
        title:\'澳外长称朝鲜外资流和技术流掌握在中国手中 中方回应\',\
        id:\'20170727054126\',\
        pubtime:\'2017-07-27 20:25\',\
        type:\'1\',\
        article_url:\'http://news.qq.com/a/20170727/054126.htm\',\
        sosokeys:{\
          key1:\'外交部\',key2:\'威胁\',key3:\'中美关系\'}\
        ,\
        tags:[\'外交部\',\'威胁\',\'中美关系\'],\
        catalog:\'newsgn\',\
        catalog_full:\'news-newsgn-zhxw\',\
        sub_nav:\'zhxw\',\
        topic:{\
          name:'',cname:'',ztcatalog:''}\
        ,\
        subName:{\
          name:\'newsgn\',url:\'http://news.qq.com/china_index.shtml\', cname:\'国内新闻\'},\
        isShowLastAD:'',\
        tpl:{\
          dev:\'def\',ver:\'1.0.0.0\',time:\'20160512\',type:\'1\',stype:''}\
      }\
\
    </script>'


def my_split(text, sep):
    array = []
    flag = True
    pos = 0
    for i in range(len(text)):
        if text[i] == sep:
            if flag:
                seg = text[pos:i]
                if seg[0] == ',' or seg[0] == '}':
                    seg = '""' + seg
                array.append(seg)
                pos = i + 1
        elif text[i] == "\"":
            flag = not flag
    seg = text[pos:]
    if seg[0] == ',' or seg[0] == '}':
        seg = '""' + seg
    array.append(seg)
    return array


def to_json_with_quates(text):
    new_text = []
    ms = my_split(text, ":")
    for i in ms:
        length = len(i)
        pos = length - 1
        new_split = ""
        for j in range(length):
            if i[length - j - 1] is ',' or i[length - j - 1] is '{':
                pos = length - j - 1
                break
        new_split += i[:pos + 1]
        new_split += "\""
        new_split += i[pos + 1:]
        new_split += "\""
        new_text.append(new_split)
    return ":".join(new_text)[:-2]


def get_object_from_js(text):
    p = r'window.ARTICLE_INFO.*?\|\|(.*?)</script>'
    js_info = re.findall(p, text, re.S | re.M)[0].replace("'", '"')
    js_info = js_info.replace(" ", "")
    js_info = js_info.replace("\n", "")
    js_info = to_json_with_quates(js_info)
    json_obj = json.loads(js_info)
    return json_obj
o = get_object_from_js(text)
print(o)
