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


class View(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = None

    @discord.ui.button(label="Formulário", style=discord.ButtonStyle.blurple, disabled=False,
                       custom_id="persistent_view:button_modal")
    async def modalButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Onboarding())


class ButtonResponseView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = None

        botao = discord.ui.Button(label="Complete o formulario",
                                  url="https://docs.google.com/forms/d/e/1FAIpQLSco5asfmgmCqZaoBwMaKoUIk-lUC63nbAW1R5cNGG8k-5woPw/viewform",
                                  disabled=False)
        self.add_item(botao)


class Onboarding(discord.ui.Modal, title="Onboarding - HBNetwork"):
    name = discord.ui.TextInput(
        label="Nome completo",
        style=discord.TextStyle.short,
        placeholder="Digite seu nome",
        required=True,
    )
    email = discord.ui.TextInput(
        label="E-mail",
        style=discord.TextStyle.short,
        placeholder="Digite o seu email",
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        name = self.name.value.capitalize()
        words = [w.capitalize() for w in name.split()]
        name = ' '.join(words)

        if not emailValid(self.email.value):
            await interaction.response.send_message("Email Invalido.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Mensagem de resposta. EX: nome = {name}, email = {self.email.value}",
                                                    view=ButtonResponseView(), ephemeral=True)

            role = discord.utils.get(interaction.guild.roles, id=1067444184048484474)  # Role ID
            await interaction.user.add_roles(role)

            canal = interaction.guild.get_channel(1063428213633724427)  # ID channel
            embed = discord.Embed(
                title=interaction.user.id,
                description="Descrição completa",
                colour=discord.Colour.random()
            )

            embed.add_field(name="Usuario", value=f"<@{interaction.user.id}>", inline=False)
            embed.add_field(name="Nome completo: ", value=self.name.value, inline=False)
            embed.add_field(name="E-mail: ", value=self.email.value, inline=False)
            await canal.send(embed=embed)


def emailValid(endereco):
    encontrado = bool(
        re.match(r'[^0-9]\w*(\+\w*)?@\w*\.{1}\w*\.?\w*$', endereco))
    return encontrado


@client.tree.command()
@app_commands.default_permissions(kick_members=True)
async def onboarding(interaction: discord.Interaction):
    await interaction.channel.send("Para participar do nosso servidor, clique no botão abaixo e preencha o formulário.",
                                   view=View())


TOKEN = config('SECRET_KEY')  # BOT TOKEN https://discord.com/developers/applications/
client.run(TOKEN)
