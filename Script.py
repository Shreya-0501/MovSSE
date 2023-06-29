import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString, Comment
import re

URL = "https://imsdb.com/scripts/Devil-Wears-Prada,-The.html"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

scrape = soup.find("pre")
# print(scrape)


x = str(scrape)

y = x.replace("</b>","<start>")

x = y.replace("<b>","</start>")

list_string = x.split('INT.')

# # print(list_string)

int2int = '--------'.join(list_string)
# # print(int2int)

list_Estring = int2int.split('EXT.')

parts = '--------'.join(list_Estring)

# print(parts)

final_p = parts.split('--------')

# print(final_p)


# print(x)

# file = open("strop.html","w")

# file.write(parts)

# file.close()

# with open('strop.html', 'r') as f:

#     contents = f.read()

#     soup = BeautifulSoup(contents,'html.parser')

Final_script =[]

for l_parts in final_p:

    soup = BeautifulSoup(l_parts,'html.parser')

    # print(soup)

    btags = soup.findAll("start")
    # print(btags)

    data=[] 

    for para in soup.find_all("start"):
        # print(para.get_text())
        data.append(para.get_text())

    # spli_n = data[6].split('\n')

    final_dialogues =[]
    for i in data:
        spli_n = i.split('\n')

        dialogues = []
        for part in spli_n:
            if part != "":
                
                dialogues.append(part)
        final_dialogues.append(dialogues)


    # print(final_dialogues)

    dias = []

    for parts in final_dialogues:

        subdias =[]
        for subparts in parts:
            if "               " in subparts:
                str = subparts.strip()
                subdias.append(str)
        
        dias.append(subdias)


    final_script =[]
    for i in dias:
        str=""
        for j in i:
            str += " "
            str += j

        if str != "":
                
            final_script.append(str)

            # print(j)
        

    # print(final_script)
    final_dia = ""
    if final_script !="":

        for i in final_script:
            final_dia +="  "
            final_dia +=i 
    
        Final_script.append(final_dia)
    

final =[]
for idx,k in enumerate(Final_script):
    if k !="":
        # str1 = str(idx)
        # l = str1+" "+k
        final.append(k)
    # print(k)

    # print("\n-----\n")
# print(final)

# for i in final:
#     print(i)
#     print("\n-------\n")


fileSub = open("dwp.txt", encoding="utf-8")

contentSub = fileSub.read()                                     #full subtitle file

listSub = contentSub.split("\n\n")

listSubLower = []                                               #has the content in lowercase
ScriptpartLow = []

for i in listSub:                                               #converting everything in listSub to lowercase and appending it to a new list
    x = i.lower()
    listSubLower.append(x)

for i in final:                                               #converting everything in CoList2 to lowercase and appending it to a new list
    x = i.lower()
    ScriptpartLow.append(x)



Scriptedit1 = []

for i in ScriptpartLow:                                            #making short forms of have to full forms
    x = i.replace("'ve", " have")
    x = x.replace("...", " ")
    x = x.replace("--", " ")
    # x = x.replace("\n\n"," ")
    # x = x.replace("\n"," ")

    Scriptedit1.append(x)


Subedit1 = []

for i in listSubLower:                                          #making short forms of have to full forms
    x = i.replace("'ve", " have")
    Subedit1.append(x)

punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''                       #punctuation

Scriptedit2 = []                                                    #has lowercase content without '\n' chars


for i in Scriptedit1:                                           #removing all the '\n' chars and appending it to a new list
    
    x = i

    for ele in punc:
        x = x.replace(ele, "")

    Scriptedit2.append(x)

# for idx,i in enumerate(Scriptedit2):
#     print(idx,i)
# print(Scriptedit2)

dict = {0: {"dialogueNo" : "0", "scene" : 0, "timeStamp" : "00:00:00", "dialogue" : " ", "change" : False}}

def dictMaker(s, idx, subDialogue):                      #makes a dictionary
    dict[subDialogue[0]] = {}
    dict[subDialogue[0]]["dialogueNo"] = subDialogue[0]
    dict[subDialogue[0]]["scene"] = idx
    dict[subDialogue[0]]["timestamp"] = subDialogue[1]

    str1 = ""                                           #empty string
    # traverse in the string
    for ele in subDialogue[s]:                          #converting a list to a string
        str1 += ele

    dict[subDialogue[0]]["dialogue"] = str1             #stores dialogue(string)
    dict[subDialogue[0]]["change"] = False              #stores where the cut-to num changes


before = 0
flag = 0
notfoundc = 0                                       #stores the number of dialogues that aren't found
foundc = 0                                         #stores the number of dialogues found in script file from the subtitle file

