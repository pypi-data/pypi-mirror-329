==========
Philosophy
==========

Nullspace package offers you a new floating base robotics control strategy.

Intuitively, we might wanna control the orientation and position of base directly or by any
inverse kinematics like approach. However, the contact point between legs and ground
which could be abstracted to a ball joint hinge make it almost impossible. Others try to introduce
the 6 more dimensions in configuration space for base directly. However, control position and 
orientation of base directly is unrealistic.

In assumption that contract points isn't slip, connecting all contact points could form a virtual 
rigid object, a object that has all contact points fixed on it. In other words, The distance between any two given contact points on this virtual rigid body remains constant. Control this virtual rigid body 
enable us control base. By doing this, forward caluculation is all you need.


In a prioritized tasks definition:
We might have a tasks from higher priority to lower:

  1.fixed distance between each end effectors, that's conbination of N
  2.there is a target position of Object
  3.there is a target orientation Object

These tasks could be achieved by nullspace method

Some examples which could be benefit from this strategy:

Robot hand(3 fingers)
There is a triangle between 3 fingers. If you coordinate control task 2 and 3 together by considering lead of screw, bottle cap could be moved very
decently.

Qudrupeds(4)

Hexapods(6)

Octopods(8)
