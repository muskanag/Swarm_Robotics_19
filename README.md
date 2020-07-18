# Swarm_Robotics
Swarm robotics is the study of how to coordinate rhead large groups of relatively simple robots through the use of local rules. It takes its inspiration from societies of insects that can perform tasks that are beyond the capibilities of the individuals.

### GUI

We have an overhead camera mounted to capture the view of the whole aren acontinously and detect the location and orientation of the robots through unique aruco marker placed on top of each robot. The user then inputs any shape into the GUI, which we map to the arena as the final coordinates that the robots must move to.

![GUI](https://github.com/muskanag/Swarm_Robotics_19/blob/master/GUI.png)
![GUI with shape given by the user](https://github.com/muskanag/Swarm_Robotics_19/blob/master/GUIwithshape.png)

---

### Hardware used for the robot:
- Motor Driver
- 3 wheels(2 normal wheels and 1 castor wheel)
- NodeMCU
- 3-5volt Battery
- 2 IR sensors

A overhead logitech camera was used as a central network.

![Hardwareof our robot](https://github.com/muskanag/Swarm_Robotics_19/blob/master/hardware.jpg)

---

# Aruco Marker generation and Detection
We used OpenCV in python to generate and detect the ArUco Marker. The axes in ArUco markers are in pre-defined orientation and can be found by finding angle between one of the side of arena and x-axis of marker. Then apply cropping, and perspective transform to get final image of arena.

# Getting the Goal Location
The GUI gets input of the shape drawn by the user(certain pixels in image of arena make one cell on GUI). Then the shape is selected depending on the number of robots.

# Planning the Path
We used CBS(Conflict-Based Search) path planning algorithm. CBS is a two level algorithm that does not convert the problem into the single 'joint agent' model. At the high level, a search is performed on a Conflict Tree(CT) which is a tree based on conflicts between individual agents.

# Communication between Robots
We used NodeMCU to share the data robot and the central server. They shared the information like the current position of the robot and it's and final goal, it's orientation. Then NodeMCU drives motors through motor driver to ultimately reach final location.
