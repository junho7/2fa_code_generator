from elasticsearch import Elasticsearch, helpers
from block_list import same_digits, hexspeak
import random

es = Elasticsearch(hosts="http://localhost:9200/", http_auth=('elastic', 'password'), timeout=30, max_retries=10, retry_on_timeout=True)

IDX = '2fa_3shards_idx'
ISSENT_REVERSE_IDX = 'issent_reverse_idx'

def get_issent_reverse():
  result = es.search(index=ISSENT_REVERSE_IDX, body={"query":{"match":{"id":{"query":1}}}},size=1)
  res = result['hits']['hits'][0]['_source']['issent_reverse']
  return bool(res)

ISSENT_REVERSE = bool(get_issent_reverse())


failure_count = 0
MAX_ID = 294967295
# MAX_ID = 4294967295
CHECK_ID_RANGE = 1000000
MAX_FAILURE_COUNT = 10




def generate_random_number(start_id=None):
  global failure_count
  
  random_range_start = random.randint(1, MAX_ID) if not start_id else start_id
  random_range_end = MAX_ID if random_range_start + CHECK_ID_RANGE > MAX_ID or start_id else random_range_start + CHECK_ID_RANGE
  print('Generating random number between ', random_range_start, ' and ', random_range_end)
  
  random_query = {
    
  "query": {
    "function_score": {
    "query": {
        "bool": {
            "must": [
                {"range": {"id": {"gte": random_range_start, "lte": random_range_end}}},
                {"match": {"is_sent" : False if not ISSENT_REVERSE else True}},
                {"match": {"is_blocked" : False}},
            ]
        }
    },
      "random_score": {},
      "boost_mode": "sum"
    }
  }
}
  
  res = es.search(index=IDX, body=random_query,size=1)
  
  if start_id and res['hits']['total']['value'] == 0:
    print('All combinations are sent out')
    reset_issent()
    res = generate_random_number()
  elif res['hits']['total']['value'] == 0:
    print('No number is available in this random range')
    failure_count += 1
    new_start_id = None
    if failure_count > MAX_FAILURE_COUNT:
      new_start_id = 1
    res = generate_random_number(new_start_id)
    
  return res

def search_by_keyword(keyword):
  
  query_DSL = {
    # "query": {
    #   "query_string": {
    #     "default_field": "hexadecimal",
    #     "query": f"*{keyword}*"
    #   }
    # }
      "query": {
      "wildcard": {
        "hexadecimal": {
          "value": f"*{keyword}*",
          "boost": 1.0,
          "rewrite": "constant_score"
        }
      }
    }
  }
  
  res = es.search(index=IDX, body=query_DSL)
  return res
  
def update_isblocked_by_id(id):

  update_value = {
      "doc": {
        "is_blocked": True
      }
  }
  res = es.update(index=IDX, body=update_value, id=id)
  print('update result: ', res)
  
def update_issent_by_id(id):

  update_value = {
      "doc": {
        "is_sent": True if not ISSENT_REVERSE else False
      }
  }
  res = es.update(index=IDX, body=update_value, id=id)
  
def reset_issent():
  cur_issent_reverse = bool(get_issent_reverse())
  new_issent_reverse = not cur_issent_reverse
  update_value = {
      "doc": {
        "issent_reverse": new_issent_reverse
      }
  }
  res = es.update(index=ISSENT_REVERSE_IDX, body=update_value, id=1)
  
def initial_update_isblocked():
  # blocklist = same_digits
  blocklist = hexspeak
  print('initial_update_isblocked')
  
  for blockedcode in blocklist:
    print('blockedcode: ', blockedcode)
    res = search_by_keyword(blockedcode)
    print('res: ', res)
    hits = res['hits']['hits']
    for hit in hits:
      print("2FA Code: ", "0x"+hit['_source']['hexadecimal'])
      id = hit['_source']['id']
      print('id; ', id)
      update_isblocked_by_id(id)
    