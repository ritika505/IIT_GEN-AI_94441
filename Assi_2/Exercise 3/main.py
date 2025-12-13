import requests

id = input("Enter ID of user : ")
try : 
    url = f"https://jsonplaceholder.typicode.com/users/{id}"

    response = requests.get(url)

    print("Status code : " ,response.status_code)
    userdata = response.json()

    print("responce data : ", userdata)
    # print("Name : ",userdata["name"])
    print("Address : ",userdata["address"]["city"])
    print("Company : ",userdata["company"]["name"])


except :
   print("Error occured...!")
