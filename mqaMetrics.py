'''
YODA (Your Open DAta)
EU CEF Action 2019-ES-IA-0121
University of Cantabria
Developer: Johnny Choque (jchoque@tlmat.unican.es)
'''
import requests
from rdflib import Graph, URIRef

def accessURL(urls, weight):
  checked = True
  for url in urls:
    try:
      res = requests.head(url)
      if res.status_code in range(200, 399):
        checked = checked and True
      else:
        checked = checked and False
    except:
      checked = checked and False
  if checked:
    weight = weight + 50
    print('   Result: OK. Weight assigned 50')
  else:
    print('   Result: ERROR - Responded status code of HTTP HEAD request is not in the 200 or 300 range')
  return weight

def downloadURL(urls, weight):
  checked = True
  print('   Result: OK. The property is set. Weight assigned 20')
  weight = weight + 20
  for url in urls:
    try:
      res = requests.head(url)
      if res.status_code in range(200, 399):
        checked = checked and True
      else:
        checked = checked and False
    except:
      checked = checked and False
  if checked:
    weight = weight + 30
    print('   Result: OK. Weight assigned 30')
  else:
    print('   Result: ERROR - Responded status code of HTTP HEAD request is not in the 200 or 300 range')
  return weight

def keyword(weight):
  weight = weight + 30
  print('   Result: OK. The property is set. Weight assigned 30')
  return weight

def theme(weight):
  weight = weight + 30
  print('   Result: OK. The property is set. Weight assigned 30')
  return weight

def spatial(weight):
  weight = weight + 20
  print('   Result: OK. The property is set. Weight assigned 20')
  return weight

def temporal(weight):
  weight = weight + 20
  print('   Result: OK. The property is set. Weight assigned 20')
  return weight

def format(urls, mach_read_voc, non_prop_voc, weight):
  mach_read_checked = True
  non_prop_checked = True
  found_checked = True
  print('   Result: OK. The property is set. Weight assigned 20')
  weight = weight + 20
  for url in urls:
    if str(url) in mach_read_voc:
      mach_read_checked = mach_read_checked and True
    else:
      mach_read_checked = mach_read_checked and False
    if str(url) in non_prop_voc:
      non_prop_checked = non_prop_checked and True
    else:
      non_prop_checked = non_prop_checked and False
    g = Graph()
    g.parse(url, format="application/rdf+xml")
    if (url, None, None) in g:
      found_checked = found_checked and True
    else:
      found_checked = found_checked and False
  if mach_read_checked:
    print('   Result: OK. The property is machine-readable. Weight assigned 20')
    weight = weight + 20
  else:
    print('   Result: ERROR. The property is not machine-readable')
  if non_prop_checked:
    print('   Result: OK. The property is non-propietary. Weight assigned 20')
    weight = weight + 20
  else:
    print('   Result: ERROR. The property is not non-propietary')
  if found_checked:
    result = True
  else:
    result = False
  return {'result': result, 'url':str(url), 'weight': weight}

def license(urls, weight):
  checked = True
  weight = weight + 20
  print('   Result: OK. The property is set. Weight assigned 20')
  for url in urls:
    g = Graph()
    g.parse(url, format="application/rdf+xml")
    if (url, None, None) in g:
      checked = checked and True
    else:
      checked = checked and False
  if checked:
    weight = weight + 10
    print('   Result: OK. The property provides the correct license information. Weight assigned 10')
  else:
    print('   Result: ERROR. The license is incorrect -',str(url))
  return weight

def contactpoint(weight):
  weight = weight + 20
  print('   Result: OK. The property is set. Weight assigned 20')
  return weight

def mediatype(urls, weight):
  checked = True
  weight = weight + 10
  print('   Result: OK. The property is set. Weight assigned 10')
  for url in urls:
    res = requests.head(str(url))
    if res.status_code != 404:
      checked = checked and True
    else:
      checked = checked and False
  if checked:
    result = True
  else:
    result = False
  return {'result': result, 'weight': weight}

def publisher(weight):
  weight = weight + 10
  print('   Result: OK. The property is set. Weight assigned 10')
  return weight

def accessrights(urls, weight):
  uri = URIRef('')
  checked = True
  isURL = True
  weight = weight + 10
  print('   Result: OK. The property is set. Weight assigned 10')
  for url in urls:
    g = Graph()
    if type(url) != type(uri):
      isURL = False
      continue
    g.parse(url, format="application/rdf+xml")
    if (url, None, None) in g:
      checked = checked and True
    else:
      checked = checked and False
  if isURL:
    if checked:
      weight = weight + 5
      print('   Result: OK. The property uses a controlled vocabulary. Weight assigned 5')
    else:
      print('   Result: ERROR. The license is incorrect -', str(url))
  else:
    print('   Result: ERROR. The property does not use a valid URL. No additional weight assigned')
  return weight

def issued(weight):
  weight = weight + 5
  print('   Result: OK. The property is set. Weight assigned 5')
  return weight

def modified(weight):
  weight = weight + 5
  print('   Result: OK. The property is set. Weight assigned 5')
  return weight

def rights(weight):
  weight = weight + 5
  print('   Result: OK. The property is set. Weight assigned 5')
  return weight

def byteSize(weight):
  weight = weight + 5
  print('   Result: OK. The property is set. Weight assigned 5')
  return weight

