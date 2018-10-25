# _*_ coding: utf-8 _*_
# @Time : 2017/5/10 22:57
# @Author : 0x3E6
# @File : android_qq_praise.py
import os
import re


class QQPraise():
    def __init__(self):
        self.screen_center_x = 0
        self.screen_center_y = 0
        self.fd = None
        self.contact_UI_content = None
        self.profile_crad_content = None
        self.pattern = None
        self.points = None
        self.x = 0
        self.y = 0
        self.num = 0

    def entry_point(self):
        self.prepare()
        i = 0
        while 1:
            type = self.find_type_of_selected_widget()
            if type == "friend_widget":
                self.parse_coordinate()
                os.system("adb shell input tap %s %s" % (self.x, self.y))
                self.praise_and_return()
            elif type == "group_widget":
                self.expand_group()
            else:
                i += 1
                if i == 10:
                    break
            if self.cursor_out_of_screen():
                os.system("adb shell input keyevent KEYCODE_PAGE_DOWN")
            os.system("adb shell input keyevent KEYCODE_DPAD_DOWN")

    def prepare(self):
        # 先切换到QQ主界面的中间联系人列表界面
        self.load_layout_xml("contacts_list.xml", 1)
        self.pattern = "bounds=\"\[(\d{1,4}),(\d{1,4})\]\[(\d{1,4}),(\d{1,4})\][^>]*><node[^>]*text=\"联系人\" resource-id=\"com\.tencent\.mobileqq:id/name\""
        contact_widget = self.parse_UI(self.contact_UI_content)
        if contact_widget:
            os.system("adb shell input tap %s %s" % (self.x, self.y))
        # 选择好友列表
        self.load_layout_xml("contacts_list.xml", 1)
        points = re.search("<node[^>]*text=\"好友\"[^>]*bounds=\"\[(\d{1,4}),(\d{1,4})\]\[(\d{1,4}),(\d{1,4})\]",
                           self.contact_UI_content).groups()

        x = int(points[0]) + (int(points[2]) - int(points[0])) / 2
        y = int(points[1]) + (int(points[3]) - int(points[1])) / 2
        os.system("adb shell input tap %s %s" % (x, y))
        # 折叠好友列表
        os.system("adb shell input tap %s %s" % (self.x, self.y))
        # 获取屏幕分辨率计算屏幕中心
        f = os.popen("adb shell wm size")
        screen_width, screen_height = re.search("(\d{3,4})x(\d{3,4})", f.read()).groups()
        center = (int(screen_width) / 2, int(screen_height) / 2)
        self.screen_center_x = center[0]
        self.screen_center_y = center[1]
        # 向上划一下，将“好友、群、...”那一行移动到最上面
        os.system("adb shell input swipe %s %s %s %s" % (center[0], center[1], center[0], 0))
        # 发送KEYCODE_MOVE_HOME将光标定位到“特别关心”分组
        os.system("for /L %%i in (1,1,2) do adb shell input keyevent KEYCODE_MOVE_HOME")

    def load_layout_xml(self, xml_name, option):
        # os.system("adb shell uiautomator dump /storage/sdcard0/friend_profile_card.xml")
        os.system("adb shell uiautomator dump /storage/sdcard0/%s" % xml_name)
        os.system("adb pull /storage/sdcard0/%s ./%s" % (xml_name, xml_name))
        self.fd = open(xml_name, "r")
        if option == 1:
            self.contact_UI_content = self.fd.read()
        elif option == 2:
            self.profile_crad_content = self.fd.read()
        self.fd.close()

    def parse_UI(self, content):
        result = re.search(self.pattern, content)
        if result:
            if len(result.groups()) == 5:
                self.points = result.groups()[1:]
                return result.groups()[0]
            elif len(result.groups()) == 4:
                self.points = result.groups()
                self.parse_coordinate()
                return True
            elif len(result.groups()) == 1:
                return result.groups()[0]
        else:
            return False

    def parse_coordinate(self):
        min_x = int(self.points[0])
        min_y = int(self.points[1])
        max_x = int(self.points[2])
        max_y = int(self.points[3])
        self.x = min_x + (max_x - min_x) / 2
        self.y = min_y + (max_y - min_y) / 2

    def find_type_of_selected_widget(self):
        self.load_layout_xml("contacts_list.xml", 1)
        self.pattern = "<node[^>]*(id/group|LinearLayout)[^>]*selected=\"true\"[^>]*bounds=\"\[(\d{1,4}),(\d{1,4})\]\[(\d{1,4}),(\d{1,4})\]\"[^>]*>"
        contact_widget = self.parse_UI(self.contact_UI_content)
        if contact_widget:
            if "LinearLayout" == contact_widget:
                # print "好友控件", "坐标", type.groups()[1:]
                return "friend_widget"
            elif "id/group" == contact_widget:
                # print "分组控件", "坐标", type.groups()[1:]
                return "group_widget"
        else:
            return None

    def expand_group(self):
        coordinate = (int(self.points[0]), int(self.points[1]), int(self.points[2]), int(self.points[3]))
        self.pattern = "\[%s,%s\]\[%s,%s\]\"><node[^>]*checked=\"([^\"]*)\"" % coordinate
        checked = self.parse_UI(self.contact_UI_content)
        if checked == 'false':
            self.parse_coordinate()
            os.system("adb shell input tap %s %s" % (self.x, self.y))

    def praise_and_return(self):
        self.num += 1
        # 若有的好友资料卡中赞的位置被厘米秀挡住，需要取消下面这一行的注释，但这并不能解决所有问题
        os.system("adb shell input swipe %s %s %s %s" % (
        self.screen_center_x, self.screen_center_y, self.screen_center_x, self.screen_center_y * 2 / 3))
        self.load_layout_xml("friend_profile_card.xml", 2)
        # 找点赞位置
        self.pattern = "<node [^<]*点击可赞[^>]* bounds=\"\[(\d{1,4}),(\d{1,4})\]\[(\d{1,4}),(\d{1,4})\].*"
        result = self.parse_UI(self.profile_crad_content)
        if result:
            os.system("FOR /L %%v IN (1,1,10) DO adb shell input tap %s %s" % (self.x, self.y))
            os.system("adb shell input keyevent KEYCODE_BACK && adb shell input keyevent KEYCODE_MOVE_HOME")

    def cursor_out_of_screen(self):
        self.pattern = "<node[^>]*selected=\"true\"[^>]*>[^<]*(</node>){6}"
        is_out = re.search(self.pattern, self.contact_UI_content)
        if is_out:
            return True
        else:
            return False


def main():
    praiser = QQPraise()
    praiser.entry_point()

if __name__ == "__main__":
    main()
