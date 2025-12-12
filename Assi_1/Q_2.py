numbers = input("Enter numbers (comma-separated): ")

num_list = [int(x) for x in numbers.split(",")]

even_count = 0
odd_count = 0
zero_count = 0
for n in num_list:
    if n == 0:
       zero_count +=1
    elif  n % 2 == 0 and n != 0:
        even_count += 1
    else:
        odd_count += 1

print("Total Zero present:", zero_count)
print("Even numbers:", even_count)
print("Odd numbers:", odd_count)
