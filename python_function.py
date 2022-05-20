#print("Hola Mundo")
passwordFile = open('SecretPassword.txt')
secretPassword = passwordFile.read()
print(type(secretPassword))
typedPassword = input("Enter your password: ")
print(type(typedPassword))
if typedPassword == secretPassword:
    print("Access Granted")
    if typedPassword == '12345':
        print("Your password is weak")
else: 
    print("Access denied")
