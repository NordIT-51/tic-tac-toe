import aiogram
import random
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

token = '6499859568:AAEXZzXQNpHHWBAdN5kegUuKuBk6gCmf1h4'

status_game = False
ga = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
bot = aiogram.Bot(token=token)
dp = aiogram.Dispatcher(bot)


def make_keyboard():
    keyboard = InlineKeyboardMarkup()
    for i in range(0, 3):
        keyboard.add(InlineKeyboardButton(text=ga[(0 + 3 * i) // 3][(0 + 3 * i) % 3], \
                                          callback_data=str(1 + 3 * i)),
                     InlineKeyboardButton(text=ga[(1 + 3 * i) // 3][(1 + 3 * i) % 3], \
                                          callback_data=str(2 + 3 * i)),
                     InlineKeyboardButton(text=ga[(2 + 3 * i) // 3][(2 + 3 * i) % 3], \
                                          callback_data=str(3 + 3 * i)))
    return keyboard


@dp.message_handler(commands=['game'])
async def handler(msg):
    global status_game
    status_game = True
    await msg.reply('Ходи первым!', reply_markup=make_keyboard())


def is_win(s):
    if ga[0][0] == ga[1][1] == ga[2][2] == s:
        return True
    if ga[0][2] and ga[1][1] == ga[2][0] == s:
        return True
    for i in range(0, 3):
        if ga[0][i] == ga[1][i] == ga[2][i] == s:
            return True
        if ga[i][0] == ga[i][1] == ga[i][2] == s:
            return True
    return False


def is_not_draw():
    for i in range(0, 3):
        for j in range(0, 3):
            if ga[i][j] == ' ':
                return True
    return False


@dp.callback_query_handler()
async def gamer(call: aiogram.types.CallbackQuery):
    global status_game, ga
    print(ga)
    if not status_game:
        await bot.send_message(call.from_user.id, 'Ты сейчас не играешь!')
        return

    coord = int(call.data) - 1
    if ga[coord // 3][coord % 3] == ' ':
        ga[coord // 3][coord % 3] = 'X'
        await bot.edit_message_text(call.message.text, call.message.chat.id, call.message.message_id, reply_markup=make_keyboard())
        if is_win('X'):
            await bot.edit_message_text('Ты выиграл!', call.message.chat.id, call.message.message_id, reply_markup=make_keyboard())
            status_game = False
            ga = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
            return
        if not is_not_draw():
            await bot.edit_message_text('Ничья!', call.message.chat.id, call.message.message_id, reply_markup=make_keyboard())
            status_game = False
            ga = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
            return
        while True:
            n = random.randint(0, 10000) % 9
            if ga[n // 3][n % 3] == ' ':
                ga[n // 3][n % 3] = 'O'
                await bot.edit_message_text(call.message.text, call.message.chat.id, call.message.message_id,
                                            reply_markup=make_keyboard())
                break
        if is_win('O'):
            await bot.edit_message_text('Я выиграл!', call.message.chat.id, call.message.message_id, reply_markup=make_keyboard())
            status_game = False
            ga = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
            return
        if not is_not_draw():
            await bot.edit_message_text('Ничья!', call.message.chat.id, call.message.message_id, reply_markup=make_keyboard())
            status_game = False
            ga = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
            return
    else:
        await bot.edit_message_text('Вы не можете поставить сюда крестик!',
                                    call.message.chat.id, call.message.message_id, reply_markup=make_keyboard())
        return


if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
