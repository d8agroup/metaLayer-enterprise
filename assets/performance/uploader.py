########################################################################################################################
# TEST VARIABLE SETTINGS
########################################################################################################################
total_number_of_items_to_include_in_test = 5000
total_number_of_threads_to_use = 2
number_of_content_items_to_include_in_each_post = 500
post_url = 'http://localhost/aggregation/post_content'
commit_url = 'http://localhost:8080/solr/update?commit=true'
skip_duplicate_check = 'true'
actions_to_apply_to_each_content_item = [
    {'name':'localsentimentanalysis'},
    {'name':'localtagging'},
]
########################################################################################################################
# END TEST VARIABLE SETTINGS
########################################################################################################################



from random import randint
import sys
import urllib, urllib2
import json
import datetime
from Queue import Queue
import threading


finished = []

class Poster(threading.Thread):
    def __init__(self, content, thread_count):
        self.content = content
        self.thread_count = thread_count
        self.time_taken = 0
        threading.Thread.__init__(self)

    def run(self):
        try:
            start_time = datetime.datetime.now()
            post_data = {
                'content':json.dumps(self.content),
                'actions':json.dumps(actions_to_apply_to_each_content_item),
                'skip_duplicate_check':skip_duplicate_check,
                }
            response = urllib2.urlopen(post_url, urllib.urlencode(post_data)).read()
            time_taken = datetime.datetime.now() - start_time
            self.time_taken = time_taken
            print 'package %i: - finished in %s  (%s)' % (self.thread_count, time_taken, response)
        except Exception as e:
            print 'package %i: - error %s' % (self.thread_count, e)
            self.time_taken = None

def producer(q, content_packages):
    x = 1
    for package in content_packages:
        thread = Poster(package, x)
        thread.start()
        q.put(thread, True)
        x += 1

def consumer(q, package_count):
    while len(finished) < package_count:
        thread = q.get(True)
        thread.join()
        finished.append(thread.thread_count)

stock_tweets = [
        {'source': {'display_name': 'TestData', 'id': '932ef63c661d734ba7f2d11b88b815c1'}, 'link': 'http://twitter.com/LovelyDeadBear/statuses/181972701051752449', 'time': 1332209847, 'text': [{'title': u'#DoritosLocosTacos one of the best parts of my spring break - candymountain'}], 'author': {'link': 'http://twitter.com/lovelydeadbear', 'image': 'http://purl.org/net/spiurl/lovelydeadbear', 'display_name': 'lovelydeadbear'}, 'id': 'dbb3a269c5c50548ab32024ef69e0f38', 'channel': {'type': 'testdata', 'id': '85d52cc25a3e0c30262de5426b94ea09', 'sub_type': 'testdata'}}
]
data = []
for x in range(total_number_of_items_to_include_in_test):
    i = stock_tweets[randint(0, len(stock_tweets) - 1)].copy()
    i['id'] = '%i' % x
    data.append(i)

content_packages = []
number_of_items_sent = 0
for r in range(0, len(data), number_of_content_items_to_include_in_each_post):
    if r >= total_number_of_items_to_include_in_test:
        break
    post_data = data[r:r + number_of_content_items_to_include_in_each_post]
    content_packages.append(post_data)
    number_of_items_sent += len(post_data)

start_time = datetime.datetime.now()
queue = Queue(total_number_of_threads_to_use)
producer_thread = threading.Thread(target=producer, args=(queue, content_packages))
consumer_thread = threading.Thread(target=consumer, args=(queue, len(content_packages)))
producer_thread.start()
consumer_thread.start()
producer_thread.join()
consumer_thread.join()
if commit_url:
    urllib2.urlopen(commit_url).read()
print '******************************************************'
print 'All threads finished in %s' % (datetime.datetime.now() - start_time)
print 'Average time to one item = %s' % ((datetime.datetime.now() - start_time) / number_of_items_sent)
print 'Average object size = %f bytes' % (float(sum([sys.getsizeof(i) for i in data])) / len(data))
print 'Queue size: %i' % total_number_of_threads_to_use
print 'Post size: %i' % number_of_content_items_to_include_in_each_post
print '******************************************************'