import json
from bilibili_api import search,sync, video_zone,Credential,request_settings
import dotenv

def searcher(args):
    env_path = ".env"
    # sessdata = dotenv.get_key(env_path,"SESSDATA")
    # bili_jct = dotenv.get_key(env_path,"BILI_JCT")
    # buvid3 = dotenv.get_key(env_path,"BUVID3") 
    # credential = Credential(sessdata=sessdata,bili_jct=bili_jct,buvid3=buvid3)
    request_settings.set_verify_ssl(False)

    search_by_type_fun = lambda : search.search_by_type(
       "小马宝莉",
        search_type=search.SearchObjectType.VIDEO,
        order_type=search.OrderVideo.SCORES,
        time_range=10,
        video_zone_type=video_zone.VideoZoneTypes.DOUGA_MMD,
        page=1,
    )
    res = sync(search_by_type_fun())
    print(json.dumps(res,ensure_ascii=False,indent=4))
