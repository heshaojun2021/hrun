import requests
import ast

class wxPush():
    def __init__(self, webhook, user_ids):
        self.url = webhook
        self.user_ids = user_ids

    def markdown(self, project, url, env, plan, pass_rate, all, success, fail, error, all_time):
        markdown_params = {
                        "msgtype": "markdown",
                        "markdown": {
                            "content": f"""## [{project}] 测试报告 \n
                                       ><font color=\"warning\">请相关同事注意！</font>\n
                                       >报告地址：[点击查看]({url})
                                       >执行环境：<font color=\"comment\">{env}</font>
                                       >执行计划：<font color=\"comment\">{plan}</font>\n
                                       >执行通过率：**{pass_rate}%**
                                       >用例总数：**{all}**
                                       >成功用例：<font color=\"info\">{success}</font>
                                       >失败用例：<font color=\"warning\">{fail}</font>
                                       >错误用例：<font color=\"warning\">{error}</font>
                                       >耗时：{all_time}s
                                       """
                            }
                        }
        requests.post(self.url, json=markdown_params)

    def text(self):
        if self.user_ids == '' or self.user_ids == '[]':
            return True
        text_params = {
            "msgtype": "text",
            "text": {
                "content": "通知人：", "mentioned_list":  ast.literal_eval(self.user_ids),
                # "mentioned_mobile_list":["13800001111","@all"]
            }
        }

        requests.post(self.url, json=text_params)


