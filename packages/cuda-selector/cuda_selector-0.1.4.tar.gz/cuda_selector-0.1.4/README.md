# Auto Cuda Selector

A simple tool to select the optimal CUDA device based on memory, power, or utilization.


### Install
```bash
pip install cuda-selector
```
### Usage
```python
from cuda_selector import auto_cuda

# Select the CUDA device with the most memory available
device = auto_cuda()

# Select the CUDA device with the lowest power usage
device = auto_cuda('power')

# Select the CUDA device with the lowest GPU utilization
device = auto_cuda('utilization')

# Select the CUDA device with the lowest temperature
device = auto_cuda('temperature')

# Select multiple devices with the most free memory
devices = auto_cuda(n=3)

# Exclude specific devices by their index
devices = auto_cuda(exclude=[0, 1])

# Apply thresholds for power usage and utilization
devices = auto_cuda(thresholds={'power': 150, 'utilization': 70})

# Use a custom ranking function for selecting devices
devices = auto_cuda(sort_fn=lambda d: d['memory_free'] * 0.7 + d['utilization'] * 0.3)
```