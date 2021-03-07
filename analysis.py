import sys
import os
import xlsxwriter

class Major:
    def __init__(self, q1, q3, q4):
        self.q1 = {}
        self.q4 = {}
        self.major = q3

        self.add_q1_answer(q1)
        self.add_q4_answer(q4)

    def add_q1_answer(self, q1):
        try:
             self.q1[q1] = self.q1[q1] + 1
        except:
            self.q1[q1] = 1

    def add_q4_answer(self, q4):
        try:
            self.q4[q4] = self.q4[q4] + 1
        except:
            self.q4[q4] = 1
    
    
        
#file exports
IN = open(sys.argv[1])
OUT = wb = xlsxwriter.Workbook('out.xlsx')
EXTR = open("extra.csv", 'w+')

Q1_DICT = {}
Q3_DICT = {}
Q4_DICT = {}

MAJOR_DICT = {}

MAJOR_CONV = {
    "1":"No College",
    "2":"Computer Sciences",
    "3":"Business",
    "4":"Language",
    "5":"Arts or Creative Works",
    "6":"Science ",
    "7":"Mathematics",
    "8":"Engineering",
    "9":"History or Political Science",
    "10":"Other"
}

SKILL_CONV = {
    "0":"0",
    "1":"1",
    "2":"2",
    "3":"3",
    "4":"4",
    "5":"5",
    "6":"6",
    "7":"7",
    "8":"8",
    "9":"9",
    "10":"10"
}

AGE_CONV = {
    "1":"0-9",
    "2":"10-17",
    "3":"18-24",
    "4":"25-34",
    "5":"35-44",
    "6":"45-54 ",
    "7":"55-64 ",
    "8":"65+",
    "9":"No Experience "
}




#method to filter private data
def analyze(file, out, extra):
    
    with file as f:
        f.readline()
        for l in f:
            l = l.split(',')
            
            if(len(l) == 4):
                __increment(l, 0,1,2)
                __major(l, 0,1,2)
            elif(len(l) == 5):
                __increment(l, 0,2,3)
                __major(l, 0,2,3)
            else:
                extra.write(','.join(l))
def __increment(l, indx1, indx2, indx3):
    try:
        Q1_DICT[l[indx1]] = Q1_DICT[l[indx1]] + 1
    except:
        Q1_DICT[l[indx1]] = 1
    try:
        Q3_DICT[l[indx2]] = Q3_DICT[l[indx2]] + 1
    except:
        Q3_DICT[l[indx2]] = 1
    try:
        Q4_DICT[l[indx3]] = Q4_DICT[l[indx3]] + 1
    except:
        Q4_DICT[l[indx3]] = 1

def __major(l, indx1, indx2, indx3):
    try:
        MAJOR_DICT[l[indx2]].add_q1_answer(l[indx1])
    except:
        MAJOR_DICT[l[indx2]] = Major(l[indx1], l[indx2], l[indx3])

    try:
        MAJOR_DICT[l[indx2]].add_q4_answer(l[indx3])
    except:
        MAJOR_DICT[l[indx2]] = Major(l[indx1], l[indx2], l[indx3])

def write_q1():
    ws = wb.add_worksheet(name="Q1")
    ws.set_column(0,0, 60) #set first column width
    ws.write('A1', "How familiar would you say you are with computer programming?")
    ws.write('A2', "Level:")
    ws.write('A3', "# of Responses:")
    row = 1
    col = 1
    for i in range(0,11):
        ws.write(row, col, i)
        try:
            ws.write(row + 1, col, Q1_DICT[i])
        except:
            ws.write(row + 1, col, 0)
        col = col + 1

def write_q3():
    ws = wb.add_worksheet(name="Q3")
    ws.set_column(0,0, 60) #set first column width
    ws.set_column(1,10, 30) #set other column widths
    ws.write('A1', "Primary field of study in college?")
    ws.write('A2', "Field:")
    ws.write('A3', "# of Responses:")
    row = 1
    col = 1
    for key in MAJOR_CONV:
        ws.write(row, col, MAJOR_CONV[key])
        try:
            ws.write(row + 1, col, Q3_DICT[key])
        except:
            ws.write(row + 1, col, 0)
        
        col = col + 1

def write_q4():
    ws = wb.add_worksheet(name="Q4")
    ws.set_column(0,0, 60) #set first column width
    ws.write('A1', "What age were you exposed to programming?")
    ws.write('A2', "Ages:")
    ws.write('A3', "# of Responses:")
    row = 1
    col = 1
    for key in AGE_CONV:
        ws.write(row, col, AGE_CONV[key])
        try:
            ws.write(row + 1, col, Q4_DICT[key])
        except:
            ws.write(row + 1, col, 0)
        
        col = col + 1

def write_major(major):
    name = MAJOR_CONV[major.major]

    ws = wb.add_worksheet(name=name)
    ws.set_column(0,0, 60) #set first column width
    ws.write('A1', name)

    ws.write('A3', "What age were you exposed to programming?")
    ws.write('A4', "Ages:")
    ws.write('A5', "# of Responses:")
    row = 4
    col = 1
    for key in AGE_CONV:
        ws.write(row, col, AGE_CONV[key])
        try:
            ws.write(row + 1, col, major.q4[key])
        except:
            ws.write(row + 1, col, 0)
        
        col = col + 1

    ws.write('A9', "How familiar would you say you are with computer programming?")
    ws.write('A10', "Level:")
    ws.write('A11', "# of Responses:")
    row = 10
    col = 1
    for i in range(0, 11):
        ws.write(row, col, i)
        try:
            ws.write(row + 1, col, major.q1[str(i)])
        except: 
            ws.write(row + 1, col, 0)
        col = col + 1
def main():
    analyze(IN, OUT, EXTR)

    #write question sheets
    write_q1()
    write_q3()
    write_q4()
    
    #write sheet for each major
   
    for key in MAJOR_DICT:
        
        write_major(MAJOR_DICT[key])
    
    #output
    wb.close()
    print("Complete.. no errors")


if __name__ == "__main__":
    main()

