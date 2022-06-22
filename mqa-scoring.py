#!/usr/bin/env python3
'''
YODA (Your Open DAta)
EU CEF Action 2019-ES-IA-0121
University of Cantabria
Developer: Johnny Choque (jchoque@tlmat.unican.es)
'''
import requests
import json
from rdflib import Graph
import argparse
import mqaMetrics as mqa
import os

URL_EDP = 'https://data.europa.eu/api/mqa/shacl/validation/report'
HEADERS = {'content-type': 'application/rdf+xml'}
MACH_READ_FILE = os.path.join('edp-vocabularies', 'edp-machine-readable-format.rdf')
NON_PROP_FILE = os.path.join('edp-vocabularies', 'edp-non-proprietary-format.rdf')

def otherCases(pred, objs, g):
  for obj in objs:
    met = str_metric(obj, g)
    if met == None:
      print('   Result: WARN. Not included in MQA - '+ str_metric(pred, g))
    else:
      print('   Result: WARN. Not included in MQA - '+ str(met))

def str_metric(val, g):
  valStr=str(val)
  for prefix, ns in g.namespaces():
    if val.find(ns) != -1:
      metStr = valStr.replace(ns,prefix+":")
      return metStr

def load_edp_vocabulary(file):
  g = Graph()
  g.parse(file, format="application/rdf+xml")
  voc = []
  for sub, pred, obj in g:
    voc.append(str(sub))
  return voc

def edp_validator(file, weight):
  print('* SHACL validation')
  try:
    rdfFile = open(file, "r")
  except Exception as e:
    raise SystemExit(e)
  with rdfFile:
    try:
      payload = rdfFile.read().replace("\n", " ")
      r_edp = requests.post(URL_EDP, data=payload.encode('utf-8'), headers=HEADERS)
      r_edp.raise_for_status()
    except requests.exceptions.HTTPError as err:
      raise SystemExit(err)
    report = json.loads(r_edp.text)
    if valResult(report):
      print('   Result: OK. The metadata has successfully passed the EDP validator. Weight assigned 30')
      weight = weight + 30
    else:
      print('   Result: ERROR. DCAT-AP errors found in metadata')
  return weight

def valResult(d):
  if 'sh:conforms' in d:
    return d['sh:conforms']
  for k in d:
    if isinstance(d[k], list):
      for i in d[k]:
        if 'sh:conforms' in i:
          return i['sh:conforms']

def get_metrics(g):
  metrics = {}
  for sub, pred, obj in g:
    if pred not in metrics.keys():
      metrics[pred] = None
  for pred in metrics.keys():
    obj_list=[]
    for obj in g.objects(predicate=pred):
      obj_list.append(obj)
    metrics[pred] = obj_list
  return metrics

def main():
  mach_read_voc = []
  non_prop_voc = []

  parser = argparse.ArgumentParser(description='Calculates the score obtained by a metadata according to the MQA methodology specified by data.europa.eu')
  parser.add_argument('-f', '--file', type=str, required=True, help='RDF file to be validated')
  args = parser.parse_args()

  g = Graph()
  g.parse(args.file, format="application/rdf+xml")

  mach_read_voc = load_edp_vocabulary(MACH_READ_FILE)
  non_prop_voc = load_edp_vocabulary(NON_PROP_FILE)

  weight = 0
  weight = edp_validator(args.file, weight)
  print('   Current weight =',weight)

  metrics = get_metrics(g)
  f_res = {}
  f_res = f_res.fromkeys(['result', 'url', 'weight'])
  m_res = {}
  m_res = m_res.fromkeys(['result', 'weight'])

  for pred in metrics.keys():
    met = str_metric(pred, g)
    objs = metrics[pred]
    print('*',met)
    if met == "dcat:accessURL":
      weight = mqa.accessURL(objs, weight)
    elif met == "dcat:downloadURL":
      weight = mqa.downloadURL(objs, weight)
    elif met == "dcat:keyword":
      weight = mqa.keyword(weight)
    elif met == "dcat:theme":
      weight = mqa.theme(weight)
    elif met == "dct:spatial":
      weight = mqa.spatial(weight)
    elif met == "dct:temporal":
      weight = mqa.temporal(weight)
    elif met == "dct:format":
      f_res = mqa.format(objs, mach_read_voc, non_prop_voc, weight)
      weight = f_res['weight']
    elif met == "dct:license":
      weight = mqa.license(objs, weight)
    elif met == "dcat:contactPoint":
      weight = mqa.contactpoint(weight)
    elif met == "dcat:mediaType":
      m_res = mqa.mediatype(objs, weight)
      weight = m_res['weight']
    elif met == "dct:publisher":
      weight = mqa.publisher(weight)
    elif met == "dct:accessRights":
      weight = mqa.accessrights(objs, weight)
    elif met == "dct:issued":
      weight = mqa.issued(weight)
    elif met == "dct:modified":
      weight = mqa.modified(weight)
    elif met == "dct:rights":
      weight = mqa.rights(weight)
    elif met == "dcat:byteSize":
      weight = mqa.byteSize(weight)
    else:
      otherCases(pred, objs, g)
    print('   Current weight =',weight)

  print('* dct:format & dcat:mediaType')
  if f_res['result'] and m_res['result']:
    weight = weight + 10
    print('   Result: OK. The properties belong to a controlled vocabulary. Weight assigned 10')
    print('   Current weight=',weight)
  else:
    print('   Result: WARN. The properties do not belong to a controlled vocabulary')

  print('\n')
  print('Overall MQA scoring:', str(weight))

if __name__ == "__main__":
  main()
