# Adapto - AI-Powered AutoScaler

Adapto is an intelligent auto-scaling Python library that monitors system metrics like CPU, memory, and network usage. It uses machine learning to predict resource needs and proactively scale up or down.

## Features
- Real-time monitoring of CPU, memory, and network usage
- Prediction-based scaling using machine learning
- Automatic scale-up and scale-down based on thresholds
- **Customizable Scaling Strategies** – Define custom rules for scaling based on your needs

## Installation
Install Adapto via pip:
```sh
pip install adapto
```

## Usage
### Import the library
```python
from adapto.scaler import AutoScaler
```

### Create an instance of AutoScaler
```python
scaler = AutoScaler()
```

### Start monitoring and auto-scaling
```python
scaler.monitor()
```

### Fetch current system metrics
```python
metrics = scaler.get_system_metrics()
print(metrics)
```

### Predict future resource usage
```python
predictions = scaler.predict_future_usage()
print(predictions)
```

### Define Custom Scaling Strategies
You can pass a custom scaling function to the `AutoScaler`:
```python
def my_scaling_strategy(metrics):
    if metrics['cpu'] > 80 and metrics['memory'] > 75:
        return 'scale_up'
    elif metrics['cpu'] < 30 and metrics['memory'] < 40:
        return 'scale_down'
    return 'no_change'

scaler = AutoScaler(custom_scaling=my_scaling_strategy)
```

## Configuration
You can customize thresholds and instance limits:
```python
scaler = AutoScaler(
    scale_up_threshold=75,
    scale_down_threshold=30,
    memory_threshold=70,
    bandwidth_threshold=100000000,  # in bytes per second
    min_instances=1,
    max_instances=10
)
```

## License
This project is licensed under the MIT License.