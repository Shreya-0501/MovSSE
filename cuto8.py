import string
import re
import pprint
import stanza
#import spacy
#from spacy import displacy
from collections import Counter
#import en_core_web_sm
#nlp = en_core_web_sm.load()
#spacy.load('en_core_web_trf')

#THE BREAKFAST CLUB

#class Segregate :

#file = open("tbcsc.txt", "r")                                   #script file
#fileSub = open("tbcsub.txt", "r")                               #subtitle file

#file = open("bttf.txt", "r")                                   #script file
#fileSub = open("bttfSc.txt", "r")                               #subtitle file

file = open("hangsc.txt", "r")                                   #script file
fileSub = open("hangsub.txt", "r")                               #subtitle file

# Reading from file
Content = file.read()                                           #full script file
contentSub = fileSub.read()                                     #full subtitle file

CoList2 = Content.split("CUT TO:")                              #stores cut to - cut to
listSub = contentSub.split("\n\n")                              #splits the subtitle file paragraph to  paragraph (dialogue no., timestamp, dialogue)

listSubLower = []                                               #has the content in lowercase
CoList2Low = []

for i in listSub:                                               #converting everything in listSub to lowercase and appending it to a new list
    x = i.lower()
    listSubLower.append(x)

for i in CoList2:                                               #converting everything in CoList2 to lowercase and appending it to a new list
    x = i.lower()
    CoList2Low.append(x)


CoListFullf = []

for i in CoList2Low:                                            #making short forms of have to full forms
    x = i.replace("'ve", " have")
    x = x.replace("...", " ")
    x = x.replace("--", " ")
    CoListFullf.append(x)

#print(CoListFullf)

listSubFullf = []

for i in listSubLower:                                          #making short forms of have to full forms
    x = i.replace("'ve", " have")
    listSubFullf.append(x)

punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''                       #punctuation

CoList3 = []                                                    #has lowercase content without '\n' chars
CoListn = []

for i in CoListFullf:                                           #removing all the '\n' chars and appending it to a new list
    #x = i
    x = i.replace("\n\n", " ")
    x = x.replace("\n", " ")
    #x = x.replace("  ", " ")
    for ele in x:
        if ele in punc:
            x = x.replace(ele, "")
    CoList3.append(x)

#print(CoList3)

dict = {0: {"dialogueNo" : "0", "cut to" : 0, "timeStamp" : "00:00:00", "dialogue" : " ", "change" : False}}

def dictMaker(s, idx, subDialogue):                      #makes a dictionary
    dict[subDialogue[0]] = {}
    dict[subDialogue[0]]["dialogueNo"] = subDialogue[0]
    dict[subDialogue[0]]["cut to"] = idx
    dict[subDialogue[0]]["timestamp"] = subDialogue[1]

    str1 = ""                                           #empty string
    # traverse in the string
    for ele in subDialogue[s]:                          #converting a list to a string
        str1 += ele

    dict[subDialogue[0]]["dialogue"] = str1             #stores dialogue(string)
    dict[subDialogue[0]]["change"] = False              #stores where the cut-to num changes

#for cut in CoList3:
    #print(cut , "\n")

#print(*CoList2, sep = "\n\n")
#print(*listSub, sep = "\n\n")

before = 0
flag = 0
counter = 0                                       #stores the number of dialogues that aren't found
count = 0                                         #stores the number of dialogues found in script file from the subtitle file

for j in listSubFullf:                            #has paragraphs of subtitles   --> we are splitting every paragraph into:
    subDialogue = j.split("\n")                   #{"1486", "02:49:52,390 --> 02:49:55,225'", "I'm not gonna be coming back,to this place."}

    if len(subDialogue) < 2:                      # then dialogue doesn't exist
        continue                                  #then continue
    x = subDialogue[2]                            #else first dialogue starts from 2

    flag = 0                                            #indicates whether dialogue is found or not

    for ele in x:                                       #removing punc in dialogues(index -1)
        if ele in punc:
            x = x.replace(ele, "")

    for idx, i in enumerate(CoList3):                            #idx is iterator(cut to number), i has script in cut to - cut to (in paragraphs)
        if ((idx<=before+3) and (idx>before-1)):                 #to ensure the dialogue is in the present index or in the ones after this
            if(i.find(x) != -1):                                 #if we find the dialogue
                #print(subDialogue[0],x , idx)                   #print the dialogue no., dialogue and the cut-to index
                s = slice(2, len(subDialogue))                   #contains full dialogue
                dictMaker(s, idx, subDialogue)                   #passing sliced dialogue, cut to index, and subDialogue list
                flag = 1
                count +=1
                #print(count)                                    #prints the number of dialogues found
                before = idx
                break

            else:
                if flag == 0 :
                    fcount = 0                                         #found count
                    sentence = x.split(" ")                            #dialogue -> word by word  , x-->dialogue
                    totcount = len(sentence)                           #size of the dialogue
                    for word in sentence:                              #for every word in dialogue
                        if (CoList3[before].find(word) != -1):         #searching word in CoList3()
                            fcount += 1

                    percentage = fcount/totcount

                    if(percentage >= 0.75):
                        #print(subDialogue[0], "   ",x , before, "hoi found it by the new else")
                        #print(subDialogue[0], x , before)
                        s = slice(2, len(subDialogue))                          #slices the dialogue from the subDialogue list
                        dictMaker(s, idx, subDialogue)
                        count += 1
                        flag = 1

    if flag == 0:                                               #not found dialogues
        counter += 1
        #print(counter)                                         #prints the number of dialogues not found

cutonum = 0

for dictNum, info in dict.items():                              #dictNum -> high level key  #initial index number of dictionary -->initial high level key
    for key in info:                                            #info -> the inner dict's key  (dialogueNo, change)
        if cutonum != info["cut to"]:                           #if the number changes
            dict[dictNum]["change"] = True                      #True --> when cut to num changes
    cutonum = info["cut to"]                                    #initially initialised to the cut to num

print("Number of dialogues not found :-", counter)
print("Number of dialogues found :-", count)

#pprint.pprint(dict, sort_dicts = False)

#nlp = stanza.Pipeline('en')                    #for stanza
nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')

#print(CoList2[5])
#character[]

for para in CoList2:
    doc = nlp(para)
    for ent in doc.ents:
        if ent.type == 'PERSON':
            print("Person: ", ent.text)
        if ent.type == 'GPE':
            print("GPE:    ",ent.text)

    print("\n###\n")
#doc2 = nlp("hawaii.")                          #for stanza
#print(doc2)

# doc = nlp(CoList3[5])
#
# pprint([(X.text, X.label_) for X in doc.ents])
