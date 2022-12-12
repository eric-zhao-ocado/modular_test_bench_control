import tkinter as tk
from tkinter import ttk, font

root = tk.Tk()
root.title("Test Bench Control")


# Make the app responsive
root.columnconfigure(index=0, weight=1)
root.columnconfigure(index=1, weight=1)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)
root.rowconfigure(index=2, weight=1)

# Create a style
style = ttk.Style(root)
root.tk.call("source", "routine/static/forest-dark.tcl")  # theme
style.theme_use("forest-dark")

# Create lists for the Comboboxes
option_menu_list = ["", "OptionMenu", "Option 1", "Option 2"]
combo_list = ["Combobox", "Editable item 1", "Editable item 2"]
readonly_combo_list = ["Readonly combobox", "Item 1", "Item 2"]

# Create control variables 
a = tk.BooleanVar()
b = tk.BooleanVar(value=True)
c = tk.BooleanVar()
d = tk.IntVar(value=2)
e = tk.StringVar(value=option_menu_list[1])
f = tk.BooleanVar()
g_x = tk.DoubleVar(value=75.0)
g_y = tk.DoubleVar(value=75.0)
g_z = tk.DoubleVar(value=75.0)
h = tk.BooleanVar()

# Separator
# separator = ttk.Separator(root)
# separator.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")

# Create a Frame for input widgets
widgets_frame = ttk.Frame(root, padding=(0, 0, 0, 10))
widgets_frame.grid(row=0, column=0, padx=10, pady=(30, 10), sticky="nsew", rowspan=3)
widgets_frame.columnconfigure(index=0, weight=1)

# Entry
entry = ttk.Entry(widgets_frame)
entry.insert(0, "Entry")
entry.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="ew")

# Spinbox
spinbox = ttk.Spinbox(widgets_frame, from_=0, to=100)
spinbox.insert(0, "Spinbox")
spinbox.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

# Combobox
combobox = ttk.Combobox(widgets_frame, values=combo_list)
combobox.current(0)
combobox.grid(row=2, column=0, padx=5, pady=30,  sticky="ew")



# Button
button = ttk.Button(widgets_frame, text="Button")
button.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

# Accentbutton
accentbutton = ttk.Button(widgets_frame, text="Accentbutton", style="Accent.TButton")
accentbutton.grid(row=7, column=0, padx=5, pady=10, sticky="nsew")

# Togglebutton
button = ttk.Checkbutton(widgets_frame, text="Togglebutton", style="ToggleButton")
button.grid(row=8, column=0, padx=5, pady=10, sticky="nsew")

# Switch
switch = ttk.Checkbutton(widgets_frame, text="Switch", style="Switch")
switch.grid(row=9, column=0, padx=5, pady=10, sticky="nsew")

# Panedwindow
paned = ttk.PanedWindow(root)
paned.grid(row=0, column=1, pady=(25, 5), sticky="nsew", rowspan=3)

# Pane #1
pane_1 = ttk.Frame(paned)
paned.add(pane_1, weight=1)

# Create a Frame for the Treeview
treeFrame = ttk.Frame(pane_1)
treeFrame.pack(expand=True, fill="both", padx=5, pady=5)

# Scrollbar
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

# Treeview
treeview = ttk.Treeview(treeFrame, selectmode="extended", yscrollcommand=treeScroll.set, columns=(1, 2), height=12)
treeview.pack(expand=True, fill="both")
treeScroll.config(command=treeview.yview)

# Treeview columns
treeview.column("#0", width=120)
treeview.column(1, anchor="w", width=120)
treeview.column(2, anchor="w", width=120)

# Treeview headings
treeview.heading("#0", text="Column 1", anchor="center")
treeview.heading(1, text="Column 2", anchor="center")
treeview.heading(2, text="Column 3", anchor="center")

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
tab_1.rowconfigure(index=3, weight=1)
tab_1.rowconfigure(index=4, weight=1)
tab_1.rowconfigure(index=5, weight=1)
notebook.add(tab_1, text="Dynamic Controls")

