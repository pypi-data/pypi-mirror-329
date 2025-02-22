
import sys
import time
from datetime import datetime
import logging
import os
import hashlib
import requests
import json
import shutil
import ast


ENVIRONMENT_VARIABLE = "BE_CE_APPS_BASEDIR"
PATH_BASEDIR = f'{os.getcwd()}' if os.environ.get(ENVIRONMENT_VARIABLE) is None else f'{os.environ.get(ENVIRONMENT_VARIABLE)}'


## logger ...
class Logger(object):

    def __init__(self, log_path='httppool-logger', format_log='%(asctime)s : %(levelname)s : HTTPPOOL : %(message)s \n'):
        self.log_path = f'{log_path}.log'
        self.format_log = format_log

        print(os.getcwd())
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

        logging.basicConfig(
            level=logging.DEBUG,
            format=self.format_log,
            handlers=[
                logging.FileHandler(self.log_path),
            ]
        )

    def change_format(self, format_log):
        self.format_log = format_log

        logging.basicConfig(
            level=logging.DEBUG,
            format=self.format_log,
            handlers=[
                logging.FileHandler(f'{self.log_path}.log'),
            ]
        )

    def add_info(self, log):
        logging.info(log)

    def add_debug(self, log):
        logging.debug(log)

    def add_warning(self, log):
        logging.warning(log)

    def add_error(self, log):
        logging.error(log)

    def add_critical(self, log):
        logging.critical(log)

    def delete_logger(self):
        if os.path.exists(f'{self.log_path}.log'):
            os.remove(f'{self.log_path}.log')
            return 'Logger file has been removed'
        return 'No exist the logger file'

    def clear_logger(self):
        if os.path.exists(f'{self.log_path}.log'):
            f = open(f'{self.log_path}.log', 'w')
            f.write('')
            f.close()
            return 'Logger file content has been clear'
        return 'No exist the logger file'

