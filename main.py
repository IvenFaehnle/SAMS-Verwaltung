import discord
import os
from discord.ext import commands
from server import stay_alive

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='>', intents=intents)
tree = bot.tree

ALLOWED_ROLE_IDS = [1367220175744798721, 943241957654814790, 993615970390261770, 950844059025539112]
CHANNEL_GENERAL_ID = 979128951723155557
CHANNEL_QUIT_ID = 979128097527976017
CHANNEL_BLACKLIST_ID = 1009520367284531220
CHANNEL_GEBURTSURKUNDEN_ID = 1389714794575040663
CHANNEL_LOG_ID = 1390077428944212118
SYNC_ROLE_ID = 906845737281810443

def has_required_role(interaction: discord.Interaction) -> bool:
    return any(role.id in ALLOWED_ROLE_IDS for role in interaction.user.roles)

def is_allowed_channel(interaction: discord.Interaction, expected_channel: int | list[int]) -> bool:
    if isinstance(expected_channel, list):
        return interaction.channel_id in expected_channel
    return interaction.channel_id == expected_channel

async def send_wrong_channel_response(interaction: discord.Interaction, expected_channel_id: int | list[int]):
    if isinstance(expected_channel_id, list):
        channels = ', '.join(f"<#{cid}>" for cid in expected_channel_id)
    else:
        channels = f"<#{expected_channel_id}>"
    await interaction.response.send_message(
        f"❌ Dieser Befehl darf nur in {channels} verwendet werden.", ephemeral=True)

async def send_missing_role_response(interaction: discord.Interaction):
    await interaction.response.send_message(
        "❌ Du hast keine Berechtigung, diesen Befehl zu verwenden.", ephemeral=True)

async def resolve_mentions_to_text(interaction: discord.Interaction, text: str) -> str:
    for user_id in [int(u_id) for u_id in set(discord.utils.re.findall(r'<@!?(\d+)>', text))]:
        user = interaction.guild.get_member(user_id)
        if user:
            text = text.replace(f"<@{user_id}>", user.display_name)
            text = text.replace(f"<@!{user_id}>", user.display_name)

    for role_id in [int(r_id) for r_id in set(discord.utils.re.findall(r'<@&(\d+)>', text))]:
        role = interaction.guild.get_role(role_id)
        if role:
            text = text.replace(f"<@&{role_id}>", role.name)

    return text

async def log_command_use(interaction: discord.Interaction, command_name: str, params: dict):
    channel = bot.get_channel(CHANNEL_LOG_ID)
    if channel is None:
        print(f"⚠️ Log-Kanal mit ID {CHANNEL_LOG_ID} nicht gefunden!")
        return

    param_lines = "\n".join(f"**{key}:** {value}" for key, value in params.items())
    embed = discord.Embed(
        title=f"Slash-Befehl verwendet: /{command_name}",
        description=f"**Benutzer:** {interaction.user} ({interaction.user.id})\n**Kanal:** <#{interaction.channel_id}>",
        color=discord.Color.blurple()
    )
    embed.add_field(name="Parameter", value=param_lines or "Keine", inline=False)
    embed.timestamp = discord.utils.utcnow()

    await channel.send(embed=embed)


@tree.command(name="beförderung", description="Fülle eine Beförderung aus.")
async def befoerderung(interaction: discord.Interaction, name: str, alter_rang: str, neuer_rang: str, ausgefuehrt_von: str, datum: str, grund: str):
    await log_command_use(interaction, "beförderung", {
        "name": name,
        "alter_rang": alter_rang,
        "neuer_rang": neuer_rang,
        "ausgefuehrt_von": ausgefuehrt_von,
        "datum": datum,
        "grund": grund
    })

    if not has_required_role(interaction):
        await send_missing_role_response(interaction)
        return
    if not is_allowed_channel(interaction, CHANNEL_GENERAL_ID):
        await send_wrong_channel_response(interaction, CHANNEL_GENERAL_ID)
        return

    name = await resolve_mentions_to_text(interaction, name)
    alter_rang = await resolve_mentions_to_text(interaction, alter_rang)
    neuer_rang = await resolve_mentions_to_text(interaction, neuer_rang)
    ausgefuehrt_von = await resolve_mentions_to_text(interaction, ausgefuehrt_von)
    grund = await resolve_mentions_to_text(interaction, grund)

    embed = discord.Embed(title="__**Beförderung:**__ :green_square:", color=discord.Color.green())
    embed.add_field(name="Name der beförderten Person", value=name, inline=False)
    embed.add_field(name="Alter Rang", value=alter_rang, inline=False)
    embed.add_field(name="Neuer Rang", value=neuer_rang, inline=False)
    embed.add_field(name="Name des Ausführenden", value=ausgefuehrt_von, inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)
    embed.add_field(name="Grund", value=grund, inline=False)

    await bot.get_channel(CHANNEL_GENERAL_ID).send(embed=embed)
    await interaction.response.send_message("✅ Beförderung wurde erfolgreich veröffentlicht.", ephemeral=True)

