## Overview

This Python package provides code regarding the RDG networks project.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)
- [Contact](#contact)

## Features

### No thickness
- **generate_line_segments:** Function that determines the linesegments of a RDG network.
- **generate_line_network:** Function that makes the underlying network of the linesegments.
- **get_intersection_segments:** Function that determines the intersection segments of a RDG network.
- **generate_line_segments_dynamic:** Function that determines the segments of a dynamic RDG network (with increasing linelengths in time).
- **draw_segments:** Function that draws the segments.

### Thickness
- **generate_line_segments_thickness:** Generates segment network with thicknesses
- **orientate_network:** Generates various rotated versions of the initial network.

- **save_to_stl:** Saves the network as a stl file.
- **save_to_json:** Saves data as a json file.
- **load_from_json:** Loads data as a json file.

## Installation
You can install the package using pip:

```bash
pip install RDG-networks
```

## Usage
### Output
The main function is called *generate_line_segments_thickness* and outputs the following data:
```python
data_dict = {'segments_dict': segments_dict, 
             'polygon_arr': polygon_arr, 
             'segment_thickness_dict': segment_thickness_dict, 
             'jammed': jammed,
             'generated_config': generated_config}
```
- *segment_thickness_dict*: contains the generated network, represented by multiple polygons.
- *segments_dict*: contains auxilliary information of the generated network.
- *polygon_arr*: contains auxilliary information of the generated network.
- *jammed*: A boolean indicating if the system is jammed.
- *generated_config*: An array containing all nucleation points and orientations of the segments.

### Code example
```python
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import random
from RDG_networks.thickness.generate_line_segments_thickness import generate_line_segments_thickness
from RDG_networks import save_to_stl
from RDG_networks.save_data import save_to_json, load_from_json

size = 15
lamb0 = 0.2
alpha = 0.52
thickness_arr = [lamb0 * t**(-alpha) for t in range(1, size + 1)]
box_size = 1
angles = [random.random() * 2 * np.pi for _ in range(size)]

# Generate initial structure with specified parameters
data_dict = generate_line_segments_thickness(size=size, thickness_arr=thickness_arr, angles=angles, box_size=box_size)

# Setup plot
fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))

segment_thickness_dict = data_dict['segment_thickness_dict']
for key, segment in segment_thickness_dict.items():
    segment.draw(ax1)
    middle_segment = segment.middle_segment
    if middle_segment:
        middle_segment.draw(ax1)

# Set plot limits and disable ticks
ax1.set(xlim=(0, 1), ylim=(0, 1))
ax1.set_xticks([])
ax1.set_yticks([])

# Save to STL and JSON files
save_to_stl(segment_thickness_dict, thickness=0.2, name=os.path.join(sys.path[0], 'network.stl'), frame_thickness=0.1)
file_path = os.path.join(sys.path[0], 'data.json')
save_to_json(data_dict, file_path)
data = load_from_json(file_path)

# Display the plot
plt.show()
```

## Configuration
No specific configuration is required.

## License
All Rights Reserved

The following code and its accompanying documentation are the property of Martijn (Niek) Mooij. All rights are reserved. No part of this code may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the author, except in the case of brief quotations embodied in critical reviews and certain other noncommercial uses permitted by copyright law. For permission requests, write to the author at mooij.niek@gmail.com.

Copyright 2024 Niek Mooij

## Contact
You can contact me at mooij.niek@gmail.com for any questions or suggestions.