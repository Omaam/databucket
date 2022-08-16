# databucket
Super-easy data access.


# Requirements
* HEASoft: this software use HEASoft command XSELECT to create light curve.


# Usage
Super simple.

```python
from databucket import DataBucket
object_satelite = DataBucket(object_name, satelite_name)
df_event = object_satelite.request_event(
               obsid="XXXXXXXXXX")
df_curve = object_satelite.request_curve(
               obsid="XXXXXXXXXX",
			   dt=1, energy_range=[0.1, 10])
```

# Prepare
When you first install DataBucket, there is a few steps to
prepare configure bucket directory.
We recommend you to use interactive python console.

```python
from databucket import configure
configure.create_bucket(path_to_bucket)
configure.update_bucket(glob_style_pathname)
```

When you add a new obsevation, you can add to bucket as follow:
```python
from databucket import configure
configure.update_eventfiles(object_name, satelite_name, glob_style_abspath)
```

It's quite easy, isn't it!
Let's dive into astronomical data analysis world!


# Data Flow

* Args:
  * object\_name,
  * obsid
  * time\_resolution
* Return:
  * pandas.DataFrame
