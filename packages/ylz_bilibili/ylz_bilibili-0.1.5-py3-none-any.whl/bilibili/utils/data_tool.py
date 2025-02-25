from typing import Union
import json
def to_sse(obj:Union[dict,str])->str:
    if isinstance(obj,dict):
        obj_sse = f"data: ```json\n{json.dumps(obj,ensure_ascii=False)}```\n\n"
    else:
        obj_sse = f"data: ```json\n{str(obj)}````\n\n"
    return obj_sse

def to_event_stream(obj:Union[dict,str])->str:
    if isinstance(obj,dict):
        obj_sse = f"```json\n{json.dumps(obj,ensure_ascii=False)}```"
    else:
        obj_sse = f"```json\n{str(obj)}````"
    return obj_sse