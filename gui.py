import tkinter
import tkinter.messagebox as messagebox
import clips

def createFace(faceNo,yu,colorIndex):

    face=[]
    xu=(3*faceNo-2)*30+faceNo*5

    for j in range(1,10):

        new_button=tkinter.Button(window, text="")
        new_button.place(x=xu, y=yu, width=30, height=30)
        new_button.configure(bg=colors[colorIndex])
        if j is not 5 and colorIndex is not 5:
            new_button.bind("<Button-1>", nextColor)
        face.append(new_button)
        xu=xu+30
        if j%3==0:
            xu=(3*faceNo-2)*30+faceNo*5
            yu+=30

    faces.append(face)


def createCube():
    xu=35
    yu=180

    "* 1=Left (Blue) 2=F (Red) 3=R (Green) 4=B (Orange) 5=U (Yellow) 6=D (White) *"

    for i in range(1,5):
        createFace(i,180,i-1)
    createFace(2,yu=85, colorIndex=4)
    createFace(2,yu=275, colorIndex=5)


def colorFace(faceIndex, color):
    for b in faces[faceIndex]:
        b.configure(bg=color)


def addMenu():
    menu_label = tkinter.Label(window,text="Meniu:")
    menu_label.place(x=600, y=50)

    info_label = tkinter.Label(window,text="Pentru a schimba culorile, click stanga pe fiecare. ")
    info_label.place(x=30, y=10)

    solve_button=tkinter.Button(window, text="Rezolva")
    solve_button.place(x=600, y=80)
    solve_button.bind("<Button-1>", solveYellowFace)

    reset_button=tkinter.Button(window, text="Reset")
    reset_button.place(x=600, y=110)
    reset_button.bind("<Button-1>", resetCube)


def resetCube(event):
    for f in range(0,6):
        colorFace(f,colors[f])
    global no_pieces_colors
    no_pieces_colors=[9,9,9,9,9]
    T.delete('1.0', tkinter.END)



def test():
    for e in no_pieces_colors:
        if e is not 9:
            return False
    return True


def solveYellowFace(event):
    if test() is False:
        lipsa=[]
        surplus=[]
        for e in no_pieces_colors:
            if e<9:
                lipsa.append([cicle_colors[no_pieces_colors.index(e)],abs(e-9)])
            if e>9:
                surplus.append([cicle_colors[no_pieces_colors.index(e)],abs(e-9)])

        messagebox.showwarning("Warning",f"Configuratie gresita!\nLipsesc: {lipsa}\nSunt in plus: {surplus}")
        return

    solveInClips()



def nextColor(event):
    caller = event.widget
    cc=caller['bg']
    i = (cicle_colors.index(cc)+1)%5

    color = cicle_colors[i]
    caller.configure(bg=color)

    no_pieces_colors[i-1]-=1
    no_pieces_colors[i]+=1

    print(no_pieces_colors)


def getFacesForCLIPS():
    global faces_CLIPS

    for face in faces:
        #fact = "(Face"
        fact=[]
        for b in face:
            fact.append(b['bg'][0])
        #fact += ")"
        faces_CLIPS.append(fact)



def solveInClips():
    global faces_CLIPS

    env = clips.Environment()
    env.clear()
    env.load("rubiks-cube.clp")
    env.reset()

    getFacesForCLIPS()
   
    for e in faces_CLIPS:
        strToAdd = "(Face "+e[0]+' '+e[1]+' '+e[2]+' '+e[3]+' '+e[4]+' '+e[5]+' '+e[6]+' '+e[7]+' '+e[8]+")"
        fact = env.assert_string(strToAdd)

    for c,o in [('R','F'),('G','R'),('O','B'),('B','L')]:
        strToAdd = "(Face-Orientation "+c+' '+o+")"
        fact = env.assert_string(strToAdd)  

    fact = env.assert_string('(Solution)')    

    env.run()

    facts = env.eval("(get-fact-list *)")

    for f in facts:
        print(f)

    sol = str(facts[-2])

    import nltk
    tok_sol = nltk.word_tokenize(sol)

    T.insert(tkinter.END, tok_sol[3:-1])
    facts.clear()



"*MAIN*"

window = tkinter.Tk()
window.configure(width=900, height=500, bg='#f1f1f1')
window.title("Kyuubi")

faces = []
colors = ['Blue','Red','Green','Orange','Yellow','White']
cicle_colors = ['Blue','Red','Green','Orange','Yellow']

global no_pieces_colors
global faces_CLIPS
faces_CLIPS = []
no_pieces_colors = [9,9,9,9,9]

createCube()
colorFace(5,'White')

addMenu()

T = tkinter.Text(window)
T.place(x=500,y=140, height=300, width=350)
T.insert(tkinter.END, "Solutia:\n")

window.mainloop()