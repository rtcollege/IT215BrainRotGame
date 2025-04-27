class Data:

    def __init__(self, ui):
        self.ui = ui
        self._currency = 5
        self._health = 100
        self.difficulty = 'medium'
        self.volume = 100    
        
        self._experience = 0
        self._level = 1
        self.base_exp_required = 100  # Base XP needed for first level
        self.exp_scaling = 1.5  # Each level requires 50% more XP
        
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
        return self.currency
    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, health):
        self._health = health

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value):
        self._experience = value
        # Check for level up
        exp_needed = self.get_exp_for_level(self._level)
        while self._experience >= exp_needed:
            self._experience -= exp_needed
            self._level += 1
            # Award currency for leveling up (50 base + 25 per level)
            if hasattr(self, '_currency'):
                self._currency += 50 + (self._level * 25)
            exp_needed = self.get_exp_for_level(self._level)

    @property
    def level(self):
        return self._level

    def get_exp_for_level(self, level):
        return int(self.base_exp_required * (self.exp_scaling ** (level - 1)))
