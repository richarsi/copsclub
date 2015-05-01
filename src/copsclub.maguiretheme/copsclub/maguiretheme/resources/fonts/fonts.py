import re
pattern = '/([^\\/]*)\\.ttf'

with open('fonts.txt', 'rb') as f:
     lines = f.readlines()
     for line in lines:
         fontnames = re.search(pattern, line).groups()
         print "@font-face {\n    font-family: \'%s\';" % fontnames
         print line.replace('\n','')
         print "}"

