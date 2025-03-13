class Processor:
    def __init__(self):
        """
        Initialize the TrajectoryProcessor with data.
        
        """ 
        self.data = [(i, i + 1) for i in range(10)]

    def calculate_distance(self):
        """
        Calculate the total distance traveled along the trajectory.
        
        :return: The total distance as a float.
        """
        distance = 0
        for i in range(1, len(self.data)):
            distance += ((self.data[i][0] - self.data[i-1][0])**2 + (self.data[i][1] - self.data[i-1][1])**2)**0.5
        return distance