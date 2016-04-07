#!/usr/bin/python

import pickle
import json
import sys

if __name__ == '__main__':
  filename = sys.argv[1]
  p = pickle.load(open(filename, 'r'))
  for arr in p:
      print arr
