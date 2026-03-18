import math

def projectilemotion_solver(vi, angle):
    
    radian = math.radians(angle)
    
    #for the sin2theta part, it is simply the double angle identity because I 
    r = ((vi)**2 * (2 * (math.sin(radian)) * (math.cos(radian)))) / 9.8
    
    h = ((vi)**2 * (2 * (math.sin(radian)) * (math.cos(radian)))) / (2*9.8)
    
    print("The horizontal direction travelled is: ", r, " m/s.")
    print("The maximum height reached is: ", h , " m.")
    

velocity = int(input("Enter initial velocity: "))
degrees = int(input("Enter angle in degrees: "))

projectilemotion_solver(velocity, degrees)
    
    
