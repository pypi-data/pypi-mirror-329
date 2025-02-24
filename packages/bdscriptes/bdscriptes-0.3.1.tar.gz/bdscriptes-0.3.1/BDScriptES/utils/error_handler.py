import traceback
import discord

async def handle_error(ctx, error):
    """Maneja errores y envía el mensaje con el error específico."""
    if isinstance(error, ValueError):
        await ctx.send(f"❌ {str(error)}")  # Solo muestra el mensaje del error
    else:
        await ctx.send("❌ Ha ocurrido un error inesperado.")
        print("Error detallado:", traceback.format_exc())  # Imprime el error completo en consola
