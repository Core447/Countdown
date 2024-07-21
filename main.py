# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder

# Import actions
from .actions.Countdown.Countdown import Countdown

class PluginTemplate(PluginBase):
    def __init__(self):
        super().__init__()

        ## Register actions
        self.countdown_holder = ActionHolder(
            plugin_base = self,
            action_base = Countdown,
            action_id_suffix="Countdown",
            action_name = "Countdown",
        )
        self.add_action_holder(self.countdown_holder)

        # Register plugin
        self.register()