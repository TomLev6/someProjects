import tkinter as tk

top = tk.Tk()

mb=  tk.Menubutton ( top, text="condiments", relief='raised')
mb.grid()
mb.menu =  tk.Menu ( mb, tearoff = 0 )
mb["menu"] =  mb.menu

mayoVar = tk.IntVar()
ketchVar = tk.IntVar()

mb.menu.add_checkbutton ( label="mayo",
                          variable=mayoVar )
mb.menu.add_checkbutton ( label="ketchup",
                          variable=ketchVar )

mb.pack()
top.mainloop()