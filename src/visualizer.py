import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Test Bench Control")

# split screen into sections (2 x 3)
root.columnconfigure(index=0, weight=1)
root.columnconfigure(index=1, weight=1)
root.rowconfigure(index=0, weight=1)



style = ttk.Style(root)  # create a style
root.tk.call("source", "routine/static/forest-dark.tcl")  # theme
style.theme_use("forest-dark")

# control variables
j1_sel = tk.BooleanVar(False)
j1_val = tk.DoubleVar(value=75.0)
j2_sel = tk.BooleanVar(False)
j2_val = tk.DoubleVar(value=75.0)
j3_sel = tk.BooleanVar(False)
j3_val = tk.DoubleVar(value=75.0)
j4_sel = tk.BooleanVar(False)
j4_val = tk.DoubleVar(value=75.0)
j5_sel = tk.BooleanVar(False)
j5_val = tk.DoubleVar(value=75.0)
j6_sel = tk.BooleanVar(False)
j6_val = tk.DoubleVar(value=75.0)


a = tk.BooleanVar()
b = tk.BooleanVar(value=True)
c = tk.BooleanVar()
d = tk.IntVar(value=2)
f = tk.BooleanVar()
g_x = tk.DoubleVar(value=75.0)
g_y = tk.DoubleVar(value=75.0)
g_z = tk.DoubleVar(value=75.0)
h = tk.BooleanVar()

# Create a Frame for input widgets
widgets_frame = ttk.Frame(root, padding=(0, 0, 0, 10))
widgets_frame.grid(row=0, column=0, padx=10, pady=(30, 10), sticky="nsew", rowspan=1)
widgets_frame.columnconfigure(index=0, weight=1)

# Entry
entry = ttk.Entry(widgets_frame)
entry.insert(0, "Entry")
entry.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="ew")

# Spinbox
spinbox = ttk.Spinbox(widgets_frame, from_=0, to=100)
spinbox.insert(0, "Spinbox")
spinbox.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

# Accentbutton
accentbutton = ttk.Button(widgets_frame, text="Accentbutton", style="Accent.TButton")
accentbutton.grid(row=7, column=0, padx=5, pady=10, sticky="nsew")

# Togglebutton
button = ttk.Checkbutton(widgets_frame, text="Togglebutton", style="ToggleButton")
button.grid(row=8, column=0, padx=5, pady=10, sticky="nsew")

switch = ttk.Radiobutton(widgets_frame, text= 'J1')
switch.grid(row=0, column=0, padx=(20, 10), sticky="ew")

scale = ttk.Scale(widgets_frame, from_=100, to=0, variable=g_x, command=lambda event: g_x.set(scale.get()))
scale.grid(row=0, column=0, padx=(90, 20), sticky="ew")

switch = ttk.Radiobutton(widgets_frame, text="J2")
switch.grid(row=1, column=0, padx=(20, 10), sticky="nsew")

scale2 = ttk.Scale(widgets_frame, from_=100, to=0, variable=g_y, command=lambda event: g_y.set(scale2.get()))
scale2.grid(row=1, column=0, padx=(90, 10), sticky="ew")

switch = ttk.Radiobutton(widgets_frame, text="J3")
switch.grid(row=2, column=0, padx=(20, 10), sticky="nsew")

scale3 = ttk.Scale(widgets_frame, from_=100, to=0, variable=g_z, command=lambda event: g_z.set(scale3.get()))
scale3.grid(row=2, column=0, padx=(90, 10), sticky="ew")

# stored waypoints display

paned = ttk.PanedWindow(root)
paned.grid(row=0, column=1, pady=(25, 5), sticky="nsew", rowspan=8)

pane_1 = ttk.Frame(paned)
paned.add(pane_1, weight=1)

treeFrame = ttk.Frame(pane_1)
treeFrame.pack(expand=True, fill="both", padx=5, pady=5)

treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

treeview = ttk.Treeview(treeFrame, selectmode="extended", yscrollcommand=treeScroll.set, columns=(1, 2), height=12)
treeview.pack(expand=True, fill="both")
treeScroll.config(command=treeview.yview)

# Treeview columns
treeview.column("#0", width=120)
treeview.column(1, anchor="w", width=120)
treeview.column(2, anchor="w", width=120)

# Treeview headings
treeview.heading("#0", text="Title", anchor="center")
treeview.heading(1, text="Arm One", anchor="center")
treeview.heading(2, text="Arm Two", anchor="center")

