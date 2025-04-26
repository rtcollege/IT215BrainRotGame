class Data:

    def __init__(self, ui):
        self.ui = ui
        self._currency = 5
        self._health = 100
        self.difficulty = 'medium'
        self.volume = 100    

        self.unlocked_level = 0
        self.current_level = 0
        
        # Upgrade levels
        self._multi_ball_level = 0
        self._shrink_reduction_level = 0
        self._rotation_reduction_level = 0
        self._health_regen_level = 0
        
        # Upgrade costs (increase by 50% per level)
        self.base_upgrade_cost = 10
        
    @property
    def multi_ball_level(self):
        return self._multi_ball_level
        
    @property
    def shrink_reduction_level(self):
        return self._shrink_reduction_level
        
    @property
    def rotation_reduction_level(self):
        return self._rotation_reduction_level
        
    @property
    def health_regen_level(self):
        return self._health_regen_level
        
    def get_upgrade_cost(self, level):
        return int(self.base_upgrade_cost * (1.5 ** level))
        
    def can_afford_upgrade(self, level):
        return self._currency >= self.get_upgrade_cost(level)

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, currency):
        self._currency = currency
        self.ui.show_currency(self.currency)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, health):
        self._health = health
