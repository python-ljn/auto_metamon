class Backpack:

    def __init__(self):
        self._raca = 0
        self._potion = 0
        self._ydiamond = 0
        self._pdiamond = 0
        self._fragment = 0
        self._egg = 0
        self._mintable_egg = 0

    @property
    def raca(self):
        return self._raca

    @raca.setter
    def raca(self, value):
        self._raca = value

    @property
    def potion(self):
        return self._potion

    @potion.setter
    def potion(self, value):
        self._potion = value

    @property
    def ydiamond(self):
        return self._ydiamond

    @ydiamond.setter
    def ydiamond(self, value):
        self._ydiamond = value

    @property
    def pdiamond(self):
        return self._pdiamond

    @pdiamond.setter
    def pdiamond(self, value):
        self._pdiamond = value

    @property
    def fragment(self):
        return self._fragment

    @fragment.setter
    def fragment(self, value):
        self._fragment = value

    @property
    def egg(self):
        return self._egg

    @egg.setter
    def egg(self, value):
        self._egg = value

    @property
    def mintable_egg(self):
        return self._mintable_egg

    @mintable_egg.setter
    def mintable_egg(self, value):
        self._mintable_egg = value

    def log(self):
        for k, v in self.__dict__.items():
            print(f"{k}: {v}")
