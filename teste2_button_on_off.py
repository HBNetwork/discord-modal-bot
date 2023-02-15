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
        self.botao = None

        self.botao = discord.ui.Button(label="onboarding externo", url="https://forms.gle/zCDSZ9BkkLz4u8h19",
                                       disabled=True)
        self.add_item(self.botao)

    @discord.ui.button(label="onboarding interno", style=discord.ButtonStyle.blurple, disabled=False,
                       custom_id="persistent_view:button_modal")
    async def modalButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Onboarding())
        self.botao.disabled = False                          # button on/of
        await interaction.edit_original_response(view=self)  #


class Onboarding(discord.ui.Modal, title="Onboarding - HBNetwork"):
    def __init__(self):
        super().__init__()
        self.botao = None
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
        name = self.name.value
        words = [w.capitalize() for w in name.split()]
        name = ' '.join(words)

        await interaction.response.send_message(f"nome = {name}, email = {self.email.value}", ephemeral=True)


@client.tree.command()
@app_commands.default_permissions(kick_members=True)
async def onboarding(interaction: discord.Interaction):
    await interaction.channel.send("Mensagem.", view=View())


TOKEN = config('SECRET_KEY')  # BOT TOKEN https://discord.com/developers/applications/
client.run(TOKEN)
