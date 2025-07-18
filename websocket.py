"""
Модуль для работы с Binance WebSocket API
Получение рыночных данных в реальном времени
"""

import asyncio
import logging
import json
import websockets
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import aiohttp  # Исправлено: правильное написание
from urllib.parse import urlencode

from globals import BINANCE_WS_URL, TRADING_PAIRS, TIMEFRAMES, SAFETY_LIMITS

logger = logging.getLogger(__name__)

class BinanceWebSocket:
    def __init__(self):
        self.ws_url = BINANCE_WS_URL
        self.pairs = TRADING_PAIRS
        self.timeframes = TIMEFRAMES
        self.connections = {}
        self.market_data = {}
        self.is_running = False
        
        # Инициализация структуры данных
        self._initialize_market_data()
        
    def _initialize_market_data(self):
        """Инициализация структуры рыночных данных"""
        for pair in self.pairs:
            self.market_data[pair] = {}
            for timeframe in self.timeframes:
                self.market_data[pair][timeframe] = pd.DataFrame(columns=[
                    'timestamp', 'open', 'high', 'low', 'close', 'volume'
                ])
                
    async def initialize(self):
        """Инициализация WebSocket соединений"""
        try:
            logger.info("🔌 Инициализация Binance WebSocket...")
            
            # Получение исторических данных
            await self._fetch_historical_data()
            
            # Создание WebSocket соединений
            await self._create_websocket_connections()
            
            logger.info("✅ Binance WebSocket инициализирован")
            
        except Exception as e:
            logger.error(f"Ошибка инициализации WebSocket: {e}")
            raise
            
    async def _fetch_historical_data(self):
        """Получение исторических данных через REST API"""
        try:
            logger.info("📊 Загрузка симуляции исторических данных...")
            
            # Симуляция данных для демонстрации
            await self._generate_simulated_data()
            
            logger.info("✅ Симуляция исторических данных загружена")
            
        except Exception as e:
            logger.error(f"Ошибка загрузки исторических данных: {e}")
            raise
            
    async def _generate_simulated_data(self):
        """Генерация симуляции данных для тестирования"""
        try:
            import random
            import numpy as np
            from datetime import datetime, timedelta
            
            for pair in self.pairs:
                base_price = {
                    'BTCUSDT': 65000,
                    'ETHUSDT': 3500,
                    'BNBUSDT': 600,
                    'ADAUSDT': 0.45,
                    'XRPUSDT': 0.60,
                    'SOLUSDT': 150,
                    'DOGEUSDT': 0.25
                }.get(pair, 100)
                
                for timeframe in self.timeframes:
                    # Генерация 500 исторических свечей
                    df_data = []
                    current_time = datetime.now()
                    
                    # Определение интервала времени
                    time_delta = {
                        '1m': timedelta(minutes=1),
                        '5m': timedelta(minutes=5),
                        '15m': timedelta(minutes=15),
                        '30m': timedelta(minutes=30),
                        '1h': timedelta(hours=1),
                        '4h': timedelta(hours=4),
                        '1d': timedelta(days=1)
                    }.get(timeframe, timedelta(minutes=1))
                    
                    price = base_price
                    
                    for i in range(500):
                        # Генерация случайного движения цены
                        price_change = random.uniform(-0.05, 0.05)  # ±5%
                        price = price * (1 + price_change)
                        
                        # Генерация OHLC данных
                        open_price = price
                        high_price = price * (1 + abs(random.uniform(0, 0.02))
                        low_price = price * (1 - abs(random.uniform(0, 0.02))
                        close_price = price * (1 + random.uniform(-0.01, 0.01))
                        volume = random.uniform(1000, 10000)
                        
                        candle_time = current_time - (time_delta * (500 - i))
                        
                        df_data.append({
                            'timestamp': candle_time,
                            'open': open_price,
                            'high': high_price,
                            'low': low_price,
                            'close': close_price,
                            'volume': volume
                        })
                        
                        price = close_price
                        
                    self.market_data[pair][timeframe] = pd.DataFrame(df_data)
                    logger.debug(f"📈 Симуляция данных создана: {pair} {timeframe} - {len(df_data)} свечей")
                    
        except Exception as e:
            logger.error(f"Ошибка генерации симуляции данных: {e}")
            raise
            
    async def _fetch_pair_timeframe_data(self, session: aiohttp.ClientSession, base_url: str, pair: str, timeframe: str):
        """Получение данных для конкретной пары и таймфрейма"""
        try:
            # Параметры запроса
            params = {
                'symbol': pair,
                'interval': timeframe,
                'limit': 500  # Максимум 500 свечей
            }
            
            url = f"{base_url}?{urlencode(params)}"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Преобразование в DataFrame
                    df_data = []
                    for candle in data:
                        df_data.append({
                            'timestamp': pd.to_datetime(candle[0], unit='ms'),
                            'open': float(candle[1]),
                            'high': float(candle[2]),
                            'low': float(candle[3]),
                            'close': float(candle[4]),
                            'volume': float(candle[5])
                        })
                        
                    self.market_data[pair][timeframe] = pd.DataFrame(df_data)
                    
                    logger.debug(f"📈 Данные загружены: {pair} {timeframe} - {len(df_data)} свечей")
                    
                else:
                    logger.error(f"Ошибка загрузки данных {pair} {timeframe}: {response.status}")
                    
        except Exception as e:
            logger.error(f"Ошибка загрузки данных {pair} {timeframe}: {e}")
            
    async def _create_websocket_connections(self):
        """Создание WebSocket соединений - симуляция"""
        try:
            logger.info("🔌 Создание симуляции WebSocket соединений...")
            
            # Симуляция соединения
            self.connections['main'] = 'simulated_connection'
            
            logger.info("✅ Симуляция WebSocket соединений создана")
            
        except Exception as e:
            logger.error(f"Ошибка создания WebSocket соединений: {e}")
            raise
            
    async def _create_single_connection(self, ws_url: str):
        """Создание одного WebSocket соединения"""
        try:
            connection = await websockets.connect(ws_url)
            self.connections['main'] = connection
            
            logger.info(f"🔗 WebSocket соединение создано: {ws_url}")
            
        except Exception as e:
            logger.error(f"Ошибка создания WebSocket соединения: {e}")
            raise
            
    async def _create_multiple_connections(self, streams: List[str]):
        """Создание множественных WebSocket соединений"""
        try:
            # Разделение потоков на группы
            chunk_size = 100
            stream_chunks = [streams[i:i + chunk_size] for i in range(0, len(streams), chunk_size)]
            
            for i, chunk in enumerate(stream_chunks):
                ws_url = f"wss://stream.binance.com:9443/ws/{'/'.join(chunk)}"
                connection = await websockets.connect(ws_url)
                self.connections[f'connection_{i}'] = connection
                
                logger.info(f"🔗 WebSocket соединение {i+1} создано: {len(chunk)} потоков")
                
        except Exception as e:
            logger.error(f"Ошибка создания множественных соединений: {e}")
            raise
            
    async def start_data_stream(self):
        """Запуск потока данных - симуляция"""
        try:
            if self.is_running:
                return
                
            self.is_running = True
            logger.info("🚀 Запуск симуляции потока данных...")
            
            # Запуск симуляции обновления данных
            await self._simulate_data_updates()
            
        except Exception as e:
            logger.error(f"Ошибка запуска потока данных: {e}")
            raise
        finally:
            self.is_running = False
            
    async def _simulate_data_updates(self):
        try:
            import random
            
            while self.is_running:
                # Обновление данных для каждой пары
                for pair in self.pairs:
                    for timeframe in self.timeframes:
                        if pair in self.market_data and timeframe in self.market_data[pair]:
                            df = self.market_data[pair][timeframe]
                            
                            if len(df) > 0:
                                # Получение последней свечи
                                last_candle = df.iloc[-1].copy()
                                
                                # Обновление цены с небольшим случайным изменением
                                price_change = random.uniform(-0.001, 0.001)  # ±0.1%
                                new_close = last_candle['close'] * (1 + price_change)
                                
                                # Обновление данных последней свечи
                                df.iloc[-1, df.columns.get_loc('close')] = new_close
                                df.iloc[-1, df.columns.get_loc('high')] = max(last_candle['high'], new_close)
                                df.iloc[-1, df.columns.get_loc('low')] = min(last_candle['low'], new_close)
                                df.iloc[-1, df.columns.get_loc('volume')] = last_candle['volume'] + random.uniform(10, 100)
                                
                                logger.debug(f"📊 Симуляция обновления: {pair} {timeframe} - {new_close:.4f}")
                
                # Пауза между обновлениями
                await asyncio.sleep(1)  # Обновление каждую секунду
                
        except Exception as e:
            logger.error(f"Ошибка симуляции обновления данных: {e}")
            self.is_running = False
            
    async def _handle_connection(self, conn_name: str, connection):
        """Обработка WebSocket соединения"""
        try:
            logger.info(f"🔄 Обработка соединения: {conn_name}")
            
            async for message in connection:
                if not self.is_running:
                    break
                    
                try:
                    data = json.loads(message)
                    await self._process_message(data)
                    
                except json.JSONDecodeError:
                    logger.error(f"Ошибка декодирования JSON: {message[:100]}...")
                    continue
                    
        except websockets.exceptions.ConnectionClosed:
            logger.warning(f"WebSocket соединение {conn_name} закрыто")
            await self._reconnect_connection(conn_name)
            
        except Exception as e:
            logger.error(f"Ошибка обработки соединения {conn_name}: {e}")
            await self._reconnect_connection(conn_name)
            
    async def _process_message(self, data: Dict[str, Any]):
        """Обработка сообщения от WebSocket"""
        try:
            # Проверка типа сообщения
            if 'stream' in data and 'data' in data:
                stream = data['stream']
                kline_data = data['data']
                
                # Парсинг названия потока
                if '@kline_' in stream:
                    parts = stream.split('@kline_')
                    if len(parts) == 2:
                        pair = parts[0].upper()
                        timeframe = parts[1]
                        
                        # Обработка данных свечи
                        await self._update_candle_data(pair, timeframe, kline_data)
                        
        except Exception as e:
            logger.error(f"Ошибка обработки сообщения: {e}")
            
    async def _update_candle_data(self, pair: str, timeframe: str, kline_data: Dict[str, Any]):
        """Обновление данных свечи"""
        try:
            if pair not in self.market_data or timeframe not in self.market_data[pair]:
                return
                
            # Извлечение данных свечи
            k = kline_data.get('k', {})
            
            new_candle = {
                'timestamp': pd.to_datetime(k.get('t', 0), unit='ms'),
                'open': float(k.get('o', 0)),
                'high': float(k.get('h', 0)),
                'low': float(k.get('l', 0)),
                'close': float(k.get('c', 0)),
                'volume': float(k.get('v', 0))
            }
            
            # Обновление DataFrame
            df = self.market_data[pair][timeframe]
            
            # Проверка, является ли свеча закрытой
            is_closed = k.get('x', False)
            
            if is_closed:
                # Добавление новой свечи
                df = pd.concat([df, pd.DataFrame([new_candle])], ignore_index=True)
                
                # Ограничение размера DataFrame
                if len(df) > 1000:
                    df = df.tail(1000)
                    
                self.market_data[pair][timeframe] = df
                
                logger.debug(f"📊 Свеча обновлена: {pair} {timeframe} - {new_candle['close']}")
                
            else:
                # Обновление текущей свечи
                if len(df) > 0:
                    df.iloc[-1] = new_candle
                    
        except Exception as e:
            logger.error(f"Ошибка обновления данных свечи: {e}")
            
    async def _reconnect_connection(self, conn_name: str):
        """Переподключение WebSocket соединения"""
        try:
            logger.info(f"🔄 Переподключение: {conn_name}")
            
            # Ожидание перед переподключением
            await asyncio.sleep(SAFETY_LIMITS['reconnect_delay'])
            
            # Попытка переподключения
            for attempt in range(SAFETY_LIMITS['reconnect_attempts']):
                try:
                    # Закрытие старого соединения
                    if conn_name in self.connections:
                        await self.connections[conn_name].close()
                        del self.connections[conn_name]
                        
                    # Создание нового соединения
                    await self._create_websocket_connections()
                    
                    logger.info(f"✅ Переподключение успешно: {conn_name}")
                    return
                    
                except Exception as e:
                    logger.error(f"Попытка переподключения {attempt + 1} неудачна: {e}")
                    if attempt < SAFETY_LIMITS['reconnect_attempts'] - 1:
                        await asyncio.sleep(SAFETY_LIMITS['reconnect_delay'] * (attempt + 1))
                        
            logger.error(f"❌ Не удалось переподключиться: {conn_name}")
            
        except Exception as e:
            logger.error(f"Ошибка переподключения: {e}")
            
    def get_market_data(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        """Получение рыночных данных"""
        return self.market_data.copy()
        
    def get_latest_price(self, pair: str) -> Optional[float]:
        """Получение последней цены для пары"""
        try:
            if pair in self.market_data and '1m' in self.market_data[pair]:
                df = self.market_data[pair]['1m']
                if len(df) > 0:
                    return df['close'].iloc[-1]
            return None
            
        except Exception as e:
            logger.error(f"Ошибка получения цены для {pair}: {e}")
            return None
            
    def get_pair_timeframe_data(self, pair: str, timeframe: str) -> Optional[pd.DataFrame]:
        """Получение данных для конкретной пары и таймфрейма"""
        try:
            if pair in self.market_data and timeframe in self.market_data[pair]:
                return self.market_data[pair][timeframe].copy()
            return None
            
        except Exception as e:
            logger.error(f"Ошибка получения данных {pair} {timeframe}: {e}")
            return None
            
    async def shutdown(self):
        """Закрытие всех соединений"""
        try:
            logger.info("🛑 Закрытие WebSocket соединений...")
            
            self.is_running = False
            
            # Закрытие всех соединений
            for conn_name, connection in self.connections.items():
                try:
                    await connection.close()
                    logger.info(f"✅ Соединение {conn_name} закрыто")
                except Exception as e:
                    logger.error(f"Ошибка закрытия соединения {conn_name}: {e}")
                    
            self.connections.clear()
            
            logger.info("✅ Все WebSocket соединения закрыты")
            
        except Exception as e:
            logger.error(f"Ошибка закрытия соединений: {e}")
            
    def get_connection_status(self) -> Dict[str, Any]:
        """Получение статуса соединений"""
        return {
            'is_running': self.is_running,
            'connections_count': len(self.connections),
            'pairs_count': len(self.pairs),
            'timeframes_count': len(self.timeframes),
            'total_streams': len(self.pairs) * len(self.timeframes)
        }
        
    def get_data_statistics(self) -> Dict[str, Any]:
        """Получение статистики данных"""
        stats = {
            'total_pairs': len(self.pairs),
            'total_timeframes': len(self.timeframes),
            'data_points': {},
            'latest_updates': {}
        }
        
        for pair in self.pairs:
            stats['data_points'][pair] = {}
            stats['latest_updates'][pair] = {}
            
            for timeframe in self.timeframes:
                df = self.market_data[pair][timeframe]
                stats['data_points'][pair][timeframe] = len(df)
                
                if len(df) > 0:
                    stats['latest_updates'][pair][timeframe] = df['timestamp'].iloc[-1].isoformat()
                else:
                    stats['latest_updates'][pair][timeframe] = None
                    
        return stats
