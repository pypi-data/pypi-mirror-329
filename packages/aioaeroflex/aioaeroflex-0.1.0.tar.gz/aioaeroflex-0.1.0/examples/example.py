"""Module for controlling Aeroflex adjustable beds via Bluetooth."""

import asyncio
from typing import List, Optional
from aioaeroflex.aeroflex_bed import AeroflexBed, BedCommand


class AeroflexController:
    """Controller class for Aeroflex adjustable beds."""

    def __init__(self, address: Optional[str] = None, timeout: float = 10.0):
        """Initialize the bed controller.

        Args:
            address: The Bluetooth address of the bed. If None, will attempt to discover.
            timeout: Connection timeout in seconds.
        """
        self.address = address
        self.timeout = timeout
        self._bed: Optional[AeroflexBed] = None

    @staticmethod
    async def discover() -> List[AeroflexBed]:
        """Discover available Aeroflex beds.

        Returns:
            List of discovered bed devices.
        """
        devices = await AeroflexBed.discover()
        return devices

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()

    async def connect(self) -> None:
        """Connect to the bed."""
        if not self.address:
            beds = await self.discover()
            if not beds:
                raise ConnectionError("No beds found")
            self._bed = beds[0]  # be317cf2c498d6edb7127c83a76e8988
        else:
            self._bed = AeroflexBed(address=self.address)

        # Create a task for the connection attempt
        connect_task = asyncio.create_task(self._bed.connect())
        try:
            await asyncio.wait_for(connect_task, timeout=self.timeout)
        except asyncio.TimeoutError as exc:
            # Cancel the connection attempt if it times out
            connect_task.cancel()
            try:
                await connect_task
            except asyncio.CancelledError:
                pass
            raise ConnectionError(
                f"Connection timed out after {self.timeout} seconds"
            ) from exc

    async def disconnect(self) -> None:
        """Disconnect from the bed."""
        if self._bed:
            await self._bed.disconnect()
            self._bed = None

    async def move(self, command: BedCommand, duration: float) -> None:
        """Move the bed for a specified duration.

        Args:
            command: The movement command to execute.
            duration: How long to move in seconds.

        Raises:
            ConnectionError: If not connected to a bed.
        """
        if not self._bed:
            raise ConnectionError("Not connected to a bed")

        try:
            await self._bed.start_movement(command)
            await asyncio.sleep(duration)
        finally:
            await self._bed.stop_movement()


# Example usage
async def main():
    """Run example bed movements."""
    async with AeroflexController() as bed:
        # Move head up for 2 seconds
        await bed.move(BedCommand.HEAD_UP, 2.0)
        await asyncio.sleep(1)

        # Move head down for 2 seconds
        await bed.move(BedCommand.HEAD_DOWN, 2.0)


if __name__ == "__main__":
    asyncio.run(main())
