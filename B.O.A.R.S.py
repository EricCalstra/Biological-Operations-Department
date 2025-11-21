import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(e)

# ---- REGISTER COMMAND ----
@bot.tree.command(name="register", description="Register a user with ranks")
@app_commands.describe(rank="Rank to give", user="User to register")
async def register(interaction: discord.Interaction, rank: str, user: discord.Member):

    # Roles you want to add
    roles_to_add = ["ScD", "Intern", "Registered"]

    # Make the rank given in the command also count as a role
    roles_to_add.insert(0, rank)

    # Try to add roles
    added = []
    missing = []

    for role_name in roles_to_add:
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if role:
            await user.add_roles(role)
            added.append(role_name)
        else:
            missing.append(role_name)

    # Response message
    msg = f"✅ **{user.display_name}** has been registered!\n\n**Added roles:** {', '.join(added)}"

    if missing:
        msg += f"\n⚠ Missing roles on server: {', '.join(missing)}"

    await interaction.response.send_message(msg, ephemeral=True)

bot.run(TOKEN)
