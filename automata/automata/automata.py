###################################
    # L 36 [ L 4 [ PEN 2 F 100 R 90 ] R 10 COLOR K ]

    # L 36 [ L 4 [ F 100 R 90 ] R 10 ]
###################################

# IMPORT

###################################
from tkinter import *
from tkinter import filedialog

import turtle

import ply.lex as lex
import ply.yacc as yacc



###################################

# CREATING WINDOW

###################################
root = Tk()

root.geometry("1000x800")
root.title("Drawing Robot G-4")
root.configure(bg="#7b337d")



###################################

# OPENFILE

###################################

def get_path(param):
    global program
    program = param



def openFile():
    
    taken_path = filedialog.askopenfilename(initialdir= "C:/Users/Pc/Downloads",
                                          title= "Select File",
                                          filetypes= ( ("text files","*.txt"),
                                                       ("all files","*.*") ) )
    program_file = open(taken_path, "r")
    get_path(program_file)

button = Button(root, text="Open File", command=openFile, width=10, bg="#430d4b", fg="#f5d5e0")
button.place(x=100,y=150)



lexingLabel = Label(root,text= "Lexer Output", bg="#c874b2", fg="#430d4b", height=1, width=15)
lexingLabel.place(x=200,y=487)

lexingText = Text(root, bg="#f5d5e0", fg="#210535", height=5, width=42)
lexingText.place(x=200,y=510)


parserLabel = Label(root,text= "Parser Output", bg="#c874b2", fg="#430d4b", height=1, width=15)
parserLabel.place(x=562,y=487)

parserText = Text(root, bg="#f5d5e0", fg="#210535", height=5, width=42)
parserText.place(x= 562,y=510)



errorLabel = Label(root,text= "ERRORS", bg="#c874b2", fg="#430d4b", height=1, width=15)
errorLabel.place(x=200,y=597)

errorText = Text(root, bg="#f5d5e0", fg="#210535", height=5, width=87)
errorText.place(x=200,y=620)

#---------------------------------------------
ek = Label(root, text="enter program: ", bg="#c874b2", fg="#430d4b", height=1, width=15 )
ek.place(x=200,y=710)

ek_text = Text(root, bg="#f5d5e0", fg="#210535", height=1, width=87)
ek_text.place(x=200,y=733)
ek_button = Button(root, text="take it", 
                             command= lambda: get_path(ek_text.get("1.0",END)), 
                             width=10, bg="#430d4b", fg="#f5d5e0")
ek_button.place(x=100,y=710)

#---------------------------------------------

###################################

# LEXER PARSER

###################################

def get_run(run):
    global running_program 
    running_program = run


def lexer_parser(path):


    tokens = ('F','B', 'R', 'L', 'COLOR', 'PEN',
              'NUMBER', 
              'COLOR_TYPE',
              'LBRACKET','RBRACKET' )

    t_F = r'F'
    t_B = r'B'
    t_R = r'R'
    t_L = r'L'
    t_COLOR = r'COLOR'
    t_PEN = r'PEN'

    t_NUMBER = r"\d+"

    t_COLOR_TYPE = r"K|Y|M|S"

    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'

    t_ignore = " \t"

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        
        errorText.delete("1.0","end")
        errorText.insert(END, "Illegal character '%s'\n" % t.value[0])
        t.lexer.skip(1)


    global program 

    lexer = lex.lex()
    lexer.input(program)

    for token in lexer:
        print(token)
        lexingText.delete("1.0","end")
        lexingText.insert(END, token)
        
    
    errorText.delete("1.0","end")
    errorText.insert(END, "lexing successful\n")
    
    run = []

    def p_expression_loop_type1(t):
        'expression : L NUMBER LBRACKET expression RBRACKET' 
        run.append( [ t[1],t[2] ] )
        print("p_expression_loop_type1")
        print(*t, "\n")

    
    def p_expression_loop_type2(t):
        'expression : L NUMBER LBRACKET expression expression RBRACKET' 
        run.append( [ t[1],t[2], t[4],t[5] ] )
        print("p_expression_loop_type2")
        print(*t, "\n")

    def p_expression_loop_type3(t):
        'expression : L NUMBER LBRACKET instructions RBRACKET'
        run.append([t[1], t[2] ,t[4] ])
        print("p_expression_loop3")
        print(*t, "\n")

    def p_expression_loop_type4(t):
        'expression : L NUMBER LBRACKET instructions RBRACKET instructions' 
        run.append([ t[1], t[2] ])
        print("p_expression_loop_type4")
        print(*t, "\n")

    def p_instruc_instruc(t):
        'instructions : instruction instruction'
        for i in range(3):
            if i!=None:
                return
            else:
                run.append([t[1],t[2]])
        print("p_instruc_instruc")
        print(*t, "\n")
        
    def p_instruction(t):
        '''instruction :  F NUMBER R NUMBER 
                        | B NUMBER R NUMBER
                        | PEN NUMBER
                        | COLOR COLOR_TYPE
                        | R NUMBER 
                        | F NUMBER
                        | B NUMBER
                        
                      '''
        if(len(t)==5):
            run.append([t[1],t[2],t[3],t[4]])
        else:
            run.append([t[1],t[2]])
        print("p_instruction")
        print(*t, "\n")



    def p_error(t):
        print("Syntax error at '%s'" % t.value)
        print("p_error")
        print(t.value, "\n")

        errorText.delete("1.0","end")
        errorText.insert(END, "Syntax error at '%s'" % t.value)

    parser = yacc.yacc()
    parser.parse(program)

    # errorText.delete("1.0","end")
    errorText.insert(END, "parsing successful\n")

    parserText.delete("1.0","end")
    parserText.insert(END, run)

    print("\n\n*****************\n\n", run)
    get_run(run)


