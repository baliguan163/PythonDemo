# -*-encoding:utf-8-*-
import os
import re
import shutil
import time
import itchat
from itchat.content import *

# ˵�������Գ��ص����ı����֡���������Ƶ��ͼƬ��λ�á���Ƭ����������

# {msg_id:(msg_from,msg_to,msg_time,msg_time_rec,msg_type,msg_content,msg_share_url)}
msg_dict = {}

# �ļ��洢��ʱĿ¼
rev_tmp_dir = "/home/alic/RevDir/"
if not os.path.exists(rev_tmp_dir): os.mkdir(rev_tmp_dir)

# ������һ������ | ������Ϣ�ͽ���note��msg_id��һ�� �ɺϽ������
face_bug = None


# �����յ�����Ϣ������ֵ��У������յ�����Ϣʱ���ֵ��г�ʱ����Ϣ�������� | �����ܲ����г��ع��ܵ���Ϣ
# [TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO, FRIENDS, NOTE]
@itchat.msg_register([TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO])
def handler_receive_msg(msg):
    global face_bug
    # ��ȡ���Ǳ���ʱ�������ʽ������ʱ��� e: 2017-04-21 21:30:08
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # ��ϢID
    msg_id = msg['MsgId']
    # ��Ϣʱ��
    msg_time = msg['CreateTime']
    # ��Ϣ�������ǳ� | ����Ҳ����ʹ��RemarkName��ע�������Լ�����û�б�ע����ΪNone
    msg_from = (itchat.search_friends(userName=msg['FromUserName']))["NickName"]
    # ��Ϣ����
    msg_content = None
    # ���������
    msg_share_url = None
    if msg['Type'] == 'Text' \
            or msg['Type'] == 'Friends':
        msg_content = msg['Text']
    elif msg['Type'] == 'Recording' \
            or msg['Type'] == 'Attachment' \
            or msg['Type'] == 'Video' \
            or msg['Type'] == 'Picture':
        msg_content = r"" + msg['FileName']
        # �����ļ�
        msg['Text'](rev_tmp_dir + msg['FileName'])
    elif msg['Type'] == 'Card':
        pass
        # msg_content = msg['RecommendInfo']['NickName'] + r" ����Ƭ"
    elif msg['Type'] == 'Map':
        pass
        # x, y, location = re.search(
        #     "<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
        # if location is None:
        #     # msg_content = r"γ��->" + x.__str__() + " ����->" + y.__str__()
        # else:
        #     msg_content = r"" + location
    elif msg['Type'] == 'Sharing':
        msg_content = msg['Text']
        msg_share_url = msg['Url']
    face_bug = msg_content

    # �����ֵ�
    msg_dict.update(
        {
            msg_id: {
                "msg_from": msg_from, "msg_time": msg_time, "msg_time_rec": msg_time_rec,
                "msg_type": msg["Type"],
                "msg_content": msg_content, "msg_share_url": msg_share_url
            }
        }
    )


# �յ�note֪ͨ����Ϣ���ж��ǲ��ǳ��ز�������Ӧ����
@itchat.msg_register([NOTE])
def send_msg_helper(msg):
    global face_bug
    if re.search(r"\<\!\[CDATA\[.*������һ����Ϣ\]\]\>", msg['Content']) is not None:
        # ��ȡ��Ϣ��id
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
        old_msg = msg_dict.get(old_msg_id, {})
        if len(old_msg_id) < 11:
            itchat.send_file(rev_tmp_dir + face_bug, toUserName='filehelper')
            os.remove(rev_tmp_dir + face_bug)
        else:
            msg_body = "������һ������~" + "\n" \
                       + old_msg.get('msg_from') + " ������ " + old_msg.get("msg_type") + " ��Ϣ" + "\n" \
                       + old_msg.get('msg_time_rec') + "\n" \
                       + "������ʲô ?" + "\n" \
                       + r"" + old_msg.get('msg_content')
            # ����Ƿ����������
            if old_msg['msg_type'] == "Sharing": msg_body += "\n�����������? " + old_msg.get('msg_share_url')

            # ��������Ϣ���͵��ļ�����
            itchat.send(msg_body, toUserName='filehelper')
            # ���ļ��Ļ�ҲҪ���ļ����ͻ�ȥ
            if old_msg["msg_type"] == "Picture" \
                    or old_msg["msg_type"] == "Recording" \
                    or old_msg["msg_type"] == "Video" \
                    or old_msg["msg_type"] == "Attachment":
                file = '@fil@%s' % (rev_tmp_dir + old_msg['msg_content'])
                itchat.send(msg=file, toUserName='filehelper')
                os.remove(rev_tmp_dir + old_msg['msg_content'])
            # ɾ���ֵ����Ϣ
            msg_dict.pop(old_msg_id)


if __name__ == '__main__':
    itchat.auto_login(hotReload=True,enableCmdQR=2)
    itchat.run()
