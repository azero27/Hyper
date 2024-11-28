from tkinter import *
import opendp.prelude as dp
dp.enable_features('contrib')
import requests
import socket

tk = Tk()
tk.geometry("550x400")

def submit_data():
    id1 = "user1"
    ip1 = socket.gethostbyname(socket.gethostname())
    # 로컬 IP 주소 가져오기
    
    data1 = entry1.get()
    noise1 = entry2.get()
    space = (dp.atom_domain(T=float), dp.absolute_distance(T=float))
    laplace_mechanism = space >> dp.m.then_laplace(scale=noise1)
    dp_value = laplace_mechanism(data1)
    label3.configure(text="노이즈 삽입 데이터 = " + str(dp_value))
    
    # REST API로 데이터 전송
    url = 'http://localhost:3000/submitData'
    payload = {'id': id1, 'ip': ip1, 'data': dp_value}
    response = requests.post(url, json=payload)
    result = response.json()

    # 결과 표시
    if result['success']:
        label4.config(text="성공")
    else:
        label4.config(text="실패")


label1 = Label(tk,text='데이터를 입력해주세요.',font=20)
label1.place(x=0, y=0)
label2 = Label(tk,text='노이즈 추가 정도를 입력해주세요.(0~1)',font=20)
label2.place(x=200, y=0)

entry1 = Entry(tk)
entry1.place(x=10, y=30)
entry2 = Entry(tk)
entry2.place(x=250, y= 30)

btn1 = Button(tk,text='입력',width=30,height=2,font=15, command=submit_data)
btn1.place(x=60, y=60)


label3 = Label(tk,font=10)
label3.place(x=0, y=130)

label4 = Label(tk,font=10)
label4.place(x=0, y=150)

tk.mainloop()
