# -*- coding:utf-8 -*-
# ! ./usr/bin/env python
import json
jsonpath = 'C:/Users/Administrator/Desktop/test.json'
data = {
    "carDark": {
        "name": "CarDark",
        "image_files": [
            "0001.jpg",
            "0002.jpg",
            "0003.jpg",
            "0004.jpg",
            "0005.jpg",
        ],
        "init_rect": [
            73,
            126,
            29,
            23
        ],
    }
}
# one line show
data1 = json.dumps(data)
# multi lines show as dict format
data2 = json.dumps(data, indent=2) # indent 表示缩进
# write to json file , one line show
# with open(jsonpath, 'w') as f:
#     json.dump(data, f)
# # write to json file , multi lines show as dict format
# with open(jsonpath, 'w') as f:
#     json.dump(data, f, indent=2)
print(data1)
print(data2)
