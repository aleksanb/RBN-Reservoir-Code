import sys
import json
import numpy as np

inp = sys.stdin.read()
j = json.loads(inp)

mal=[d['mean_attractor_length'] for d in j if d['accuracy'] >= 0.85]
na=[d['n_attractors'] for d in j if d['accuracy'] >= 0.85]

mean_mal = np.mean(mal)
median_mal = np.median(mal)

mean_na = np.mean(na)
median_na = np.median(na)

print "MAL {:.02f} / {:.02f}".format(mean_mal, median_mal)
print "NA {:.02f} / {:.02f}".format(mean_na, median_na)
