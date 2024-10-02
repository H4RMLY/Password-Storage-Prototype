import os.path
import Encryption

class passwordList:
    def __init__(self):
        self.list = {
        }
        self.filename = 'passwords.txt'
        self.filepath = './' + self.filename
    
    def addItem(self, outerKey, listItem):
        '''Adds an item to the list'''
        self.list[outerKey] = listItem

    def removeItem(self, listItem):
        '''Removes a specified item from the list'''
        self.list.pop(listItem)

    def getList(self):
        '''Returns all items in list'''
        return self.list
    
    def editItem(self, listKey, newItem):
        '''Edits specified key in the list'''
        self.list[listKey] = newItem
    
    def getItem(self, listKey):
        '''Returns the specified item from the list'''
        return self.list[listKey]
    
    def addToFile(self, key, item):
        '''Adds an item to the file'''
        file = open(self.filepath, 'a')
        file.write(key + ":" + item + "\n")
        file.close()
    
    def readFile(self):
        '''Reads the file and adds it to the list'''
        if os.path.isfile(self.filepath):
            with open(self.filepath,"r") as passwordFile:
                lines = passwordFile.read().splitlines()
                for line in lines:
                    keyAndItem = line.split(":")
                    key = keyAndItem[0]
                    item = Encryption.decrypt(keyAndItem[1], "tempKey")
                    self.list[key] = item
            passwordFile.close()
        else:
             return "File does not exist"
    
    def saveList(self):
        '''Saves the list to the file'''
        if os.path.isfile(self.filepath):
            output = ""
            for x, y in self.list.items():
                y = Encryption.encrypt(y, "tempKey")
                output += x + ":" + y + "\n"
            with open(self.filepath, "w") as passwordFile:
                passwordFile.write(output)
                passwordFile.close()
        else:
            return "File does not exist"
        
    def createFile(self):
        if not os.path.isfile(self.filepath):
            file = open(self.filepath, 'a')
            file.close()
            
    def deleteFile(self):
        if os.path.isfile(self.filepath):
           with open(self.filepath, "a") as passwordFile:
               passwordFile.delete()    
      
    def __str__(self):
        '''Returns a formatted list of all items'''
        output = ""
        for x, y in self.list.items():
            output += x + " : " + y + "\n"
        return output
                      ### BACK END ###
#################################################################
                      ### FRONT END ###
from tkinter import *
import random, string

passList = passwordList()

def main():
    passList.createFile()
    passList.readFile()
    mainWin = Tk()
    mainWin.title("Password List")
    mainWin.rowconfigure(10, weight=1)
    drawList(mainWin)
    mainWin.mainloop()
    

def drawList(mainWin):
    valueLabel = Label(mainWin, text="Index")
    valueLabel.grid(row=0, column=0)
    valueLabel = Label(mainWin, text="Username")
    valueLabel.grid(row=0, column=1)
    valueLabel = Label(mainWin, text="Password")
    valueLabel.grid(row=0, column=2)
    
    ##Draws the keys and items on screen##
    count = 0
    for x, y in passList.list.items():
        key = x
        item = y
        indexLabel = Label(mainWin, text=count+1)
        indexLabel.grid(row=count+1, column=0)
        
        deviceText = Text(mainWin, height=1, width=30)
        deviceText.insert("1.0", key)
        deviceText.grid(row=count+1, column=1)
        
        deviceText = Text(mainWin, height=1, width=30)
        deviceText.insert("1.0", item)
        deviceText.grid(row=count+1, column=2)
        
    ##Draws the buttons on screen##

        editButton = (Button(mainWin, text="Edit Pass", command=lambda key=key: editPassCommand(key, mainWin)))
        editButton.grid(row=count+1, column=3)
        
        deleteButton = (Button(mainWin, text="X", command=lambda key=key: removeItemCommand(key,mainWin)))
        deleteButton.grid(row=count+1, column=4)
        count += 1
    
    addButton = (Button(mainWin, text="Add", command=lambda mainWin=mainWin: addItemCommand(mainWin)))
    addButton.grid(row=count+1, column=1)
    
    saveButton = (Button(mainWin, text="Save", command=saveCommand))
    saveButton.grid(row=count+1, column=2)
    
def editPassCommand(key, mainWin):
    modifyWin = Tk()
    modifyWin.title("Edit")
    
    def applyChanges():
        passList.editItem(key, itemEntry.get())
        drawList(mainWin)
        modifyWin.destroy()
    
    def randomPasswordCommand():
        itemEntry.delete(0,END)
        itemEntry.insert(0,randomPassword())
        
    itemEntry = Entry(modifyWin)
    itemEntry.pack(fill='x', expand=True)
    
    applyButton = Button(modifyWin, text="Apply", command=applyChanges)
    applyButton.pack(fill='x', expand=True)
    
    randButton = Button(modifyWin, text="Generate Random Password", command=randomPasswordCommand)
    randButton.pack(fill='x', expand=True)     
    
def removeItemCommand(key, mainWin):
    passList.removeItem(key)
    passList.saveList()
    mainWin.destroy()
    main()

def saveCommand():
    passList.saveList()

def randomPassword():
        password = ""
        length = random.randint(12,18)
        for i in range(length):
            charNum = random.randint(0,2)
            if charNum == 0:
                password += random.choice(string.ascii_letters)
            if charNum == 1:
                password += random.choice(string.digits)
            if charNum == 2:
                password += random.choice(string.punctuation)
        return password

def addItemCommand(mainWin):
    addWin = Tk()
    addWin.title("Add Details")
    userLabel = Label(addWin, text="Username")
    userLabel.grid(row=0, column=0)
    passLabel = Label(addWin, text="Password")
    passLabel.grid(row=0, column=1)
    
    innerKeyEntry = Entry(addWin)
    innerKeyEntry.grid(row=1, column=0)
    itemEntry = Entry(addWin)
    itemEntry.grid(row=1, column=1)
    
    def add(mainWin):
        passList.addItem(innerKeyEntry.get(), itemEntry.get())
        passList.saveList()
        drawList(mainWin)
        addWin.destroy()
        mainWin.destroy()
        main()
    
    def randomPasswordCommand():
        itemEntry.delete(0,END)
        itemEntry.insert(0,randomPassword())
        
    saveButton = (Button(addWin, text="Save", command=lambda mainWin=mainWin: add(mainWin)))
    saveButton.grid(row=2, column=0)
    
    randButton = Button(addWin, text="Generate Random Password", command=randomPasswordCommand)
    randButton.grid(row=2, column=1)
    
main()