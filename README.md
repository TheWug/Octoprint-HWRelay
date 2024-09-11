# HW Relay Control

This just allows me to toggle the bistable relays which control printer and accessory power via the octoprint interface.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/TheWug/relaycontrol/archive/master.zip

## Configuration

There is one configuration section, main_relay. Within it there are 3 options:
	gpio_set   (default: 17)
	gpio_reset (default: 27)
	inverted   (default: false)
	
	These options define the electrical connections used to control the relay.
	The relay is assumed to be bi-stable: that is, it has a dedicated SET and RESET line.
	Pulsing SET will turn the printer and accessories ON.
	Pulsing RESET will correspondingly turn them OFF.
	The state of the relay will be preserved otherwise, even between losses of power.
	If the inverted option is set, lines will be default high and pulse low.
	