@tree.command(name="degradierung", description="Fülle eine Degradierung aus.")
async def degradierung(interaction: discord.Interaction, name: str, alter_rang: str, neuer_rang: str, datum: str, grund: str):
    await log_command_use(interaction, "degradierung", {
        "name": name,
        "alter_rang": alter_rang,
        "neuer_rang": neuer_rang,
        "datum": datum,
        "grund": grund
    })

    if not has_required_role(interaction):
        await send_missing_role_response(interaction)
        return
    if not is_allowed_channel(interaction, CHANNEL_GENERAL_ID):
        await send_wrong_channel_response(interaction, CHANNEL_GENERAL_ID)
        return

    name = await resolve_mentions_to_text(interaction, name)
    alter_rang = await resolve_mentions_to_text(interaction, alter_rang)
    neuer_rang = await resolve_mentions_to_text(interaction, neuer_rang)
    grund = await resolve_mentions_to_text(interaction, grund)

    embed = discord.Embed(title="__**Degradierung:**__ 🟥", color=discord.Color.dark_red())
    embed.add_field(name="Name der degradierten Person", value=name, inline=False)
    embed.add_field(name="Alter Rang", value=alter_rang, inline=False)
    embed.add_field(name="Neuer Rang", value=neuer_rang, inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)
    embed.add_field(name="Grund", value=grund, inline=False)

    await bot.get_channel(CHANNEL_GENERAL_ID).send(embed=embed)
    await interaction.response.send_message("✅ Degradierung wurde erfolgreich veröffentlicht.", ephemeral=True)

@tree.command(name="suspendierung", description="Fülle eine Suspendierung aus.")
async def suspendierung(interaction: discord.Interaction, name: str, ausgefuehrt_von: str, datum: str, grund: str):
    await log_command_use(interaction, "suspendierung", {
        "name": name,
        "ausgefuehrt_von": ausgefuehrt_von,
        "datum": datum,
        "grund": grund
    })

    if not has_required_role(interaction):
        await send_missing_role_response(interaction)
        return
    if not is_allowed_channel(interaction, CHANNEL_QUIT_ID):
        await send_wrong_channel_response(interaction, CHANNEL_QUIT_ID)
        return

    name = await resolve_mentions_to_text(interaction, name)
    ausgefuehrt_von = await resolve_mentions_to_text(interaction, ausgefuehrt_von)
    grund = await resolve_mentions_to_text(interaction, grund)

    embed = discord.Embed(title="__**Suspendierung:**__ 🟨", color=discord.Color.gold())
    embed.add_field(name="Name der Suspendierten Person:", value=name, inline=False)
    embed.add_field(name="Ausgeführt von", value=ausgefuehrt_von, inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)
    embed.add_field(name="Grund", value=grund, inline=False)

    await bot.get_channel(CHANNEL_QUIT_ID).send(embed=embed)
    await interaction.response.send_message("✅ Suspendierung wurde erfolgreich veröffentlicht.", ephemeral=True)

@tree.command(name="kündigung", description="Fülle eine Kündigung aus.")
async def kuendigung(interaction: discord.Interaction, name: str, ausgefuehrt_von: str, datum: str, grund: str):
    await log_command_use(interaction, "kündigung", {
        "name": name,
        "ausgefuehrt_von": ausgefuehrt_von,
        "datum": datum,
        "grund": grund
    })

    if not has_required_role(interaction):
        await send_missing_role_response(interaction)
        return
    if not is_allowed_channel(interaction, CHANNEL_QUIT_ID):
        await send_wrong_channel_response(interaction, CHANNEL_QUIT_ID)
        return

    name = await resolve_mentions_to_text(interaction, name)
    ausgefuehrt_von = await resolve_mentions_to_text(interaction, ausgefuehrt_von)
    grund = await resolve_mentions_to_text(interaction, grund)

    embed = discord.Embed(title="__**Kündigung:**__ ❌", color=discord.Color.red())
    embed.add_field(name="Name der gekündigten Person:", value=name, inline=False)
    embed.add_field(name="Ausgeführt von", value=ausgefuehrt_von, inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)
    embed.add_field(name="Grund", value=grund, inline=False)

    await bot.get_channel(CHANNEL_QUIT_ID).send(embed=embed)
    await interaction.response.send_message("✅ Kündigung wurde erfolgreich veröffentlicht.", ephemeral=True)

