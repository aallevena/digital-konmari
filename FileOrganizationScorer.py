
import os
import webbrowser
import datetime

results = []
redCount = 0
yellowCount = 0
greenCount = 0
folderCount = 0
fileCount = 0
totalKBSize =0
def getFolderScore(path):
    for root, dirs, files in os.walk(path):
        #print(root, "has",len(dirs),"directories and", len(files),"files in it")
        #print(os.path.getsize(root))
        state=""
        global folderCount, fileCount, redCount, yellowCount, greenCount, totalKBSize
        folderCount+=len(dirs)
        fileCount+=len(files)
        totalKBSize +=os.path.getsize(root)
        if 2 <= len(files) <= 20 and len(dirs)==0:
            state="Green"
            greenCount+=1
        elif 2 <= len(dirs) <= 20 and len(files)==0:
            state="Green"
            greenCount+=1
        elif len(files) ==0:
            state="Yellow"
            yellowCount+=1
        elif len(dirs) ==0:
            state="Yellow"
            yellowCount+=1 
        elif len(files) <=5:
            state="Yellow"
            yellowCount+=1
        else: 
            state="Red"
            redCount+=1
        results.append([state, root, len(dirs), len(files)],os.path.getsize(root))
        #print("It's rating is", state)

path = 'C:/Users/aalleven/OneDrive/'

#Show me the files and directories in a path
#print(os.listdir(path))
getFolderScore(path)

for i in results:
    print(i)

d = datetime.datetime.today()
report = "FolderScore"+d.strftime("%y-%m-%d-%H-%M")+".html"
#Okay, time to put together the html plan. We are going to generate one line for each entry. Ideally we will color the first
#word based on their value. 
cwd = os.getcwd()
os.path.join(cwd,report)
print(os.path.join(os.getcwd(),report))
f = open(os.path.join(os.getcwd(),report),'w')

message = """<html>
<head>"""
f.write(message) 
message = """</head>
<body><h1>File Organization Score Report</h1>"""
f.write(message)
message = "<p>We have {} files, and {} folders. There are {} greens, {} yellows, and {} red folders. </p>".format(fileCount, folderCount, greenCount, yellowCount, redCount)
f.write(message)
message = "<p>The directory we are searching is {} and the file name is {}. </p>".format(path, report)
f.write(message)
message = "<p>The Status colors are based on my view of how folders should be organized. </p>".format(path, report)
f.write(message)
message = "<p>Green means a folder is organized. Generally it means there are only 2-20 items and they are either all files or folders. </p>".format(path, report)
f.write(message)
message = "<p>Yellow is still good, but I couldn't make it green. It's cases where there are more than 20 items in a folder of the same type (hard to visually scan), there is a mix with most 5 files, or there is 0-1 items in the folder. </p>".format(path, report)
f.write(message)
message = "<p>Red means the folder has a mix of files and folders such that there is just too much confusion going on in the file. </p>".format(path, report)
f.write(message)
strTable = "<html><table><tr><th>Status</th><th>Directory</th><th>Folders</th><th>Files</th></tr>"
f.write(strTable)
strRW = "<tr><td style='font-weight: bold'>"+str("{:.2%}".format((greenCount+yellowCount)/(greenCount+yellowCount+redCount)))+ "</td><td>"+str(path)+"</td><td>"+str(folderCount)+"</td><td>"+str(fileCount)+"</td></tr>"
f.write(strRW)

for i in results: 
    if i[0]=='Red':
        strRW = "<tr><td style='color:red'>"+str(i[0])+ "</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td></tr>"
    elif i[0] =='Yellow':
        strRW = "<tr><td style='color:gold'>"+str(i[0])+ "</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td></tr>"
    else:
        strRW = "<tr><td style='color:green'>"+str(i[0])+ "</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td></tr>"
    f.write(strRW)
message = """</table></body></html>"""

f.write(message)
f.close()
webbrowser.open_new_tab(os.path.join(os.getcwd(),report))