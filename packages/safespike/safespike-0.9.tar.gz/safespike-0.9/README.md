# SpikeSafe ACL Risk Detection Algorithm
## Important directories

```spikesafe```: Contains package implemntation

```data```: Some sample csv's to play around with

```notebooks```: previouse experimentation, some may not run anymore



## Usage
***For an example walkthrough, check out notebooks/tutorial.ipynb***

### 1. Clone Repo

### 2.In parent directory (e.g should say stride-sense-algo) install spikesafe package
``` pip install -e .```

### 3. Import SensorTandem, Sensor, and SensorData
``` 
from spikesafe import Sensor, SensorTandem
```
### 4. Convert orientation data into an array of quaternions  (this code only works if going from a csv)

```
thigh_orientation = np.array([
    np.quaternion(row.W, row.X, row.Y, row.Z)
    for _, row in thigh_orientation_df.iterrows()
])

shin_orientation = np.array([
    np.quaternion(row.W, row.X, row.Y, row.Z)
    for _, row in shin_orientation_df.iterrows()
])
```
### 5. Create two sensor objects, one for thigh and one for shank, and pass in your data as an nd_array
```
thigh_sensor = Sensor(sensor_orientation=thigh_orientation,
                 x_acceleration=x_data, y_acceleration=y_data, z_acceleration=z_data,time_arr=time_arr) 
shank_sensor = Sensor(...) # same thing but for the shank data
```

### 6. Pass the sensor objects to a sensor tandem object 
```
sensor_tandem = SensorTandem(thigh_sensor=thigh_sensor,shank_sensor=shank_sensor)
```
### 7. Synchronize the two sensors
```
sensor_tandem.sync_sensors()
```

### 8. Detect ACL Risk - set desired parameters 
```
acl_events = sensor_tandem.find_acl_risk(landing_time=0.02, flexion_threshold=25,
                                       jump_thresh=1, land_thresh=-1, hang_time=0.53,
                                       angle_method='euler', rotation_threshold=4.5)
```
