#name = ''
#while name != 'your name':
#    print("PLease type your name")
#    name = input()
#print("Thank you")

#while True:
#    print("PLease enter your name: ")
#    name = input()
#    if(name == 'your name'):
#        break

#print("Thank you")

while True: 
    print("Enter username: ")
    username = input()
    if username != 'Joe':
        continue
    print("Welcome," + username + ", PLease enter your password: ")
    password = input()
    if password == "asdfg":
        break

print("Access Granted")