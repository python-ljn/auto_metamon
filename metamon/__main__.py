from metamon.metamon import Metamon

import argparse

my_addr = "0x92F3a621100e999b0EAc54684b55895957EcD420"
parser = argparse.ArgumentParser(description="元兽自动战斗脚本")
parser.add_argument("-addr", type=str, default=my_addr, help="钱包地址")
parser.add_argument("-token", type=str, default=None, help="token")
parser.add_argument("-open", type=bool, default=False, help="open egg")
args = parser.parse_args()


def main():
    my_metamon = Metamon(address=args.addr, token=args.token, open=args.open)
    # 对战元兽id
    my_metamon.run(192494)


if __name__ == '__main__':
    main()
