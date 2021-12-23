class Url:
    def __init__(self):
        self.base = "https://metamon-api.radiocaca.com/usm-api/{}"
        self.login = self.base.format("login")
        self.check_bag = self.base.format("checkBag")
        self.wallet_property_list = self.base.format("getWalletPropertyList")
        self.compose_monster_egg = self.base.format("composeMonsterEgg")
        self.start_battle = self.base.format("startBattle")
        self.open_monster_egg = self.base.format("openMonsterEgg")
        self.update_monster = self.base.format("updateMonster")