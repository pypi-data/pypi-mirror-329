
class DepthCameraData():
    def __init__(self, point_cloud, distance_from_patient: float):
        self.point_cloud = point_cloud
        self.distance_from_patient = distance_from_patient
    
    @staticmethod
    def fromDict(depth_camera_data):
        return DepthCameraData(depth_camera_data["point_cloud"], depth_camera_data["distance_from_patient"])

    def toDict(self):
        return {
            "point_cloud": self.point_cloud,
            "distance_from_patient": self.distance_from_patient,
        }

    def __eq__(self, other): 
        if not isinstance(other, DepthCameraData):
            # don't attempt to compare against unrelated types
            return NotImplemented
        
        # TODO: Implement equality function
        return False