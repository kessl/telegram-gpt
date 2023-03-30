from telegram import BotCommand
from telegram.ext import (
    AIORateLimiter,
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)

import handlers
from src.config import openai_api_key, telegram_token
from src.openai_utils import Chat

openai_instance: Chat = Chat(openai_api_key)


async def post_init(application: Application) -> None:  # type: ignore
    await application.bot.set_my_commands(
        [
            BotCommand("/reset", "reset the conversation"),
            BotCommand("/mention", "toggle answer on mention"),
        ]
    )


def run_bot() -> None:
    application = (
        ApplicationBuilder()
        .token(telegram_token)
        .concurrent_updates(True)
        .rate_limiter(AIORateLimiter(max_retries=5))
        .post_init(post_init)
        .build()
    )

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.message_handler)
    )
    application.add_handler(CommandHandler("reset", handlers.reset_handler))
    application.add_handler(CommandHandler("mention", handlers.mention_handler))

    application.run_polling()


if __name__ == "__main__":
    run_bot()
