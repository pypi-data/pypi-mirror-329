import asyncio
from bilibili_api import Geetest, GeetestType, login_v2, sync,request_settings

async def test(args):
    request_settings.set_verify_ssl(False)
    gee = Geetest() 
    await gee.generate_test() 
    gee.start_geetest_server()                                      
    print(gee.get_geetest_server_url()) 



# import asyncio
# from bilibili_api import video,request_settings


# async def main() -> None:
#     request_settings.set_verify_ssl(False)
#     # 实例化 Video 类
#     v = video.Video(bvid="BV1uv411q7Mv")
#     # 获取信息
#     info = await v.get_info()
#     # 打印信息
#     print(info)


# if __name__ == "__main__":
#     asyncio.run(main())


# from bilibili_api import login_v2, sync
# import time


# async def main() -> None:
#     qr = login_v2.QrCodeLogin(platform=login_v2.QrCodeLoginChannel.WEB) # 生成二维码登录实例，平台选择网页端
#     print("abc")
#     await qr.generate_qrcode()                                          # 生成二维码
#     print("xyz")
#     print(qr.get_qrcode_terminal())                                     # 生成终端二维码文本，打印
#     while not qr.has_done():                                            # 在完成扫描前轮询
#         print(await qr.check_state())                                   # 检查状态
#         time.sleep(1)                                                   # 轮训间隔建议 >=1s
#     print(qr.get_credential().get_cookies())                            # 获取 Credential 类，打印其 Cookies 信息

# if __name__ == '__main__':
#     sync(main())

# #示例：终端简易密码登录和验证码登录脚本
# from bilibili_api import Geetest, GeetestType, login_v2, sync


# async def main() -> None:
#     choice = input("pwd / sms:")
#     if not choice in ["pwd", "sms"]:
#         return

#     gee = Geetest()                                                         # 实例化极验测试类
#     await gee.generate_test()                                               # 生成测试
#     gee.start_geetest_server()                                              # 在本地部署网页端测试服务
#     print(gee.get_geetest_server_url())                                     # 获取本地服务链接
#     while not gee.has_done():                                               # 如果测试未完成
#         pass                                                                # 就等待
#     gee.close_geetest_server()                                              # 关闭部署的网页端测试服务
#     print("result:", gee.get_result())

#     # 1. 密码登录
#     if choice == "pwd":
#         username = input("username:")                                       # 手机号/邮箱
#         password = input("password:")                                       # 密码
#         cred = await login_v2.login_with_password(
#             username=username, password=password, geetest=gee               # 调用接口登陆
#         )

#     # 2. 验证码登录
#     if choice == "sms":
#         phone = login_v2.PhoneNumber(input("phone:"), "+86")                # 实例化手机号类
#         captcha_id = await login_v2.send_sms(phonenumber=phone, geetest=gee)# 发送验证码
#         print("captcha_id:", captcha_id)                                    # 顺便获得对应的 captcha_id
#         code = input("code: ")
#         cred = await login_v2.login_with_sms(
#             phonenumber=phone, code=code, captcha_id=captcha_id             # 调用接口登陆
#         )

#     # 安全验证
#     if isinstance(cred, login_v2.LoginCheck):
#         # 如法炮制 Geetest
#         gee = Geetest()                                                     # 实例化极验测试类
#         await gee.generate_test(type_=GeetestType.VERIFY)                   # 生成测试 (注意 type_ 为 GeetestType.VERIFY)
#         gee.start_geetest_server()                                          # 在本地部署网页端测试服务
#         print(gee.get_geetest_server_url())                                 # 获取本地服务链接
#         while not gee.has_done():                                           # 如果测试未完成
#             pass                                                            # 就等待
#         gee.close_geetest_server()                                          # 关闭部署的网页端测试服务
#         print("result:", gee.get_result())
#         await cred.send_sms(gee)                                            # 发送验证码
#         code = input("code:")
#         cred = await cred.complete_check(code)                              # 调用接口登陆

#     print("cookies:", cred.get_cookies())                                   # 获得 cookies

# if __name__ == "__main__":
#     sync(main())

