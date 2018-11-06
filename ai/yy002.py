# _*_ coding:UTF-8 _*_
# win32虽然也可控制键盘，但不如使用PyUserInput的方便。需要注意在windows和mac下接口参数可能有所不同。
from pymouse import PyMouse
from pykeyboard import PyKeyboard
m = PyMouse()
k = PyKeyboard()

x_dim, y_dim = m.screen_size()
# 鼠标点击
m.click(x_dim/2, y_dim/2, 1)
# 键盘输入
k.type_string('Hello, World!')

# 按住一个键
k.press_key('H')
# 松开一个键
k.release_key('H')
# 按住并松开，tap一个键
k.tap_key('e')
# tap支持重复的间歇点击键
k.tap_key('l',n=2,interval=5)
# 发送判断文字
k.type_string('123456')

#创建组合键
k.press_key(k.alt_key)
k.tap_key(k.tab_key)
k.release_key(k.alt_key)
# 特殊功能键
k.tap_key(k.function_keys[5]) # Tap F5
k.tap_key(k.numpad_keys['Home']) # Tap 'Home' on the numpad
k.tap_key(k.numpad_keys[5], n=3) # Tap 5 on the numpad, thrice

# Mac系统
k.press_keys(['Command','shift','3'])
# Windows系统
k.press_keys([k.windows_l_key,'d'])

# 其中的PyMouseEvent和PyKeyboardEvent还可用于监听鼠标和键盘事件的输入
