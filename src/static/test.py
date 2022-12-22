import tkinter as tk
from tkinter import font

#Fonts text display in tkinter dialog
def generate_frm(frame):
    row = 1
    for fitem in fonts:
        tk.Label(frame, font=(fitem, 16, "normal"), text=fitem).grid(row=row, column=1)
        row = row + 1

# Tool Dialog configuration
root = tk.Tk()
root.geometry('400x600')
root.title('Font Families with Respective Style')
fonts=list(font.families())
fonts.sort()

#Frame creation with scroll bar
canvas = tk.Canvas(root)
frame = tk.Frame(canvas)
scrolbr = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrolbr.set)
scrolbr.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((20,4), window=frame, anchor="nw")
frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))
generate_frm(frame)

root.mainloop()