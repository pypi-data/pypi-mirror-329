from .vector3 import Vector3

class RobotData():
    def __init__(self, enabled: bool, emergency: float, pressure: Vector3):
        self.enabled = enabled
        self.emergency = emergency # data to be sent to notify UI of stoppage
        self.pressure = pressure

    @staticmethod
    def fromDict(robot_data):
        return RobotData(
            robot_data["enabled"],
            robot_data["emergency"],
            Vector3.fromDict(robot_data["pressure"]))

    def toDict(self):
        return {
            "enabled": self.enabled,
            "emergency": self.emergency,
            "pressure": self.pressure.toDict(),
        }

    def __eq__(self, other): 
        if not isinstance(other, RobotData):
            # don't attempt to compare against unrelated types
            return NotImplemented
        
        return self.enabled == other.enabled and \
            self.emergency == other.emergency and self.pressure == other.pressure