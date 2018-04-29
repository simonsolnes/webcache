import os
import json
import random
import requests
import threading
import time
import shutil

'''
To Do:
- automatically enter and exit each time
- iteration
'''

class _DLth(threading.Thread):
    def __init__(self, directory, url, fault_pages):
        threading.Thread.__init__(self)
        self.dir = directory
        self.url = url
        self.fault_pages = fault_pages

    def run(self):
        res = requests.get(self.url)
        if res.status_code != 200:
            self.fault_pages.append(self.url)
            return
        with open(self.dir[self.url]['path'], 'w') as f:
            f.write(res.content.decode('utf-8'))
        self.dir[self.url]['present'] = True
        self.dir[self.url]['time-updated'] = time.time()

class _Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class WebCache():
    __metaclass__ = _Singleton

    def __init__(self):
        self.path = os.path.dirname(__file__) + '/cache/'
        self.dir_path = os.path.dirname(__file__) + '/dir.json'
        self.entered = False


    def __enter__(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            
        if os.path.isfile(self.dir_path):
            with open(self.dir_path, 'r') as f:
                self.dir = json.loads(f.read())
        else:
            self.dir = {}
        self.entered = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.dir_path, 'w') as f:
            f.write(json.dumps(self.dir))
        self.entered = False

    def insert(self, url):
        assert(self.entered)
        if url in self.dir:
            self.dir[url]['present'] = False
        else:
            self.__new_page(url)
            self.dir[url]['present'] = False

    def update(self, url = None, age = None, use_time = 0):
        assert(self.entered)

        assert(type(url) in [type(None), list, str])
        assert(type(age) in [type(None), int, float])
        assert(type(use_time) in [type(None), int, float])

        if isinstance(url, str):
            u_url = [url]
        else:
            u_url = url

        now = time.time()

        to_update = []

        for d_url, meta in self.dir.items():
            if u_url:
                if d_url in u_url:
                    to_update.append(d_url)
                    continue
            else:
                if age:
                    age_diff = now - meta['time-updated']
                    if age_diff > age:
                        to_update.append(d_url)
                else:
                    to_update.append(d_url)

        if not to_update:
            return

        threads = []
        fault_pages = []

                
        for d_url in to_update:
            th = _DLth(self.dir, d_url, fault_pages)
            threads.append(th)

        t = float(use_time) / len(to_update)
        for th in threads:
            time.sleep(t)
            th.start()
        for th in threads:
            th.join()

        return fault_pages
    
    def get(self, url):
        inout = not self.entered

        if not self.entered:
            self.__enter__()
        assert(self.entered)



        if url in self.dir and self.dir[url]['present']:
            pass
        else:
            self.__new_page(url)
            f = []
            th = _DLth(self.dir, url, f)
            th.start()
            th.join()
            assert(not f)

        with open(self.dir[url]['path'], 'r') as f:
            retval = f.read()

        if inout:
            self.__exit__(None, None, None)

        return retval

    def __new_page(self, url):
        taken = True
        while taken:
            page_id = self.path + str(random.randint(0, 2 ** 64)).zfill(20)
            taken = False
            for k, v in self.dir.items():
                if page_id == v['path']:
                    taken = True
                    break
        self.dir[url] = {}
        self.dir[url]['path'] = page_id

    def reset(self):
        inout = self.entered
        if inout:
            self.__exit__(None, None, None)

        # it should never happen but better to be on the safe side
        assert(self.path != '/')

        if os.path.exists(self.path):
            shutil.rmtree(self.path)
        if os.path.exists(self.dir_path):
            os.remove(self.dir_path)

        if inout:
            self.__enter__()
