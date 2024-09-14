import gpiozero
import time
from typing import Optional

# nothing uses this right now, but I'm leaving it in and you can't stop me
class Relay():
	def __init__(self, pin: int, inverted: bool = False, setState: Optional[bool] = False):
		self.pin = pin
		self.inverted = inverted
		self.handle = gpiozero.LED(pin=pin, active_high=not inverted, initial_value=setState)

	def isOn(self) -> bool:
		return self.handle.is_lit()

	def turnOn(self):
		self.handle.on()

	def turnOff(self):
		self.handle.off()

	def toggle(self):
		self.handle.toggle()

class BistableRelay(Relay):
	cache = {}

	def __init__(self, name: str, pinOn: int, pinOff: int, inverted: bool = False, assumeState: bool = False, setState: Optional[bool] = None):
		self.name = name
		self.pinOn = pinOn
		self.pinOff = pinOff
		self.memory = None
		self.inverted = inverted
		self.handleOn = gpiozero.LED(pin=pinOn, active_high=not inverted, initial_value=False)
		self.handleOff = gpiozero.LED(pin=pinOff, active_high=not inverted, initial_value=False)

		if setState is True:
			self.turnOn()
		elif setState is False:
			self.turnOff()
		else:
			self.memory = assumeState

	def isOn(self) -> bool:
		return self.memory

	def turnOn(self):
		self.handleOn.blink(on_time=0.05, off_time=0, n=1)
		self.memory = True

	def turnOff(self):
		self.handleOff.blink(on_time=0.05, off_time=0, n=1)
		self.memory = False

	def assignState(self, newState: bool):
		self.memory = newState

	def toggle(self):
		if self.isOn():
			self.turnOff()
		else:
			self.turnOn()

	@classmethod
	def ensure(cls, name: str, pinOn: int, pinOff: int, inverted: bool = False, assumeState: bool = False, setState: Optional[bool] = None):
		relay = cls.cache.get(name, None)
		if relay is None:
			relay = BistableRelay(name, pinOn, pinOff, inverted, assumeState, setState)
			cls.cache[name] = relay
		return relay
