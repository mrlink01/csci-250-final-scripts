import sys
import os
import xlsxwriter

#file exports
IN = open(sys.argv[1])
OUT = open("out.csv",'w+')


#method to filter private data
def filter(file, out):
    
    with file as f:
        for l in f:
            l = l.split(',')
            
            q1 = 9
            
            l = l[9:]
            tmp = []
            for i in l: 
                if not i == '':
                    tmp.append(i)
                    
            out.write(','.join(tmp))
            tmp = []



def main():
    filter(IN, OUT)
    

if __name__ == "__main__":
    main()

