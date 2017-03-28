import requests,pickle,random,re,time,threading
import IProxypool
proxypool = IProxypool.Proxypool()
companylist = []
lock = threading.Lock()
page = 0
class ITOrange(threading.Thread):

        def __init__(self,thread_id,pages,func):
                super(ITOrange,self).__init__()
                self.thread_id = thread_id
                self.func = func
                self.pages = pages
        def run(self):
                print("线程 %d 开始"%self.thread_id)
                self.func(self.thread_id,self.pages)
                print("线程 %d 完成任务"%self.thread_id)

def worker(parafunc):
        def in_worker(thread_id,pages):
                header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
                proxy = None 
                global proxypool
                global companylist
                global page
                page_number = page
                pages,urls,repattern,thread_id = parafunc(thread_id,pages)
                while page_number < pages:
                        
                        url = eval(urls)
                        if page == 125:
                                continue
                        try:
                                request = requests.get(url,headers = header,proxies= proxy,timeout=10)
                                print(request.status_code) 
                                print("Thread %d get the page No.%d"%(thread_id,page_number))
                                if request.status_code != 200:
                                        raise ConnectError("Cannot connect to server")
                                request.encoding = 'utf8'
                                buff = request.text
                                recomp = re.compile(repattern,re.S)
                        except:
                                lock.acquire()
                                if proxypool:
                                        proxy = get_a_proxy(proxypool,thread_id)
                                else:
                                        proxypool = IProxypool.Proxypool()               
                                        proxy = get_a_proxy(proxypool,thread_id)
                                        time.sleep(60)
                                        print("IP锁释放")
                                lock.release()
                                continue 
                        complist = re.findall(recomp,buff)
                        for company in complist:
                                compform = [company[0]+'\n',company[1]+'\n',company[2]+'\t',company[3]+'\t',company[4].strip()+'\t'+company[5]+'\n\n\n'] 
                                if compform not in companylist:
                                        companylist.append(compform)
                        
                        print("Thread %d get page %d Done!"%(thread_id,page_number))
                        lock.acquire()
                        page+=1
                        page_number=page
                        lock.release()
                        #sand = random.randint(1,3)
                        #time.sleep(3)
        return in_worker

@worker
def ITOcomp(thread_id,pages):
        urls = '"http://www.itjuzi.com/company?page=%d"%page_number'
        #repattern = r'<p class="title">.*?<span>(.+?)</span>.*?<p class="des"><span>(.+?)</span>.*?<a href=.*?>(.+?)</a>.*?<a href=.*?>(.+?)</a>.*?<i class="cell date">(.+?)</i>.*?<span class=.*?>(.+?)</span>'
        #repattern=r'<p class="title">.*?<span>(.+?)</span>.*?<a href.*?>(.+?)</a>.*?<a href.*?>(.+?)</a>.*?date">(.+?)</i>.*?<span.*?>(.+?)</span>'
        
        repattern = r'<p class="title">.*?<span>(.+?)</span>.*?<p class="des">.*?<span>(.+?)</span>.*?</p>.*?<span.*?<a href.*?>(.+?)</a>.*?</span>.*?<span.*?<a href.*?>(.+?)</a>.*?</span>.*?<i.*?>(.*?)</i>.*?<a.*?>(.*?)</a>'
        return pages,urls,repattern,thread_id







def compCraw():
        global page
        print("* * * * * Welcome to IT Citus Crawler * * * * *")
        pages = int(input("please enter the pages you want:"))
        print("主线程开始...")
        threads = [ITOrange(i,pages,ITOcomp) for i in range(1,11)]
        for thread in threads:
                time.sleep(1)
                page+=1
                thread.start()
        for t in threads:
                t.join()

        print("主线程结束,正在保存...")
        compdata = open("ITOcompany.pkl","wb")
        pickle.dump(companylist,compdata)
        print("保存完毕！")
        
        






def get_a_proxy(pool,thread_id):
        if pool:
                proxy = {"http":"http://%s:%s"%(pool[0][0],pool[0][1])}
                print("线程切换到ip地址:%s"%(pool[0][0]))
                del pool[0]        
                return proxy 

compCraw()
