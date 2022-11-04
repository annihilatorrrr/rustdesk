#!/usr/bin/env python3

import os
import glob
import sys
import csv
    
def get_lang(lang): 
  out = {}
  for ln in open(f'./src/lang/{lang}.rs'):
    ln = ln.strip()
    if ln.startswith('("'):
      k, v = line_split(ln)
      out[k] = v
  return out 

def line_split(line):
    toks = line.split('", "')    
    assert(len(toks) == 2)    
    k = toks[0][2:]    
    v = toks[1][:-3]
    return k, v


def main():
  if len(sys.argv) == 1:
    expand()
  elif sys.argv[1] == '1':
    to_csv()
  else:
    to_rs(sys.argv[1])


def expand():
  for fn in glob.glob('./src/lang/*'): 
    lang = os.path.basename(fn)[:-3]
    if lang in ['en','cn']: continue
    dict = get_lang(lang)
    with open(f"./src/lang/{lang}.rs", "wt") as fw:
      for line in open('./src/lang/cn.rs'):
        line_strip = line.strip()
        if line_strip.startswith('("'):
          k, v = line_split(line_strip)
          line = line.replace(v, dict[k]) if k in dict else line.replace(v, "")
        fw.write(line)
 

def to_csv():
  for fn in glob.glob('./src/lang/*.rs'): 
    lang = os.path.basename(fn)[:-3]
    with open(f'./src/lang/{lang}.csv', "wt") as csvfile:
      csvwriter = csv.writer(csvfile)
      for line in open(fn):
        line_strip = line.strip()
        if line_strip.startswith('("'):
          k, v = line_split(line_strip)
          csvwriter.writerow([k, v])


def to_rs(lang):
  csvfile = open(f'{lang}.csv', "rt")
  with open(f"./src/lang/{lang}.rs", "wt") as fw:
    fw.write('''lazy_static::lazy_static! {
pub static ref T: std::collections::HashMap<&'static str, &'static str> =
    [
''')
    for row in csv.reader(csvfile):
      fw.write('        ("%s", "%s"),\n'%(row[0].replace('"', '\"'), row[1].replace('"', '\"')))
    fw.write('''    ].iter().cloned().collect();
}
''')


main()
