import os
import requests
import json
import time

def test_huawei_push():
    # 1. 从 GitHub Secrets 读取配置
    APP_ID = os.environ.get("HUAWEI_APP_ID")
    APP_SECRET = os.environ.get("HUAWEI_APP_SECRET")
    DEVICE_TOKEN = os.environ.get("HUAWEI_DEVICE_TOKEN")

    print(f"检查配置: APP_ID={APP_ID[:4]}***, TOKEN长度={len(DEVICE_TOKEN) if DEVICE_TOKEN else 0}")

    if not all([APP_ID, APP_SECRET, DEVICE_TOKEN]):
        print("❌ 错误：Secrets 配置缺失！请检查 GitHub 设置。")
        return

    # 2. 获取 Access Token (这是钥匙)
    print("正在向华为申请 Access Token...")
    auth_url = "https://oauth-login.cloud.huawei.com/oauth2/v3/token"
    auth_data = {
        "grant_type": "client_credentials",
        "client_id": APP_ID,
        "client_secret": APP_SECRET
    }
    
    try:
        resp = requests.post(auth_url, data=auth_data)
        if resp.status_code != 200:
            print(f"❌ 鉴权失败: {resp.text}")
            return
        
        access_token = resp.json().get("access_token")
        print("✅ Access Token 获取成功！")

        # 3. 发送推送消息
        print("正在发送测试消息...")
        push_url = f"https://push-api.cloud.huawei.com/v1/{APP_ID}/messages:send"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "validate_only": False,
            "message": {
                "notification": {
                    "title": "🎉 测试成功",
                    "body": f"恭喜！GitHub Action 已成功连接你的鸿蒙手机！\n时间: {time.strftime('%H:%M:%S')}"
                },
                "android": {
                    "notification": {
                        "click_action": {
                            "type": 3  # 3 表示点击打开 App
                        }
                    }
                },
                "token": [DEVICE_TOKEN]
            }
        }
        
        push_resp = requests.post(push_url, headers=headers, json=payload)
        print(f"华为服务器响应: {push_resp.text}")
        
        if '"SUCCESS"' in push_resp.text:
            print("🎉🎉🎉 推送成功！快看手机！")
        else:
            print("❌ 推送失败，请检查错误代码。")

    except Exception as e:
        print(f"❌ 发生异常: {e}")

if __name__ == "__main__":
    test_huawei_push()
