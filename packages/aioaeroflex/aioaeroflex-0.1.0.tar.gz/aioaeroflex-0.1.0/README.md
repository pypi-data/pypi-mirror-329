# aioaeroflex

An async Python library for controlling Aeroflex adjustable beds via Bluetooth.

## Installation

```bash
pip install aioaeroflex
```

## Usage

```python
import asyncio
from aioaeroflex import AeroflexBed, BedCommand

async with AeroflexBed("00000000-0000-0000-0000-000000000000") as bed:
    await bed.start_movement(BedCommand.HEAD_UP)
    await asyncio.sleep(3.0)
    await bed.stop_movement()
```

## Features

- Async/await support
- Automatic bed discovery
- Simple movement controls
- Context manager support

## Requirements

- Python 3.7+
- Bluetooth LE support

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
