# Steel Hero

LIBRARIES TO INSTALL
- pyGame
- pyTMX

ISSUE:
- If the ball hits the corner of a collider (wall), it does not know which direction to deflect to, often deflecting in the wrong direction.

HOW IT WORKS SO FAR:
- If the ball collides with a change in xPos, its xVel is reflected (*-1).
- If the ball collides with a change in yPos, its yVel is reflected (*-1).

- Upon a wall collision, the position of the ball is checked with an array containing all wall positions. If the ball's position is with the wall, the rebound is allowed to occur.


TODO:
- redo/modify the ball collision and rebound code

WHERE:
- found in the sprites.py file under the class BULLET and OBSTACLE
