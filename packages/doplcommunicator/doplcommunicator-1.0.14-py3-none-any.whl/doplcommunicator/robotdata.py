from .vector3 import Vector3
from .pose import Pose

class RobotData():
    def __init__(self, enabled: bool, emergency: float, robot_pose: Pose, camera_pose: Pose, pressure: Vector3):
        self.enabled = enabled
        self.emergency = emergency # data to be sent to notify UI of stoppage
        self.robot_pose = robot_pose
        self.camera_pose = camera_pose
        self.pressure = pressure

    @staticmethod
    def fromDict(robot_data):
        return RobotData(
            robot_data["enabled"],
            robot_data["emergency"],
            Pose.fromDict(robot_data["robot_pose"]),
            Pose.fromDict(robot_data["robot_pose"]),
            Vector3.fromDict(robot_data["pressure"]))
    
    def toDict(self):
        return {
            "enabled": self.enabled,
            "emergency": self.emergency,
            "robot_pose": self.robot_pose.toDict(),
            "camera_pose": self.camera_pose.toDict(),
            "pressure": self.pressure.toDict(),
        }

    def __eq__(self, other): 
        if not isinstance(other, RobotData):
            # don't attempt to compare against unrelated types
            return NotImplemented
        
        return self.enabled == other.enabled and \
            self.emergency == other.emergency \
            and self.robot_pose == other.robot_pose and \
            self.camera_pose == other.camera_pose\
            and self.pressure == other.pressure
