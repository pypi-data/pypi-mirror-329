# JsonHandler

This is a simple package that allows you to store nested Model objects in a JSON file. Completely asynchronous and allows the json file to be edited then rebooted. 

Example Usage:
```python
class People(CustomModel):
    name: Name
    age: int

class Name(CustomModel):
    first: str
    last: str
    
class Data(CustomModel):
    people: list[People]

json_handler = JsonHandler(Data, "data.json")

# prints the first name of the first person
if json_handler.data.people:
    print(json_handler.data.people[0].name.first)
else:
    # if there is no data, add some
    json_handler.data.people.append(People(name=Name(first="John", last="Doe"), age=30))
```