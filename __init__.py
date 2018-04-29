import os
import json
import random
import requests
import threading
import time
import shutil

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

    def __init__(self, time = 1):
        self.path = os.path.dirname(__file__) + '/cache/'
        self.dir_path = os.path.dirname(__file__) + '/dir.json'
        self.entered = False
        self.time = time


    def insert(self, *urls):
        assert(self.entered)
        for url in urls:
            if url in self.dir:
                self.dir[url]['present'] = False
            else:
                self.__new_page(url)
                self.dir[url]['present'] = False


    def fetch(self):
        ''' Will download urls that doesn't exist locally '''
        return self._update([k for k, v in self.dir.items() if not v['present']])

    def update_url(self, *urls):
        ''' Will update one or several urls'''
        return self._update([k for k in self.dir if k in urls])

    def update_all(self):
        ''' Will update all urls'''
        return self._update([k for k in self.dir])

    def update_old(self, age):
        ''' Will update all urls'''
        now = time.time()
        get_age = lambda x: now - x['time-updated']
        return self._update([k for k, v in self.dir.items() if get_age(v) > age])
            
    def _update(self, to_dl):
        if len(to_dl) == 0:
            return []

        fault_pages = []

        if len(to_dl) == 1:
            th = _DLth(self.dir, to_dl[0], fault_pages)
            th.start()
            th.join()
            
        else:
            threads = []
            for d_url in to_dl:
                th = _DLth(self.dir, d_url, fault_pages)
                threads.append(th)
            t = float(self.time) / len(to_dl)
            for th in threads:
                time.sleep(t)
                th.start()
            for th in threads:
                th.join()

        return fault_pages, len(to_dl)
        
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

        assert(self.path != '/')

        if os.path.exists(self.path):
            shutil.rmtree(self.path)
        if os.path.exists(self.dir_path):
            os.remove(self.dir_path)

        if inout:
            self.__enter__()
