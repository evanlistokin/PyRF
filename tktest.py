import tkinter as tk

root = tk.Tk()
root.grid_columnconfigure(0,pad=10)
root.grid_columnconfigure(1,pad=10)
def input(Trace, Frequency):
    trace_result = listbox1.curselection()
    frequency_result = text2.get("1.0", "end-1c")
    root.destroy()

textbox1 = tk.Entry(root)
listbox1 = tk.Listbox(root, height="4")
button_ok = tk.Button(root,text='OK', width=10)
button_cancel = tk.Button(root,text='Cancel', width=10)

button_ok.grid(row=3,column = 1, padx=5, pady=5)
button_cancel.grid(row=3,column=0, padx=5, pady=5)

textbox1.grid(row=2,column=1, columnspan=2, padx=5, pady=5)
listbox1.grid(row=1,column=1, columnspan=2,padx=5, pady=5)
listbox1.insert(0, "S11", "S22")

label0 = tk.Label(root,text='Enter values to add trace:')
label1 = tk.Label(root,text='Trace: ')
label2 = tk.Label(root,text='Frequency: ')
label0.grid(row=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
label1.grid(row=1,column=0, sticky=tk.NW, padx=5, pady=5)
label2.grid(row=2,column=0, sticky=tk.W, padx=5, pady=5)

textbox1.focus()

root.mainloop()
test
test
test
