# databucket
Super-easy data access.

# Usage
Super simple.

```python
from databucket import DataBucket
object_satelite = DataBucket("object_name", "satelite")
df_event = object_satelite.request_event(
               obsid="XXXXXXXXXX")
df_curve = object_satelite.request_curve(
               obsid="XXXXXXXXXX",
			   dt=1, energy_range=[0.1, 10])
```

# Prepare
When you first install DataBucket, there are small prepare for
configure bucket directory.
You need a few steps to create bucket.
We recommend you to use interactive python console.

```python
from databucket import configure
configure.create_bucket(path_to_bucket)
configure.update_bucket(glob_style_pathname)
```

When you add a new obsevation, you can add to bucket as follow:
```python
from databucket import configure
configure.update_bucket(glob_style_pathname)
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
