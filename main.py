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

        botao = discord.ui.Button(label="onboarding externo", url="https://www.google.com/", disabled=False)
        self.add_item(botao)

    @discord.ui.button(label="onboarding interno", style=discord.ButtonStyle.blurple, disabled=False,
                       custom_id="persistent_view:button")
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
        style=discord.TextStyle.short,
        placeholder="Digite seu Apelido",
        required=True,
    )
    naturalness = discord.ui.TextInput(
        label="Cidade/Estado",
        style=discord.TextStyle.short,
        placeholder="exemplo Salvador/BA",
        required=False,
    )
    phone = discord.ui.TextInput(
        label="numero de telefone/Whatsapp",
        style=discord.TextStyle.short,
        placeholder="Digite seu telefone",
        min_length=11,
        required=True,
    )
    email = discord.ui.TextInput(
        label="E-mail",
        style=discord.TextStyle.short,
        placeholder="Digite o seu email",
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        name = self.name.value
        words = [w.capitalize() for w in name.split()]
        name = ' '.join(words)

        await interaction.response.send_message(f"nome = {name}, apelido = {self.nickName.value}, "
                                                f"nascido em {self.phone.value}, de {self.naturalness.value}, "
                                                f"email = {self.email.value}", ephemeral=True)
        role = discord.utils.get(interaction.guild.roles, id=1067444184048484474)  # Role ID
        await interaction.user.add_roles(role)

        canal = interaction.guild.get_channel(1063428213633724427)  # ID channel
        embed = discord.Embed(
            title=interaction.user.id,
            description="Descrição completa",
            colour=discord.Colour.random()
        )
        embed.add_field(name="Usuario", value=f"<@{interaction.user.id}>", inline=False)
        embed.add_field(name="Nome: ", value=name, inline=False)
        embed.add_field(name="Apelido: ", value=self.nickName.value, inline=False)
        embed.add_field(name="Naturalidade: ", value=self.naturalness.value, inline=False)
        embed.add_field(name="Numero de telefone: ", value=self.phone.value, inline=False)
        embed.add_field(name="E-mail: ", value=self.email.value, inline=False)
        await canal.send(embed=embed)


@client.tree.command()
@app_commands.default_permissions(kick_members=True)
async def onboarding(interaction: discord.Interaction):
    await interaction.channel.send("Mensagem.", view=View())


load_dotenv()
TOKEN = os.getenv("TOKEN")  # BOT TOKEN https://discord.com/developers/applications/
client.run(TOKEN)
