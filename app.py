import os
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import pandas as pd
import numpy as np

class model_data:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.configure(bg="gray")
        self.root.title("data_app")
        # file number
        self.file1 = 1
        self.file2 = 2
        self.index_list = []
        self.col_1 = []
        self.col_2 = []
        self.choosed_columns = []
        self.col_1_ch = []
        self.col_2_ch = []
        self.info()
    """
    information
    """
    def info(self):
        ### 大枠
        frame1 = tk.Frame(master=self.root, relief="groove", bd=5, width=320, height=520)
        frame1.pack(side="left")
        frame1.pack_propagate(0)
        frame2 = tk.Frame(master=self.root, relief="groove", bd=5, width=320, height=520)
        frame2.pack(side="left")
        frame2.pack_propagate(0)

        # file1_path
        static1 = tk.Label(master=frame1)
        static1.configure(text='file1 path')
        static1.pack(side="top", pady=10)
        self.file1_path = tk.StringVar()
        form1 = tk.Entry(master=frame1, width=30)
        form1.configure(textvariable=self.file1_path)
        form1.pack(side="top")
        # ボタン (fileselect)
        button1 = tk.Button(master=frame1, text="select file", width=20, fg="blue", command=lambda : self.fileselect(self.file1))
        button1.pack(side="top", pady=20)

        # file2_path
        static2 = tk.Label(master=frame2)
        static2.configure(text='file2 path')
        static2.pack(side="top", pady=10)
        self.file2_path = tk.StringVar()
        form2 = tk.Entry(master=frame2, width=30)
        form2.configure(textvariable=self.file2_path)
        form2.pack(side="top")
        # ボタン (fileselect)
        button2 = tk.Button(master=frame2, text="select file", width=20, fg="blue", command=lambda : self.fileselect(self.file2))
        button2.pack(side="top", pady=20)

        ## file1
        static3 = tk.Label(master=frame1)
        static3.configure(text="column names")
        static3.pack(side="top", pady=5)
        frame3 = tk.Frame(master=frame1, relief="groove", bd=2)
        frame3.pack(side="top")
        column1 = tk.StringVar(value=[])
        self.columns_list1 = tk.Listbox(master=frame1,
                                  listvariable=column1,
                                  width=30,
                                  height=15,
                                  selectmode='multiple')
        # スクロールバー
        scrollbar1 = tk.Scrollbar(frame1, command=self.columns_list1.yview)
        self.columns_list1.yscrollcommand = scrollbar1.set
        scrollbar1.pack(fill=tk.BOTH, side=tk.RIGHT)
        self.columns_list1.pack()
        # ボタン (OK)
        self.btn_ok_1 = tk.Button(master=frame1, text="OK", width=5)
        self.btn_ok_1.pack(side="top", pady=20, ipadx=20, ipady=5)
        self.btn_ok_1.configure(command=lambda : self.OK(self.file1))

        ## file2
        static4 = tk.Label(master=frame2)
        static4.configure(text="column names")
        static4.pack(side="top", pady=5)
        frame4 = tk.Frame(master=frame2, relief="groove", bd=2)
        frame4.pack(side="top")
        column2 = tk.StringVar(value=[])
        self.columns_list2 = tk.Listbox(master=frame2,
                                  listvariable=column2,
                                  width=30,
                                  height=15,
                                  selectmode='multiple')
        # スクロールバー
        scrollbar2 = tk.Scrollbar(frame2, command=self.columns_list2.yview)
        self.columns_list2.yscrollcommand = scrollbar2.set
        scrollbar2.pack(fill=tk.BOTH, side=tk.RIGHT)
        self.columns_list2.pack()
        # ボタン (OK)
        self.btn_ok_2 = tk.Button(master=frame2, text="OK", width=5)
        self.btn_ok_2.pack(side="top", pady=20, ipadx=20, ipady=5)
        self.btn_ok_2.configure(command=lambda : self.OK(self.file2))


        ## ボタン
        # join
        self.btn_join = tk.Button(master=self.root, text="join", width=10)
        self.btn_join.pack(side="top", pady=20)
        # concat
        self.btn_concat = tk.Button(master=self.root, text="concat", width=10)
        self.btn_concat.pack(side="top", pady=20)
        # query
        self.btn_query = tk.Button(master=self.root, text="query", width=10)
        self.btn_query.pack(side="top", pady=20)
        # merge
        self.btn_merge = tk.Button(master=self.root, text="merge", width=10)
        self.btn_merge.pack(side="top", pady=20)
        # describe
        self.btn_describe = tk.Button(master=self.root, text="describe", width=10)
        self.btn_describe.pack(side="top", pady=20)
        # reset
        self.btn_reset = tk.Button(master=self.root, text="reset", width=10)
        self.btn_reset.pack(side="bottom", pady=20)
        self.btn_reset.configure(command=lambda : self.reset())
        # save
        self.btn_save = tk.Button(master=self.root, text="save", width=10)
        self.btn_save.pack(side="bottom", pady=20)

    """
    DataSet
    """
    def fileselect(self, num):
        fTyp = [("","*")]
        fDir = "/Users/tanakaroberuto/Desktop"
        self.path = tk.filedialog.askopenfilename(filetypes=fTyp, initialdir=fDir)
        # extension 拡張子 （正規表現）
        ex = self.path.split(".", 1)[1]
        if ex == "csv" or ex == "xlsx":
            if num == 1:
                self.file1_path.set(self.path)
                self.pandas(ex, num)
            elif num == 2:
                self.file2_path.set(self.path)
                self.pandas(ex, num)
        else:
            tk.messagebox.showinfo("Error", 'Choose csv or excel file!')

    def pandas(self, ex, num):
        global df1, df2
        if ex == "csv":
            if num == 1:
                df1 = pd.read_csv(self.path)
                df1 = df1.set_index(list(df1.columns)[0])
                print(df1)
                self.view(df1, num)
            else:
                df2 = pd.read_csv(self.path)
                df2 = df2.set_index(list(df2.columns)[0])
                self.view(df2, num)

        elif ex == "xlsx":
            if num == 1:
                df1 = pd.read_excel(self.path)
                self.view(df1, num)
            else:
                df2 = pd.read_excel(self.path)
                self.view(df2, num)


    def view(self, df, num):
        for column in df.columns:
            self.choosed_columns.append(column)
        for column, col in zip(enumerate(df.columns), df.columns):
            if num == 1:
                self.columns_list1.insert(tk.END, column)
                self.col_1.append(col)
            elif num == 2:
                self.columns_list2.insert(tk.END, column)
                self.col_2.append(col)

    def OK(self, num):
        if num == 1:
            choosed_index1 = self.columns_list1.curselection()
            if len(choosed_index1) != 0:
                for index in choosed_index1:
                    self.index_list.append(df1.iloc[:, [index]])
                    self.col_1_ch.append(self.col_1[index])
                    self.choosed_columns.append(self.col_1_ch)
                self.df1 = df1.iloc[:, list(choosed_index1)]
        elif num == 2:
            choosed_index2 = self.columns_list2.curselection()
            if len(choosed_index2) != 0:
                for index in choosed_index2:
                    self.index_list.append(df2.iloc[:, [index]])
                    self.col_2_ch.append(self.col_2[index])
                    self.choosed_columns.append(self.col_2_ch)
                self.df2 = df2.iloc[:, list(choosed_index2)]

        print(self.index_list)
        if len(self.index_list) != 0:
            self.btn_join.configure(command=lambda : self.Join(self.index_list))
            self.btn_concat.configure(command=lambda : self.Concat_win(self.index_list))
            self.btn_query.configure(command=lambda : self.Query_win(self.index_list))
            self.btn_merge.configure(command=lambda : self.Merge_win())
            self.btn_describe.configure(command=lambda : self.describe())

    """
    MakeDataframe
    """
    # join
    def Join(self, list):
        self.df = pd.concat(list, axis=1)
        print(self.df)
        self.btn_save.configure(command=lambda : self.Save_win())

    # concat
    def Concat_win(self, list):
        if len(self.col_1_ch) == 0:
            tk.messagebox.showinfo("Error", 'Choose both file!')
        elif len(self.col_2_ch) == 0:
            tk.messagebox.showinfo("Error", 'Choose both file!')
        else:
            self.New_win(self.root, "concat")
            Static = tk.Label(master=self.new_win, text="set_index")
            Static.pack(side="top")
            self.key = tk.Entry(master=self.new_win, width=10)
            self.key.pack(side="top")
            self.var_join = tk.IntVar()
            self.var_join.set(0)
            chk_rank = tk.Radiobutton(master=self.new_win, value=0, variable=self.var_join, text="inner", width=10)
            chk_rank.pack(side="top")
            chk_max = tk.Radiobutton(master=self.new_win, value=1, variable=self.var_join, text="outer", width=10)
            chk_max.pack(side="top")
            self.var_axis = tk.IntVar()
            self.var_axis.set(True)
            self.chk_axis = tk.Checkbutton(master=self.new_win, text="axis", width=10, variable=self.var_axis)
            self.chk_axis.pack(side="top", pady=10)

            self.btn_Done(self.new_win)
            self.btn_done.configure(command=lambda : self.Concat())

    def Concat(self):
        join_list = ["inner", "outer"]
        self.df = pd.concat([self.df1, self.df2], axis=self.var_axis.get(), join=join_list[self.var_join.get()], sort=True)
        if len(self.key.get()) != 0:
            if self.key.get() in self.choosed_columns:
                self.df = self.df.set_index(self.key.get())
            else:
                tk.messagebox.showinfo("Error", 'Fill in exists column name!')
        print(self.df)
        self.new_win.destroy()
        self.btn_save.configure(command=lambda : self.Save_win())

    # query
    def Query_win(self, list):
        self.New_win(self.root, "query")

        self.var = tk.IntVar()
        self.var.set(0)

        chk_rank = tk.Radiobutton(master=self.new_win, value=0, variable=self.var, text="rank", width=10)
        chk_rank.pack(side="top")
        chk_max = tk.Radiobutton(master=self.new_win, value=1, variable=self.var, text="max", width=10)
        chk_max.pack(side="top")
        chk_min = tk.Radiobutton(master=self.new_win, value=2, variable=self.var, text="min", width=10)
        chk_min.pack(side="top")
        chk_mean = tk.Radiobutton(master=self.new_win, value=3, variable=self.var, text="mean", width=10)
        chk_mean.pack(side="top")
        chk_count = tk.Radiobutton(master=self.new_win, value=4, variable=self.var, text="count", width=10)
        chk_count.pack(side="top")

        self.answer_form = tk.Entry(master=self.new_win, width=30)
        self.answer_form.pack(side="top", pady=10)

        self.btn_Done(self.new_win)
        self.btn_done.configure(command=lambda : self.query(list))

    def query(self, list):
        if self.var.get() == 0:
            self.Rank_win(list)

        else:
            if len(list) == 1:
                df = pd.concat(list, axis=1)
                if self.var.get() == 1:
                    self.answer_form.delete(0, tk.END)
                    self.answer_form.insert(tk.END, "max: " + str(np.max(df.iloc[:, 0])))
                elif self.var.get() == 2:
                    self.answer_form.delete(0, tk.END)
                    self.answer_form.insert(tk.END, "min: " + str(np.min(df.iloc[:, 0])))
                elif self.var.get() == 3:
                    self.answer_form.delete(0, tk.END)
                    self.answer_form.insert(tk.END, "mean: " + str(np.mean(df.iloc[:, 0])))
                else:
                    self.answer_form.delete(0, tk.END)
                    self.answer_form.insert(tk.END, "count: " + str(len(df.iloc[:, 0])))
            else:
                tk.messagebox.showinfo("Error", 'If you want to do max, min, mean, count, select only one column!')

    def Rank_win(self, list):
        self.New_win_sec(self.new_win, "rank")

        Static = tk.Label(master=self.new_win_sec, text="Fill in column's name which \n you want to set for key!")
        Static.pack(side="top", pady=10)
        self.key = tk.Entry(master=self.new_win_sec, width=20)
        self.key.pack(side="top")
        self.var = tk.IntVar()
        self.var.set(True)
        chk_ascending = tk.Checkbutton(master=self.new_win_sec, text="ascending", width=10, variable=self.var)
        chk_ascending.pack(side="top", pady=10)

        df_sort = pd.concat(list, axis=1)

        self.btn_Done(self.new_win_sec)
        self.btn_done.configure(command=lambda : self.Rank(df_sort))

    def Rank(self, df):
        if self.var.get() == 1:
            self.df = df.sort_values(self.key.get())
        else:
            self.df = df.sort_values(self.key.get(), ascending=False)
        print(self.df)
        self.new_win.destroy()
        self.new_win_sec.destroy()

        self.btn_save.configure(command=lambda : self.Save_win())

    # merge
    def Merge_win(self):
        if len(self.col_1_ch) == 0:
            tk.messagebox.showinfo("Error", 'Choose both file!')
        elif len(self.col_2_ch) == 0:
            tk.messagebox.showinfo("Error", 'Choose both file!')
        else:
            self.New_win(self.root, "merge")
            Static = tk.Label(master=self.new_win, text="Fill in which column you want to set for key!")
            Static.pack(side="top")
            self.key = tk.Entry(master=self.new_win, width=10)
            self.key.pack(side="top")

            self.var = tk.IntVar()
            self.var.set(0)
            chk_rank = tk.Radiobutton(master=self.new_win, value=0, variable=self.var, text="inner", width=10)
            chk_rank.pack(side="top")
            chk_max = tk.Radiobutton(master=self.new_win, value=1, variable=self.var, text="outer", width=10)
            chk_max.pack(side="top")

            self.btn_Done(self.new_win)
            self.btn_done.configure(command=lambda : self.Merge())

    def Merge(self):
        self.same_list = []
        for i in self.col_1_ch:
            if i in self.col_2_ch:
                self.same_list.append(i)
        # inner, outer
        # key
        if self.var.get() == 0:
            if len(self.key.get()) != 0:
                if self.key.get() in self.same_list:
                    self.Merge_default(self.key.get(), "inner")
                else:
                    tk.messagebox.showinfo("Error", 'Fill in exists column name!')
            else:
                self.Merge_default(self.same_list, "inner")
        else:
            if len(self.key.get()) != 0:
                if self.key.get() in self.same_list:
                    self.Merge_default(self.key.get(), "outer")
                else:
                    tk.messagebox.showinfo("Error", 'Fill in exists column name!')
            else:
                self.Merge_default(self.same_list, "outer")

        print(self.same_list)
        print(self.df)
        self.new_win.destroy()
        self.btn_save.configure(command=lambda : self.Save_win())

    def Merge_default(self, key, how):
        self.df = pd.merge(self.df1, self.df2, on=key, how=how, indicator=True)

    # describe
    def describe(self):
        if len(self.col_1_ch) != 0 and len(self.col_2_ch) != 0:
            tk.messagebox.showinfo("Error", 'Choose only one file!')
        elif len(self.col_1_ch) == 0 and len(self.col_2_ch) == 0:
            tk.messagebox.showinfo("Error", 'Choose file!')
        else:
            print(self.df1)
            if len(self.col_1_ch) != 0:
                self.df = self.df1.describe().T
            elif len(self.col_1_ch) != 0:
                self.df = self.df2.describe().T

            print(self.df)




    """
    Save
    """
    def Save_win(self):
        self.New_win(self.root, "save")
        Static = tk.Label(master=self.new_win, text="Choose your extension!")
        Static.pack(side="top", pady=20)
        self.var = tk.IntVar()
        self.var.set(0)
        chk_text = tk.Radiobutton(master=self.new_win, value=0, variable=self.var, text="CSV", width=10)
        chk_text.pack(side="top")
        chk_excel = tk.Radiobutton(master=self.new_win, value=1, variable=self.var, text="Excel", width=10)
        chk_excel.pack(side="top")

        self.btn_Done(self.new_win)
        self.btn_done.configure(command=lambda : self.Save())

    def Save(self):
        self.filetypes = [('CSV files', '*.csv'),
                          ("Excel files", "*.xlsx"),]
        # 保存するファイルのパスを取得
        # セーブ
        if self.var.get() == 0:  # csv
            self.asksave(self.var.get())
            self.df.to_csv(self.save_path, encoding="shift-jis")
        elif self.var.get() == 1:  # excel
            self.asksave(self.var.get())
            self.df.to_excel(self.save_path)

        self.new_win.destroy()

    def asksave(self, num):
        self.save_path = tk.filedialog.asksaveasfilename(
                                        title="save as",
                                        filetypes=[(self.filetypes[num]),(self.filetypes[1])]
                                        )

    """
    Others
    """
    def New_win(self, master, name):
        self.new_win = tk.Toplevel(master=master)
        self.new_win.geometry("300x200")
        self.new_win.title(name)

    def New_win_sec(self, master, name):
        self.new_win_sec = tk.Toplevel(master=master)
        self.new_win_sec.geometry("300x200")
        self.new_win_sec.title(name)

    def reset(self):
        if tk.messagebox.askokcancel("Reset", "Do you want to reset?"):
            self.file1_path.set("")
            self.file2_path.set("")
            self.index_list = []
            self.columns_list1.delete(0, tk.END)
            self.columns_list2.delete(0, tk.END)

    def btn_Done(self, master):
        self.btn_done = tk.Button(master=master, text="Done", width=10)
        self.btn_done.pack(side="bottom", pady=10)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    model = model_data()
    model.run()
