
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException,APIRouter,Request
from fastapi.responses import JSONResponse,StreamingResponse
import fastapi_cdn_host
from bilibili import BilibiliLib

from bilibili.utils.data_tool import to_sse

def serve(args):
    host = args.host 
    port = args.port
    app = FastAPI(title="bilibiliServe")
    fastapi_cdn_host.patch_docs(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(content={"error": exc.detail}, status_code=exc.status_code)
    
    bilibiliLib = BilibiliLib()
    bilibiliLib.register_router()
    app.include_router(bilibiliLib.router,prefix="/v1")
    
    app.include_router(info_router,prefix="")
    uvicorn.run(app, host = host, port = port)

info_router = APIRouter()
@info_router.get("/info",tags=["注册API info"])
def _info(req:Request):
    res = {"app":
        {
            "profile":{
                "name": "ylz_bilibili",
                "icon": "图标",
                "title": "bilibili视频大纲解析",
                "version": "0.1.5",
                "author": "youht",
                "describe": "bilibili视频大纲解析"
            },
            "api":{
                "method": "GET",
                "url": "/v1/parse_video",
                "query":[{
                    "name": "video_url",
                    "title": "video的bvid码",
                    "type": "string",
                    "require": True,
                    "describe": "可以传入一个或多个视频rul或视频id,如果多个视频请用`,`分隔",
                    "defaultValue": "",
                }],        
            }
        }
    }
    return StreamingResponse(to_sse(res),media_type="text/event-stream")
