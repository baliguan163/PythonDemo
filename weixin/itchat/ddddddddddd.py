# -*-encoding:utf-8-*-

import itchat
from itchat.content import TEXT, SHARING, PICTURE, VIDEO
from wxpy.api.chats import groups


@itchat.msg_register([TEXT, SHARING], isGroupChat=True)
def group_reply_text(msg):
    # ��ȡȺ�ĵ�ID������Ϣ�������ĸ�Ⱥ��
    # ������԰�source��ӡ������ȷ�����ĸ�Ⱥ�ĺ�
    # ��Ⱥ�ĵ�ID�����Ƽ���groups
    source = msg['FromUserName']
    print('-----------------group_reply_text--------------------')
    print(source)
    # �����ı���Ϣ
    if msg['Type'] == TEXT:
        # ��Ϣ��������Ҫͬ����Ϣ��Ⱥ��
        if groups.has_key(source):
            # ת����������Ҫͬ����Ϣ��Ⱥ��
            for item in groups.keys():
                if not item == source:
                    # groups[source]: ��Ϣ�������ĸ�Ⱥ��
                    # msg['ActualNickName']: �����ߵ�����
                    # msg['Content']: �ı���Ϣ����
                    # item: ��Ҫ��ת����Ⱥ��ID
                    itchat.send('%s: %s\n%s' % (groups[source], msg['ActualNickName'], msg['Content']), item)
    # ���������Ϣ
    elif msg['Type'] == SHARING:
        if groups.has_key(source):
            for item in groups.keys():
                if not item == source:
                    # msg['Text']: ����ı���
                    # msg['Url']: ���������
                    itchat.send('%s: %s\n%s\n%s' % (groups[source], msg['ActualNickName'], msg['Text'], msg['Url']), item)


# ����ͼƬ����Ƶ����Ϣ
@itchat.msg_register([PICTURE, VIDEO], isGroupChat=True)
def group_reply_media(msg):
    source = msg['FromUserName']
    # ����ͼƬ����Ƶ
    msg['Text'](msg['FileName'])
    # if groups .has_key(source):
    #     for item in groups.keys():
    #         if not item == source:
    #             # ��ͼƬ����Ƶ���͵�������Ҫͬ����Ϣ��Ⱥ��
    #             itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']), item)


# ��auto_login()�����ṩһ��True����hotReload=True
# ���ɱ�����½״̬
# ��ʹ����رգ�һ��ʱ�������¿���Ҳ���Բ�������ɨ��
itchat.auto_login(True)
itchat.run()