for j in Subedit1:                            #has paragraphs of subtitles   --> we are splitting every paragraph into:
    subDialogue = j.split("\n")                   #{"1486", "02:49:52,390 --> 02:49:55,225'", "I'm not gonna be coming back,to this place."}

    if len(subDialogue) < 2:                      # then dialogue doesn't exist
        continue                                  #then continue

    x = subDialogue[2]                            #else first dialogue starts from 2

    flag = 0                                            #indicates whether dialogue is found or not

    for ele in x:                                       #removing punc in dialogues(index -1)
        if ele in punc:
            x = x.replace(ele, "")

    for idx, i in enumerate(Scriptedit2):                            #idx is iterator(scene number), i has cuto no in cut to - cut to (in paragraphs)
        
        # if (idx==before):                 #to ensure the dialogue is in the present index or in the ones after this
        if(i.find(x) != -1):                                 #if we find the dialogue
            # print(subDialogue[0],x , idx)                   #print the dialogue no., dialogue and the cut-to index
            s = slice(2, len(subDialogue))                   #contains full dialogue
            dictMaker(s, idx, subDialogue)                   #passing sliced dialogue, scene index, and subDialogue list
            flag = 1
            foundc +=1
            #print(foundc)                                    #prints the number of dialogues found
            before = idx
            break

        else:
            if (flag == 0) :
                fcount = 0                                         #found count
                sentence = x.split(" ")                            #dialogue -> word by word  , x-->dialogue
                totcount = len(sentence)                           #size of the dialogue
                for word in sentence:                              #for every word in dialogue
                    if (Scriptedit2[before].find(word) != -1):         #searching word in Scriptedit2()
                        fcount += 1

                percentage = fcount/totcount
                
                if(percentage >= 0.6):
                    # print(subDialogue[0], x , before)
                    s = slice(2, len(subDialogue))                          #slices the dialogue from the subDialogue list
                    dictMaker(s, idx, subDialogue)
                    foundc += 1
                    flag = 1
                    before = idx
                    break
                else:
                    # print(subDialogue[0],x , before,percentage)
                    s = slice(2, len(subDialogue))                          #slices the dialogue from the subDialogue list
                    dictMaker(s, before, subDialogue)

        
    if flag == 0:                                               #not found dialogues
        notfoundc += 1
    else:
        break
        #print(subDialogue[0],x , idx)
        #print(notfoundc)                                         #prints the number of dialogues not found

# print(before)

def string_found(string1, string2):
    if re.search(r"\b" + re.escape(string1) + r"\b", string2):
        return True
    return False

before= 0                           ######ADDED########
flag = 0
notfoundc = 0                                       #stores the number of dialogues that aren't found
foundc = 0 

for j in Subedit1:                            #has paragraphs of subtitles   --> we are splitting every paragraph into:
    subDialogue = j.split("\n")                   #{"1486", "02:49:52,390 --> 02:49:55,225'", "I'm not gonna be coming back,to this place."}

    if len(subDialogue) < 2:                      # then dialogue doesn't exist
        continue                                  #then continue

    x = subDialogue[2]                            #else first dialogue starts from 2
    # print(x)
    flag = 0                                            #indicates whether dialogue is found or not

    for ele in x:                                       #removing punc in dialogues(index -1)
        if ele in punc:
            x = x.replace(ele, "")

    for idx, i in enumerate(Scriptedit2):                            #idx is iterator(scene number), i has cuto no in cut to - cut to (in paragraphs)
        
        if (idx>before-1 and idx<before+3):                 #to ensure the dialogue is in the present index/next/next
            if(i.find(x) != -1):                                 #if we find the dialogue
                # print(subDialogue[0],x , idx)                   #print the dialogue no., dialogue and the cut-to index
                s = slice(2, len(subDialogue))                   #contains full dialogue
                dictMaker(s, idx, subDialogue)                   #passing sliced dialogue, scene index, and subDialogue list
                flag = 1
                foundc +=1
                #print(foundc)                                    #prints the number of dialogues found
                before = idx
                break

            else:
                if (flag == 0) :
                    fcount = 0                                         #found count
                    sentence = x.split(" ")                            #dialogue -> word by word  , x-->dialogue
                    totcount = len(sentence)                           #size of the dialogue

                    for word in sentence:                              #for every word in dialogue
                        # if (Scriptedit2[idx].find(word) != -1):         #searching word in Scriptedit2()
                        # if(word in Scriptedit2[idx]):
                        if(string_found(word,Scriptedit2[idx] )):
                            # print("FOUND#########")
                            fcount += 1


                    percentage = fcount/totcount
                    
                    if(percentage >= 0.4):
                        # print(subDialogue[0], x , before ,percentage, Scriptedit2[idx])
                        s = slice(2, len(subDialogue))                          #slices the dialogue from the subDialogue list
                        dictMaker(s, idx, subDialogue)
                        foundc += 1
                        flag = 1
                        before = idx
                        break
        
                    else:
                        # print(subDialogue[0],x , before,percentage,idx)
                        s = slice(2, len(subDialogue))                          #slices the dialogue from the subDialogue list
                        dictMaker(s, before, subDialogue)
                        
                        
    if flag == 0:                                               #not found dialogues
        
        notfoundc += 1
    
        #print(subDialogue[0],x , idx)
        #print(notfoundc)                                         #prints the number of dialogues not found



cutonum = 0

for dictNum, info in dict.items():                              #dictNum -> high level key  #initial index number of dictionary -->initial high level key
    for key in info:                                            #info -> the inner dict's key  (dialogueNo, change)
        if cutonum != info["scene"]:                           #if the number changes
            dict[dictNum]["change"] = True                      #True --> when scene num changes
    cutonum = info["scene"]                                    #initially initialised to the scene num

print("Number of dialogues found :-", foundc)
print("Number of dialogues not found :-", notfoundc)


    

