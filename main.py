import json
import os
import tkinter as tk
from binance.spot import Spot


class CoinTools(tk.Tk):
    def __init__(self, **configs):
        super().__init__()
        self.btc_price = tk.StringVar()
        self.eth_price = tk.StringVar()
        self.bnb_price = tk.StringVar()
        self.client = Spot(**configs)

        # 窗口标题
        self.title('Coin Tools')

        # 窗口大小设置
        self.geometry('250x150')

        self.coin_start_x = 10
        self.coin_start_y = 5
        self.coin_start_x_step = 120
        self.coin_start_y_step = 22

        # 初始化价格
        # self.btc_price_set()
        # self.eth_price_set()
        # self.bnb_price_set()

        # btc label设置
        self.btc_label = tk.Label(self, textvariable=self.btc_price)
        self.btc_label.place(x=self.coin_start_x + self.coin_start_x_step * 0, y=self.coin_start_y)

        # eth label设置
        self.eth_label = tk.Label(self, textvariable=self.eth_price)
        self.eth_label.place(x=self.coin_start_x + self.coin_start_x_step * 1, y=self.coin_start_y)

        # bnb label设置
        self.bnb_label = tk.Label(self, textvariable=self.bnb_price)
        self.bnb_label.place(x=self.coin_start_x + self.coin_start_x_step * 0,
                             y=self.coin_start_y + self.coin_start_y_step * 1)

        # 查询币价label
        tk.Label(self, text='查价：').place(x=self.coin_start_x, y=self.coin_start_y + self.coin_start_y_step * 2)

        # coin 输入变量
        self.var_coin = tk.StringVar()

        # 设置输入框
        self.search_input = tk.Entry(self, show=None, textvariable=self.var_coin, width=15)
        self.search_input.place(x=60, y=self.coin_start_y + self.coin_start_y_step * 2)
        # self.search_input.bind('<Enter>', self.search_coin)
        self.search_input.bind('<Return>', self.search_coin)

        # 搜索价格
        self.search_price = tk.StringVar('')
        self.search_label = tk.Label(self, textvariable=self.search_price, anchor='w')
        self.search_label.place(x=self.coin_start_x, y=self.coin_start_y + self.coin_start_y_step * 3 + 10)

        # 放置按钮
        search_btn = tk.Button(self, text='查找', command=self.search_coin)
        search_btn.place(x=self.coin_start_x, y=self.coin_start_y + self.coin_start_y_step * 4 + 10)
        update_btn = tk.Button(self, text='更新', command=self.refresh_data)
        update_btn.place(x=75, y=self.coin_start_y + self.coin_start_y_step * 4 + 10)
        close_btn = tk.Button(self, text='关闭', command=quit)
        close_btn.place(x=160, y=self.coin_start_y + self.coin_start_y_step * 4 + 10)

        # 置顶设置
        self.wm_attributes('-topmost', 1)

    """查价"""

    def search_coin(self, *args):
        search_coin = self.var_coin.get().upper()
        if search_coin.find('USDT') == -1:
            search_coin = search_coin + 'USDT'
        self.search_price.set('{}最新价格：${}'.format(search_coin, str(self.coin_price(search_coin))))

    """价格刷新"""

    def refresh_data(self):
        self.btc_price_set()
        self.eth_price_set()
        self.bnb_price_set()

    """定时更新"""

    def refresh_always(self):
        self.refresh_data()
        # 注意是传值方法名
        self.after(1000 * 30, self.refresh_always)

    """api价格查询"""

    def coin_price(self, symbol):
        value = 0
        try:
            price = self.client.ticker_price(symbol.upper())
            value = round(float(price['price']), 2)
            print('{}: {}'.format(symbol.upper(), value))
        except Exception as ex:
            print(ex)

        return value

    """btc价格设置"""

    def btc_price_set(self):
        # btc价格
        self.btc_price.set('BTC: ${}'.format(str(self.coin_price('BTCUSDT'))))

    """eth价格设置"""

    def eth_price_set(self):
        # eth价格
        self.eth_price.set('ETH: ${}'.format(str(self.coin_price('ETHUSDT'))))

    """bnb价格设置"""

    def bnb_price_set(self):
        # bnb价格
        self.bnb_price.set('BNB: ${}'.format(str(self.coin_price('BNBUSDT'))))


if __name__ == '__main__':
    # 配置读取
    config_path = os.path.join(os.getcwd(), 'config')
    with open(os.path.join(config_path, 'api.json')) as f:
        api_config = json.load(f)

    # 实例化
    window = CoinTools(**api_config)
    # 设置价格定时更新
    window.refresh_always()
    # 展示窗口
    window.mainloop()
