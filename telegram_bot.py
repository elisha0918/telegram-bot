#!/usr/bin/env python3
"""
Telegram Bot 主程式
支援接收訊息、回覆訊息、處理命令等基本功能
"""

import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# 載入環境變數
load_dotenv()

# 設定日誌
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 從環境變數取得 Bot Token
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("請設定 TELEGRAM_BOT_TOKEN 環境變數")


# 命令處理器
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /start 命令"""
    user = update.effective_user
    await update.message.reply_html(
        f"您好 {user.mention_html()}！👋\n\n"
        f"我是您的 Telegram Bot。\n\n"
        f"可用命令：\n"
        f"/start - 顯示此訊息\n"
        f"/help - 獲取幫助\n"
        f"/echo [文字] - 重複您的訊息"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /help 命令"""
    help_text = """
📚 **幫助**

以下是可用的命令：

/start - 開始使用 Bot
/help - 顯示此幫助訊息
/echo [文字] - 重複您輸入的文字

**功能說明：**
- 您可以直接發送任何訊息給 Bot
- Bot 會自動回覆並記錄您的訊息
- 使用命令前加上 / 符號
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /echo 命令 - 重複使用者的訊息"""
    if not context.args:
        await update.message.reply_text("請提供要重複的文字。\n用法: /echo [文字]")
        return
    
    text = ' '.join(context.args)
    await update.message.reply_text(f"🔄 您說: {text}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理一般訊息"""
    user = update.effective_user
    message_text = update.message.text
    
    logger.info(f"收到來自 {user.first_name} (ID: {user.id}) 的訊息: {message_text}")
    
    # 簡單的回應邏輯
    if '你好' in message_text or '你好' in message_text:
        response = f"你好 {user.first_name}！很高興認識您 😊"
    elif '謝謝' in message_text:
        response = "不客氣！有什麼我可以幫助的嗎？"
    elif '幫助' in message_text or '幫忙' in message_text:
        response = "您可以使用 /help 命令來查看所有可用的功能。"
    else:
        response = f"我收到您的訊息: \"{message_text}\"\n\n有什麼我可以幫助的嗎？"
    
    await update.message.reply_text(response)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """記錄錯誤"""
    logger.error(msg="發生例外:", exc_info=context.error)


def main() -> None:
    """啟動 Bot"""
    # 建立 Application
    application = Application.builder().token(BOT_TOKEN).build()

    # 新增命令處理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("echo", echo))

    # 新增訊息處理器（在命令處理器之後）
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # 新增錯誤處理器
    application.add_error_handler(error_handler)

    # 啟動 Bot
    logger.info("Bot 啟動中...")
    application.run_polling()


if __name__ == '__main__':
    main()