## Shared cache ....
class Shared_Cache(object):

    def __init__(self, cache_path='httppool-cache'):
        self.cache_name = os.path.basename(cache_path)
        self.cache_path = f'{cache_path}'

        os.makedirs(self.cache_path, exist_ok=True)

    def keys(self):
        keylist = []
        for file_name in os.listdir(self.cache_path):
            if file_name[-4:].lower() == '.url':
                file_name = self.cache_path + os.path.sep + file_name
                print(file_name)
                f = open(file_name)
                content = f.readlines()
                f.close()
                if len(content) > 0:
                    keylist.append(content[0][0:-1])
        return keylist

    def read_headers(self, url):
        name_preffix = hashlib.md5(url.encode('utf-8')).hexdigest()
        path = f'{self.cache_path}{os.path.sep}{name_preffix}.url'
        if os.path.exists(path):
            f = open(path)
            content = f.readlines()
            f.close()
            for line in content:
                if line.startswith('headers: '):
                    res = ast.literal_eval(line[9:])
                    return res
        return None

    def read_lastaccess_file(self, path):
        access_data = {'read': None, 'write': None, 'retry': '15'}
        path = path + '.lastaccess'

        if not os.path.exists(path):
            return access_data
        f = open(path)
        content = f.readlines()
        f.close()

        for line in content:
            if line.startswith('read: '):
                access_data['read'] = line[6:-1]
            if line.startswith('write: '):
                access_data['write'] = line[7:-1]
            if line.startswith('retry: '):
                access_data['retry'] = line[7:-1]
        return access_data

    def save_lastaccess_file(self, path, key, value):
        access_data = self.read_lastaccess_file(path)
        access_data[key] = value

        f = open(path + '.lastaccess', 'w')
        if access_data['read'] is not None:
            f.write(f'read: {access_data["read"]}\n\n')
        else:
            f.write(f'read: -- still defined --\n\n')
        if access_data['write'] is not None:
            f.write(f'write: {access_data["write"]}\n\n')
        else:
            f.write(f'write: -- still defined --\n\n')
        if access_data['retry'] is not None:
            f.write(f'retry: {access_data["retry"]}\n\n')
        else:
            f.write(f'retry: 15\n\n')
        f.close()

    def save(self, key, content, save_read_access=True, headers=None):
        name_preffix = hashlib.md5(key.encode('utf-8')).hexdigest()
        ext = f'.webpagedata'
        path_temp = self.cache_path + os.path.sep + 'temp.' + name_preffix + ext
        path = self.cache_path + os.path.sep + name_preffix + ext

        # create cache of website content ...
        f = open(path_temp, 'wb')
        f.write(content.encode('utf-8'))
        f.close()

        if os.path.exists(path):
            os.remove(path)
        os.rename(path_temp, path)

        # create cache of website url ...
        if not os.path.exists(f'{self.cache_path}{os.path.sep}{name_preffix}.url'):
            f = open(f'{self.cache_path}{os.path.sep}{name_preffix}.url', 'w')
            f.write(key)
            f.write(f'\n\nheaders: {headers}')
            f.close()

        # create cache of website lastaccess ...
        lastaccess_path = self.cache_path + os.path.sep + name_preffix
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.save_lastaccess_file(lastaccess_path, 'write', date)
        if save_read_access:
            self.save_lastaccess_file(lastaccess_path, 'read', date)

    ## Return the content of website on cache, and update the .lastaccess file ...
    def get(self, key):
        file = None
        update_time = 0
        name_preffix = hashlib.md5(key.encode('utf-8')).hexdigest()

        for f in os.listdir(self.cache_path):
            if f.startswith(name_preffix) and f[-4:].lower() != '.url' and f[-11:].lower() != '.lastaccess':
                f = self.cache_path + os.path.sep + f
                stats = os.stat(f)
                file_update_time = stats.st_mtime
                if stats.st_size > 0 and file_update_time > update_time:
                    update_time = file_update_time
                    file = f

        if file is None or (not open(file, 'rb').read().decode('utf-8').__contains__("<html") and not open(file, 'rb').read().decode('utf-8').__contains__('{"')):
            return None

        # update the .lastaccess file like read ...
        lastaccess_path = self.cache_path + os.path.sep + name_preffix
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.save_lastaccess_file(lastaccess_path, 'read', date)

        # get content ...
        content = open(file, 'rb').read().decode('utf-8')
        return content

    def delete_folder_cache(self):
        if os.path.exists(self.cache_path):
            shutil.rmtree(self.cache_path)
            return 'Shared cache directory has been removed'
        return 'No exist a shared cache directory'

    def convert_timedelta(self, deltatime):
        h = (deltatime.days * 24) + (deltatime.seconds // 3600)
        remaining_seconds = deltatime.seconds % 3600
        m = remaining_seconds // 60
        s = remaining_seconds % 60
        return h, m, s

    def clean(self, url):
        namepreffix = hashlib.md5(url.encode('utf-8')).hexdigest()
        for file in os.listdir(self.cache_path):
            if file.startswith(namepreffix):
                file = self.cache_path + os.path.sep + file
                os.remove(file)

    def must_be_updated(self, url):
        namepreffix = hashlib.md5(url.encode('utf-8')).hexdigest()
        access_data = self.read_lastaccess_file(self.cache_path + os.path.sep + namepreffix)
        if access_data['write'] is None or access_data['write'] == '-- still defined --':
            return True

        access_time = time.strptime(access_data['write'], '%Y-%m-%d %H:%M:%S')
        timestamp = time.mktime(access_time)
        delta = datetime.now() - datetime.fromtimestamp(timestamp)
        h, m, s = self.convert_timedelta(delta)
        if (h * 60 + m) > int(access_data['retry'].strip()):
            return True
        return False

    def has_recent_access(self, url):
        namepreffix = hashlib.md5(url.encode('utf-8')).hexdigest()
        access_data = self.read_lastaccess_file(self.cache_path + os.path.sep + namepreffix)
        if access_data['read'] is None or access_data['write'] == '-- still defined --':
            self.clean(url)
            return False

        access_time = time.strptime(access_data['read'], '%Y-%m-%d %H:%M:%S')
        timestamp = time.mktime(access_time)
        delta = datetime.now() - datetime.fromtimestamp(timestamp)
        if delta.days > 7:
            self.clean(url)
            return False
        return True

    def old_content_is_api(self, url):
        namepreffix = hashlib.md5(url.encode('utf-8')).hexdigest()
        for f in os.listdir(self.cache_path):
            if f.startswith(namepreffix) and f[-4:].lower() != '.url' and f[-11:].lower() != '.lastaccess':
                f = self.cache_path + os.path.sep + f
                if not open(f, 'rb').read().decode('utf-8').__contains__('<html'):
                    return True
        return False

    def set_max_retry(self, url, minutes):
        namepreffix = hashlib.md5(url.encode('utf-8')).hexdigest()
        path = self.cache_path + os.path.sep + namepreffix
        self.save_lastaccess_file(path, 'retry', minutes)

## GLOBAL PROPERTIES ...
GLOBAL_CONFIG = {
    "http_proxy": "",
    "shared_cache": Shared_Cache(f"{PATH_BASEDIR}{os.path.sep}httppool-cache"),
    "logger": Logger(f"{PATH_BASEDIR}{os.path.sep}httppool-logger"),
    "headers": {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    },
    "thread_interval": 1,
}

## Producer ...
class Producer(object):

    def __init__(self, headers=None, config=GLOBAL_CONFIG):
        self.logger = config['logger']
        self.shared_cache = config['shared_cache']
        if headers is None:
            self.headers = config['headers']
        if headers is not None:
            self.headers = headers

    def get_url_content(self, url, api=False):
        content = None

        try:
            response = requests.get(url, headers=self.headers, verify=False)
            if response.status_code != 200 or response is None:
                if api:
                    self.logger.add_warning('Producer API : URL content is empty or inaccessible')
                else:
                    self.logger.add_warning('Producer : URL content is empty or inaccessible')
            else:
                if api:
                    self.logger.add_info(f'Producer API : Got URL content --> {url}')
                else:
                    self.logger.add_info(f'Producer : Got URL content --> {url}')
                content = response.content
        except Exception as e:
            if api:
                self.logger.add_error(f'Producer API : Error getting URL content {str(e)}')
            else:
                self.logger.add_error(f'Producer : Error getting URL content {str(e)}')

        return content.decode('utf-8')

    def produce(self, url, api=False):
        content = self.get_url_content(url, api)
        if content is not None and len(content) > 0:
            self.shared_cache.save(url, content, headers=self.headers)
        return content

## Consumer ...
class Consumer(object):

    def __init__(self, headers=None, config=GLOBAL_CONFIG):
        self.shared_cache = config['shared_cache']
        self.logger = config['logger']
        if headers is not None:
            self.headers = headers
        else:
            self.headers = None

    def consume(self, url, api=False):
        content = self.shared_cache.get(url)
        if content is None or (not content.__contains__('html') and not content.__contains__('{"')):
            producer = Producer(headers=self.headers)
            content = producer.produce(url, api)
        return content



## METHODS ...

## returns a dictionary if api is True, and returns a string (contains the DOM of the website in UTF-8) if api is False
def get_url_content(url, config=GLOBAL_CONFIG, api=False, headers=None):
    logger = config['logger']
    logger.add_info(f'Client : Consumming URL --> {url}')
    consumer = Consumer(headers=headers)

    if not api:
        content = consumer.consume(url)
        if content is None:
            logger.add_error(f'Client : No content available for URL --> {url}')
        return content
    else:
        content = consumer.consume(url, api)
        if content is None:
            logger.add_error(f'Client API : No content available for URL --> {url}')
        return json.loads(content)

# run in second plane a daemon process for update the httppool-cache every certain time ...
def run_producer_thread(config=GLOBAL_CONFIG):
    shared_cache = config['shared_cache']
    logger = config['logger']
    thread_interval = config['thread_interval']

    while True:
        logger.add_info('ProducerThread : Loop : (BEGIN)')
        for url in shared_cache.keys():
            is_api = shared_cache.old_content_is_api(url)
            if shared_cache.must_be_updated(url) and shared_cache.has_recent_access(url):
                logger.add_info(f'ProducerThread : Producing URL --> {url}')
                p = Producer(headers=shared_cache.read_headers(url))
                content = None
                if is_api:
                    content = p.produce(url, api=True)
                else:
                    content = p.produce(url, api=False)
                if content is None:
                    logger.add_error(f'ProducerThread : Could not produce content for url --> {url}')
                logger.add_info(f'ProducerThread : Cleaning older entries for url --> {url}')
            else:
                logger.add_info(f'ProducerThread : It is not necessary to update the cache for url --> {url}')
        logger.add_info('ProducerThread : Loop : (END)')
        # sleep for minutes ...`
        time.sleep(thread_interval * 60)

# change the time of retry get content from an url ...
def set_url_retry_time(url, minutes, config=GLOBAL_CONFIG):
    shared_cache = config['shared_cache']
    logger = config['logger']
    shared_cache.set_max_retry(url, minutes)
    logger.add_info(f'RetryTime : Setting retry time on "{minutes} minutes" for url --> {url}')



if __name__ == '__main__':

    args = sys.argv

    # no arguments ...
    if len(args) == 1:
        pass

    # 1 argument (httppool admin) ...
    if len(args) == 2:

        if args[1].lower() == 'deletelog':
            print(GLOBAL_CONFIG['logger'].delete_logger())

        if args[1].lower() == 'clearlog':
            print(GLOBAL_CONFIG['logger'].clear_logger())

        if args[1].lower() == 'deletecache':
            print(GLOBAL_CONFIG['shared_cache'].delete_folder_cache())

        if args[1].lower() == 'test':
            print(PATH_BASEDIR)

