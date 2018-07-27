#!/usr/bin/python3

import os
import sys
import time
import json
import redis
import urllib.request

DOCKER_HOST = os.getenv('DOCKER_HOST')
REDIS_ADDR = '127.0.0.1'
REDIS_PORT = 6379


def redisDump():
  conn = redis.Redis(host=REDIS_ADDR, port=REDIS_PORT)
  for key in conn.keys():
    print(key)
    print(conn.get(key))
  return conn.keys()

def addData(datas):
  conn = redis.Redis(host=REDIS_ADDR, port=REDIS_PORT)
  for key in set(list(datas.keys()) + list(conn.keys())):
    if isinstance(key, bytes):
      key = key.decode('utf-8')
    if key in datas:
      conn.set(key, datas[key])
    else:
      conn.delete(key)

def getContainers():
  response = urllib.request.urlopen('http://' + DOCKER_HOST + '/containers/json?all=1')
  jsonData = json.loads(response.read().decode('utf-8'))

  datas = {}
  for con in jsonData:
    name = con['Names'][-1][1:]
    con_ip = getIpAddress(con['Id'])

    for port in con['Ports']:
      key = name + '-' + str(port['PrivatePort'])
      value=con_ip + ':' + str(port['PrivatePort'])
      datas[key] = value

  return datas


def getIpAddress(con_id):
  response = urllib.request.urlopen('http://' + DOCKER_HOST + '/containers/' + con_id + '/json')
  jsonData = json.loads(response.read().decode('utf-8'))
  #print(json.dumps(jsonData))
  ret = jsonData['NetworkSettings']['IPAddress']
  return ret

while True:
  addData(getContainers())
  print( redisDump() )
  sys.stdout.flush()
  time.sleep(3)