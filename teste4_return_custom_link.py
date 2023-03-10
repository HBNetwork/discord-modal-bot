import re
import discord
from discord import app_commands
from decouple import config

id_ = 1063136274715779102  # SERVER ID
id_server = discord.Object(id_)


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents, application_id=1063513740156342374)  # CLIENT ID
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.add_view(View())
        self.tree.copy_global_to(guild=id_server)
        await self.tree.sync(guild=id_server)


client = MyClient(intents=discord.Intents.default())


@client.event
async def on_ready():
    print("O bot está funcionando!")


class View(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = None

    @discord.ui.button(label="onboarding interno", style=discord.ButtonStyle.blurple, disabled=False,
                       custom_id="persistent_view:button_modal")
    async def modalButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Onboarding())


class Onboarding(discord.ui.Modal, title="Onboarding - HBNetwork"):
    name = discord.ui.TextInput(
        label="Nome completo",
        style=discord.TextStyle.short,
        placeholder="Digite o seu nome completo",
        required=True,
    )

    email = discord.ui.TextInput(
        label="E-mail",
        style=discord.TextStyle.short,
        placeholder="Digite o seu email",
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        name = self.name.value.replace(" ", "%20")

        if not emailValid(self.email.value):
            await interaction.response.send_message("Email Invalido.", ephemeral=True)
        else:
            await interaction.response.send_message(f"https://docs.google.com/forms/d/e/1FAIpQLSco5asfmgmCqZaoBwMaKoUIk-lUC63nbAW1R5cNGG8k-5woPw/viewform?usp=pp_url&entry.546964655={interaction.user.id}&entry.516220657={self.email.value}&entry.1409361470={name}&entry.28498539={interaction.user.name}",
                                                    ephemeral=True)


def emailValid(endereco):
    encontrado = bool(
        re.match(r'[^0-9]\w*(\+\w*)?@\w*\.{1}\w*\.?\w*$', endereco))
    return encontrado


@client.tree.command()
@app_commands.default_permissions(kick_members=True)
async def onboarding(interaction: discord.Interaction):
    await interaction.channel.send("Mensagem.", view=View())


TOKEN = config('SECRET_KEY')  # BOT TOKEN https://discord.com/developers/applications/
client.run(TOKEN)
