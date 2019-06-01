import fileinput
import re

lines = list(fileinput.input())
RA =lines[0]
DEC = lines[1]
name = lines[2]
print(RA)
print(DEC)
print(name)

RA=re.split(" |,|]", RA)
print(RA)
print("RA coordinates are between ["+RA[1]+","+RA[3]+"]")

DEC=re.split(" |,|]", DEC)
print(DEC)
print("DEC coordinates are between ["+DEC[1]+","+DEC[3]+"]")