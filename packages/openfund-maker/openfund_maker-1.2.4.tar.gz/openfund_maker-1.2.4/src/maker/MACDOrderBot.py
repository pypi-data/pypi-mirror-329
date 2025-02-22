# -*- coding: utf-8 -*-
import time
import ccxt
import traceback
import requests
import pandas as pd
import talib as ta

from logging.handlers import TimedRotatingFileHandler
from concurrent.futures import ThreadPoolExecutor, as_completed
from maker.ThreeLineOrderBot import ThreeLineOrdergBot


class MACDOrdergBot(ThreeLineOrdergBot):
    def __init__(self, config, platform_config, feishu_webhook=None,logger=None):
        super().__init__(config, platform_config, feishu_webhook, logger)
        
    def judge_order_side(self, symbol, pair_config, macd:pd.DataFrame) -> str:
        order_side = 'none'

        '''
        零轴之上的macd与signal形成金叉
        零轴之下的死叉
        零轴之上的死叉-金叉-死叉
        零轴之下的金叉-死叉-金叉
        '''

           
        # 计算最近三个交叉点
        last_up_crosses = []
        last_down_crosses = []
        other_crosses = []
        all_cross = []
        # 遍历MACD数据 FIXME macd 要有根数限制，太久之前的无效
        # 从最新数据开始往前遍历
        for i in range(len(macd)-1, 2, -1):
            # 检查是否发生死叉（MACD从上方穿过Signal）
            if (macd.iloc[i-1]['macd'] <= macd.iloc[i-1]['signal'] and                 
                macd.iloc[i]['macd'] > macd.iloc[i]['signal'] 
                ):
                all_cross.append(('golden', i))
                
                # 判断如果都在零轴之上加入last_up_crosses , 判断如果都在零轴之下加入last_down_crosses
                if macd.iloc[i]['macd'] > 0 and macd.iloc[i]['signal'] > 0 :
                    last_up_crosses.append(('golden', i))
                elif macd.iloc[i]['macd'] < 0 and macd.iloc[i]['signal'] < 0 :
                    last_down_crosses.append(('golden', i))
                else:
                    other_crosses.append(('golden', i))
   
            # 检查是否发生死叉（MACD从上方穿过Signal）
            elif macd.iloc[i-1]['macd'] >= macd.iloc[i-1]['signal'] and macd.iloc[i]['macd'] < macd.iloc[i]['signal']:
                all_cross.append(('death', i))
                # 判断如果都在零轴之上加入last_up_crosses , 判断如果都在零轴之下加入last_down_crosses
                if macd.iloc[i]['macd'] > 0 and macd.iloc[i]['signal'] > 0 :
                    last_up_crosses.append(('death', i))
                elif macd.iloc[i]['macd'] < 0 and macd.iloc[i]['signal'] < 0 :
                    last_down_crosses.append(('death', i))
                else:
                    other_crosses.append(('golden', i))
            # 只保留最后三个交叉点
            if len(last_up_crosses) == 3 or len(last_down_crosses) == 3:
                break
            
        self.logger.debug(f"{symbol} : \n- 所有cross {all_cross} \n- 零轴之上cross {last_up_crosses} \n- 零轴之下cross {last_down_crosses} \n- 其他corss {other_crosses}。")
        valid_klines = pair_config.get('valid_klines', 3)
        # 如果最新的交叉是金叉，且又是零轴上方的金叉
        if len(last_up_crosses) > 0 and all_cross[0][0] == 'golden' and all_cross[0][1] == last_up_crosses[0][1] and len(macd) - all_cross[0][1] <= valid_klines:
            order_side =  'buy'
            self.logger.debug(f"{symbol} : 零轴之上的macd与signal形成金叉{all_cross[0]} 。") 
            
        # 如果最新的交叉是死叉，且又是零轴下方的死叉
        elif len(last_down_crosses) > 0 and all_cross[0][0] == 'death' and all_cross[0][1] == last_down_crosses[0][1] and len(macd) - all_cross[0][1] <= valid_klines:
            order_side ='sell'
            self.logger.debug(f"{symbol} : 零轴之下的macd与signal形成死叉{all_cross[0]} 。")
        # 分析交叉点模式，要满足连续的三个交叉都是零上
        elif len(last_up_crosses) == 3 and len(all_cross) == 3:
      
           # 零轴之上的死叉-金叉-死叉模式
            if (last_up_crosses[0][0] == 'death' and 
                last_up_crosses[1][0] == 'golden' and 
                last_up_crosses[2][0] == 'death'):
                order_side = 'sell'
                self.logger.debug(f"{symbol} : 零轴之上的死叉-金叉-死叉模式 {order_side}。")
            
        elif len(last_down_crosses) == 3 and len(all_cross) == 3:
            # 零轴之下的金叉-死叉-金叉模式
            if (last_down_crosses[0][0] == 'golden' and 
                  last_down_crosses[1][0] == 'death' and 
                  last_down_crosses[2][0] == 'golden'):
                order_side = 'buy'
                self.logger.debug(f"{symbol} : 零轴之下的金叉-死叉-金叉模式 {order_side}。")
                
        
        
        # # 零轴之上的macd与signal形成金叉
        # if macd.iloc[-1]['macd'] > 0 and macd.iloc[-1]['signal'] > 0 and macd.iloc[-1]['macd'] >= macd.iloc[-1]['signal'] and macd.iloc[-2]['macd'] < macd.iloc[-2]['signal']:
        #     order_side =  'buy'
        #     self.logger.debug(f"{symbol} : 零轴之上的macd与signal形成金叉 {order_side}。")
        # elif macd.iloc[-1]['macd'] < 0 and macd.iloc[-1]['signal'] < 0 and macd.iloc[-1]['macd'] <= macd.iloc[-1]['signal'] and macd.iloc[-2]['macd'] > macd.iloc[-2]['signal']:
        #     order_side = 'sell'
        #     self.logger.debug(f"{symbol} : 零轴之下的macd与signal形成死叉 {order_side}。")
        # else:
        #     order_side = 'none'
        
        
        return order_side

       
    def process_pair(self,symbol,pair_config):
        self.logger.info("=" * 60)
        # 检查是否有持仓，有持仓不进行下单
        if self.check_position(symbol=symbol) :
            self.logger.info(f"{symbol} 有持仓合约，不进行下单。")
            return 
        self.cancel_all_orders(symbol=symbol)  
        klines_period = str(pair_config.get('klines_period', '1m')) 
        
        try:
            kLines = self.get_historical_klines(symbol=symbol, bar=klines_period)
            self.logger.debug(f"开始监控 {symbol} : klines {klines_period} - {len(kLines)}")
            
            df = pd.DataFrame(kLines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            # 将时间戳转换为日期时间格式
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms').dt.strftime('%m-%d %H:%M')
            
            # 使用 TA-Lib 计算 MACD
            df[['macd', 'signal', 'hist']] = pd.DataFrame(ta.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)).T
            self.logger.debug(f"{symbol} : MACD Values = \n {df.tail(5)}")
            side = self.judge_order_side(symbol, pair_config , df)
            
            long_amount_usdt = pair_config.get('long_amount_usdt', 5)
            short_amount_usdt = pair_config.get('short_amount_usdt', 5) 
            order_amount_usdt = 5
            order_type='optimal_limit_ioc'
            order_price = df['close'].iloc[-1]
            if side == 'none' :
                self.logger.debug(f"{symbol} : 没有触发下单条件。")
                return 
            elif side == 'sell' :
                self.logger.debug(f"{symbol} : 触发做空下单条件。")
                order_amount_usdt = short_amount_usdt
            elif side == 'buy' :
                self.logger.debug(f"{symbol} : 触发做多下单条件。")
                order_amount_usdt = long_amount_usdt
            # 下单    
            self.place_order(symbol=symbol, price=order_price, amount_usdt=order_amount_usdt, side=side,order_type=order_type)
            
            
        except KeyboardInterrupt:
            self.logger.info("程序收到中断信号，开始退出...")
        except Exception as e:
            error_message = f"程序异常退出: {str(e)}"
            self.logger.error(error_message,exc_info=True)
            traceback.print_exc()
            self.send_feishu_notification(error_message)
            
        self.logger.info("-" * 60)    
        
    def monitor_klines(self):
        symbols = list(self.trading_pairs_config.keys())  # 获取所有币对的ID
        batch_size = 5  # 每批处理的数量
        while True:

            for i in range(0, len(symbols), batch_size):
                batch = symbols[i:i + batch_size]
                with ThreadPoolExecutor(max_workers=batch_size) as executor:
                    futures = [executor.submit(self.process_pair, symbol,self.trading_pairs_config[symbol]) for symbol in batch]
                    for future in as_completed(futures):
                        future.result()  # Raise any exceptions caught during execution

            time.sleep(self.monitor_interval)