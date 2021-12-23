import os
import json
from functools import wraps
from typing import Dict, List, Any

import requests

os.environ.setdefault("NO_PROXY", "https://metamon-api.radiocaca.com/")


def catch(func):
    @wraps(func)
    def _wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            print(f"catch exception: {ex}")
            raise

    return _wrap


BP_TYPE_MAPPING = {
    1: "fragment",
    2: "potion",
    3: "ydiamond",
    4: "pdiamond",
    5: "raca",
    6: "egg",
}

# 每局战斗需要耗费raca数量
BATTLE_RACA = 10


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


class Session:

    def __init__(self):
        self.session = requests.session()
        self.base_headers = {
            'origin': 'https://metamon.radiocaca.com',
            'referer': 'https://metamon.radiocaca.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        }

    def post(self, url, headers: Dict[str, Any], data: Dict[str, Any]):
        if headers:
            headers.update(self.base_headers)
        return self.session.post(url, headers=headers, data=data)


class MetamonSession(Session):

    def __init__(self, token):
        super(MetamonSession, self).__init__()
        self.token = token

    def post(self, url, headers: Dict[str, Any] = None, data: Dict[str, Any] = None, **kwargs):
        if not headers:
            headers = dict()
        headers.update(accesstoken=self.token)
        ret = super().post(url, headers, data).json()
        if ret["code"] != "SUCCESS":
            raise ValueError(f"请求失败{ret}")
        return ret


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


class Metamon:

    def __init__(self, address, token):
        self.address = address
        # self.token = token
        self.url = Url()
        self.session = MetamonSession(token)
        self.backpack = Backpack()
        self.base_request_data = dict(address=self.address)
        self.metamon_list = list()

    def list_wallet_property(self):
        request_data = {
            "address": self.address,
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
        response_data = self.session.post(self.url.check_bag,
                                          data={"address": self.address})
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


import argparse
my_addr = "0x92F3a621100e999b0EAc54684b55895957EcD420"
parser = argparse.ArgumentParser(description="元兽自动战斗脚本")
parser.add_argument("-addr", type=str, default=my_addr, help="钱包地址")
parser.add_argument("-token", type=str, default=None, help="token")
args = parser.parse_args()


if __name__ == "__main__":
    my_metamon = Metamon(address=args.addr, token=args.token)
    # 对战元兽id
    my_metamon.run(192494)