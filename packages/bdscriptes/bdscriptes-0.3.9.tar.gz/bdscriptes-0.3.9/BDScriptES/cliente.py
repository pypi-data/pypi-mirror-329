import discord
from discord.ext import commands
from BDScriptES.commands.command_handler import CommandHandler

class BDScriptES(commands.Bot):
    def __init__(self, *args, **kwargs):
        intents = discord.Intents().all()
        super().__init__(*args, **kwargs, intents=intents)
        self.command_handler = CommandHandler(self)

    def new_command(self, name, type, code):
        """
        Registra un nuevo comando.
        """
        self.command_handler.new_command(name, type, code)

    def new_event(self, type, code):
        """
        Registra un nuevo evento.
        """
        self.command_handler.new_event(type, code)

    async def on_ready(self):
        print(f'✅ Bot conectado como {self.user}')
