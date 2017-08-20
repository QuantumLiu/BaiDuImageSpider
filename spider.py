# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 15:08:22 2017

@author: Quantum Liu
"""

import sys, os,re,urllib,traceback
from multiprocessing import Pool,cpu_count,freeze_support
import requests

str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}
char_table = {ord(key): ord(value) for key, value in char_table.items()}


def decode(url):
    for key, value in str_table.items():
        url = url.replace(key, value)
    return url.translate(char_table)

def mkdir(dirname):
    dirpath = os.path.join(sys.path[0], dirname)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath

def checkpath(fname):
    return  re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", fname)

def iterpages(word,max_num=10000,start_page=1):
    if start_page*60>max_num:
        raise ValueError('The start page is to large')
    if start_page<1:
        raise ValueError('Thea start page must be a uint')
    word = urllib.parse.quote(word)
    url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&ie=utf-8&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
    urls = [url.format(word=word, pn=x) for x in [n*60 for n in range(start_page-1,int(max_num/60)+1)]]
    return urls

def parse_page(page_url):
    try:
        res=requests.get(page_url)
        res.encoding='utf-8'
        img_urls=[decode(obj_url) for obj_url in re.findall(r'"objURL":"(.*?)"',res.text)]
    except requests.exceptions.BaseHTTPError:
        img_urls=[]
    return img_urls

def get_img_urls(word,max_num=1000,start_page=1):
    return [img_url for urls in [parse_page(page_url) for page_url in iterpages(word,max_num,start_page)] for img_url in urls][:max_num]
    
def dowload_img(img_url,dirname,i):
    form=img_url.split('.')[-1]
    if not (form.lower() in ['jpg','png','gif']):
        form='png'
        print('Unknown format for img_url {u}\n Save as a PNG file'.format(u=img_url))
    fname=os.path.join(dirname,str(i)+'.'+form)
    print('Download image {i} to file {fname}'.format(i=i,fname=fname))
    try:
        data=requests.get(img_url).content
        with open(fname,'wb') as f:
            f.write(data)
    except (requests.exceptions.BaseHTTPError,IOError):
        traceback.print_exc()
        print('Got error during download img \n{img}\n to file \n{fname}\nPass'.format(img=img_url,fname=fname))
        return 0
    else:
        return 1

def crawl_p(word,dirname='./',max_num=1000,start_page=1,nb_jobs=0):
    mkdir(dirname)
    results=[]
    mpool=Pool(nb_jobs if nb_jobs else cpu_count())
    for i,img_url in enumerate(get_img_urls(word,max_num,start_page)):
        results.append(mpool.apply_async(dowload_img,(img_url,dirname,i)))
    mpool.close()
    mpool.join()
    nb_succeed=sum([result.get() for result in results])
    return nb_succeed

if __name__=='__main__':
    if sys.platform.startswith('win'):
        freeze_support()
    if len(sys.argv)<2:
        word='猫 全身'
    else:
        word=sys.argv[1]
    dirname=checkpath(word)
    crawl_p(word,dirname,*sys.argv[3:])