buttonLex = Button(root, text="Lexer-Parser", command=lambda :  lexer_parser(program), width=10, bg="#430d4b", fg="#f5d5e0")
buttonLex.place(x=100,y=200)

###################################

# DRAWING PART

###################################

drawingCanvas = Canvas(root, bg="white", height=425, width=700)
drawingCanvas.place(x=200,y=40)

panel = turtle.RawTurtle(drawingCanvas)


def draw():

    global running_program

    for tokens in running_program:
        for instruction in tokens:

            if instruction == 'F':
                panel.down()
                if( 0 <= tokens.index(instruction)+1 < len(tokens)):
                    value = tokens[tokens.index(instruction)+1]
                    panel.forward(value)
                    panel.up()

            elif instruction == 'B':
                panel.down()
                if( 0 <= tokens.index(instruction)+1 < len(tokens)):
                    value = tokens[tokens.index(instruction)+1]
                    panel.backward(value)
                    panel.up()

            elif instruction == 'R':
                panel.down()
                if( 0 <= tokens.index(instruction)+1 < len(tokens)):
                    value = tokens[tokens.index(instruction)+1]
                    panel.rigth(value)
                    panel.up()


            elif instruction == 'COLOR':
                if( 0 <= tokens.index(instruction)+1 < len(tokens)):
                    value = tokens[tokens.index(instruction)+1]
                    if(value=='K'):
                        color_type = "red"
                    elif(value=='Y'):
                        color_type = "green"
                    elif(value=='M'):
                        color_type = "blue"
                    elif(value=='S'):
                        color_type = "black"
                    panel.pencolor(color_type)
            
            elif instruction == 'PEN':
                if( 0 <= tokens.index(instruction)+1 < len(tokens)):
                    value = tokens[tokens.index(instruction)+1]
                    panel.width(value)

            elif instruction == 'L':
                if( 0 <= tokens.index(instruction)+1 < len(tokens)):
                    value = tokens[tokens.index(instruction)+1]

buttonDraw = Button(root, text="Draw", command=draw, width=10, bg="#430d4b", fg="#f5d5e0")
buttonDraw.place(x=100,y=250) 



#-----------------------------------------------------------------------------------------------------
def clear_program():
    global flag 
    flag = False
    panel.clear()
    panel.goto(0,0)
    panel.up()
    lexingText.delete("1.0","end")
    parserText.delete("1.0","end")
    errorText.delete("1.0","end")
    


clear = Button(root, text="Clear", command=clear_program, width=10, bg="#430d4b", fg="#f5d5e0")
clear.place(x=100,y=300) 
#-----------------------------------------------------------------------------------------------------

flag = True
def default_drawing(color="red", size=1):
    panel.goto(0,0)
    panel.pencolor(color)
    panel.width(size)
    for outer in range(36):
        while(flag == True):
            for inner in range(4):
                panel.forward(100)
                panel.right(90)
            panel.right(10)




default_drawing_btn = Button(root, text="Example", 
                             command=default_drawing, 
                             width=10, bg="#430d4b", fg="#f5d5e0")
default_drawing_btn.place(x=100,y=400) 


#-----------------------------------------------------------------------------------------------------


root.mainloop()
