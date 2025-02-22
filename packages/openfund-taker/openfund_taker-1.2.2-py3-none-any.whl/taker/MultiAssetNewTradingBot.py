# -*- coding: utf-8 -*-
import ccxt
import time
import requests
import traceback
import pandas as pd

class MultiAssetNewTradingBot:
    def __init__(self,g_config, platform_config, feishu_webhook=None, monitor_interval=4,logger=None):
        self.trading_pairs_config = g_config.get('tradingPairs', {})
        
        self.stop_loss_pct = platform_config["all_stop_loss_pct"]  # 全局止损百分比
        # 止盈比例
        self.low_trail_stop_loss_pct = platform_config["all_low_trail_stop_loss_pct"] # 第一档
        self.trail_stop_loss_pct = platform_config["all_trail_stop_loss_pct"]# 第二档
        self.higher_trail_stop_loss_pct = platform_config["all_higher_trail_stop_loss_pct"]# 第三档
        # 止盈阈值
        self.low_trail_profit_threshold = platform_config["all_low_trail_profit_threshold"]# 第一档
        self.first_trail_profit_threshold = platform_config["all_first_trail_profit_threshold"]# 第二档
        self.second_trail_profit_threshold = platform_config["all_second_trail_profit_threshold"]# 第三档
        
        self.feishu_webhook = feishu_webhook
        self.monitor_interval = monitor_interval  # 监控循环时间是分仓监控的3倍
        
        self.highest_total_profit = 0  # 记录最高总盈利
        self.current_tier = "无" # 记录当前的仓位模式
                
        self.global_symbol_stop_loss_flag = {} # 记录每个symbol是否设置全局止损
        self.global_symbol_take_profit_price = {} # 记录每个symbol的止盈价格
        # 保留在止盈挂单中最高最低两个价格，计算止盈价格。
        self.max_market_price = 0.0
        self.min_market_price = float('inf')  # 初始化为浮点数最大值
        
        self.cross_directions = {} # 持仓期间，存储每个交易对的交叉方向 

        # 配置交易所
        self.exchange = ccxt.okx({
            'apiKey': platform_config["apiKey"],
            'secret': platform_config["secret"],
            'password': platform_config["password"],
            'timeout': 3000,
            'rateLimit': 50,
            'options': {'defaultType': 'future'},
            'proxies': {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'},
        })
        self.logger = logger
        self.position_mode = self.get_position_mode()  # 获取持仓模式
    # 获取市场信息
    def getMarket(self,symbol):
        self.exchange.load_markets()
        return self.exchange.market(symbol)
    # 获取tick_size
    def get_tick_size(self,symbol):
        return float(self.getMarket(symbol)['precision']['price'])
    # 获取价格精度
    def get_precision_length(self,symbol) -> int:
        tick_size = self.get_tick_size(symbol)
        return len(f"{tick_size:.10f}".rstrip('0').split('.')[1]) if '.' in f"{tick_size:.10f}" else 0
    # 获取当前持仓模式
    def get_position_mode(self):
        try:
            # 假设获取账户持仓模式的 API
            response = self.exchange.private_get_account_config()
            data = response.get('data', [])
            if data and isinstance(data, list):
                # 取列表的第一个元素（假设它是一个字典），然后获取 'posMode'
                position_mode = data[0].get('posMode', 'single')  # 默认值为单向
                self.logger.info(f"当前持仓模式: {position_mode}")
                return position_mode
            else:
                self.logger.error("无法检测持仓模式: 'data' 字段为空或格式不正确")
                return 'single'  # 返回默认值
        except Exception as e:
            self.logger.error(f"无法检测持仓模式: {e}")
            return None

    def send_feishu_notification(self, message):
        if self.feishu_webhook:
            try:
                headers = {'Content-Type': 'application/json'}
                payload = {"msg_type": "text", "content": {"text": message}}
                response = requests.post(self.feishu_webhook, json=payload, headers=headers)
                if response.status_code == 200:
                    self.logger.debug("飞书通知发送成功")
                else:
                    self.logger.warn("飞书通知发送失败，状态码: %s", response.status_code)
            except Exception as e:
                self.logger.error("发送飞书通知时出现异常: %s", str(e))

    def fetch_positions(self):
        try:
            positions = self.exchange.fetch_positions()
            return positions
        except Exception as e:
            self.logger.warning(f"Warn fetching positions: {e}")
            return []

    # 获取当前委托
    def fetch_open_orders(self,symbol,params={}):
        try:
            orders = self.exchange.fetch_open_orders(symbol=symbol,params=params)
            return orders
        except Exception as e:
            self.logger.error(f"Error fetching open orders: {e}")
            return []

    def get_historical_klines(self,symbol, bar='1m', limit=241):
        # response = market_api.get_candlesticks(instId, bar=bar, limit=limit)
        params = {
            # 'instId': instId,
        }
        klines = self.exchange.fetch_ohlcv(symbol, timeframe=bar,limit=limit,params=params)
        # if 'data' in response and len(response['data']) > 0:
        if klines :
            # return response['data']
            return klines
        else:
            raise ValueError("Unexpected response structure or missing candlestick data")

    def judge_cross_direction(self,symbol, fastklines ,slowklines) :
        # 创建DataFrame
        df = pd.DataFrame({
            'fast': fastklines,
            'slow': slowklines
        })
        
        # 判断金叉和死叉
        df['golden_cross'] = (df['fast'] > df['slow']) & (df['fast'].shift(1) < df['slow'].shift(1))
        df['death_cross'] = (df['fast'] < df['slow']) & (df['fast'].shift(1) > df['slow'].shift(1))
        
        # 从后往前找最近的交叉点
        last_golden = df['golden_cross'].iloc[::-1].idxmax() if df['golden_cross'].any() else None
        last_death = df['death_cross'].iloc[::-1].idxmax() if df['death_cross'].any() else None
        # self.logger.debug(f"golden_cross = {last_golden}, death_cross = {last_death}")
        
        # self.logger.debug(f"df= \n{df[['fast','slow','golden_cross','death_cross']].tail()}")
        # 判断最近的交叉类型
        if last_golden is None and last_death is None:
            return {
                'cross': -1,  # 无交叉
                'index': None
            }
        
        # 如果金叉更近或只有金叉
        if last_golden is not None and (last_death is None or last_golden > last_death):
            return {
                'cross': 1,  # 金叉
                'index': last_golden
            }
        # 如果死叉更近或只有死叉
        else:
            return {
                'cross': 0,  # 死叉
                'index': last_death
            }
    
    def judge_ma_apex(self,symbol,pair_config, fastklines,slowklines) -> bool:
        period = int(pair_config.get('ema_range_period', 3))
        precision= self.get_precision_length(symbol)
        
        df = pd.DataFrame({
            'ema': fastklines,
            'sma': slowklines
        })
        # 快线和慢线的差值
        # 将ema和sma转换为tick_size精度
        # df['diff'] = df['ema'].apply(lambda x: float(self.round_price_to_tick(x, tick_size))) - df['sma'].apply(lambda x: float(self.round_price_to_tick(x, tick_size)))
        df['diff'] = df['ema'].round(precision)-df['sma'].round(precision)
        df['ema_diff'] = df['ema'] - df['ema'].shift(1)
        df['sma_diff'] = df['sma'] - df['sma'].shift(1)
        # 计算斜率，【正】表示两线距离扩张，【负】表示两线距离收缩
        df['slope'] = df['diff'].abs().diff().round(4)
        
        self.logger.debug(f"{symbol}: slopes = \n{df[['ema','ema_diff','sma','sma_diff','diff','slope']].iloc[-6:-1]}  ")
        
        # 两条线的距离是扩张状态还是收缩状态 true 是收缩 flase 是扩张
        is_expanding_or_contracting = all(df['slope'].tail(period) <= 0 ) and any(df['slope'].tail(period) < 0)

        return is_expanding_or_contracting 
    
        # 定义根据均线斜率判断 K 线方向的函数： 0 空 1 多 -1 平
    
    def judge_range_diff(self,symbol,pair_config,prices:pd.Series) -> bool:
        """
        计算价格列表中最后一个价格与第一个价格的差值。
        Args:
            prices: 价格列表。
        Returns:
            diff: 计算最高价列的最大值与最小值的差值
。
        """
        limit = int(pair_config.get('ema_range_limit', 1))
        period = int(pair_config.get('ema_range_period', 3))
        tick_size = self.get_tick_size(symbol)
        if prices.empty:
            return None     
  
        diff = prices.tail(period).max() - prices.tail(period).min()   
        self.logger.debug(f"{symbol}: 最高价列的最大值与最小值的差值 = {diff:.9f}")     
        return abs(diff) <= tick_size * limit
    
    # 定义根据均线斜率判断 K 线方向的函数： 0 空 1 多 -1 平
    def judge_k_line_direction(self, symbol, pair_config, ema: pd.Series, klines) -> int:
        """
        判断K线方向
        Args:
            symbol: 交易对
            pair_config: 配置参数
            ema: EMA数据
        Returns:
            int: -1:平, 0:空, 1:多
        """
        # 获取配置参数
        period = int(pair_config.get('ema_range_period', 3))
        
        ema_diff = ema.diff().tail(period)
 
        direction = None
        if ema_diff.iloc[-1] < 0:
            # 下降趋势
            direction = 0 
        elif ema_diff.iloc[-1] > 0:
            # 上升趋势
            direction = 1
        else:
            # 震荡趋势
            direction = -1 
        self.logger.debug(f"{symbol}: K线极差={ema_diff.map('{:.9f}'.format).values}  ,K线方向={direction}")
        return direction
  
    def check_reverse_position(self,symbol,position,pair_config):
        side = position['side']
        try:
            klines_period = str(pair_config.get('klines_period', '1m'))
            klines = self.get_historical_klines(symbol=symbol,bar=klines_period)

            # 计算 快线EMA & 慢线SMA
            ema_length = pair_config.get('ema', 15)
            sma_length = pair_config.get('sma', 50)
            
            # 增加 金叉死叉 方向确认的 20250209
            fastk = self.calculate_ema_pandas(symbol, klines, period=ema_length)
            slowk = self.calculate_sma_pandas(symbol, klines, period=sma_length)

            cross_direction = self.judge_cross_direction(symbol=symbol,fastklines=fastk,slowklines=slowk)

            # 更新交叉状态
            if cross_direction['cross'] != -1 :  #本次不一定有交叉
                self.cross_directions[symbol] = cross_direction
            
            # 最新交叉方向
            last_cross_direction = self.exchange.safe_dict(self.cross_directions,symbol,None)
            # 计算 快线EMA & 慢线SMA
            # 结合金叉死叉判断是否是周期顶部和底部
            is_apex = self.judge_ma_apex(symbol=symbol,pair_config=pair_config, fastklines=fastk,slowklines=slowk)
            
            kline_direction = self.judge_k_line_direction(symbol=symbol, pair_config=pair_config, ema=fastk, klines=klines)
            # if_inner_range = self.judge_range_diff(symbol=symbol, pair_config=pair_config, prices=fastk)
            
            self.logger.debug(f"{symbol} cross={last_cross_direction},两线收缩={is_apex}，持仓方向={side} ,K线方向={kline_direction}")
            order_stop_loss_pct = None
            # 20250213 增加趋势顶部/底部判断 
            # 金叉逻辑 ,如果是金叉，且是周期顶部，且K线方向是空头，
            if last_cross_direction and last_cross_direction['cross'] == 1 and is_apex and side == 'long' and kline_direction == 0: 
                self.logger.debug(f"{symbol} 金叉:{last_cross_direction['cross']},两线收缩={is_apex}，持仓方向={side} ,K线方向={kline_direction} ,开始清理多单！！")
                # self.close_all_positions(symbol=symbol, position=position)
                order_stop_loss_pct = self.stop_loss_pct / 2
                self.logger.debug(f"{symbol} 全局止损阈值-修正后= {self.stop_loss_pct:.2f} -> {order_stop_loss_pct:.2f}%")

       
            # 死叉逻辑 ,如果是死叉，且是周期底部，且K线方向是多头，就清仓空单    
            if last_cross_direction and last_cross_direction['cross'] == 0 and is_apex and side == 'short' and kline_direction == 1: 
                self.logger.debug(f"{symbol} 死叉:{last_cross_direction['cross']},两线收缩={is_apex}，持仓方向={side} ,K线方向={kline_direction} ,开始清理空单！！")
                # self.close_all_positions(symbol=symbol, position=position)
                order_stop_loss_pct = self.stop_loss_pct / 2
                self.logger.debug(f"{symbol} 全局止损阈值-修正后= {self.stop_loss_pct:.2f} -> {order_stop_loss_pct:.2f}%")

            # 根据情况 重新修正 止损
            if order_stop_loss_pct is not None :
                self.global_symbol_stop_loss_flag[symbol] = False    
                self.set_global_stop_loss(symbol=symbol,position=position,stop_loss_pct=order_stop_loss_pct)
            else :
                self.global_symbol_stop_loss_flag[symbol] = False 

        except KeyboardInterrupt:
            self.logger.info("程序收到中断信号，开始退出...")
        except Exception as e:
            error_message = f"程序异常退出: {str(e)}"
            self.logger.error(error_message,exc_info=True)
            traceback.print_exc()
            self.send_feishu_notification(error_message)
    
    def calculate_sma_pandas(self,symbol,kLines,period):
        """
        使用 pandas 计算 SMA
        :param KLines K线
        :param period: SMA 周期
        :return: SMA 值
        """
 
        df = pd.DataFrame(kLines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        sma = df['close'].rolling(window=period).mean()
        return sma 
            
    def calculate_ema_pandas(self,symbol,kLines, period):
        """
        使用 pandas 计算 EMA
        :param KLines K线
        :param period: EMA 周期
        :return: EMA 值
        """

        df = pd.DataFrame(kLines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        # 计算EMA
        ema = df['close'].ewm(span=period, adjust=False).mean()
        return ema 
    
   # 计算平均利润
    def calculate_average_profit(self,symbol,position):
        # positions = self.fetch_positions()
        total_profit_pct = 0.0
        num_positions = 0

        entry_price = float(position['entryPrice'])
        current_price = float(position['markPrice'])
        side = position['side']

        # 计算单个仓位的浮动盈利百分比
        if side == 'long':
            profit_pct = (current_price - entry_price) / entry_price * 100
        elif side == 'short':
            profit_pct = (entry_price - current_price) / entry_price * 100
        else:
            return

        # 累加总盈利百分比
        total_profit_pct += profit_pct
        num_positions += 1

        # 记录单个仓位的盈利情况
        self.logger.info(f"仓位 {symbol}，方向: {side}，开仓价格: {entry_price}，当前价格: {current_price}，"
                            f"浮动盈亏: {profit_pct:.2f}%")

        # 计算平均浮动盈利百分比
        average_profit_pct = total_profit_pct / num_positions if num_positions > 0 else 0
        return average_profit_pct

    def reset_highest_profit_and_tier(self):
        """重置最高总盈利和当前档位状态"""
        self.highest_total_profit = 0
        self.current_tier = "无"
        self.global_symbol_stop_loss_flag.clear()
        # self.logger.debug("已重置最高总盈利和档位状态")
    # FIXME 目前只支持 单symbol
    def reset_take_profie(self):
        self.global_symbol_take_profit_price.clear()
        self.global_symbol_stop_loss_flag.clear()
        # 保留在止盈挂单中最高最低两个价格，计算止盈价格。
        self.max_market_price = 0.0
        self.min_market_price = float('inf')  # 初始化为浮点数最大值
        self.cross_directions = {}
       
    def round_price_to_tick(self,symbol, price):
        tick_size = float(self.exchange.market(symbol)['info']['tickSz'])
        # 计算 tick_size 的小数位数
        tick_decimals = len(f"{tick_size:.10f}".rstrip('0').split('.')[1]) if '.' in f"{tick_size:.10f}" else 0

        # 调整价格为 tick_size 的整数倍
        adjusted_price = round(price / tick_size) * tick_size
        return f"{adjusted_price:.{tick_decimals}f}"
        # 放弃当前委托
    
    def cancel_all_algo_orders(self,symbol):
        
        params = {
            "ordType": "conditional",
        }
        orders = self.fetch_open_orders(symbol=symbol,params=params)
        # 如果没有委托订单则直接返回
        if not orders:
            self.global_symbol_stop_loss_flag.clear()
            self.logger.debug(f"{symbol} 未设置策略订单列表。")
            return
     
        algo_ids = [order['info']['algoId'] for order in orders if 'info' in order and 'algoId' in order['info']]
        try:
            params = {
                "algoId": algo_ids,
                "trigger": 'trigger'
            }
            rs = self.exchange.cancel_orders(ids=algo_ids, symbol=symbol, params=params)
            self.global_symbol_stop_loss_flag.clear()
            # self.logger.debug(f"Order {algo_ids} cancelled:{rs}")
        except Exception as e:
            self.logger.error(f"{symbol} Error cancelling order {algo_ids}: {e}")
            
    def set_stop_loss_take_profit(self, symbol, position, stop_loss_price=None, take_profit_price=None) -> bool:
        self.cancel_all_algo_orders(symbol=symbol)
        stop_params = {}
            
        if not position:
            self.logger.warning(f"{symbol}: No position found for {symbol}")
            return
            
        amount = abs(float(position['contracts']))
        
        if amount <= 0:
            self.logger.warning(f"{symbol}: amount is 0 for {symbol}")
            return

        adjusted_price = self.round_price_to_tick(symbol, stop_loss_price)
            
        # 设置止损单 ccxt 只支持单向（conditional）不支持双向下单（oco、conditional）
        if not stop_loss_price:
            return False
        
        stop_params = {
            'slTriggerPx':adjusted_price , 
            # 'slOrdPx':'-1', # 委托价格为-1时，执行市价止损
            'slOrdPx' : adjusted_price,
            'slTriggerPxType':'last',
            'tdMode':position['marginMode'],
            'sz': str(amount),
            # 'closeFraction': '1',
            'cxlOnClosePos': True,
            'reduceOnly':True
        }
        
        side = 'short' 
        if position['side'] == side: # 和持仓反向相反下单
            side ='long'
            
        orderSide = 'buy' if side == 'long' else 'sell'
    
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                self.logger.debug(f"{symbol} - {orderSide}:Pre Stop loss order set for {symbol} at {stop_loss_price} Starting....  ")
                self.exchange.create_order(
                    symbol=symbol,
                    type='conditional',
                    # type='limit',
                    price=adjusted_price,
                    side=orderSide,
                    amount=amount,
                    params=stop_params
                )
                self.logger.debug(f"{symbol} - {orderSide}: Stop loss order set for {symbol} at {stop_loss_price} Done.")
                return True
            except ccxt.NetworkError as e:
                # 处理网络相关错误
                retry_count += 1
                self.logger.warning(f"!! 设置止损单时发生网络错误,正在进行第{retry_count}次重试: {str(e)}")
                time.sleep(0.1)  # 重试前等待1秒
                continue
            except ccxt.ExchangeError as e:
                # 处理交易所API相关错误
                retry_count += 1
                self.logger.warning(f"!! 设置止损单时发生交易所错误,正在进行第{retry_count}次重试: {str(e)}")
                time.sleep(0.1)
                continue
            except Exception as e:
                # 处理其他未预期的错误
                retry_count += 1
                self.logger.warning(f"!! 设置止损单时发生未知错误,正在进行第{retry_count}次重试: {str(e)}")
                time.sleep(0.1)
                continue

        # 重试次数用完仍未成功设置止损单
        self.logger.warning(f"!! {symbol} 设置止损单时重试次数用完仍未成功设置成功。 ")
        return False
            
    def set_global_stop_loss(self, symbol, position, stop_loss_pct=None):
        """设置全局止损
        
        Args:
            symbol: 交易对
            position: 持仓信息
            side: 持仓方向
            stop_loss_algo: 止损算法信息
        """
        # 如果已经触发过全局止损并且有止损单，则跳过
        if self.global_symbol_stop_loss_flag.get(symbol, False):

            return
        else :
            self.logger.debug(f"{symbol} - 是否设置过全局止损 {self.global_symbol_stop_loss_flag.get(symbol, False)} ")   
        if stop_loss_pct is None :
            stop_loss_pct = self.stop_loss_pct  
             
        # 根据持仓方向计算止损价格
        side = position['side'] 
        if side == 'long':
            stop_loss_price = position['entryPrice'] * (1 - stop_loss_pct/100)
        elif side == 'short': 
            stop_loss_price = position['entryPrice'] * (1 + stop_loss_pct/100)
            
        order_price = float(self.round_price_to_tick(symbol, stop_loss_price))
        
        last_take_profit_price= self.global_symbol_take_profit_price.get(symbol,None)  
        if last_take_profit_price is not None and last_take_profit_price == order_price:
            self.global_symbol_stop_loss_flag[symbol] = True
            self.logger.debug(f"{symbol} - {side} 全局止损价没变化: {last_take_profit_price} = {order_price}")
            return 
            
        try:
            # 设置止损单
            if_success = self.set_stop_loss_take_profit(
                symbol=symbol,
                position=position,
                stop_loss_price=order_price
            )
            if if_success:
                # 设置全局止损标志
                self.logger.debug(f"{symbol} - {side} 设置全局止损价: {order_price}")
                self.global_symbol_stop_loss_flag[symbol] = True
                self.global_symbol_take_profit_price[symbol] = order_price
                
        except Exception as e:
            error_msg = f"{symbol} - 设置止损时发生错误: {str(e)}"
            self.logger.error(error_msg)
            self.send_feishu_notification(error_msg)  
    
    def calculate_take_profit_price(self, symbol, position, stop_loss_pct, offset=1) -> float:
        tick_size = float(self.exchange.market(symbol)['precision']['price'])
        market_price = position['markPrice']
        entry_price = position['entryPrice']
        side = position['side']
        # base_price = abs(market_price-entry_price) * (1-stop_loss_pct)
        # 计算止盈价格，用市场价格（取持仓期间历史最高）减去开仓价格的利润，再乘以不同阶段的止盈百分比。
        latest_take_profit_price = self.exchange.safe_float(self.global_symbol_take_profit_price,symbol,None)
        if side == 'long':
            self.max_market_price = max(market_price,self.max_market_price)
            base_price = abs(self.max_market_price - entry_price) * (1-stop_loss_pct)
            take_profit_price = entry_price + base_price - offset * tick_size
            if latest_take_profit_price :
                take_profit_price = max(take_profit_price,latest_take_profit_price)

        elif side == 'short':
            self.min_market_price = min(market_price,self.min_market_price)
            base_price = abs(self.min_market_price - entry_price) * (1-stop_loss_pct)
            take_profit_price = entry_price - base_price + offset * tick_size
            if latest_take_profit_price :
                take_profit_price = min(take_profit_price,latest_take_profit_price)
        return take_profit_price
    
     # 平仓
    
    def close_all_positions(self,symbol,position):

        amount = abs(float(position['contracts']))
        side = position['side']
        td_mode = position['marginMode']
        if amount > 0:
            try:
                self.logger.info(f"{symbol}: Preparing to close position for {symbol}, side: {side}, amount: {amount}")

                if self.position_mode == 'long_short_mode':
                    # 在双向持仓模式下，指定平仓方向
                    pos_side = 'long' if side == 'long' else 'short'
                else:
                    # 在单向模式下，不指定方向
                    pos_side = 'net'
                orderSide = 'buy' if side == 'long' else 'sell'
                
                
                params = {
                    
                    'mgnMode': td_mode,
                    'posSide': pos_side,
                    'autoCxl': 'true'
            
                }

                # 发送平仓请求并获取返回值
                order = self.exchange.close_position(
                    symbol=symbol,
                    side=orderSide,
                    params=params
                )
                time.sleep(0.1)  # 短暂延迟后再试
                self.reset_take_profie()
                self.logger.info(f"{symbol} Close position response for {symbol}: {order}")
                self.send_feishu_notification(f"{symbol} 平仓订单完全成交 -{symbol} side: {side}")

            except Exception as e:
                self.logger.error(f"{symbol} Error closing position for {symbol}: {e}")
                self.send_feishu_notification(f"{symbol} Error closing position for {symbol}: {e}")             

    def check_take_profit_trigger(self, symbol: str, position: dict) -> bool:
            """
            检查是否触发止盈条件
            Args:
                symbol: 交易对
                position: 持仓信息
            Returns:
                bool: 是否需要平仓
            """
            latest_take_profit_price = self.exchange.safe_float(self.global_symbol_take_profit_price, symbol, 0.0)
            if latest_take_profit_price == 0.0:
                self.logger.warning(f"{symbol} 未设置止盈价格，执行平仓")
                return True
                
            mark_price = position['markPrice']
            side = position['side']
            
            if side == 'long' and mark_price < latest_take_profit_price:
                self.logger.warning(f"!![非正常关闭]: {symbol} 方向 {side} - 市场价格 {mark_price} 低于止盈 {latest_take_profit_price}，触发全局止盈")
                return True
            elif side == 'short' and mark_price > latest_take_profit_price:
                self.logger.warning(f"!![非正常关闭]: {symbol} 方向 {side} - 市场价格 {mark_price} 高于止盈价 {latest_take_profit_price}，触发全局止盈")
                return True
                
            return False
    
    def check_position(self, symbol, position):
        # 清理趋势相反的仓位
        pair_config = self.trading_pairs_config.get(symbol, {})
        self.check_reverse_position(symbol=symbol, position=position, pair_config=pair_config)
        
        # 检查是否触发止盈
        if self.check_take_profit_trigger(symbol, position):
            self.close_all_positions(symbol=symbol, position=position)
            return
        
    
    def check_total_profit(self, symbol, position):

        total_profit = self.calculate_average_profit(symbol, position)
        if total_profit > 0.0 :
            self.logger.info(f"{symbol} 当前总盈利: {total_profit:.2f}%")
            self.send_feishu_notification(f"{symbol} 当前总盈利: {total_profit:.2f}%")
        if total_profit > self.highest_total_profit:
            self.highest_total_profit = total_profit
        # 确定当前盈利档位
        if self.highest_total_profit >= self.second_trail_profit_threshold:
            self.current_tier = "第二档移动止盈"
     
        elif self.highest_total_profit >= self.first_trail_profit_threshold:
            self.current_tier = "第一档移动止盈"
         
        elif self.highest_total_profit >= self.low_trail_profit_threshold:
            self.current_tier = "低档保护止盈"
            
            
        if total_profit > 0.0 :
            self.logger.info(
                f"{symbol} 档位[{self.current_tier} ]: 当前总盈利: {total_profit:.2f}%，最高总盈利: {self.highest_total_profit:.2f}%")
            self.send_feishu_notification(
                f"{symbol} 档位[{self.current_tier} ]: 当前总盈利: {total_profit:.2f}%，最高总盈利: {self.highest_total_profit:.2f}%")
                
        '''
        第一档 低档保护止盈:当盈利达到0.3%触发,要么到第二档,要么回到0.2%止盈
        第二档:盈利达到1%触发,记录最高价,最高价的80%是止盈位
        第三档:盈利达到3%触发,记录最高价,最高价的75%是止盈位
        '''
        # 各档止盈逻辑
           
        if self.current_tier == "低档保护止盈":
            self.logger.info(f"{symbol} 低档回撤止盈阈值: {self.low_trail_stop_loss_pct:.2f}%")
            if total_profit >= self.low_trail_stop_loss_pct:
                
                take_profit_price = self.calculate_take_profit_price(symbol=symbol, position=position,stop_loss_pct=self.low_trail_stop_loss_pct )
                # 判断止盈价格是否变化，无变化不需要设置
                latest_take_profit_price = self.exchange.safe_float(self.global_symbol_take_profit_price,symbol,0.0)
                if take_profit_price == latest_take_profit_price:
                    self.logger.debug(f"{symbol} 止盈价格未变化，不设置")
                    return 
                if_success = self.set_stop_loss_take_profit(symbol, position, stop_loss_price=take_profit_price)
                if if_success:
                    self.logger.info(f"{symbol} 总盈利触发低档保护止盈，当前回撤到: {total_profit:.2f}%，市场价格:{position['markPrice']},设置止盈位: {take_profit_price:.9f}")
                    self.global_symbol_take_profit_price[symbol] = take_profit_price
                    self.reset_highest_profit_and_tier()
                    self.send_feishu_notification(f"{symbol} 总盈利触发低档保护止盈，当前回撤到: {total_profit:.2f}%，市场价格:{position['markPrice']},设置止盈位: {take_profit_price:.9f}")
                return
        elif self.current_tier == "第一档移动止盈":
            trail_stop_loss = self.highest_total_profit * (1 - self.trail_stop_loss_pct)
            self.logger.info(f"{symbol} 第一档回撤止盈阈值: {trail_stop_loss:.2f}%")
            if total_profit >= trail_stop_loss:
                take_profit_price = self.calculate_take_profit_price(symbol=symbol, position=position,stop_loss_pct=self.trail_stop_loss_pct )                
                # 判断止盈价格是否变化，无变化不需要设置
                latest_take_profit_price = self.exchange.safe_float(self.global_symbol_take_profit_price,symbol,0.0)
                if take_profit_price == latest_take_profit_price :
                    self.logger.debug(f"{symbol} 止盈价格未变化，不设置")
                    return  
                if_success = self.set_stop_loss_take_profit(symbol, position, stop_loss_price=take_profit_price)
                if if_success:
                    self.logger.info(
                        f"{symbol} 总盈利达到第一档回撤阈值，最高总盈利: {self.highest_total_profit:.2f}%,当前回撤到: {total_profit:.2f}%，市场价格: {position['markPrice']},设置止盈位: {take_profit_price:.9f}")
                    # 记录一下止盈价格
                    self.global_symbol_take_profit_price[symbol] = float(take_profit_price)
                    self.reset_highest_profit_and_tier()
                    self.send_feishu_notification(
                        f"{symbol} 总盈利达到第一档回撤阈值，最高总盈利: {self.highest_total_profit:.2f}%，当前回撤到: {total_profit:.2f}%，市场价格: {position['markPrice']}, 设置止盈位: {take_profit_price:.9f}")
                return 

        elif self.current_tier == "第二档移动止盈":
            trail_stop_loss = self.highest_total_profit * (1 - self.higher_trail_stop_loss_pct)
            self.logger.info(f"{symbol} 第二档回撤止盈阈值: {trail_stop_loss:.2f}%")
            if total_profit >= trail_stop_loss:
                take_profit_price = self.calculate_take_profit_price(symbol=symbol, position=position,stop_loss_pct=self.higher_trail_stop_loss_pct)                
                # 判断止盈价格是否变化，无变化不需要设置
                latest_take_profit_price = self.exchange.safe_float(self.global_symbol_take_profit_price,symbol,0.0)
                if take_profit_price == latest_take_profit_price:
                    self.logger.debug(f"{symbol} 止盈价格未变化，不设置")
                    return   
                if_success = self.set_stop_loss_take_profit(symbol, position, stop_loss_price=take_profit_price)
                if if_success:
                    self.logger.info(f"{symbol} 总盈利达到第二档回撤阈值，最高总盈利: {self.highest_total_profit:.2f}%，当前回撤到: {total_profit:.2f}%，市场价格: {position['markPrice']},设置止盈位: {take_profit_price:.9f}")
                    # 记录一下止盈价格
                    self.global_symbol_take_profit_price[symbol] = take_profit_price
                    self.reset_highest_profit_and_tier()
                    self.send_feishu_notification(f"{symbol} 总盈利达到第二档回撤阈值，最高总盈利: {self.highest_total_profit:.2f}%，当前回撤到: {total_profit:.2f}%，市场价格: {position['markPrice']},设置止盈位: {take_profit_price:.9f}")
                return 
        else :
            self.logger.info(f"{symbol} 全局止损阈值: {self.stop_loss_pct:.2f}%")
            
            self.set_global_stop_loss(symbol, position)

            return
        
    def monitor_total_profit(self):
        self.logger.info("启动主循环，开始监控总盈利...")
        previous_position_size = sum(
            abs(float(position['contracts'])) for position in self.fetch_positions())  # 初始总仓位大小
        while True:
            try:
                
                positions = self.fetch_positions()
                # 检查是否有仓位
                if not positions:
                    # self.logger.debug("没有持仓，等待下一次检查...")
                    self.reset_highest_profit_and_tier()
                    self.reset_take_profie()
                    time.sleep(1)
                    continue
                self.logger.info("+" * 60)
                # 检查仓位总规模变化
                current_position_size = sum(abs(float(position['contracts'])) for position in self.fetch_positions())
                if current_position_size > previous_position_size:
                    self.send_feishu_notification(f"检测到仓位变化操作，重置最高盈利和档位状态")
                    self.logger.info("检测到新增仓位操作，重置最高盈利和档位状态")
                    self.reset_highest_profit_and_tier()
                    previous_position_size = current_position_size
                    time.sleep(0.1)
                    continue  # 跳过本次循环

                for position in positions:
                    symbol = position['symbol']
                    self.check_total_profit(symbol, position)
                    time.sleep(0.1) 
                    # 检查仓位和挂单是否有问题
                    self.check_position(symbol, position)

                self.logger.info("-" * 60)
                time.sleep(self.monitor_interval)

            except Exception as e:
                print(e)
                error_message = f"程序异常退出: {str(e)}"
                self.logger.error(error_message)
                self.send_feishu_notification(error_message)
                continue
            except KeyboardInterrupt:
                self.logger.info("程序收到中断信号，开始退出...")
                break

