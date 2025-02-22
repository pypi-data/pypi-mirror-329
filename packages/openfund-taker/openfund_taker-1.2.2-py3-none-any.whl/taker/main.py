import os
import json
import logging
from logging.handlers import TimedRotatingFileHandler

from taker.MultiAssetNewTradingBot import MultiAssetNewTradingBot
from taker.ThreeLineTradingBot import ThreeLineTradingBot

def build_logger(log_config) -> logging.Logger:
            # 配置日志
        # log_file = "log/okx_MultiAssetNewTradingBot.log"
        log_file = log_config["file"] 
        logger = logging.getLogger(__name__)
        logger.setLevel(log_config["level"])

        file_handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7, encoding='utf-8')
        file_handler.suffix = "%Y-%m-%d"
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger



def main():
    import importlib.metadata
    version = importlib.metadata.version("openfund-taker")
    
    openfund_config_path = 'config.json'
    
    with open(openfund_config_path, 'r') as f:
        config_data = json.load(f)
        
    platform_config = config_data['okx']
    feishu_webhook_url = config_data['feishu_webhook']
    monitor_interval = config_data.get("monitor_interval", 60)  # 默认值为60秒
    logger = build_logger(config_data["Logger"])
    package_name = __package__ or "taker"
    
    logger.info(f" ++ {package_name}:{version} is doing...")
    bot = MultiAssetNewTradingBot(config_data, platform_config, feishu_webhook=feishu_webhook_url, monitor_interval=monitor_interval,logger=logger)
    bot.monitor_total_profit()
    # bot = ThreeLineTradingBot(platform_config, feishu_webhook=feishu_webhook_url, monitor_interval=monitor_interval)
    # bot.monitor_klines()

if __name__ == "__main__":
    main()
