from typing import Dict, List, Any


from .session import MetamonSession
from .url import Url
from .backpack import Backpack
from .config import BP_TYPE_MAPPING, BATTLE_RACA


class Metamon:

    def __init__(self, address, token):
        # self.address = address
        # self.token = token
        self.url = Url()
        self.session = MetamonSession(address, token)
        self.backpack = Backpack()
        self.metamon_list = list()

    def list_wallet_property(self):
        request_data = {
            "page": "1",
            "pageSize": 99999,
        }
        return self.session.post(self.url.wallet_property_list,
                                 data=request_data)

    def list_metamon(self) -> List[Dict[str, Any]]:
        ret = self.list_wallet_property()
        if not ret["data"]:
            return list()
        return ret["data"].get("metamonList", list())

    def set_backpack(self):
        """设置背包道具数量"""
        response_data = self.session.post(self.url.check_bag)
        for item in response_data["data"]["item"]:
            if item["bpType"] in BP_TYPE_MAPPING:
                setattr(self.backpack, BP_TYPE_MAPPING[item["bpType"]], int(item["bpNum"]))
        self.backpack.mintable_egg = self.backpack.fragment // 1000

    def check_log(self):
        print("====设置背包道具数量=======")
        self.set_backpack()
        print("====打印背包日志=======")
        self.backpack.log()
        print()

    def is_can_battle(self):
        """是否有足够的raca可以进行战斗"""
        if self.backpack.raca < BATTLE_RACA:
            print(f"raca is not enough, min({BATTLE_RACA})")
            return False
        return True

    def update_monster(self, nft_id: int) -> bool:
        """升级元兽"""
        self.set_backpack()
        request_data = dict(nftId=nft_id)
        if not self.backpack.potion:
            print("potion is not enough")
            return False

        response_data = self.session.post(self.url.update_monster,
                                          data=request_data)
        if response_data["result"] != 1:
            return False

        self.backpack.potion -= 1
        print(f"metamon({nft_id}) level up!")
        return True

    def compose_monster_egg(self, number=0):
        """合成元兽蛋"""
        self.check_log()
        compose_number = self.backpack.mintable_egg
        if number > compose_number:
            number = compose_number
        if number == 0:
            number = compose_number
        for i in range(number):
            self.session.post(self.url.compose_monster_egg)
        print(f"Composed {number} eggs")

    def run(self, fight_id):
        self.metamon_list = self.list_metamon()
        self.check_log()
        self.start_battle(fight_id)
        self.compose_monster_egg()
        self.check_log()

    def start_battle(self, fight_metamon_id):
        for metamon_info in self.metamon_list:
            if not self.is_can_battle():
                break

            _id = metamon_info["id"]
            exp = metamon_info["exp"]
            exp_max = metamon_info["expMax"]
            tear = metamon_info["tear"]
            battle_data = dict(battleLevel=1, monsterA=_id, monsterB=fight_metamon_id)
            win = lose = battle = 0

            # update_result = 1

            while 1:
                if not self.is_can_battle():
                    break
                if tear == 0:
                    break

                response_data = self.session.post(self.url.start_battle,
                                                  data=battle_data)
                battle += 1
                if response_data["data"]["challengeResult"]:
                    win += 1
                else:
                    lose += 1
                exp += response_data["data"]["challengeExp"]
                tear -= 1
                self.backpack.raca -= BATTLE_RACA
                self.backpack.fragment += response_data["data"]["bpFragmentNum"]
                # if exp < exp_max:
                # else:
                #     update_result = self.update_monster(_id)
                #     exp = 0
                # if update_result == 0:
                #     break
            print(f"metamon {_id} battled: {battle}, Win: {win} Lose:{lose};")
