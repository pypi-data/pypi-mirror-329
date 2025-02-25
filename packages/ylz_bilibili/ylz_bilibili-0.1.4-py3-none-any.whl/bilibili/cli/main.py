import argparse
import asyncio

from bilibili.cli.init import init
from bilibili.cli.serve import serve
from bilibili.cli.searcher import searcher
from bilibili.cli.test import test

def run():
    main()

def main():
    usage= \
"""
    examples:
        # 初始化配置信息 
        ylz_bilibili reset 

        # 启动server
        ylz_bilibili serve --host 0.0.0.0 --port 8000

        # 搜索
        ylz_bilibili search 
        
        # 测试
        ylz_bilibili test --bvid BV**********
        
"""
    parser = argparse.ArgumentParser(description = "测试工具",usage=usage)
    parser.add_argument("--project_name",type=str,default="bilibili",help="project名称")
    parser.add_argument("--log_level",type=str,default="INFO",choices=["INFO","DEBUG"],help="日志级别,默认:INFO")
    parser.add_argument("--log_name",type=str,default="bilibili.log",help="日志文件名称")
    

    subparsers = parser.add_subparsers(dest="command", required=True, help="可以使用的子命令")
    serve_parser = subparsers.add_parser("serve", help="启动serve")
    serve_parser.add_argument("--host",type=str,default="0.0.0.0",help="bind host,default:0.0.0.0")
    serve_parser.add_argument("--port",type=int,default=3000,help="listen port,default::3000")
           
    test_parser = subparsers.add_parser("test", help="测试")
    test_parser.add_argument("--bvid",type=str,required=True,help="bvid,BV开头的长度为12的字符串")

    search_parser = subparsers.add_parser("search", help="搜索")
    search_parser.add_argument("--bvid",type=str,required=True,help="bvid,BV开头的长度为12的字符串")

    args:argparse.Namespace = parser.parse_args()

    init(args)
   
    if args.command == "serve":
        serve(args)
    elif args.command == "search":
        searcher(args)
    else:
        asyncio.run(test(args))   
if __name__ == '__main__':
    main()
