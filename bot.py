async def get_category_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("ðŸ“¥ Use: /get <category>")
        return

    category = context.args[0]

    if category not in categories:
        await update.message.reply_text(f"âŒ Invalid category! Use one of these:\n{', '.join(categories)}")
        return

    image_list = image_urls.get(category)
    if image_list:
        image_link = random.choice(image_list)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_link)
    else:
        await update.message.reply_text("âŒ No images found in this category.")
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "ai_chat":
        await query.edit_message_text("ðŸ§  AI Chat active! Use /ai <message>")
    elif query.data == "save_image":
        await query.edit_message_text("ðŸ“¥ Use /save <category> <image_url>")
    elif query.data == "youtube_info":
        await query.edit_message_text("ðŸŽ¥ Use /youtube <url>")
    elif query.data == "weather":
        await query.edit_message_text("ðŸŒ¤ Use /weather <city>")
    elif query.data == "web_search":
        await query.edit_message_text("ðŸ” Use /search <query>")
    elif query.data == "bot_stats":
        await bot_stats_command(update, context)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_stats['messages_processed'] += 1
    if not update.message.text.startswith('/'):
        context.args = update.message.text.split()
        await ai_chat(update, context)

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ai", ai_chat))
    app.add_handler(CommandHandler("youtube", youtube_info))
    app.add_handler(CommandHandler("weather", weather_command))
    app.add_handler(CommandHandler("search", web_search))
    app.add_handler(CommandHandler("save", save_image_command))
    app.add_handler(CommandHandler("stats", bot_stats_command))
    app.add_handler(CommandHandler("get", get_category_image))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(button_callback))
    logger.info("ðŸš€ Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
