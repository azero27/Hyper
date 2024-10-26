from tkinter import *
import opendp.prelude as dp
dp.enable_features('contrib')

tk = Tk()
tk.geometry("550x400")

def Send1():
	data1 = float(entry1.get())
	noise1 = float(entry2.get())
	space = (dp.atom_domain(T=float), dp.absolute_distance(T=float))
	laplace_mechanism = space >> dp.m.then_laplace(scale=noise1)
	dp_value = laplace_mechanism(data1)
	label3.configure(text="노이즈 삽입 데이터 = " + str(dp_value))
    


label1 = Label(tk,text='데이터를 입력해주세요.',font=20)
label1.place(x=0, y=0)
label2 = Label(tk,text='노이즈 추가 정도를 입력해주세요.(0~1)',font=20)
label2.place(x=200, y=0)

entry1 = Entry(tk)
entry1.place(x=10, y=30)
entry2 = Entry(tk)
entry2.place(x=250, y= 30)

btn1 = Button(tk,text='입력',width=30,height=2,font=15, command=Send1)
btn1.place(x=60, y=60)


label3 = Label(tk,font=10)
label3.place(x=0, y=130)


tk.mainloop()
