
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel,Field
from langchain_community.document_loaders import BiliBiliLoader
import bilibili_api
import logging
import dotenv
import os
class BilibiliSession(BaseModel):
    sessdata: str = Field(description="sessdata")
    bili_jct: str = Field(description="bili_jct")
    buvid3: str = Field(description="buvid3")

class BilibiliLib:
    def __init__(self):
        self.router = APIRouter()
        self.set_session()
        bilibili_api.request_settings.set_verify_ssl(False)
    def set_session(self,session: BilibiliSession|None = None):
        env_path = ".env"
        if session:
            dotenv.set_key(env_path,"SESSDATA",session.sessdata)
            dotenv.set_key(env_path,"BILI_JCT",session.bili_jct)
            dotenv.set_key(env_path,"BUVID3",session.buvid3)
        sessdata = dotenv.get_key(env_path,"SESSDATA")
        bili_jct = dotenv.get_key(env_path,"BILI_JCT")
        buvid3 = dotenv.get_key(env_path,"BUVID3")
        if not sessdata or not bili_jct or not buvid3:
            raise Exception("请先确保.env文件中正确设置了SESSDATA,BILI_JCT,BUVID3!")
        self.session:BilibiliSession = BilibiliSession(sessdata=sessdata,bili_jct=bili_jct,buvid3=buvid3)
        print("session=",self.session.model_dump_json())
    async def parse_video(self,urls:list[str]) -> dict:
        loader = BiliBiliLoader(
            urls,
            sessdata=self.session.sessdata,
            bili_jct=self.session.bili_jct,
            buvid3=self.session.buvid3
        )
        docs = await loader.aload()
        return [{"metadata":item.metadata,"page_content":item.page_content} for item in docs]
    def register_router(self):
        @self.router.post("/set_session",tags=["手动传入bilibili session"],deprecated=False)
        def _set_session(session:BilibiliSession):
            try:
                self.set_session(session)
                return self.session
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"{e}")
        @self.router.get("/parse_video",tags=["获取视频的文字信息"],summary="获取一个或多个视频文字信息，返回结构与List[langchain.Document]兼容",
                         description="可以传入一个或多个视频rul或视频id，如果多个视频请用`，`分隔")
        async def _parse_video(video_url:str,req:Request):
            try:
                urls = [item if item.startswith("https://") else f"https://www.bilibili.com/video/{item}"
                         for item in video_url.split(',')]
                res = await self.parse_video(urls)
                return {"video_url":video_url,"txt":res}
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"{e}")
