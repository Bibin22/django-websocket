import json
dict_data = {"a":1, "b":1, "C":3}
print('dict data',dict_data)
print('Type of Dict Data', type(dict_data))

json_data = json.dumps(dict_data)
print('json_data', json_data)
print('type of json data', type(json_data))

some_data = json.loads(json_data)
print('some_data', some_data)
print('type of some data', type(some_data))