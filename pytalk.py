import time, win32con, win32api, win32gui
import requests
from bs4 import BeautifulSoup
import schedule
import random



def get_quotaion():
    url = 'http://www.quotationspage.com/random.php'

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        quotation = soup.select_one('#content > dl > dt:nth-child(1) > a')
        author = soup.select_one('#content > dl > dd:nth-child(2) > b')
        quotation = quotation.get_text()
        author = author.get_text()
        #print(quotation)
        #print(author)
        return (quotation,author)

    else : 
        print(response.status_code)

# # 채팅방에 메시지 전송
def kakao_sendtext(chatroom_name, text):
    # # 핸들 _ 채팅방
    hwndMain = win32gui.FindWindow( None, chatroom_name)
    hwndEdit = win32gui.FindWindowEx( hwndMain, None, "RichEdit50W", None)
    # hwndListControl = win32gui.FindWindowEx( hwndMain, None, "EVA_VH_ListControl_Dblclk", None)

    win32api.SendMessage(hwndEdit, win32con.WM_SETTEXT, 0, text)
    SendReturn(hwndEdit)


# # 엔터
def SendReturn(hwnd):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    time.sleep(0.01)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)


# # 채팅방 열기
def open_chatroom(chatroom_name):
    # # 채팅방 목록 검색하는 Edit (채팅방이 열려있지 않아도 전송 가능하기 위하여)
    hwndkakao = win32gui.FindWindow(None, "카카오톡")
    hwndkakao_edit1 = win32gui.FindWindowEx( hwndkakao, None, "EVA_ChildWindow", None)
    hwndkakao_edit2_1 = win32gui.FindWindowEx( hwndkakao_edit1, None, "EVA_Window", None)
    hwndkakao_edit2_2 = win32gui.FindWindowEx( hwndkakao_edit1, hwndkakao_edit2_1, "EVA_Window", None)
    hwndkakao_edit3 = win32gui.FindWindowEx( hwndkakao_edit2_2, None, "Edit", None)

    # # Edit에 검색 _ 입력되어있는 텍스트가 있어도 덮어쓰기됨
    win32api.SendMessage(hwndkakao_edit3, win32con.WM_SETTEXT, 0, chatroom_name)
    time.sleep(1)   # 안정성 위해 필요
    SendReturn(hwndkakao_edit3)
    time.sleep(1)

# # 카톡창 이름, (활성화 상태의 열려있는 창)
#kakao_opentalk_name = '마마마'
#talk_room_list =['자민동생','3ㅇ']

def start():
    talk_room_list =['본동아이들']
    #talk_room_list =['마마마','앙기모']
    #talk_room_list =['자민동생','강문정']
    for i in talk_room_list:
        kakao_opentalk_name=i
        open_chatroom(kakao_opentalk_name)  # 채팅방 열기
        
        quotation_and_author=get_quotaion()
        quotation = quotation_and_author[0]
        author = quotation_and_author[1]
        kakao_sendtext(kakao_opentalk_name, '국모닝~ 오늘의 명언입니다!')
        time.sleep(1)
        kakao_sendtext(kakao_opentalk_name, quotation+'\n\n'+author)    # 메시지 전송
        time.sleep(1)
        kakao_sendtext(kakao_opentalk_name, '좋은하루되세요 앙기모디~')
        

def timer():
    now = time.localtime()
    result= "%02d:%02d" % (now.tm_hour, now.tm_min)
    return result.split(':')


if __name__ == "__main__":
    kakao_opentalk_name="김재구"
    open_chatroom(kakao_opentalk_name)  # 채팅방 열기
    kakao_sendtext(kakao_opentalk_name, "나데지 마세요 ㅋ")    # 메시지 전송
else:
    set_hour = '06'
    set_minute = str(random.randint(0,30))
    if len(set_minute)==1:
        set_minute='0'+set_minute
    print('Send message at {}:{}'.format(set_hour,set_minute))


    #실제 실행하게 하는 코드
    while True:
        now_time = timer()
        now_hour = now_time[0]
        now_minute = now_time[1]

        if now_hour==set_hour and now_minute==set_minute:
            start()

            set_hour = set_hour
            set_minute = str(random.randint(0,30))
            if len(set_minute)==1:
                set_minute='0'+set_minute
            print('Send message at {}:{}'.format(set_hour,set_minute))

            time.sleep(3600)

        time.sleep(1)
