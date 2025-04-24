class Data:

    def __init__(self, ui):
        self.ui = ui
        self._currency = 5
        self._health = 100
        self.difficulty = 'medium'
        self.volume = 100    

        self.unlocked_level = 0
        self.current_level = 0

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
