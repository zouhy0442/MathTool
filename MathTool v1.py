# -*- coding: utf-8 -*-
"""
    Created on Mon Mar 14 09:37:16 2022
    Program 初中数学学习工具Version 1.0
    @author: Charlie Zou
"""
import tkinter as tk
import re
import sympy
import numpy as np
# 画布库，工具栏库，快捷键库
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

def Get_Window_Inf(root):
    """
        :确保窗口居中显示
    """
    label_plt = tk.Label(root, text="数形结合--函数/方程图像",
                          font=("微软雅黑", 12), fg="blue")
    label_plt.place(relx=0.65, rely=0)

    window_height = root.winfo_screenheight()
    window_width = root.winfo_screenwidth()

    win_height = int(0.8 * window_height)
    win_width = int(0.8* window_width)
    show_x = (window_width - win_width) / 2
    show_y = (window_height - win_height) / 2
    root.title(" "*(win_height//4)+"初中数学辅助学习工具")
    return win_width, win_height, show_x, show_y

def plot_Canvas(root):
    """
    该函数返回画布对象
    :root:parent window or frame
    """
    fig = Figure(dpi=100)
    axs = fig.add_subplot(1,1,1)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # shortcut key event handler
    def on_key_press(event):
        key_press_handler(event, canvas, toolbar)
    canvas.mpl_connect("key_press_event", on_key_press)

    return axs

def TrimInput():
    """
    该函数将entry输入的内容逐行转化为list并进行替换处理,并返回自变量字母
    """
    # 判断输入框是否为空
    if len(entry.get("1.0",tk.END).strip()) <2:
        tk.messagebox.showerror("提示", "没有输入值，请重新输入：")
        return 0
    else:
        entry2.config(state='normal')  #'normal'
        entry2.delete("1.0",tk.END)
        entry2.insert(tk.END, "您输入的原表达式：\n")
        expr_List = []
        expr_List = (entry.get("1.0",tk.END).replace(" ","")).split("\n")
        expr_List.pop()#列表最后一个元素是空删除它
        m=0
        for line in expr_List:
            line=line.replace('^','**')
            line=line.strip()
            line=re.sub(r'([\d)])([A-Za-z(])',r'\1*\2',line)
            expr_List[m]=line
            entry2.insert(tk.END, line+"\n")
            # print(sympy.latex(line))
            m+=1
        str_var=re.findall(r'[a-zA-Z]',",".join(expr_List))
        if len(set(str_var))>1:
            if len(entry3.get())==0:
                tk.messagebox.showerror("Quit", "没有输入自变量字母，请输入后重试：")
                return 0
            else:
                str_var=(entry3.get().strip().replace(","," ")).split(" ")
        
        entry2.config(state='disabled')  #'normal'
        return set(str_var), expr_List
    
"""
===========8个button的执行函数============================
"""
# 1化简展开
def expr_simpl():
    global frame1
    Mod_Entry=TrimInput()
    if Mod_Entry==0: return 
    var_x=Mod_Entry[0]
    expr_List=Mod_Entry[1]
    var_x=sympy.symbols(",".join(var_x))
    # 删除原画布，重新创建画布
    if frame1!=None:
        frame1.destroy()
        frame1 = None
    frame1 = tk.Frame(MainWindow, bg="#c0c0c0")
    frame1.place(relx=0.397, rely=0.05, relwidth=0.60, relheight=0.89)
    axs = plot_Canvas(frame1)
    axs.set_xlim(0,10)
    axs.set_ylim(0,10)
    
    entry2.config(state='normal')  #'normal'
    m=0
    for n, str in enumerate(expr_List):
        str=sympy.sympify(str)
        result=sympy.simplify(str)
        entry2.insert(tk.END, "\n表达式化简：\n %s \n"  % result)
        strltx=sympy.latex(str)
        result=sympy.latex(result)
        axs.text(1,9-n-m,r"%d: $%s = %s$" % (n, strltx, result), fontsize=20, 
                 family="serif")
        m+=1
        result=sympy.expand(str)
        entry2.insert(tk.END, "表达式展开：\n %s \n"  % result)
        result=sympy.latex(result)
        axs.text(1,9-n-m,r"%d: $%s = %s$" % (n, strltx, result), fontsize=20, 
                 family="serif")
    entry2.config(state='disabled')  #'normal'

# 2因式分解
def expr_factorize():
    global frame1
    Mod_Entry=TrimInput()
    if Mod_Entry==0: return 
    var_x=Mod_Entry[0]
    expr_List=Mod_Entry[1]
    var_x=sympy.symbols(",".join(var_x))
    # 删除原画布，重新创建画布
    if frame1!=None:
        frame1.destroy()
        frame1 = None
    frame1 = tk.Frame(MainWindow, bg="#c0c0c0")
    frame1.place(relx=0.397, rely=0.05, relwidth=0.60, relheight=0.89)
    axs = plot_Canvas(frame1)
    axs.set_xlim(0,10)
    axs.set_ylim(0,10)
    
    entry2.config(state='normal')  #'normal'
    for n, str in enumerate(expr_List):
        str=sympy.sympify(str)
        result=sympy.factor(str)
        entry2.insert(tk.END, "\n因式分解：\n %s \n"  % result)
        str=sympy.latex(str)
        result=sympy.latex(result)
        axs.text(1,9-n,r"%d: $%s = %s$" % (n, str, result), fontsize=20, 
                 family="serif")
    entry2.config(state='disabled')  #'normal'

# 3分式通分合并等功能
def expr_apart():
    global frame1
    Mod_Entry=TrimInput()
    if Mod_Entry==0: return 
    var_x=Mod_Entry[0]
    expr_List=Mod_Entry[1]
    var_x=sympy.symbols(",".join(var_x))
    # 删除原画布，重新创建画布
    if frame1!=None:
        frame1.destroy()
        frame1 = None
    frame1 = tk.Frame(MainWindow, bg="#c0c0c0")
    frame1.place(relx=0.397, rely=0.05, relwidth=0.60, relheight=0.89)
    axs = plot_Canvas(frame1)
    axs.set_xlim(0,10)
    axs.set_ylim(0,10)

    entry2.config(state='normal')  #'normal'
    m=0
    for n, str in enumerate(expr_List):
        str=sympy.sympify(str)
        strltx=sympy.latex(str)
        try:
            result=sympy.apart(str)
            entry2.insert(tk.END, "\n分式分解：\n %s \n"  % result)
            result=sympy.latex(result)
            axs.text(1,9-n-m,r"%d: $%s = %s$" % (n, strltx, result), fontsize=20, 
                     family="serif")
            m+=1
        except:
            tk.messagebox.showerror("Quit", "无法分解")
        result=sympy.together(str)
        entry2.insert(tk.END, "\n分式通分：\n %s \n"  % result)
        result=sympy.latex(result)
        axs.text(1,9-n-m,r"%d: $%s = %s$" % (n, strltx, result), fontsize=20, 
                 family="serif")
        m+=1
        result=sympy.cancel(str)
        entry2.insert(tk.END, "\n分式约分：\n %s \n"  % result)
        result=sympy.latex(result)
        axs.text(1,9-n-m,r"%d: $%s = %s$" % (n, strltx, result), fontsize=20, 
                 family="serif")
    entry2.config(state='disabled')  #'normal'
    
# 4素数相关
def prime_check():
    entry2.config(state='normal')  #'normal'
    entry2.delete("1.0",tk.END)
    if len(entry.get("1.0",tk.END).strip()) <2:
        tk.messagebox.showerror("提示", "没有输入值，请重新输入：")
    else:
        try:
            
            input_data=entry.get("1.0",tk.END)
            num=re.findall(r'\d+',input_data)
            for x in num:
                input_num=int(x)
                if sympy.ntheory.generate.isprime(input_num):
                    entry2.insert(tk.END, input_num)
                    entry2.insert(tk.END, "   是素数\n")
                else:
                    entry2.insert(tk.END, input_num)
                    entry2.insert(tk.END, "的素因子：")
                    entry2.insert(tk.END, sympy.ntheory.factorint(input_num))
                    entry2.insert(tk.END, "\n")
                
                entry2.insert(tk.END, str(input_num)+ "后面一个素数：")
                entry2.insert(tk.END, sympy.ntheory.generate.nextprime(input_num))
                entry2.insert(tk.END, "   前一个素数：")
                entry2.insert(tk.END, sympy.ntheory.generate.prevprime(input_num))
                entry2.insert(tk.END, "  \n")
            if len(num)==2:
                small=int(num[0]) if int(num[0])<int(num[1]) else int(num[1])
                large=int(num[0]) if int(num[0])>int(num[1]) else int(num[1])
                entry2.insert(tk.END, "\n输入框中两个数之间的素数有：\n")
                entry2.insert(tk.END, list(sympy.sieve.primerange(small, large)))
        except:
            tk.messagebox.showerror("Quit", "数据输入错误，请重新输入")
    entry2.config(state='disabled')  #'normal'

# 5解方程的函数
def solve_eq():
    from sympy import S
    global frame1
    Mod_Entry=TrimInput()
    if Mod_Entry==0: return 
    var_x=Mod_Entry[0]
    expr_List=Mod_Entry[1]
    
    # 删除原画布，重新创建画布
    if frame1!=None:
        frame1.destroy()
        frame1 = None
    frame1 = tk.Frame(MainWindow, bg="#c0c0c0")
    frame1.place(relx=0.397, rely=0.05, relwidth=0.60, relheight=0.89)
    axs = plot_Canvas(frame1)
    axs.set_xlim(0,10)
    axs.set_ylim(0,10)
    
    if len(var_x)==1:
        var_x=sympy.symbols(",".join(var_x))
        entry2.config(state='normal')  #'normal'
        entry2.insert(tk.END, "\n结果如下：\n")
        for n, str in enumerate(expr_List):
            if str.find('=')>0 : 
                str=str.split('=')
                str=str[0]+'-('+str[1]+')'
            str=sympy.sympify(str)
            Answers=sympy.solveset(str,var_x, domain=S.Reals)
            str=sympy.latex(str)
            try:
                if len(Answers)>0:
                    latexsol=''
                    for Sol in Answers:
                        entry2.insert(tk.END, Sol)
                        entry2.insert(tk.END, ';  ')
                        latexsol=latexsol+sympy.latex(Sol)+";  "
                    axs.text(0.2,9-n,r"EQ %d: $%s=0 >> root: %s$" % (n, str,latexsol), 
                             fontsize=18, family="serif")
                    entry2.insert(tk.END, '\n')
                else:
                    entry2.insert(tk.END, "方程无实数解\n")
            except:
                entry2.insert(tk.END, "方程无实数解\n")            
        entry2.config(state='disabled')  #'normal'
      
    else:# 作为方程组处理
        var_x=sympy.symbols(",".join(var_x))
        entry2.config(state='normal')  #'normal'
        entry2.insert(tk.END, "\n结果如下：\n")
        eq_list=[]
        for str in expr_List:
            if str.find('=')>0 : 
                str=str.split('=')
                str=str[0]+'-('+str[1]+')'
            str=sympy.sympify(str)
            eq_list.append(str)
        Answers=sympy.solve(eq_list ,var_x,dict=True)
        if len(Answers)>0:
            for Sol in Answers:
                entry2.insert(tk.END, Sol)
                entry2.insert(tk.END, ';  ')
            entry2.insert(tk.END, '\n')
        else:
            entry2.insert(tk.END, "方程无解\n")
        entry2.config(state='disabled')  #'normal'
    return 
    

# 6绘图的函数
def my_plot():
    global frame1
    Mod_Entry=TrimInput()
    if Mod_Entry==0: return 
    var_x=Mod_Entry[0]
    expr_List=Mod_Entry[1]
    
    # 删除原画布，重新创建画布
    if frame1!=None:
        frame1.destroy()
        frame1 = None
    frame1 = tk.Frame(MainWindow, bg="#c0c0c0")
    frame1.place(relx=0.397, rely=0.05, relwidth=0.60, relheight=0.89)
    axs = plot_Canvas(frame1)
    
    if len(var_x)==1:
        var_x=sympy.symbols(",".join(var_x))
        LowX=float(entry4.get()) if len(entry4.get())>0 else -10
        HighX=float(entry5.get()) if len(entry5.get())>0 else 10
        x_value=np.linspace(LowX, HighX, 200)
        for str in expr_List:
            str=sympy.sympify(str)
            y=sympy.lambdify(var_x,str,'numpy')
            axs.plot(x_value, y(x_value))
        axs.axhline(0,color='r')
        axs.axvline(0,color='r')
        axs.grid(True)
        axs.legend(labels=expr_List)
        
    elif len(var_x)==2:
        tk.messagebox.showinfo("稍等", "功能开发中.")
        
    else:
        tk.messagebox.showinfo("Warning", "变量数>2，当前版本仅可处理单变量函数画图.")
    return 

# 7清除的功能函数
def clear():
    global frame1
    # entry.delete("1.0",tk.END)
    entry2.config(state='normal')  #'normal'
    entry2.delete("1.0",tk.END)

    if frame1==None:
        tk.messagebox.showerror("提示", "已经没有画布，无法清除画布。")
    else:
        frame1.destroy()
        frame1 = None

"""
===========按钮及输入框界面布局============================
"""
MainWindow = tk.Tk()
MainWindow.geometry("%dx%d+%d+%d" % (Get_Window_Inf(MainWindow)))

# 图像区Frame
frame1 = tk.Frame(MainWindow, bg="#c0c0c0")
frame1.place(relx=0.397, rely=0.05, relwidth=0.60, relheight=0.89)

# 命令区Frame
frame2 = tk.LabelFrame(MainWindow, text="功 能 及 结 果 区", 
                       font=("微软雅黑", 12), fg="blue", bg="#c0c0c0")
frame2.place(relx=0.003, rely=0.01, relwidth=0.39, relheight=0.93)

#  标签for input
label1 = tk.Label(frame2, text="请输入表达式或方程/方程组：",
               font=("微软雅黑", 12), fg="blue")
label1.place(relx=0.02, rely=0.03)

# entry for 输入框
entry = tk.Text(frame2, height=4, font=('StSong', 14))
entry.place(relx=0.02, rely=0.09, relwidth=0.92)

label3 = tk.Label(frame2, text="当表达式中有多个字母时，请输入自变量，用空格分开：",
               font=("微软雅黑", 9), bg="#c0c0c0")
label3.place(relx=0.02, rely=0.24)

entry3 = tk.Entry(frame2,  font=('Calibri', 12), fg='blue')
entry3.place(relx=0.65, rely=0.24, relwidth=0.29)

#  标签for 结果
label2 = tk.Label(frame2, text="结果如下：",
               font=("微软雅黑", 12), fg="blue")
label2.place(relx=0.02, rely=0.31)

entry2 = tk.Text(frame2,  height=12, font=('StSong', 12), fg='green')
entry2.place(relx=0.02, rely=0.36, relwidth=0.92)
entry2.config(state='disabled')  #'normal'

label4 = tk.Label(frame2, text="X轴坐标范围--请在左侧框输入下限，右侧框输入上限：",
               font=("微软雅黑", 9), bg="#c0c0c0")
label4.place(relx=0.02, rely=0.72)

entry4 = tk.Entry(frame2,  font=('Calibri', 12), fg='green')
entry4.place(relx=0.64, rely=0.72, relwidth=0.14)
entry5 = tk.Entry(frame2,  font=('Calibri', 12), fg='green')
entry5.place(relx=0.8, rely=0.72, relwidth=0.14)

btn_1 = tk.Button(frame2, text="化简/展开", font=("微软雅黑", 12), 
                  width=9, command=expr_simpl)
btn_1.place(relx=0.05, rely=0.83)

btn_2 = tk.Button(frame2, text="因式分解", font=("微软雅黑", 12), 
                  width=9, command=expr_factorize)
btn_2.place(relx=0.27, rely=0.83)

btn_3 = tk.Button(frame2, text="分式化简", font=("微软雅黑", 12), 
                  width=9, command=expr_apart)
btn_3.place(relx=0.49, rely=0.83)

btn_4 = tk.Button(frame2, text="素数判断", font=("微软雅黑", 12), 
                  width=9, command=prime_check)
btn_4.place(relx=0.71, rely=0.83)

btn_5 = tk.Button(frame2, text="方程求解", font=("微软雅黑", 12), 
                  width=9, command=solve_eq)
btn_5.place(relx=0.05, rely=0.9)

btn_6 = tk.Button(frame2, text="函数图像", font=("微软雅黑", 12), 
                  width=9, command=my_plot)
btn_6.place(relx=0.27, rely=0.9)

btn_7 = tk.Button(frame2, text="清 除", font=("微软雅黑", 12), 
                  width=9, command=clear)
btn_7.place(relx=0.49, rely=0.9)

btn_8= tk.Button(frame2, text="退 出", font=('微软雅黑', 12), 
                 width=9, command=MainWindow.destroy)
btn_8.place(relx=0.71, rely=0.9)

MainWindow.mainloop()