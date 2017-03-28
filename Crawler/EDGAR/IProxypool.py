import re,time,threading,urllib.request

pool = []
KDLpage = 0
XCpage = 0
page = {'KDL':KDLpage,'XCDL':XCpage}
lock = threading.Lock()
class ProxySeeker(threading.Thread):

        def __init__(self,thread_id,thread_type,func):
                super(ProxySeeker,self).__init__()
                self.thread_id = thread_id
                self.func = func
                self.thread_type = thread_type 
        def run(self):
                print("线程 %d 开始工作"%self.thread_id)
                self.func(self.thread_id,self.thread_type)
                print("线程 %d 完成任务"%self.thread_id)


def seeker(parafunc):
        def in_seeker(thread_id,thread_type):#decorate need closure to wrap
                global pool
                header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
                source_name,pages,urls,repattern,thread_id,thread_type = parafunc(thread_id,thread_type)
                global page
                while page[thread_type] < pages:
                        lock.acquire() #get the lock in case url get page changed by other thread before next line executed
                        page[thread_type] += 1
                        page_number = page[thread_type] #copy the page number in case other changes number and cause the Done print with wrong number
                        url = eval(urls)
                        lock.release()#release the lock 
                        request = urllib.request.Request(url, headers = header)
                        content = urllib.request.urlopen(request).read().decode('utf-8')
                        reprox = re.compile(repattern,re.S)
                        proxies = re.findall(reprox,content)
                        for prox in proxies:
                                prox = prox + (source_name,)
                                if prox not in pool:
                                        pool.append(prox)
                        print("Thread %d get page %d Done! %s"%(thread_id,page_number,source_name))
                        time.sleep(10) 
        return in_seeker


@seeker
def kuaidaili(thread_id,thread_type):
        source_name = " |  快代理  "
        pages = 15
        urls = '"http://www.kuaidaili.com/proxylist/%d/"%page[thread_type]'
        repattern  = r'<td data-title="IP">(.+?)</td>.*?<td data-title="PORT">(.+?)</td>.*?<td data-title="类型">(.+?)</td>'
        return source_name,pages,urls,repattern,thread_id,thread_type

@seeker
def xici_zh(thread_id,thread_type):
        source_name = " |  西刺代理"
        pages = 15
        urls = '"http://www.xicidaili.com/nn/%d"%page[thread_type]'
        repattern = r'<tr class=".*?<td>(.+?)</td>.*?<td>(.+?)</td>.*?<td>.*?</td>.*?<td class.*?<td>(.+?)</td>'
        return source_name,pages,urls,repattern,thread_id,thread_type



def Proxypool():
        global pool
        global page
        
        print("主线程开始...")
        thread_info = [[i,'XCDL',xici_zh] if i > 2 else [i,'KDL',kuaidaili] for i in range(1,5)]
        threads = [ProxySeeker(t_i[0],t_i[1],t_i[2]) for t_i in thread_info]
        for thread in threads:
                #time.sleep(0.5)
                thread.start()
        for t in threads:
                t.join()
        for each in pool:
                print(each) 
        print("主线程结束...")
        page['KDL'] = 0
        page['XCDL']=0
        return pool



