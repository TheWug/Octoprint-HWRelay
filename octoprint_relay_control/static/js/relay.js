const me = "relay_control" // value of plugin_identifier in setup.py

$(function() {
    function RelayControlViewModel(parameters) {
        var self = this;
        
        self.canTurnOn = ko.observable(true)
        self.canTurnOff = ko.observable(true)

        self.mainPowerOn = function() {
        	OctoPrint.simpleApiCommand(me, "POWER_ON", {})
        };
        
        self.mainPowerOff = function() {
        	OctoPrint.simpleApiCommand(me, "POWER_OFF", {})
        };
        
        self.eStop = function() {
        	OctoPrint.simpleApiCommand(me, "POWER_OFF", {})
        };

        self.onBeforeBinding = function() {
        }
        
        self.onDataUpdaterPluginMessage = function (plugin, data) {
        	if (plugin == me) {
        		self.canTurnOn(data.canTurnOn)
        		self.canTurnOff(data.canTurnOff)
        	}
        }
    }

    // This is how our plugin registers itself with the application, by adding some configuration
    // information to the global variable OCTOPRINT_VIEWMODELS
    OCTOPRINT_VIEWMODELS.push([
        // This is the constructor to call for instantiating the plugin
        RelayControlViewModel,

        // This is a list of dependencies to inject into the plugin, the order which you request
        // here is the order in which the dependencies will be injected into your view model upon
        // instantiation via the parameters argument
        [],

        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
        ["#tab_plugin_relay_control"]
    ]);
});
