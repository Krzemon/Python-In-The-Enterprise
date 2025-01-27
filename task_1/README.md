# Task 1

## Write a module that will simulate autonomic car.
The simulation is event based, an example:
car1 = Car()
car1.act(event)
print(car1.wheel_angle, car1.speed)
where event can be anything you want, i.e. :
`('obstacle', 10)` where `10` is a duration (time) of the event.
#The program should:
- act on the event
- print out current steering wheel angle, and speed
- run in infinite loop
- until user breaks the loop

The level of realism in simulation is of your choice, but more sophisticated solutions are better.
If you can think of any other features, you can add them.
Make intelligent use of pythons syntactic sugar (overloading, iterators, generators, etc)
Most of all: CREATE GOOD, RELIABLE, READABLE CODE.
The goal of this task is for you to SHOW YOUR BEST python programming skills.
Impress everyone with your skills, show off with your code.

Your program must be runnable with command "python task.py".
Show some usecases of your library in the code (print some things)