import os
import discord
from discord import app_commands
from dotenv import load_dotenv

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

    @discord.ui.button(label="Botão Normal", style=discord.ButtonStyle.blurple, disabled=False,
                       custom_id="persistent_view:botton")
    async def modalButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Onboarding())


class Onboarding(discord.ui.Modal, title="Onboarding - HBNetwork"):
    name = discord.ui.TextInput(
        label="Nome completo",
        style=discord.TextStyle.short,
        placeholder="Digite seu nome",
        required=True,
    )
    nickName = discord.ui.TextInput(
        label="Apelido",
        style=discord.TextStyle.paragraph,
        placeholder="Digite seu Apelido",
        required=True,
    )
    birthDate = discord.ui.TextInput(
        label="Data de nascimento ",
        style=discord.TextStyle.paragraph,
        placeholder="Digite sua data de nascimento",
        required=False,
    )
    naturalness = discord.ui.TextInput(
        label="Cidade/Estado",
        style=discord.TextStyle.paragraph,
        placeholder="exemplo Salvador/BA",
        required=True
    )
    email = discord.ui.TextInput(
        label="E-mail",
        style=discord.TextStyle.paragraph,
        placeholder="Digite o seu email",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"nome = {self.name.value}, apelido = {self.nickName.value}, "
                                                f"nascido em {self.birthDate.value}, de {self.naturalness.value}, "
                                                f"email = {self.email.value}", ephemeral=True)
        role = discord.utils.get(interaction.guild.roles, id=1067444184048484474)  # Role ID
        await interaction.user.add_roles(role)


@client.tree.command()
async def onboarding(interaction: discord.Interaction):
    await interaction.response.send_message("Mensagem.", view=View())


load_dotenv()
TOKEN = os.getenv("TOKEN")  # BOT TOKEN https://discord.com/developers/applications/
client.run(TOKEN)
