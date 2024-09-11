const me = "relay_control" // value of plugin_identifier in setup.py

$(function() {
    function RelayControlViewModel(parameters) {
        var self = this;

        self.mainPowerOn = function() {
        	alert("on123")
        	OctoPrint.simpleApiCommand(me, "POWER_ON", {})
        	alert("on456")
        };
        
        self.mainPowerOff = function() {
        	alert("off")
        	OctoPrint.simpleApiCommand(me, "POWER_OFF", {})
        	alert("off")
        };
        
        self.eStop = function() {
        	alert("emergency stop!")
        	OctoPrint.simpleApiCommand(me, "POWER_OFF", {})
        	alert("emergency stop!")
        };

        self.onBeforeBinding = function() {
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
