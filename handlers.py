from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from datetime import datetime
from sqlalchemy import select
from models import User, Car, Rental, LicenseCategory
from database import AsyncSessionLocal

# Keyboard layouts
MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup([
    ['🚗 Available Cars', '📱 My Rentals'],
    ['👤 My Profile', '📞 Contact Support']
], resize_keyboard=True)

LICENSE_CATEGORIES_KEYBOARD = ReplyKeyboardMarkup([
    ['A', 'B', 'C'],
    ['D', 'BE', 'CE', 'DE'],
    ['⬅️ Back']
], resize_keyboard=True)

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    async with AsyncSessionLocal() as session:
        # Check if user exists
        query = select(User).where(User.telegram_id == update.effective_user.id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            await update.message.reply_text(
                "Welcome to Menga RentaCar! 🚗\n"
                "To get started, please share your full name."
            )
            context.user_data['registration_step'] = 'name'
        else:
            await update.message.reply_text(
                f"Welcome back, {user.full_name}! 👋\n"
                "What would you like to do?",
                reply_markup=MAIN_MENU_KEYBOARD
            )

async def register_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user registration process"""
    step = context.user_data.get('registration_step')
    
    if step == 'name':
        context.user_data['full_name'] = update.message.text
        await update.message.reply_text(
            "Please share your phone number:",
            reply_markup=ReplyKeyboardMarkup([[
                KeyboardButton('📱 Share Phone Number', request_contact=True)
            ]], resize_keyboard=True)
        )
        context.user_data['registration_step'] = 'phone'
    
    elif step == 'phone':
        if update.message.contact:
            context.user_data['phone_number'] = update.message.contact.phone_number
        else:
            context.user_data['phone_number'] = update.message.text
            
        await update.message.reply_text(
            "Please enter your driver's license number:"
        )
        context.user_data['registration_step'] = 'license'
    
    elif step == 'license':
        context.user_data['license_number'] = update.message.text
        await update.message.reply_text(
            "Please select your driver's license category:",
            reply_markup=LICENSE_CATEGORIES_KEYBOARD
        )
        context.user_data['registration_step'] = 'category'
    
    elif step == 'category':
        try:
            license_category = LicenseCategory[update.message.text]
            # Create new user
            async with AsyncSessionLocal() as session:
                new_user = User(
                    telegram_id=update.effective_user.id,
                    full_name=context.user_data['full_name'],
                    phone_number=context.user_data['phone_number'],
                    license_number=context.user_data['license_number'],
                    license_category=license_category
                )
                session.add(new_user)
                await session.commit()
            
            await update.message.reply_text(
                "Registration completed successfully! 🎉\n"
                "You can now start renting cars.",
                reply_markup=MAIN_MENU_KEYBOARD
            )
            context.user_data.clear()
        except KeyError:
            await update.message.reply_text(
                "Please select a valid license category from the keyboard."
            )