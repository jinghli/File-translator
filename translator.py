#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import urllib2
import chardet

appID = 'Your app ID'
base_uri = "http://api.microsofttranslator.com/V1/Http.svc"

#lang dict encoding/language code
_lang = {
    'GB2312' : 'zh-cn'
}

def langDetect(file):
    if not os.path.exists(file):
        print 'The input file is not exist.'
        sys.exit(1)

    f = open(file, 'r')
    content = f.read()
    code = chardet.detect(content)
    lang = code.get('encoding')
    
    #return the encoding
    try:
        return _lang.get(lang),lang
    except Exception,e:
        return '',lang

def request(req):
    try:
        response = urllib2.urlopen(req)
        result = response.read()
    except urllib2.HTTPError, e:
        print e.code
        print e.read()
        result=""
    return result

def detect(text):
    uri="%s/Detect?appId=%s" % (base_uri, appID)
    req = urllib2.Request(uri, text, {'Content-Type':'text/plain'})
    return request(req)

def translate(text, fr):
    uri="%s/Translate?appId=%s&from=%s&to=en" % (base_uri,appID, fr)
    req = urllib2.Request(uri, text, {'Content-Type':'text/plain'})
    return request(req)

def main(file):
    if not os.path.exists(file):
        print '%s is not exist!' % file
        sys.exit(1)

    fr = open(file, 'r')
    fw = open('temp.txt', 'w')

    fromCode, fromLang = langDetect(file)

    if len(fromCode) > 0:
        for line in fr.readlines():
            line = line.decode(fromLang).encode('utf-8')
            trans_line = translate(line, fromCode)
            print trans_line
            fw.write(trans_line)
    else:
        print "Can't detect this file encoding"
        fr.close()
        fw.close()
        sys.exit(1)

    fr.close()
    fw.close()
    #delete the orginal file and get the new one.
    os.remove(file)
    #os.rename('temp.txt', file)


if __name__ == "__main__":
    #main('test1.txt')
    #print translate('könyvtár', 'hu')
    #test = langDetect('platform.txt')
    #print test
    main('platform.txt')