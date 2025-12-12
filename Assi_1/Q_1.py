#Q.1 Write a Python program that takes a sentence from the user and prints:

sent = input("Enter sentence : ")
print(sent)

#Number of characters
chara = len(sent.replace(" ", ""))
print("Number of characters:", chara)

# Number of words
words = len(sent.split())
print("Number of words:", words)

# Number of vowels
vowels = "aeiouAEIOU"
count = 0
for char in sent:
    if char in vowels:
        count += 1

print("Number of vowels:", count)