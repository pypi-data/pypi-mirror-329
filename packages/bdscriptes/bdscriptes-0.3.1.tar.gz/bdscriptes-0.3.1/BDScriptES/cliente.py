# cliente.py
import discord
from discord.ext import commands
from BDScriptES.commands.command_handler import CommandHandler


class BDScriptES(commands.Bot):
    def __init__(self, *args, **kwargs):
        # Configurar los intents
        intents = discord.Intents.all()
        super().__init__(*args, **kwargs, intents=intents)
        self.command_handler = CommandHandler(self)

    def new_command(self, name, type, code):
        """
        Registra un nuevo comando.
        """
        # Registrar el comando en el CommandHandler
        self.command_handler.new_command(name, type, code)

    async def on_ready(self):
        print(f'Logged in as {self.user}')

