"""Asyncio library for controlling Aeroflex adjustable beds via Bluetooth."""

from __future__ import annotations

import asyncio
import logging
from enum import IntEnum
from typing import Optional

from bleak import BleakClient, BleakScanner

_LOGGER = logging.getLogger(__name__)

# BLE UUIDs
SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
RX_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
TX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"


class BedCommand(IntEnum):
    """Commands for controlling the bed."""

    HEAD_UP = 0x34
    FEET_UP = 0x36
    HEAD_DOWN = 0x37
    BOTH_UP = 0x38
    BOTH_DOWN = 0x39
    FEET_DOWN = 0x41


class AeroflexBed:
    """Class to control an Aeroflex adjustable bed."""

    def __init__(self, address: str) -> None:
        """Initialize the bed controller.

        Args:
            address: Bluetooth address of the bed
        """
        self._address = address
        self._client: Optional[BleakClient] = None
        self._is_moving = False
        self._movement_task: Optional[asyncio.Task] = None
        self._connected = False

    @property
    def is_connected(self) -> bool:
        """Return True if connected to the bed."""
        return self._connected and self._client is not None

    async def connect(self) -> None:
        """Connect to the bed."""
        if self.is_connected:
            return

        device = await BleakScanner.find_device_by_address(self._address)
        if not device:
            raise ConnectionError(f"Could not find device with address {self._address}")

        self._client = BleakClient(device)
        await self._client.connect()
        self._connected = True
        _LOGGER.debug("Connected to bed at %s", self._address)

    async def disconnect(self) -> None:
        """Disconnect from the bed."""
        if self._movement_task:
            self._movement_task.cancel()
            try:
                await self._movement_task
            except asyncio.CancelledError:
                pass
            self._movement_task = None

        if self._client:
            await self._client.disconnect()
            self._client = None
            self._connected = False
            _LOGGER.debug("Disconnected from bed")

    async def _send_command(self, command: BedCommand) -> None:
        """Send a command to the bed.

        Args:
            command: Command to send
        """
        if not self.is_connected:
            raise ConnectionError("Not connected to bed")

        await self._client.write_gatt_char(
            RX_UUID, bytearray([command.value]), response=False
        )

    async def _continuous_movement(self, command: BedCommand) -> None:
        """Continuously send movement commands.

        Args:
            command: Movement command to send repeatedly
        """
        self._is_moving = True
        try:
            while self._is_moving:
                await self._send_command(command)
                await asyncio.sleep(0.15)  # Send command every 150ms
        except asyncio.CancelledError:
            pass
        finally:
            self._is_moving = False

    async def start_movement(self, command: BedCommand) -> None:
        """Start continuous movement.

        Args:
            command: Movement command to start
        """
        if self._movement_task:
            self._movement_task.cancel()
            try:
                await self._movement_task
            except asyncio.CancelledError:
                pass
            self._movement_task = None

        self._movement_task = asyncio.create_task(self._continuous_movement(command))

    async def stop_movement(self) -> None:
        """Stop any ongoing movement."""
        if self._movement_task:
            self._movement_task.cancel()
            try:
                await self._movement_task
            except asyncio.CancelledError:
                pass
            self._movement_task = None
            self._is_moving = False

    @classmethod
    async def discover(cls) -> list[AeroflexBed]:
        """Discover Aeroflex beds.

        Returns:
            List of discovered bed instances
        """
        devices = await BleakScanner.discover(
            return_adv=True, service_uuids=[SERVICE_UUID]
        )
        # Extract the address from each discovered device
        return [cls(address) for address, _ in devices.values()]
