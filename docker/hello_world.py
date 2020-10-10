import json
with open('tcdata/num_list.csv') as f:
	arr = list(map(int,f.readlines())) 
res = {}
arr.sort(reverse=True)
res['Q1'] = 'Hello world'
res['Q2'] = sum(arr)
res['Q3'] = arr[:10]
with open('result.json', 'w', encoding='utf-8') as f:
	json.dump(res, f)

print(json.dumps(res))
