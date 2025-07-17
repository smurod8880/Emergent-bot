"""
Глобальные переменные и настройки
Стратегия "Quantum Precision V2"
"""

import os
from typing import List, Dict, Any

# Telegram настройки
BOT_TOKEN = "8177951186:AAH6h4_BEezrjDFIwdDUfiqxPNv-8aCb8u0"
CHAT_ID = 5331567990

# Binance WebSocket URL
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/"

# Торговые пары (топ 7)
TRADING_PAIRS = [
    "BTCUSDT",
    "ETHUSDT", 
    "BNBUSDT",
    "ADAUSDT",
    "XRPUSDT",
    "SOLUSDT",
    "DOGEUSDT"
]

# Таймфреймы для анализа
TIMEFRAMES = [
    "1m",   # 1 минута
    "5m",   # 5 минут
    "15m",  # 15 минут
    "30m",  # 30 минут
    "1h",   # 1 час
    "4h",   # 4 часа
    "1d"    # 1 день
]

# Настройки стратегии Quantum Precision V2
STRATEGY_CONFIG = {
    "target_accuracy": 0.85,  # 85%+ точность
    "daily_signals_target": 35,  # 30-35 сигналов в день
    "update_interval": 10,  # Обновление каждые 10 секунд
    "signal_threshold": 0.87,  # Порог для AI предсказаний
    "volume_multiplier": 3.2,  # Множитель объема для детекции
    "price_change_threshold": 0.004,  # 0.4% изменение цены
    "vwap_gradient_threshold": 0.002,  # VWAP градиент порог
    "rsi_upper_limit": 65,  # Верхний лимит RSI
}

# Настройки индикаторов
INDICATORS_CONFIG = {
    "sma_periods": [20, 50, 200],
    "ema_periods": [9, 21, 55],
    "rsi_period": 14,
    "macd_fast": 12,
    "macd_slow": 26,
    "macd_signal": 9,
    "bollinger_period": 20,
    "bollinger_std": 2,
    "volume_sma_period": 20,
    "adx_period": 14,
    "stoch_k": 14,
    "stoch_d": 3,
    "williams_period": 14,
    "cci_period": 20,
    "mfi_period": 14,
    "obv_period": 10,
    "vwap_period": 20,
    "parabolic_sar": {
        "acceleration": 0.02,
        "maximum": 0.2
    }
}

# Веса индикаторов для финального скора
INDICATOR_WEIGHTS = {
    "vwap_gradient": 0.25,
    "volume_tsunami": 0.20,
    "neural_macd": 0.15,
    "quantum_rsi": 0.15,
    "ai_prediction": 0.25
}

# Настройки AI модели
AI_MODEL_CONFIG = {
    "sequence_length": 60,  # Длина последовательности для LSTM
    "features_count": 20,   # Количество признаков
    "hidden_size": 128,     # Размер скрытого слоя
    "num_layers": 2,        # Количество слоев LSTM
    "dropout": 0.3,         # Dropout для регуляризации
    "learning_rate": 0.001, # Скорость обучения
    "batch_size": 32,       # Размер батча
    "epochs": 100,          # Количество эпох
    "retrain_interval": 3600  # Переобучение каждые 1 час
}

# Лимиты безопасности
SAFETY_LIMITS = {
    "max_signals_per_hour": 5,
    "min_signal_interval": 60,  # Минимальный интервал между сигналами (сек)
    "max_daily_signals": 50,
    "connection_timeout": 30,
    "reconnect_attempts": 5,
    "reconnect_delay": 5
}

# Пути к файлам
DATA_DIR = "/app/data"
DB_PATH = f"{DATA_DIR}/trading_bot.db"
MODELS_DIR = f"{DATA_DIR}/models"
LOGS_DIR = f"{DATA_DIR}/logs"

# Создание директорий если их нет
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Настройки базы данных
DATABASE_CONFIG = {
    "signals_table": "signals",
    "market_data_table": "market_data",
    "performance_table": "performance",
    "max_records": 100000,  # Максимальное количество записей
    "cleanup_interval": 86400  # Очистка каждые 24 часа
}

# Форматы сообщений
MESSAGE_FORMATS = {
    "signal": """
🚀 СИГНАЛ QUANTUM PRECISION V2

📊 Пара: {pair}
⏰ Таймфрейм: {timeframe}
🎯 Точность: {accuracy}%
🕐 Время входа: {entry_time}
⏱️ Держать: {hold_duration} мин

📈 Детали:
• VWAP Gradient: {vwap_gradient}
• Volume Tsunami: {volume_tsunami}
• Neural MACD: {neural_macd}
• Quantum RSI: {quantum_rsi}
• AI Score: {ai_score}

💡 Направление: {direction}
""",
    
    "daily_stats": """
📊 ДНЕВНАЯ СТАТИСТИКА

🎯 Сигналов сегодня: {signals_count}
✅ Успешных: {successful_signals}
📈 Точность: {accuracy}%
💰 Средняя прибыль: {avg_profit}%

🔥 Лучшие пары:
{best_pairs}
""",
    
    "error": """
❌ ОШИБКА СИСТЕМЫ

🔧 Модуль: {module}
📝 Описание: {error}
🕐 Время: {timestamp}
""",
    
    "status": """
🤖 СТАТУС БОТА

🔄 Работает: {uptime}
📊 Анализируется: {pairs_count} пар
⏰ Таймфреймы: {timeframes_count}
🎯 Точность: {current_accuracy}%
📈 Сигналов за час: {signals_per_hour}
"""
}

# Настройки логирования
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "max_file_size": 10 * 1024 * 1024,  # 10 MB
    "backup_count": 5,
    "log_files": {
        "main": "trading_bot.log",
        "signals": "signals.log",
        "errors": "errors.log",
        "performance": "performance.log"
    }
}

# Переменные состояния (глобальные)
trading_active = False
bot_started = False
current_signals = {}
performance_stats = {
    "total_signals": 0,
    "successful_signals": 0,
    "failed_signals": 0,
    "accuracy": 0.0,
    "daily_signals": 0,
    "hourly_signals": 0
}

# Кэш данных рынка
market_data_cache = {}
indicators_cache = {}
ai_predictions_cache = {}

# Время последнего обновления
last_update_time = None
last_signal_time = None
last_cleanup_time = None

# Состояние подключений
connection_status = {
    "binance_ws": False,
    "telegram": False,
    "database": False,
    "ai_model": False
}
