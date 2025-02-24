import numpy as np
import quaternion
import pandas as pd
from .sensor_data import SensorData

def quaternions_to_euler(quaternions):
    roll = []
    pitch = []
    yaw = []
    
    for quat in quaternions:
        # Convert quaternion to rotation matrix, then to Euler angles
        euler_angles = quaternion.as_euler_angles(quat)
        roll.append(euler_angles[0])
        pitch.append(euler_angles[1])
        yaw.append(euler_angles[2])
    
    return np.array(roll), np.array(pitch), np.array(yaw)

def raw_to_sensor_data(orientation_file_path, vertical_acceleration_file_path):
    orientation_df = pd.read_csv(orientation_file_path)
    vertical_acceleration_df = pd.read_csv(vertical_acceleration_file_path)

    orientation = np.array([
        np.quaternion(row.W, row.X, row.Y, row.Z)
        for _, row in orientation_df.iterrows()
    ])

    vertical_acceleration = vertical_acceleration_df['Z'].values 
    orientation_epochs = orientation_df['Epoch'].values
    vertical_acceleration_epochs = vertical_acceleration_df['Epoch'].values
    orientation_data = SensorData(orientation, orientation_epochs)
    vertical_acceleration_data = SensorData(vertical_acceleration, vertical_acceleration_epochs)
    return orientation_data, vertical_acceleration_data

def mean_orientation(quaternions):
    """
    Compute the mean of a set of quaternions (geometric mean).
    quaternions: list or array of `quaternion.quaternion` objects.
    Returns: mean quaternion as a `quaternion.quaternion` object.
    """
    # Convert quaternions into a matrix (each quaternion as a row)
    Q = np.array([quaternion.as_float_array(q) for q in quaternions])  # w, x, y, z
    
    # Compute the covariance matrix (for quaternion rotations)
    M = np.dot(Q.T, Q)  # M is a 4x4 matrix
    
    # Perform eigenvalue decomposition
    eigenvalues, eigenvectors = np.linalg.eigh(M)
    
    # The mean quaternion corresponds to the eigenvector with the largest eigenvalue
    largest_eigenvalue_index = np.argmax(eigenvalues)
    mean_quat = eigenvectors[:, largest_eigenvalue_index]
    # Create a quaternion from the eigenvector
    mean_quaternion = np.quaternion(mean_quat[0], mean_quat[1], mean_quat[2], mean_quat[3])
    
    # Normalize using quaternion's built-in normalization
    mean_quaternion = mean_quaternion.normalized()
    
    return mean_quaternion