# Scale
scale = ttk.Scale(tab_1, from_=100, to=0, variable=g_x, command=lambda event: g_x.set(scale.get()))
scale.grid(row=0, column=0, padx=(20, 10), pady=(20, 0), sticky="ew")

# Progressbar
progress = ttk.Progressbar(tab_1, value=0, variable=g_x, mode="determinate")
progress.grid(row=0, column=1, padx=(10, 20), pady=(20, 0), sticky="ew")

# Scale
scale2 = ttk.Scale(tab_1, from_=100, to=0, variable=g_y, command=lambda event: g_y.set(scale2.get()))
scale2.grid(row=1, column=0, padx=(20, 10), pady=(20, 0), sticky="ew")

# Progressbar
progress2 = ttk.Progressbar(tab_1, value=0, variable=g_y, mode="determinate")
progress2.grid(row=1, column=1, padx=(10, 20), pady=(20, 0), sticky="ew")

# Scale
scale3 = ttk.Scale(tab_1, from_=100, to=0, variable=g_z, command=lambda event: g_z.set(scale3.get()))
scale3.grid(row=2, column=0, padx=(20, 10), pady=(20, 0), sticky="ew")

# Progressbar
progress3 = ttk.Progressbar(tab_1, value=0, variable=g_z, mode="determinate")
progress3.grid(row=2, column=1, padx=(10, 20), pady=(20, 0), sticky="ew")

# Scale
scale4 = ttk.Scale(tab_1, from_=100, to=0, variable=g_z, command=lambda event: g_z.set(scale3.get()))
scale4.grid(row=3, column=0, padx=(20, 10), pady=(20, 0), sticky="ew")

# Progressbar
progress4 = ttk.Progressbar(tab_1, value=0, variable=g_z, mode="determinate")
progress4.grid(row=3, column=1, padx=(10, 20), pady=(20, 0), sticky="ew")

# Scale
scale5 = ttk.Scale(tab_1, from_=100, to=0, variable=g_z, command=lambda event: g_z.set(scale3.get()))
scale5.grid(row=4, column=0, padx=(20, 10), pady=(20, 0), sticky="ew")

# Progressbar
progress5 = ttk.Progressbar(tab_1, value=0, variable=g_z, mode="determinate")
progress5.grid(row=4, column=1, padx=(10, 20), pady=(20, 0), sticky="ew")

# Scale
scale6 = ttk.Scale(tab_1, from_=100, to=0, variable=g_z, command=lambda event: g_z.set(scale3.get()))
scale6.grid(row=5, column=0, padx=(20, 10), pady=(20, 0), sticky="ew")

# Progressbar
progress6 = ttk.Progressbar(tab_1, value=0, variable=g_z, mode="determinate")
progress6.grid(row=5, column=1, padx=(10, 20), pady=(20, 0), sticky="ew")

# # Label
# label = ttk.Label(tab_1, text="90 deg", justify="center")
# label.grid(row=1, column=0, pady=10, columnspan=2)

# Tab #2
tab_2 = ttk.Frame(notebook)
notebook.add(tab_2, text="Graphs / Data")

# Tab #3
tab_3 = ttk.Frame(notebook)
notebook.add(tab_3, text="Overview")

notebook.pack(expand=True, fill="both", padx=5, pady=5)

# Sizegrip
sizegrip = ttk.Sizegrip(root)
sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))


root.update()
root.minsize(root.winfo_width(), root.winfo_height())  # set minsize
x_cordinate = int((root.winfo_screenwidth()/2) - (root.winfo_width()/2))  # center window
y_cordinate = int((root.winfo_screenheight()/2) - (root.winfo_height()/2))  # center window
root.geometry("1920x1080")  # default window size
root.mainloop()