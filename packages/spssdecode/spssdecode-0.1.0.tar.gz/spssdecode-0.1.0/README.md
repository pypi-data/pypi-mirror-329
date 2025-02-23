# spssdecode

The `spssdecode` library decodes captured star maps into structured data (e.g., positions, colors, animations). It extracts session-specific information and analyzes visual patterns like star positions, twinkling patterns, and gradients.

## Installation

Install the library using pip:

```bash
pip install spssdecode

USAGE:
from spssdecode.decoder import Decoder
import numpy as np

# Initialize the Decoder
decoder = Decoder()

# Example image data (replace with real image data)
image_data = np.zeros((400, 400, 3), dtype=np.uint8)
center = (200, 200)
boundary_radius = 150
image_data[190:200, 190:200] = 255  # Bright region (simulating a star)

# Decode the star map
decoded_data = decoder.decode_star_map(image_data, center, boundary_radius)

print(decoded_data)
```