@tree.command(name="blacklist", description="Füge jemanden zur Blacklist hinzu.")
async def blacklist(interaction: discord.Interaction, name: str, hinzugefuegt_von: str, dauer: str, datum: str, grund: str):
    await log_command_use(interaction, "blacklist", {
        "name": name,
        "hinzugefuegt_von": hinzugefuegt_von,
        "dauer": dauer,
        "datum": datum,
        "grund": grund
    })

    if not has_required_role(interaction):
        await send_missing_role_response(interaction)
        return
    if not is_allowed_channel(interaction, CHANNEL_BLACKLIST_ID):
        await send_wrong_channel_response(interaction, CHANNEL_BLACKLIST_ID)
        return

    name = await resolve_mentions_to_text(interaction, name)
    hinzugefuegt_von = await resolve_mentions_to_text(interaction, hinzugefuegt_von)
    grund = await resolve_mentions_to_text(interaction, grund)

    embed = discord.Embed(title="__**Blacklist-Eintrag:**__ ⛔", color=discord.Color.dark_purple())
    embed.add_field(name="Person", value=name, inline=False)
    embed.add_field(name="Hinzugefügt von", value=hinzugefuegt_von, inline=False)
    embed.add_field(name="Dauer", value=dauer, inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)
    embed.add_field(name="Grund", value=grund, inline=False)

    await bot.get_channel(CHANNEL_BLACKLIST_ID).send(embed=embed)
    await interaction.response.send_message("✅ Blacklist-Eintrag wurde erfolgreich veröffentlicht.", ephemeral=True)

@tree.command(name="beitritt", description="Trage einen Spezialisierungsbeitritt ein.")
async def beitritt(interaction: discord.Interaction, name: str, spezialisierung: str, ausgefuehrt_von: str, datum: str):
    await log_command_use(interaction, "beitritt", {
        "name": name,
        "spezialisierung": spezialisierung,
        "ausgefuehrt_von": ausgefuehrt_von,
        "datum": datum
    })

    if not has_required_role(interaction):
        await send_missing_role_response(interaction)
        return
    if not is_allowed_channel(interaction, CHANNEL_GENERAL_ID):
        await send_wrong_channel_response(interaction, CHANNEL_GENERAL_ID)
        return

    name = await resolve_mentions_to_text(interaction, name)
    spezialisierung = await resolve_mentions_to_text(interaction, spezialisierung)
    ausgefuehrt_von = await resolve_mentions_to_text(interaction, ausgefuehrt_von)

    embed = discord.Embed(title="__**Spezialisierungsbeitritt:**__ <:added:1103413152001048746>", color=discord.Color.blue())
    embed.add_field(name="Name der Person", value=name, inline=False)
    embed.add_field(name="Spezialisierung", value=spezialisierung, inline=False)
    embed.add_field(name="Ausgeführt von", value=ausgefuehrt_von, inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)

    await bot.get_channel(CHANNEL_GENERAL_ID).send(embed=embed)
    await interaction.response.send_message("✅ Spezialisierungsbeitritt wurde erfolgreich veröffentlicht.", ephemeral=True)

@tree.command(
    name="austritt",
    description="Trage einen spezialisierungsinternen Austritt ein."
)
async def austritt(
    interaction: discord.Interaction,
    name: str,
    spezialisierung: str,
    alter_rang: str,
    neuer_rang: str,
    ausgefuehrt_von: str,
    datum: str,
    grund: str
):
    if not has_required_role(interaction):
        await send_missing_role_response(interaction)
        return

    if not is_allowed_channel(interaction, CHANNEL_GENERAL_ID):
        await send_wrong_channel_response(interaction, CHANNEL_GENERAL_ID)
        return

    await bot.get_channel(CHANNEL_GENERAL_ID).send(embed=embed)
    await interaction.response.send_message("✅ Spezialisierungsinterner Austritt wurde erfolgreich veröffentlicht.", ephemeral=True)
