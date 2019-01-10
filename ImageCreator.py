from tkinter import *
from PIL import ImageTk, Image
root = Tk()

ptList=[]
prev = None

rad = 4

img = ImageTk.PhotoImage(Image.open("pewds2.png"))  # PIL solution
canv = Canvas(root, width=img.width(), height=img.height(), bg='white')
canv.grid(row=2, column=3)

def undo(event):
  print("oof")

  if(len(ptList)>0):
      canv.delete(ptList[len(ptList)-1])
      del ptList[len(ptList)-1]




canv.create_image(0, 0, anchor=NW, image=img)

def callback(event):  
  print("clicked at: ", event.x, event.y)  
  ptList.append(canv.create_oval(event.x-rad, event.y-rad, event.x+rad, event.y+rad,outline="#05f", fill="#05f"))
        
  canv.pack(fill=BOTH, expand=1)    

def export(event):
  print("exporting")
  s="["
  for oval in ptList:
    coords = canv.coords(oval)
    s+="("+str(int(coords[0]+rad))+ ","+str(int(coords[1]+rad))+"),"
  s+="]"
  print(s)



root.bind_all("<Control-z>",undo)
canv.bind("<Button-1>", callback)
root.bind_all("<Escape>",export)


mainloop()