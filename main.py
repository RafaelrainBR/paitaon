import random

import discord
from discord.ext import commands

from model.words_model import Words
from repository.impl.words_repository import WordsRepository
from state import BotState
from storage.storage import Storage

client = commands.Bot(command_prefix=['+'], case_insensitive=True)

state = BotState()


def start_bot():
    bot_storage = Storage()
    state.words_repository = WordsRepository(bot_storage)

    client.run('')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('+setchannel'):
        state.channel = message.channel
        await send_embed(message.author, message.channel, 'Canal do bot', 'Canal de mensagens setado com sucesso!')
        return

    if message.content.startswith('+unsetchannel'):
        state.channel = None
        await send_embed(message.author, message.channel, 'Canal do bot', 'Não irei mais utilizar esse canal.')
        return

    if message.channel != state.channel:
        return

    if message.content.startswith('+sim'):
        all_words = state.words_repository.select_all()
        if len(all_words) == 0:
            await send_embed(message.author, message.channel, 'Erro',
                             'Ainda não tem nenhuma palavra no banco de dados.')
            return

        words = random.choice(all_words)

        author = await client.fetch_user(words.author)

        await send_embed(message.author, message.channel, words.text, f'Autor: {author.name}#{author.discriminator}')

    if message.content.startswith('+adicionartexto '):
        text = message.content.replace('+adicionartexto ', '')
        words = Words(text=text, author=message.author.id)

        state.words_repository.insert(words)

        await send_embed(message.author, message.channel, 'Sucesso!', 'Você adicionou uma mensagem com sucesso!')
        return


async def send_embed(user, channel, title, description):
    embed = discord.Embed(title=title, description=description, color=0xf40101)
    embed.set_author(url=client.user.avatar_url, name='')
    embed.set_footer(text=f'comando requisitado por {user.name}#{user.discriminator}', icon_url=user.avatar_url)
    await channel.send(embed=embed)


if __name__ == '__main__':
    start_bot()
