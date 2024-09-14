import octoprint.plugin
from typing import Optional

from .relay import BistableRelay

me = "relay_control" # value of plugin_identifier in setup.py

class RelayControlPlugin(octoprint.plugin.SettingsPlugin, octoprint.plugin.AssetPlugin, octoprint.plugin.TemplatePlugin, octoprint.plugin.SimpleApiPlugin, octoprint.plugin.StartupPlugin, octoprint.plugin.EventHandlerPlugin):
	def get_settings_defaults(self):
		return {"main_relay": {"gpio_set": 17, "gpio_reset": 27, "inverted": False}}

	def get_api_commands(self):
		return {
			"POWER_ON": [],
			"POWER_OFF": [],
		}

	def on_api_get(self, req):
		self.on_api_command(req, None)

	def on_api_command(self, command, data=None):
		if command == "POWER_ON":
			self.toggle_main_relay(True)
		elif command == "POWER_OFF":
			self.toggle_main_relay(False)
		else:
			raise Exception("unexpected command")

	def toggle_main_relay(self, target: Optional[bool] = None) -> bool:
		if target is None:
			target = not self.mainRelay.isOn()

		if target is not True:
			if self._printer.is_operational():
				self._logger.debug(f"Disconnecting from the printer before turning main relay OFF")
				self._printer.disconnect()
		self._logger.info(
			f"Turning the main relay {'ON' if target else 'OFF'}"
		)

		if target:
			self.mainRelay.turnOn()
		else:
			self.mainRelay.turnOff()

		self.update_button_state()
		return target

	def get_assets(self):
		return {
			"js": ["js/relay.js"]
		}

	def on_startup(self, host, port):
		main_settings = self._settings.get(["main_relay"], merged=True)
		pinOn = int(main_settings["gpio_set"])
		pinOff = int(main_settings["gpio_reset"])
		inverted = bool(main_settings["inverted"])
		self.mainRelay = BistableRelay.ensure("main", pinOn, pinOff, inverted, assumeState=False)
		self.shutdownAllowed = True
		self.update_button_state()

	def on_event(self, event, payload):
		if event == "Connected":
			main_settings = self._settings.get(["main_relay"], merged=True)
			pinOn = int(main_settings["gpio_set"])
			pinOff = int(main_settings["gpio_reset"])
			inverted = bool(main_settings["inverted"])
			mainRelay = BistableRelay.ensure("main", pinOn, pinOff, inverted, assumeState=False)
			mainRelay.assignState(true)
			self.update_button_state()
		elif event == "PrinterStateChanged":
			self.shutdownAllowed = payload.get('state_id') in ["OPERATIONAL", "OFFLINE", "NONE", "CLOSED", "CLOSED_WITH_ERROR"]
			self.update_button_state()

	def update_button_state(self):
		already_on = self.mainRelay.isOn()
		self._plugin_manager.send_plugin_message(me, {
			canTurnOn: not already_on,
			canTurnOff: already_on and self.shutdownAllowed
		})

__plugin_implementation__ = RelayControlPlugin()
__plugin_pythoncompat__ = ">=3.7,<4"
