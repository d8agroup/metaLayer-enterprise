from hashlib import md5
import datetime
from random import randint
import urllib2
import urllib
import json
import time
import csv

from dateutil import tz
from dateutil import parser as dateutil_parser


FILE = "/home/griff/Documents/-MetaLayer/-NoeticBox/shoptiques_data_full.csv"
POST_URL = 'http://delv.demo.metalayer.com/aggregation/post_content'
COMMIT_URL = 'http://delv.demo.metalayer.com:8080/solr/update?commit=true'

lines = [l for l in csv.reader(open(FILE, 'r'))]

headers = lines[0]

rows = lines[1766:]

for row in rows:
    user_id = row[0]
    user_register_date = dateutil_parser.parse(row[1])
    email = row[2]
    first_name = row[3]
    surname = row[4]
    date_in_cart = dateutil_parser.parse(row[5])
    status = row[6]
    product_url = row[7].replace('http://www.shoptiques.com/products/', '')
    product_amount = row[8]
    product_color = row[9]
    product_size = row[10]
    product_category = row[11]
    boutique = row[12]
    label = row[13]
    order_id = row[14]
    date_order_created = dateutil_parser.parse(row[15])
    promo_code = row[16]
    link_share = row[17]
    order_total = row[18]
    order_item_count = row[19]

    channel_key = 'noeticboxsales'
    obj = {
        'id': md5("%f" % (time.time() + randint(0, 1000000))).hexdigest(),
        'text': [{'title': "Order Number:%s, Product:%s, Email:%s" % (order_id, product_url, email)}],
        'time': int(time.mktime(date_order_created.timetuple())),
        'channel': {
            'id': md5(channel_key).hexdigest(),
            'type': channel_key,
            'sub_type': channel_key
        },
        'source': {
            'id': md5(channel_key + '_source').hexdigest(),
            'display_name': 'Sales Data',
        },
        'extensions': {
            'userid': {'type': 'string', 'value': user_id},
            'userregistereddate': {'type': 'string', 'value': user_register_date.strftime('%Y-%m-%d')},
            'useremail': {'type': 'string', 'value': email},
            'userfirstname': {'type': 'string', 'value': first_name},
            'usersurname': {'type': 'string', 'value': surname},
            'dateincart': {'type': 'string', 'value': date_in_cart.strftime('%Y-%m-%d')},
            'status': {'type': 'string', 'value': status},
            'producturl': {'type': 'string', 'value': product_url},
            'productamount': {'type': 'float', 'value': product_amount},
            'productcolor': {'type': 'string', 'value': product_color},
            'productsize': {'type': 'string', 'value': product_size},
            'boutique': {'type': 'string', 'value': boutique},
            'label': {'type': 'string', 'value': label},
            'orderid': {'type': 'string', 'value': order_id},
            'ordercreateddate': {'type': 'string', 'value': date_order_created.strftime('%Y-%m-%d')},
            'promocode': {'type': 'string', 'value': promo_code},
            'linkshare': {'type': 'string', 'value': link_share},
            'ordertotal': {'type': 'float', 'value': order_total},
            'orderitemscount': {'type': 'float', 'value': order_item_count},
            'orderitemscount': {'type': 'float', 'value': order_item_count},
            'channel': {'type': 'string', 'value': 'Sales Data'},
        }
    }
    post_data = {
        'content': json.dumps([obj]),
        'actions': [],
        'skip_duplicate_check': 'true',
    }
    urllib2.urlopen(POST_URL, urllib.urlencode(post_data)).read()
    urllib2.urlopen(COMMIT_URL).read()
    print datetime.datetime.now()