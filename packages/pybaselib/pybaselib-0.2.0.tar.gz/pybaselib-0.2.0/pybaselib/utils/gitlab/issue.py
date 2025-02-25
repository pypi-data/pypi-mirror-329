# -*- coding: utf-8 -*-
# @Author: maoyongfan
# @email: maoyongfan@163.com
# @Date: 2025/2/24 17:07
import json
from pybaselib.utils.appLayer.http import Http2Client, HttpClient


class Issue:
    def __init__(self):
        pass

    def create_bug(self, bug_title: str, bug_description: str, priority: str, version: str, controllerInfo,
                   developer_id: list, token: str, host: str, uri: str):
        if version == "old":
            gitlab_title = f"[Bug_自动提交] [旧版] [{controllerInfo.net_ntcip_version}] {bug_title}"
        else:
            gitlab_title = f"[Bug_自动提交] [新版] [{controllerInfo.net_ntcip_version}] {bug_title}"

        gitlab_description = f"# 前置条件 \n\n{controllerInfo._asdict()} \n\n # bug描述 \n\n{bug_description}"

        headers = {
            "PRIVATE-TOKEN": token,
            "Content-Type": "application/json"
        }

        if priority == "P1":
            labels = "type::bug,foundByAutoTest,priority::1,severity::1"
        elif priority == "P3":
            labels = "type::bug,foundByAutoTest,priority::3,severity::3"
        else:
            labels = "type::bug,foundByAutoTest,priority::2,severity::2"

        post_data = {
            "title": gitlab_title,
            "description": gitlab_description,
            "labels": labels,
            "assignee_ids": developer_id  # 车保康
        }
        print(f"创建issue_data: \n{json.dumps(post_data, indent=4)}")
        gitlab_client = Http2Client(host,
                                    headers=headers)
        gitlab_response = gitlab_client.post(uri, json=post_data)
        print(gitlab_response)
