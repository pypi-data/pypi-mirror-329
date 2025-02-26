import numpy as np
from doplcommunicator import DepthCameraData


def test_depthcameradata():
    # Setup
    point_1 = [1, 2, 3, 0, 0, 0] # (x, y, z, r, g, b)
    point_2 = [4, 5, 6, .1, .4, .2] # (x, y, z, r, g, b)
    point_cloud = [point_1, point_2]
    distance_from_patient = 25 # mm
    depthCameraData = DepthCameraData(point_cloud, distance_from_patient)

    # Test
    assert np.all(depthCameraData.point_cloud == point_cloud)
    assert depthCameraData.distance_from_patient == distance_from_patient

def test_fromDict():
    # Setup
    point_1 = [1, 2, 3, 0, 0, 0] # (x, y, z, r, g, b)
    point_2 = [4, 5, 6, .1, .4, .2] # (x, y, z, r, g, b)
    point_cloud = [point_1, point_2]
    distance_from_patient = 25 # mm
    depth_camera_data = {
        "point_cloud": point_cloud,
        "distance_from_patient": distance_from_patient
    }
    depthCameraData = DepthCameraData.fromDict(depth_camera_data)

    # Test
    assert np.all(depthCameraData.point_cloud == point_cloud)
    assert depthCameraData.distance_from_patient == distance_from_patient

def test_toDict():
    # Setup
    point_1 = [1, 2, 3, 0, 0, 0] # (x, y, z, r, g, b)
    point_2 = [4, 5, 6, .1, .4, .2] # (x, y, z, r, g, b)
    point_cloud = [point_1, point_2]
    distance_from_patient = 25 # mm
    depthCameraData = DepthCameraData(point_cloud, distance_from_patient)
    depth_camera_dict = depthCameraData.toDict()

    # Test
    assert np.all(depth_camera_dict["point_cloud"] == point_cloud)
    assert depth_camera_dict["distance_from_patient"] == distance_from_patient