# Define treeview data -->  x,y,z coordinate and testing plan append to this list with a button
treeview_data = [
    ("", "end", 1, "Parent", ("Item 1", "Value 1")),
    (1, "end", 2, "Child", ("Subitem 1.1", "Value 1.1")),
    (1, "end", 3, "Child", ("Subitem 1.2", "Value 1.2")),
    (1, "end", 4, "Child", ("Subitem 1.3", "Value 1.3")),
    (1, "end", 5, "Child", ("Subitem 1.4", "Value 1.4")),
    ("", "end", 6, "Parent", ("Item 2", "Value 2")),
    (6, "end", 7, "Child", ("Subitem 2.1", "Value 2.1")),
    (6, "end", 8, "Sub-parent", ("Subitem 2.2", "Value 2.2")),
    (8, "end", 9, "Child", ("Subitem 2.2.1", "Value 2.2.1")),
    (8, "end", 10, "Child", ("Subitem 2.2.2", "Value 2.2.2")),
    (8, "end", 11, "Child", ("Subitem 2.2.3", "Value 2.2.3")),
    (6, "end", 12, "Child", ("Subitem 2.3", "Value 2.3")),
    (6, "end", 13, "Child", ("Subitem 2.4", "Value 2.4")),
    ("", "end", 14, "Parent", ("Item 3", "Value 3")),
    (14, "end", 15, "Child", ("Subitem 3.1", "Value 3.1")),
    (14, "end", 16, "Child", ("Subitem 3.2", "Value 3.2")),
    (14, "end", 17, "Child", ("Subitem 3.3", "Value 3.3")),
    (14, "end", 18, "Child", ("Subitem 3.4", "Value 3.4")),
    ("", "end", 19, "Parent", ("Item 4", "Value 4")),
    (19, "end", 20, "Child", ("Subitem 4.1", "Value 4.1")),
    (19, "end", 21, "Sub-parent", ("Subitem 4.2", "Value 4.2")),
    (21, "end", 22, "Child", ("Subitem 4.2.1", "Value 4.2.1")),
    (21, "end", 23, "Child", ("Subitem 4.2.2", "Value 4.2.2")),
    (21, "end", 24, "Child", ("Subitem 4.2.3", "Value 4.2.3")),
    (19, "end", 25, "Child", ("Subitem 4.3", "Value 4.3"))
    ]

# Insert treeview data
for item in treeview_data:
    treeview.insert(parent=item[0], index=item[1], iid=item[2], text=item[3], values=item[4])
    if item[0] == "" or item[2] in (8, 12):
        treeview.item(item[2], open=True) # Open parents

# Select and scroll
treeview.selection_set(10)
treeview.see(7)

# Pane #2
pane_2 = ttk.Frame(paned)
paned.add(pane_2, weight=3)

# Notebook
notebook = ttk.Notebook(pane_2)

# Tab #1
tab_1 = ttk.Frame(notebook)
tab_1.columnconfigure(index=0, weight=1)
tab_1.columnconfigure(index=1, weight=1)
tab_1.rowconfigure(index=0, weight=1)
tab_1.rowconfigure(index=1, weight=1)
tab_1.rowconfigure(index=2, weight=1)

# tab_1.rowconfigure(index=7, weight=1)
notebook.add(tab_1, text="Dynamic Controls")

# Scale
switch = ttk.Radiobutton(tab_1, text= 'J1')
switch.grid(row=0, column=0, padx=(20, 10), sticky="ew")

scale = ttk.Scale(tab_1, from_=100, to=0, variable=g_x, command=lambda event: g_x.set(scale.get()))
scale.grid(row=0, column=0, padx=(90, 20), sticky="ew")

switch = ttk.Radiobutton(tab_1, text="J2")
switch.grid(row=1, column=0, padx=(20, 10), sticky="nsew")

scale2 = ttk.Scale(tab_1, from_=100, to=0, variable=g_y, command=lambda event: g_y.set(scale2.get()))
scale2.grid(row=1, column=0, padx=(90, 10), sticky="ew")

switch = ttk.Radiobutton(tab_1, text="J3")
switch.grid(row=2, column=0, padx=(20, 10), sticky="nsew")

scale3 = ttk.Scale(tab_1, from_=100, to=0, variable=g_z, command=lambda event: g_z.set(scale3.get()))
scale3.grid(row=2, column=0, padx=(90, 10), sticky="ew")

# Label
# label = ttk.Label(tab_1, text="Joint 1: [90.000 deg]", justify="center")
# label.grid(row=0, column=1, pady=10, columnspan=2)

# label = ttk.Label(tab_1, text="Joint 2: [90.000 deg]", justify="center")
# label.grid(row=1, column=1, pady=10, columnspan=2)

# label = ttk.Label(tab_1, text="Joint 3: [90.000 deg]", justify="center")
# label.grid(row=2, column=1, pady=10, columnspan=2)

label = ttk.Label(tab_1, text="Joint 4: [90.000 deg]", justify="center")
label.grid(row=0, column=1, pady=10, columnspan=2)

label = ttk.Label(tab_1, text="Joint 5: [90.000 deg]", justify="center")
label.grid(row=1, column=1, pady=10, columnspan=2)

label = ttk.Label(tab_1, text="Joint 6: [90.000 deg]", justify="center")
label.grid(row=2, column=1, pady=10, columnspan=2)

entry = ttk.Entry(tab_1)
entry.insert(0, "Entry")
entry.grid(row=6, column=0, padx=5, pady=(7, 7), sticky="nsew")

accentbutton = ttk.Button(tab_1, text="Submit Co-ordinates", style="Accent.TButton")
accentbutton.grid(row=6, column=1, sticky="nsew", pady=(7, 7), columnspan=2)



# Tab #2
tab_2 = ttk.Frame(notebook)
notebook.add(tab_2, text="Graphs / Data")




root.update()
root.minsize(root.winfo_width(), root.winfo_height())  # set minsize
x_cordinate = int((root.winfo_screenwidth()/2) - (root.winfo_width()/2))  # center window
y_cordinate = int((root.winfo_screenheight()/2) - (root.winfo_height()/2))  # center window
root.geometry("920x1080")  # default window size
root.mainloop()