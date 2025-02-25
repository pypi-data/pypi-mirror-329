
import asyncio
import json
from typing import Union
from fastapi import APIRouter, HTTPException, Request,Path,Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel,Field
from langchain_community.document_loaders import BiliBiliLoader
import bilibili_api
import logging
import dotenv
import os

from bilibili.utils.data_tool import to_sse

class Credential(BaseModel):
    sessdata: str = Field(description="sessdata")
    bili_jct: str = Field(description="bili_jct")
    buvid3: str = Field(description="buvid3")

class BilibiliLib:
    def __init__(self):
        self.router = APIRouter()
        self.set_credential()
        bilibili_api.request_settings.set_verify_ssl(False)
    
    def set_credential(self,credential: Credential|None = None):
        env_path = ".env"
        if credential:
            dotenv.set_key(env_path,"SESSDATA",credential.sessdata)
            dotenv.set_key(env_path,"BILI_JCT",credential.bili_jct)
            dotenv.set_key(env_path,"BUVID3",credential.buvid3)
        sessdata = dotenv.get_key(env_path,"SESSDATA")
        bili_jct = dotenv.get_key(env_path,"BILI_JCT")
        buvid3 = dotenv.get_key(env_path,"BUVID3")
        if not sessdata or not bili_jct or not buvid3:
            raise Exception("请先确保.env文件中正确设置了SESSDATA,BILI_JCT,BUVID3!")
        self.credential:Credential = Credential(sessdata=sessdata,bili_jct=bili_jct,buvid3=buvid3)
        print("credential=",self.credential.model_dump_json())
    async def parse_video(self,urls:list[str]) -> dict:
        loader = BiliBiliLoader(
            urls,
            sessdata=self.credential.sessdata,
            bili_jct=self.credential.bili_jct,
            buvid3=self.credential.buvid3
        )
        docs = await loader.aload()
        return [{"metadata":item.metadata,"page_content":item.page_content} for item in docs]
    async def event_generator(self):
        messages = ["hello world!!","how old are yout?","what's your name?"]
        for message in messages:
            yield to_sse(message)
            await asyncio.sleep(1)
    def register_router(self):
        @self.router.get("/sse",tags=["测试SSE"])
        async def _test_sse(req:Request):
            response = StreamingResponse(self.event_generator(),media_type="text/event-stream") 
            return response           
        @self.router.post("/set_credential",tags=["手动传入bilibili credential"],deprecated=False)
        def _set_credential(credential:Credential):
            try:
                self.set_credential(credential)
                return self.credential
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"{e}")
        @self.router.get("/parse_video",tags=["获取视频的文字信息"],summary="获取一个或多个视频文字信息，返回结构与List[langchain.Document]兼容",
                         description="可以传入一个或多个视频rul或视频id,如果多个视频请用`,`分隔")
        async def _parse_video(
            video_url:str = Query(...,description="一个或多个视频rul或视频id,如果多个视频请用`,`分隔"),
        ):
            try:
                urls = [item if item.startswith("https://") else f"https://www.bilibili.com/video/{item}"
                         for item in video_url.split(',')]
                res = await self.parse_video(urls)
                res_sse = to_sse({"video_url":video_url,"info":res})
                return StreamingResponse(res_sse,media_type="text/event-stream")
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"{e}")
