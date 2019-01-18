# Game-Project

LIBRARIES
-pygame
-pyTMX

ISSUE:
To make the ball bounce, all wall X and Y positions were appended to 2 arrays.
The ball would then move with an X velocity and if a collision was detected, it would check if the ball's X pos was in the X array.
If it was, it would reflect the ball along x-axis.
This also occured for the Y positions and axis.
However, the position of the ball on collision was never exactly equal to the X/Y of the walls, usually off by -4 to 4 pixels.
So if the ball collided with the corner of a wall, it wouldn't know whether to reflect X or Y, since the X and Y positions overlapped

TODO:
- redo the ball collision and rebound code
