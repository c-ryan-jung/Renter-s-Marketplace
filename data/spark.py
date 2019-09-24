from pyspark import SparkContext
import itertools
import urllib.request
import urllib.parse
import json

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/access.log", 2)     # each worker loads a piece of the data file

pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition
users = pairs.groupByKey()
permutations = users.flatMapValues(lambda x: itertools.permutations(x))
permpairs = permutations.mapValues(lambda x: x[0:2]).distinct().filter(lambda x: x[1][0] != x[1][1])
flip = permpairs.map(lambda x: (x[1], x[0])).groupByKey()
count = flip.map(lambda x: (x[0], len(x[1])))
filtered = count.filter(lambda x: x[1] >= 3)
final = filtered.map(lambda x: (x[0][0], x[0][1])).groupByKey()

output = final.collect()                          # bring the data back to the master node so we can print it out

output_data = []

print("Co-views generated: ")
for item, recs in output:
    print(item, ":", *recs)
    r = []
    for rec in recs:
        r.append(rec)
    output_data.append((item, r))
    
data = {'output': json.dumps(output_data)}
json_data = urllib.parse.urlencode(data).encode('utf-8')
req = urllib.request.Request('http://models-api:8000/api/updateRecs', method='POST', data=json_data)
print(urllib.request.urlopen(req).read().decode('utf-8'))


print ("Co-views done")

sc.stop()