@tree.command(name="geburtsurkunde", description="Stellt eine Geburtsurkunde aus.") async def geburtsurkunde(interaction: discord.Interaction, name: str, geburtsdatum: str, ausgestellt_von: str, datum: str): if not has_required_role(interaction): await send_missing_role_response(interaction) return if not is_allowed_channel(interaction, CHANNEL_Geburtsurkunden_ID): await send_wrong_channel_response(interaction, CHANNEL_Geburtsurkunden_ID) return

name = await resolve_mentions_to_text(interaction, name)
ausgestellt_von = await resolve_mentions_to_text(interaction, ausgestellt_von)

@tree.command(name="geburtsurkunde", description="Stellt eine Geburtsurkunde aus.")
async def geburtsurkunde(interaction: discord.Interaction, name: str, geburtsdatum: str, ausgestellt_von: str, datum: str):
    if not has_required_role(interaction):
        await send_missing_role_response(interaction)
        return
    if not is_allowed_channel(interaction, CHANNEL_GEBURTSURKUNDEN_ID):
        await send_wrong_channel_response(interaction, CHANNEL_GEBURTSURKUNDEN_ID)
        return

    name = await resolve_mentions_to_text(interaction, name)
    ausgestellt_von = await resolve_mentions_to_text(interaction, ausgestellt_von)

    embed = discord.Embed(title="__**Geburtsurkunde Ausgestellt**__ :green_square:", color=discord.Color.green())
    embed.add_field(name="Name der Person", value=name, inline=False)
    embed.add_field(name="Geburtsdatum", value=geburtsdatum, inline=False)
    embed.add_field(name="Ausgestellt von", value=ausgestellt_von, inline=False)
    embed.add_field(name="Geldeingang Fraktionskasse", value="$200,000", inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)

    await bot.get_channel(CHANNEL_GEBURTSURKUNDEN_ID).send(embed=embed)
    await interaction.response.send_message("✅ Geburtsurkunde wurde erfolgreich ausgestellt.", ephemeral=True)

@tree.command(name="geburtsurkunden_sperre", description="Stellt eine Sperre für eine Geburtsurkunde aus.")
async def geburtsurkunden_sperre(interaction: discord.Interaction, name: str, geburtsdatum: str, ausgestellt_von: str, grund: str, datum: str):
    if not has_required_role(interaction):
        await send_missing_role_response(interaction)
        return
    if not is_allowed_channel(interaction, CHANNEL_GEBURTSURKUNDEN_ID):
        await send_wrong_channel_response(interaction, CHANNEL_GEBURTSURKUNDEN_ID)
        return

    name = await resolve_mentions_to_text(interaction, name)
    ausgestellt_von = await resolve_mentions_to_text(interaction, ausgestellt_von)
    grund = await resolve_mentions_to_text(interaction, grund)

    embed = discord.Embed(title="__**Geburtsurkunden Sperre**__ :red_square:", color=discord.Color.red())
    embed.add_field(name="Name der Person", value=name, inline=False)
    embed.add_field(name="Geburtsdatum", value=geburtsdatum, inline=False)
    embed.add_field(name="Ausgestellt von", value=ausgestellt_von, inline=False)
    embed.add_field(name="Dauer", value="2 Wochen", inline=False)
    embed.add_field(name="Grund", value=grund, inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)

    await bot.get_channel(CHANNEL_GEBURTSURKUNDEN_ID).send(embed=embed)
    await interaction.response.send_message("⛔ Sperre wurde erfolgreich veröffentlicht.", ephemeral=True)

@tree.command(name="sync", description="Synchronisiere Slash-Commands mit Discord.")
async def sync(interaction: discord.Interaction):
    if SYNC_ROLE_ID not in [role.id for role in interaction.user.roles]:
        await send_missing_role_response(interaction)
        return

    await interaction.response.defer(ephemeral=True)
    synced = await tree.sync()
    await interaction.edit_original_response(content=f"✅ Slash-Commands wurden synchronisiert. ({len(synced)} Befehle)")
    print(f"🔄 Slash-Commands synchronisiert: {len(synced)}")

@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot ist online als {bot.user}")

if __name__ == '__main__':
    stay_alive()
    bot.run(os.environ['DISCORD_TOKEN'])
