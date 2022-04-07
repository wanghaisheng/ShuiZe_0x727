from fastapi import FastAPI
import requests
from fastapi.responses import ORJSONResponse
import uvicorn
from pywebio.input import *
from pywebio.io_ctrl import Output, OutputList
from pywebio.output import *
from pywebio.platform.page import config
from pywebio.session import run_js, set_env
from pywebio.platform.fastapi import asgi_app
import time
import pywebio_battery as battery
from app.constants import *
import os
from ShuiZe import *
from Plugins.infoGather.subdomain.ksubdomain.ksubdomain import run_ksubdomain

from urllib.parse import urlparse
from subprocess import Popen
app = FastAPI()

apiapp= FastAPI()

def domainall(domain):
    print('original url',domain)
    if('http' in domain):
        domain =urlparse(domain).netloc
    print('get domain from url',domain)
    args=["bash", "run.sh",domain]
    # print('subdomain command ',args)
    p = Popen(args)

    # Wait until process terminates
    while p.poll() is None:
        time.sleep(0.5)    
    print("subdomain crack Process ended, ret code:", p.returncode)    
    try:
        with open(domain+'/'+domain+'_sub_ok.txt',encoding="utf8") as f:
            urls =f.readlines()
    except:
        urls=[]
    return urls    
@apiapp.get("/api/", response_class=ORJSONResponse)
async def sitemap(url:str):
    urls =run_ksubdomain(url)
    return {"urls": urls}



return_home="""
location.href='/'
"""
@config(theme="minty",title=SEO_TITLE, description=SEO_DESCRIPTION)
def index() -> None:
    # Page heading
    put_html(LANDING_PAGE_HEADING)
    lang='English'
    if lang == 'English':
        LANDING_PAGE_DESCRIPTION = LANDING_PAGE_DESCRIPTION_English

    with use_scope('introduction'):
        # put_html(PRODUCT_HUNT_FEATURED_BANNER)
        # put_html(LANDING_PAGE_SUBHEADING)
        put_markdown(LANDING_PAGE_DESCRIPTION, lstrip=True)
    # run_js(HEADER)
    # run_js(FOOTER)
    
    url = input("input your target domain",datalist=popular_shopify_stores)    
    # if not isvaliddomain(url):
    #     return {"urls": 'not a valid domain'}
    if url.startswith("http://"):
        url=url.replace('http://','')
    elif url.startswith("https://"):
        url=url.replace('https://','')
    else:
        url=url
    # url =trueurl(url)

    with use_scope('loading'):

        put_loading(shape='border', color='success').style('width:4rem; height:4rem')
    clear('introduction')


    put_html('</br>')
    set_env(auto_scroll_bottom=True)
    with use_scope('log'):

        with battery.redirect_stdout():
            print('crack url',url)

            urls =run_ksubdomain(url)

    print(urls,'====')
    clear('loading')
    clear('log')

    urls=list(urls)
    if len(urls)<1:
        put_text('there is no subdomain found in this domain',url)
    else:        
        data=[]
        for idx, item in enumerate(urls):
            item =[].append(idx,item,url)
            data.append(item)
        # put_logbox('log',200)

            # logbox_append('log',)
        # qufen html   image  video 
        put_file(urlparse(url).netloc+'.txt', data, 'download me')
        put_collapse('preview all subdomains',put_table(data, header=['id', 'subdomain', 'domain']))
    put_button("Try again", onclick=lambda:run_js(return_home), color='success', outline=True)



home = asgi_app(index)

app.mount("/", home)
app.mount("/api", apiapp)


if __name__ == '__main__':
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    if (os.environ.get('PORT')):
        port = int(os.environ.get('PORT'))
    else:
        port = 5001
    
    uvicorn.run(app='main:app',
                host="0.0.0.0",
                port=port,
                reload=False,
                debug=True,
                proxy_headers=True,
                log_config=log_config)