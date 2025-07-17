"""
Модуль для работы с Telegram Bot API
Отправка сигналов и управление ботом
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import json

from telegram import Update, Bot as TelegramBot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

from globals import BOT_TOKEN, CHAT_ID, MESSAGE_FORMATS

logger = logging.getLogger(name)

class TelegramBotHandler:
    def init(self, token: str, chat_id: int):
        self.token = token
        self.chat_id = chat_id
        self.bot = None
        self.application = None
        self.is_running = False
        
        # Статистика
        self.sent_messages = 0
        self.errors_count = 0
        
    async def initialize(self):
        """Инициализация Telegram бота"""
        try:
            logger.info("📱 Инициализация Telegram бота...")
            
            # Создание приложения
            self.application = Application.builder().token(self.token).build()
            self.bot = self.application.bot
            
            # Проверка подключения
            await self.test_connection()
            
            logger.info("✅ Telegram бот инициализирован")
            
        except Exception as e:
            logger.error(f"Ошибка инициализации Telegram бота: {e}")
            raise
            
    async def test_connection(self):
        """Тестирование подключения к Telegram API"""
        try:
            me = await self.bot.get_me()
            logger.info(f"🤖 Подключен к боту: @{me.username}")
            
            # Отправка тестового сообщения
            await self.send_message("🔧 Тестирование подключения... OK")
            
        except Exception as e:
            logger.error(f"Ошибка тестирования подключения: {e}")
            raise
            
    async def send_message(self, text: str, parse_mode: str = ParseMode.MARKDOWN) -> bool:
        """Отправка сообщения в Telegram"""
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                parse_mode=parse_mode
            )
            
            self.sent_messages += 1
            logger.debug(f"📤 Сообщение отправлено: {text[:50]}...")
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения: {e}")
            self.errors_count += 1
            return False
            
    async def send_signal(self, signal_data: Dict[str, Any]) -> bool:
        """Отправка торгового сигнала"""
        try:
            # Форматирование сообщения
            message = MESSAGE_FORMATS['signal'].format(
                pair=signal_data['pair'],
                timeframe=signal_data['timeframe'],
                accuracy=signal_data['accuracy'],
                entry_time=signal_data['entry_time'],
                hold_duration=signal_data['hold_duration'],
                vwap_gradient=signal_data.get('vwap_gradient', 0),
                volume_tsunami=signal_data.get('volume_tsunami', 0),
                neural_macd=signal_data.get('neural_macd', 0),
                quantum_rsi=signal_data.get('quantum_rsi', 0),
                ai_score=signal_data.get('ai_score', 0),
                direction=signal_data['direction']
            )
            
            # Отправка сигнала
            success = await self.send_message(message)
            
            if success:
                logger.info(f"✅ Сигнал отправлен: {signal_data['pair']} {signal_data['timeframe']}")
            else:
                logger.error(f"❌ Ошибка отправки сигнала: {signal_data['pair']} {signal_data['timeframe']}")
                
            return success
            
        except Exception as e:
            logger.error(f"Ошибка отправки сигнала: {e}")
            return False
            
    async def send_daily_stats(self, stats: Dict[str, Any]) -> bool:
        """Отправка дневной статистики"""
        try:

# Форматирование лучших пар
            best_pairs_text = ""
            for pair in stats.get('best_pairs', []):
                best_pairs_text += f"• {pair['pair']}: {pair['accuracy']:.1f}% ({pair['total_signals']} сигналов)\n"
                
            if not best_pairs_text:
                best_pairs_text = "Нет данных"
                
            # Форматирование сообщения
            message = MESSAGE_FORMATS['daily_stats'].format(
                signals_count=stats.get('total_signals', 0),
                successful_signals=stats.get('successful_signals', 0),
                accuracy=stats.get('accuracy', 0),
                avg_profit=stats.get('avg_profit', 0),
                best_pairs=best_pairs_text
            )
            
            return await self.send_message(message)
            
        except Exception as e:
            logger.error(f"Ошибка отправки статистики: {e}")
            return False
            
    async def send_error(self, module: str, error: str) -> bool:
        """Отправка уведомления об ошибке"""
        try:
            message = MESSAGE_FORMATS['error'].format(
                module=module,
                error=error,
                timestamp=datetime.now().strftime('%H:%M:%S')
            )
            
            return await self.send_message(message)
            
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления об ошибке: {e}")
            return False
            
    async def send_status(self, status_data: Dict[str, Any]) -> bool:
        """Отправка статуса бота"""
        try:
            message = MESSAGE_FORMATS['status'].format(
                uptime=status_data.get('uptime', 'N/A'),
                pairs_count=status_data.get('pairs_count', 0),
                timeframes_count=status_data.get('timeframes_count', 0),
                current_accuracy=status_data.get('current_accuracy', 0),
                signals_per_hour=status_data.get('signals_per_hour', 0)
            )
            
            return await self.send_message(message)
            
        except Exception as e:
            logger.error(f"Ошибка отправки статуса: {e}")
            return False
            
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /start"""
        try:
            from bot_control import BotController
            
            # Получение контроллера из globals
            import globals
            if hasattr(globals, 'bot_controller'):
                controller = globals.bot_controller
                await controller.start_trading()
                
                await update.message.reply_text(

"🚀 Торговый бот запущен!**\n\n"
                    "Анализ рынка начат. Ожидайте сигналы...",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await update.message.reply_text(
                    "❌ Контроллер бота не найден. Попробуйте позже."
                )
                
        except Exception as e:
            logger.error(f"Ошибка команды /start: {e}")
            await update.message.reply_text(
                "❌ Ошибка запуска бота. Проверьте логи."
            )
            
    async def stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /stop"""
        try:
            from bot_control import BotController
            
            # Получение контроллера из globals
            import globals
            if hasattr(globals, 'bot_controller'):
                controller = globals.bot_controller
                await controller.stop_trading()
                
                await update.message.reply_text(
                    "🛑 **Торговый бот остановлен!**\n\n"
                    "Анализ рынка приостановлен.",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await update.message.reply_text(
                    "❌ Контроллер бота не найден."
                )
                
        except Exception as e:
            logger.error(f"Ошибка команды /stop: {e}")
            await update.message.reply_text(
                "❌ Ошибка остановки бота. Проверьте логи."
            )
            
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /status"""
        try:
            # Получение статуса системы
            import globals
            
            status_data = {
                'uptime': 'N/A',
                'pairs_count': len(globals.TRADING_PAIRS),
                'timeframes_count': len(globals.TIMEFRAMES),
                'current_accuracy': globals.performance_stats.get('accuracy', 0),
                'signals_per_hour': globals.performance_stats.get('hourly_signals', 0)
            }
            
            await self.send_status(status_data)
            
        except Exception as e:
            logger.error(f"Ошибка команды /status: {e}")
            await update.message.reply_text(
                "❌ Ошибка получения статуса. Проверьте логи."
            )
            
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /stats"""
        try:
            # Получение статистики из базы данных
            import globals
            
            stats = {
                'total_signals': globals.performance_stats.get('total_signals', 0),
                'successful_signals': globals.performance_stats.get('successful_signals', 0),
                'accuracy': globals.performance_stats.get('accuracy', 0),
                'avg_profit': 0.0,
                'best_pairs': []
            }
            
            await self.send_daily_stats(stats)
            
        except Exception as e:
            logger.error(f"Ошибка команды /stats: {e}")
            await update.message.reply_text(
                "❌ Ошибка получения статистики. Проверьте логи."
            )
            
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /help"""
        try:
            help_text = """
🤖 **Команды торгового бота:

/start - Запуск анализа и торговли
/stop - Остановка торговли
/status - Текущий статус бота
/stats - Статистика за день
/help - Это сообщение

📊 Стратегия: Quantum Precision V2
🎯 Цель: 85%+ точность
📈 Сигналы: 30-35 в день
⏰ Обновление: каждые 10 секунд

🔧 Поддержка: Automatic Trading System
            """
            
            await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            logger.error(f"Ошибка команды /help: {e}")
            await update.message.reply_text(
                "❌ Ошибка отображения помощи."
            )
            
    async def run(self):
        """Запуск Telegram бота"""
        try:
            if self.is_running:
                return
                
            self.is_running = True
            logger.info("🚀 Запуск Telegram бота...")
            
            # Простой режим без polling для демонстрации
            logger.info("✅ Telegram бот запущен в демонстрационном режиме")
            
            # Отправка стартового сообщения
            await self.send_message("🚀 Бот запущен! Используйте /start для начала торговли.")
            
            # Бесконечный цикл
            while self.is_running:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Ошибка запуска Telegram бота: {e}")
            raise
        finally:
            await self.shutdown()
            
    async def shutdown(self):
        """Корректное завершение работы бота"""
        try:
            if not self.is_running:
                return
                
            self.is_running = False
            logger.info("🛑 Остановка Telegram бота...")
            
            if self.application:
                await self.application.updater.stop()
                await self.application.stop()
                await self.application.shutdown()
                
            logger.info("✅ Telegram бот остановлен")
            
        except Exception as e:
            logger.error(f"Ошибка остановки Telegram бота: {e}")
            
    def get_statistics(self) -> Dict[str, Any]:
        """Получение статистики бота"""
        return {
            'sent_messages': self.sent_messages,
            'errors_count': self.errors_count,
            'is_running': self.is_running,
            'chat_id': self.chat_id
        }
