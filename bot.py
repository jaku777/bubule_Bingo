elif query.data == "balance":
        await query.message.reply_text(f"💳 Your current balance is: {balance:.2f} ETB", parse_mode="Markdown")
    
    elif query.data == "deposit":
        deposit_text = (
            "💰 Deposit Funds via SMS Verification\n\n"
            "1. Transfer money to our accounts:\n"
            f"   🔹 Telebirr: {TELEBIRR_NUMBER}\n"
            f"   🔹 CBE Birr: {CBE_BIRR_NUMBER}\n\n"
            "2. Once you receive the bank/Telebirr SMS receipt, copy and paste that entire SMS text here in this chat."
        )
        await query.message.reply_text(deposit_text, parse_mode="Markdown")

    elif query.data == "withdraw":
        await query.message.reply_text("💸 Withdrawal feature will be available soon. Minimum withdrawal is 50 ETB.")

    elif query.data == "invite":
        await query.message.reply_text("🤝 Invite your friends and earn bonus coins! Share your referral link soon.")

    elif query.data == "patterns":
        await query.message.reply_text("🎯 Game Patterns: Learn about winning lines, four corners, full house, and more!")

    elif query.data == "instructions":
        await query.message.reply_text("📖 Instructions: Deposit funds, join a room, match numbers, and win big!")

async def handle_sms_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    cursor.execute("SELECT balance FROM users WHERE telegram_id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        return

    cleaned_text = text.replace(',', '')
    amount_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:ETB|Birr|ብር|Br\.?)', cleaned_text, re.IGNORECASE)
    
    if not amount_match:
        amount_match = re.search(r'(?:ETB|Birr|ብር)\s*(\d+(?:\.\d+)?)', cleaned_text, re.IGNORECASE)

    if amount_match:
        amount = float(amount_match.group(1))
        new_balance = user[0] + amount
        cursor.execute("UPDATE users SET balance = ? WHERE telegram_id = ?", (new_balance, user_id))
        conn.commit()

        await update.message.reply_text(
            f"✅ Deposit Successful!\n\n"
            f"💰 Added Amount: {amount:.2f} ETB\n"
            f"💳 New Wallet Balance: {new_balance:.2f} ETB",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("❌ Could not detect the amount from this SMS. Please make sure it's a valid receipt.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play_command))
    app.add_handler(CommandHandler("deposit", deposit_command))
    app.add_handler(CommandHandler("withdraw", withdraw_command))
    app.add_handler(CommandHandler("invite", invite_command))
    app.add_handler(CommandHandler("support", support_command))
    
    app.add_handler(MessageHandler(filters.CONTACT, register_contact))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_sms_deposit))
    
    app.post_init = set_bot_commands

    print("🤖 Bubule Bingo Bot is fully running with the new WebApp!")
    app.run_polling()

if name == "main":
    main()
