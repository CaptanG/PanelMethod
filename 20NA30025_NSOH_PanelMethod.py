import numpy as np
from math import pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define a class Point
class Point:

    def __init__(self, x, y ,z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"    # When we print a Point this will be the syntax
 
# Define a class Vector
class Vector:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.x = self.end_point.x - self.start_point.x
        self.y = self.end_point.y - self.start_point.y
        self.z = self.end_point.z - self.start_point.z
        self.magnitude = self.calculate_magnitude()

    def calculate_magnitude(self):
        x_diff = self.end_point.x - self.start_point.x
        y_diff = self.end_point.y - self.start_point.y
        z_diff = self.end_point.z - self.start_point.z
        magnitude = (x_diff**2 + y_diff**2 + z_diff**2)**0.5
        return magnitude

    def cross_product(self, other_vector):
        cross_x = self.y * other_vector.z - self.z * other_vector.y
        cross_y = self.z * other_vector.x - self.x * other_vector.z
        cross_z = self.x * other_vector.y - self.y * other_vector.x
        return Vector(Point(0, 0, 0), Point(cross_x, cross_y, cross_z))

    def dot_product(self, other_vector):
        return self.x * other_vector.x + self.y * other_vector.y + self.z * other_vector.z

    def __str__(self):
        return f"Vector:{self.x, self.y, self.z}\n"
    
# Define a class Panel 
class Panel:
    def __init__(self, point1, point2, point3, point4):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.point4 = point4
        self.centroid = self.calculate_centroid()
        self.normal = self.calculate_normal()
        self.area = self.calculate_area()

    def calculate_centroid(self):
        x_avg = (self.point1.x + self.point2.x + self.point3.x + self.point4.x) / 4
        y_avg = (self.point1.y + self.point2.y + self.point3.y + self.point4.y) / 4
        z_avg = (self.point1.z + self.point2.z + self.point3.z + self.point4.z) / 4
        return Point(x_avg, y_avg, z_avg)
    
    def calculate_normal(self):
        v1 = Vector(self.point1, self.point2)
        v2 = Vector(self.point1, self.point3)
        v3 = Vector(self.point1, self.point4)
        a = v1.cross_product(v3)
        b = a.calculate_magnitude()
        if (b !=0):
            x_final = a.x/b
            y_final = a.y/b
            z_final = a.z/b
        else:
            x_final, y_final, z_final = 0, 0, 0
        return Vector(Point(0, 0, 0), Point(x_final, y_final, z_final))
    

    def __str__(self):
        return f"\nPanel Centroid: {self.centroid}\nNormal {self.normal}Area = {self.area}"

    def calculate_area(self):
        v1 = Vector(self.point1, self.point2)
        v2 = Vector(self.point1, self.point3)
        v3 = Vector(self.point1, self.point4)
        c = v1.cross_product(v2)
        d = v1.cross_product(v3)
        a1 = c.calculate_magnitude()
        a2 = d.calculate_magnitude()
        area = 0.5 * (a1 + a2)
        return area
    
# Define a function to read the mesh .txt file for the points
def readPoints(filename):
    points = []

    try:
        with open(filename, "r") as file:

            num_points = int(file.readline().strip()) # Reads the number of points
            print("Number of nodes = ", num_points)

            for _ in range(num_points):
                line = file.readline().strip()
                parts = line.split(",")
                if len(parts) == 4:
                    index, x, y, z = map(int, parts[0]), float(parts[1]), float(parts[2]), float(parts[3])
                    point = Point(x, y, z)
                    points.append(point)
                else:
                    print(f"Invalid line format: {line}")

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return points

# Define a function to read the order of points for the panels
def panelOrder(filename, points):
    order = []

    try:
        with open(filename, "r") as file:
            
            num_points = int(file.readline().strip())
            
            for line_number, line in enumerate(file, start=1):
                if line_number == num_points + 1:
                    num_panels = int(line.strip()) # Make sure 168th point does not have an empty line after it
            
            print("Number of panels = ",num_panels)

        with open(filename, "r") as file:        
            c = 1
            for _ in range(num_panels + num_points + 1):
                line = file.readline().strip()
                parts = line.split(",")
                if len(parts) == 5:
                    index, x, y, z, w= map(int, parts[0]), int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4])
                    o = Panel(points[x], points[y], points[z], points[w])
                    order.append(o)
                    
                #else:
                #    print(f"xD",c)
                c = c+1
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return order

# Define a function to calculate Aij
def Aij(pan1, pan2):

    r = Vector(pan1.centroid,pan2.centroid)
    magr = r.magnitude
    d = r.dot_product(pan2.normal)
    a = (d*pan2.area)/(magr**3)*pan2.area

    return a

# Define a function to bi
def Bi(pan1, pan2):

    r = Vector(pan1.centroid, pan2.centroid)
    magr = r.magnitude
    b = (1/magr)*(pan2.area)*pan2.normal.z

    return b

# Define a function to plot the panels
def Plot(pan):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    n = len(pan)
    #print(n)
    x = np.zeros((n,5))
    y = np.zeros((n,5))
    z = np.zeros((n,5))

    for i in range(0,n):

        x[i][0] = pan[i].point1.x
        y[i][0] = pan[i].point1.y
        z[i][0] = pan[i].point1.z

        x[i][1] = pan[i].point2.x
        y[i][1] = pan[i].point2.y
        z[i][1] = pan[i].point2.z

        x[i][2] = pan[i].point3.x
        y[i][2] = pan[i].point3.y
        z[i][2] = pan[i].point3.z

        x[i][3] = pan[i].point4.x
        y[i][3] = pan[i].point4.y
        z[i][3] = pan[i].point4.z

        x[i][4] = pan[i].point1.x
        y[i][4] = pan[i].point1.y
        z[i][4] = pan[i].point1.z

        ax.plot(x[i], y[i], z[i], color='b')


    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    return plt.show()

filename = "mesh_nptel.txt"

# Get all the points from the file
coords = readPoints(filename)

# Create the panels from the mesh given in the file
pans = panelOrder(filename, coords)
n = len(pans)

# Initialize the matrices
A_mat = np.zeros((n, n))
B_mat = np.zeros((n,1))

# Get values for B matrix
for i in range (0,n):
    sum =0
    for j in range(0,n):
        if(i!=j):
            sum = sum + Bi(pans[i],pans[j])
        
        B_mat[i]=sum

# Get values for A matrix
for i in range(0,n):
    for j in range(0,n):
        if(i == j):
            A_mat[i, j] = -2*pi
        else:
            A_mat[i, j] = Aij(pans[i],pans[j])

if(np.linalg.det(A_mat) != 0):
    A_inv = np.linalg.inv(A_mat)
else:
    print("Error: The A[] Matrix is not invertible")

# Calculate Phi matrix
Phi_mat = np.dot(A_inv, B_mat)

# print(Phi_mat)

#for i in range(n):
 #   print(pans[i].normal)

sum_1 = 0

# Calculate Added Mass
for i in range(0,n):
    sum_1 = sum_1 + Phi_mat[i]*pans[i].normal.z*pans[i].area

sum_1 = abs(1.025*sum_1*2)

print("Added Mass =",sum_1) 

# Plot(pans)