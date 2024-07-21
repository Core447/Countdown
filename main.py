# Import StreamController modules
from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder

# Import actions
from .actions.Countdown.Countdown import Countdown

class CountdownPlugin(PluginBase):
    def __init__(self):
        super().__init__()

        ## Register actions
        self.countdown_holder = ActionHolder(
            plugin_base = self,
            action_base = Countdown,
            action_id_suffix="Countdown",
            action_name = "Countdown",
            action_support = {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.SUPPORTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.countdown_holder)

        # Register plugin
        self.register()