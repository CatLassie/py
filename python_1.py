# basic python, partially from:
# https://app.pluralsight.com/library/courses/python-3-fundamentals/table-of-contents

import logging as lg
import os

# types

def show_types():
    intgr = 4
    print(intgr, type(intgr))

    flt = float(4)
    print(flt, type(flt))

    bln = True
    print(bln, type(bln))

    strng = 'hello'
    print(strng, type(strng))

    print('')



# input

def show_input():
    from_user = input('input please!\n')
    print(f'input from user: {from_user}')



def calc_age():
    age_input = input('How old are you?\n')
    
    # doesnt work cause age_input is always initially a string
    # if type(age_input) != int:
    #     raise Exception('Age should be an integer!')
    
    age = None
    try:
        age = int(age_input)
    except:
        lg.exception('Age should be an integer!')
        raise
    finally:
        print('Funally block!')

    decades = age // 10
    years = age % 10
    print(f'You are {decades} decades and {years} years old')

    print('')



def between():
    nmbr = int(input('number please!\n'))
    if nmbr < 100 and nmbr > 10:
        print('Boring number!')
    else:
        print('Fascinating number!')



#lists and dicts

def lists():
    l = ['thing', 'not thing']

    for i, el in enumerate(l):
        lg.log(30, f'list item {i+1} is: {el}')

    for i, el in enumerate(range(0, 10, 3)):
        if el == 3:
            print('skipping remaining loop logic')
            continue

        print(f'hey {i}: {el}')

        if el == 6:
            print('stopping loop')
            break

    if 'thing' in l:
        print('thing is in the list!\n')
        return
    print('thing is NOT in the list! :(')

    print('')



def dicts(just_an_arg):
    d = {'k1': 'v1',
        'k2': 'v2',
        'k3': 'v3'}
    
    print(f'function arg: {just_an_arg}')
    print(f'dict value 1: {d["k1"]}, {d.get("k1")}')

    for key, val in d.items():
        print('dict key', key)
        print('dict value', val)

    print('')



#classes

class Dog:
    def __init__(self, name: str, breed: str) -> None:
        self.name = name
        self.breed = breed

    def count_legs(self) -> int:
        return 4

class Robot_Dog(Dog):
    def __init__(self, name: str, breed: str, voltage: int) -> None:
        super().__init__(name, breed)
        self.voltage = voltage

    def robot_bark(self) -> None:
        print(f'woof I am {self.breed} with {self.voltage} voltage!')

    def count_legs(self) -> int:
        return super().count_legs() * 2

def dog_example():
    dog = Robot_Dog('RoboDog', 'RoboDogBreed', 400)

    print(f'dog: {dog.name}')
    dog.robot_bark()
    print(dog.count_legs())

    print('')



# file management

def rd_file() -> None:
    with open('input_file.txt') as f:
        result = f.read()
        print('all:', result)

    with open('input_file.txt') as f:
        result = f.readlines()
        print('lines:', result)

    with open('input_file.txt') as f:
        result = f.readline()
        print('line:', result)

    with open('input_file.txt') as f:
        for l in f:
            print('loop line:', l)

    print('')



def wrt_file(): 
    with open('input_file_write.txt', 'a') as f: # 'a' is for "append", 'w' would be for "write", it replaces contents
        f.write('new line in file!\n')



def misc_file():
    curr = os.getcwd()
    entries = os.scandir(curr)
    for e in entries:
        print(f'entry: {e.name}')

    with open(os.path.join(curr, 'input_file.txt')) as f:
        result = f.read()
        print('all from path:', result)



def main():
    show_types()
    #show_input()
    #calc_age()
    #between()
    lists()
    dict_arg: str = None
    dicts(dict_arg)
    dog_example()
    rd_file()
    #wrt_file()
    misc_file()

if __name__ == '__main__':
    main()