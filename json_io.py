import json

def JSON2Dict(json_path):
    with open(json_path,"r") as json_fin:
        json_dict=json.load(json_fin)
    return json_dict

def Dict2JSON(json_dict,json_path):
    with open(json_path,"w") as fout:
        json.dump(json_dict,fout,ensure_ascii=False) 
    return 