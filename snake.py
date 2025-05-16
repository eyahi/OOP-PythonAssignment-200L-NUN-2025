class Snake:
    def __init__(self):
        self.body = [[100, 50], [90, 50], [80, 50]]  # Initialize snake with 3 body segments at starting positions
        self.direction = 'RIGHT'  # Set initial movement direction to right
    
    def move(self):
        head = self.body[0][:]  # Create a copy of the current head position
        if self.direction == 'RIGHT':
            head[0] += 10  # Move head 10 pixels to the right
        elif self.direction == 'LEFT':
            head[0] -= 10  # Move head 10 pixels to the left
        elif self.direction == 'UP':
            head[1] -= 10  # Move head 10 pixels up (y decreases going up)
        elif self.direction == 'DOWN':
            head[1] += 10  # Move head 10 pixels down (y increases going down)
        self.body.insert(0, head)  # Add the new head position to the front of the body list
        self.body.pop()  # Remove the last segment of the snake (creates movement effect)
    
    def grow(self):
        self.body.append(self.body[-1])  # Add a new segment at the tail position (duplicate last segment)
    
    def check_collision(self):
        head = self.body[0]  # Get current head position
        if head in self.body[1:] or head[0] < 0 or head[0] >= 600 or head[1] < 0 or head[1] >= 400:
            return True  # Return True if snake collides with itself or hits the boundary
        return False  # Return False if no collision detected