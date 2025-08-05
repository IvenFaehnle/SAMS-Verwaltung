import discord
from discord.ext import commands
from discord.ext import commands
from server import stay_alive
import asyncio
import re
from datetime import timedelta
import random
import string
import io

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='>', intents=intents)
tree = bot.tree

ALLOWED_ROLE_IDS = [906845737281810443, 1367220175744798721, 943241957654814790, 993615970390261770, 1378086334849093683]
CHANNEL_GENERAL_ID = 979128951723155557
CHANNEL_QUIT_ID = 979128097527976017
CHANNEL_BLACKLIST_ID = 1009520367284531220
CHANNEL_GEBURTSURKUNDEN_ID = 1389714794575040663
CHANNEL_LOG_ID = 1401575829267550330
MOD_LOG_CHANNEL_ID = 1328008745963356180
SYNC_ROLE_ID = 906845737281810443
LÖSCHEN_LOG_CHANNEL_ID = 1052369974573932626
PROMOTES_SPERREN = 1394763356023296173

def has_required_role(interaction: discord.Interaction) -> bool:
    return any(role.id in ALLOWED_ROLE_IDS for role in interaction.user.roles)


def is_allowed_channel(interaction: discord.Interaction,
                       expected_channel: int | list[int]) -> bool:
    if isinstance(expected_channel, list):
        return interaction.channel_id in expected_channel
    return interaction.channel_id == expected_channel


async def send_wrong_channel_response(interaction: discord.Interaction,
                                      expected_channel_id: int | list[int]):
    if isinstance(expected_channel_id, list):
        channels = ', '.join(f"<#{cid}>" for cid in expected_channel_id)
    else:
        channels = f"<#{expected_channel_id}>"
    await interaction.response.send_message(
        f"❌ Dieser Befehl darf nur in {channels} verwendet werden.",
        ephemeral=True)


async def send_missing_role_response(interaction: discord.Interaction):
    await interaction.response.send_message(
        "❌ Du hast keine Berechtigung, diesen Befehl zu verwenden.",
        ephemeral=True)


async def resolve_mentions_to_text(interaction: discord.Interaction,
                                   text: str) -> str:
    for user_id in [
            int(u_id)
            for u_id in set(discord.utils.re.findall(r'<@!?(\d+)>', text))
    ]:
        user = interaction.guild.get_member(user_id)
        if user:
            text = text.replace(f"<@{user_id}>", user.display_name)
            text = text.replace(f"<@!{user_id}>", user.display_name)

    for role_id in [
            int(r_id)
            for r_id in set(discord.utils.re.findall(r'<@&(\d+)>', text))
    ]:
        role = interaction.guild.get_role(role_id)
        if role:
            text = text.replace(f"<@&{role_id}>", role.name)

    return text


async def log_command_use(interaction: discord.Interaction, command_name: str,
                          params: dict):
    channel = bot.get_channel(CHANNEL_LOG_ID)
    if channel is None:
        print(f"⚠️ Log-Kanal mit ID {CHANNEL_LOG_ID} nicht gefunden!")
        return

    param_lines = "\n".join(f"**{key}:** {value}"
                            for key, value in params.items())
    embed = discord.Embed(
        title=f"Slash-Befehl verwendet: /{command_name}",
        description=
        f"**Benutzer:** {interaction.user} ({interaction.user.id})\n**Kanal:** <#{interaction.channel_id}>",
        color=discord.Color.blurple())
    embed.add_field(name="Parameter",
                    value=param_lines or "Keine",
                    inline=False)
    embed.timestamp = discord.utils.utcnow()

    await channel.send(embed=embed)


@tree.command(name="interne_weiterbildung",
              description="Trage eine interne Weiterbildung ein.")
async def interne_weiterbildung(interaction: discord.Interaction, name: str,
                                art_der_weiterbildung: str,
                                aktueller_rang: str, ausgefuehrt_von: str,
                                datum: str):
    if not has_required_role(interaction):
        await send_missing_role_response(interaction)
        return

    if not is_allowed_channel(interaction, CHANNEL_GENERAL_ID):
        await send_wrong_channel_response(interaction, CHANNEL_GENERAL_ID)
        return

    await log_command_use(
        interaction, "interne_weiterbildung", {
            "name": name,
            "art_der_weiterbildung": art_der_weiterbildung,
            "aktueller_rang": aktueller_rang,
            "ausgefuehrt_von": ausgefuehrt_von,
            "datum": datum
        })

    name = await resolve_mentions_to_text(interaction, name)
    art_der_weiterbildung = await resolve_mentions_to_text(
        interaction, art_der_weiterbildung)
    aktueller_rang = await resolve_mentions_to_text(interaction,
                                                    aktueller_rang)
    ausgefuehrt_von = await resolve_mentions_to_text(interaction,
                                                     ausgefuehrt_von)

    embed = discord.Embed(
        title="__**Interne Weiterbildung:**__ :mortar_board:",
        color=discord.Color.teal())
    embed.add_field(name="Name der Ausgebildeten Person",
                    value=name,
                    inline=False)
    embed.add_field(name="Art der Weiterbildung",
                    value=art_der_weiterbildung,
                    inline=False)
    embed.add_field(name="Aktueller Rang des Ausgebildeten",
                    value=aktueller_rang,
                    inline=False)
    embed.add_field(name="Name des Auszuführenden",
                    value=ausgefuehrt_von,
                    inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)

    await bot.get_channel(CHANNEL_GENERAL_ID).send(embed=embed)
    await interaction.response.send_message(
        "✅ Interne Weiterbildung wurde erfolgreich veröffentlicht.",
        ephemeral=True)


@tree.command(name="beförderung", description="Fülle eine Beförderung aus.")
async def befoerderung(interaction: discord.Interaction, name: str,
                       alter_rang: str, neuer_rang: str, ausgefuehrt_von: str,
                       datum: str, grund: str):
    await log_command_use(
        interaction, "beförderung", {
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
    ausgefuehrt_von = await resolve_mentions_to_text(interaction,
                                                     ausgefuehrt_von)
    grund = await resolve_mentions_to_text(interaction, grund)

    embed = discord.Embed(title="__**Beförderung:**__ :green_square:",
                          color=discord.Color.green())
    embed.add_field(name="Name der beförderten Person",
                    value=name,
                    inline=False)
    embed.add_field(name="Alter Rang", value=alter_rang, inline=False)
    embed.add_field(name="Neuer Rang", value=neuer_rang, inline=False)
    embed.add_field(name="Name des Ausführenden",
                    value=ausgefuehrt_von,
                    inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)
    embed.add_field(name="Grund", value=grund, inline=False)

    await bot.get_channel(CHANNEL_GENERAL_ID).send(embed=embed)
    await interaction.response.send_message(
        "✅ Beförderung wurde erfolgreich veröffentlicht.", ephemeral=True)


@tree.command(name="degradierung", description="Fülle eine Degradierung aus.")
async def degradierung(interaction: discord.Interaction, name: str,
                       alter_rang: str, neuer_rang: str, datum: str,
                       grund: str):
    await log_command_use(
        interaction, "degradierung", {
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

    embed = discord.Embed(title="__**Degradierung:**__ 🟥",
                          color=discord.Color.dark_red())
    embed.add_field(name="Name der degradierten Person",
                    value=name,
                    inline=False)
    embed.add_field(name="Alter Rang", value=alter_rang, inline=False)
    embed.add_field(name="Neuer Rang", value=neuer_rang, inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)
    embed.add_field(name="Grund", value=grund, inline=False)

    await bot.get_channel(CHANNEL_GENERAL_ID).send(embed=embed)
    await interaction.response.send_message(
        "✅ Degradierung wurde erfolgreich veröffentlicht.", ephemeral=True)


@tree.command(name="suspendierung",
              description="Fülle eine Suspendierung aus.")
async def suspendierung(interaction: discord.Interaction, name: str,
                        ausgefuehrt_von: str, datum: str, grund: str):
    await log_command_use(
        interaction, "suspendierung", {
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
    ausgefuehrt_von = await resolve_mentions_to_text(interaction,
                                                     ausgefuehrt_von)
    grund = await resolve_mentions_to_text(interaction, grund)

    embed = discord.Embed(title="__**Suspendierung:**__ ⌛",
                          color=discord.Color.gold())
    embed.add_field(name="Name der Suspendierten Person:",
                    value=name,
                    inline=False)
    embed.add_field(name="Ausgeführt von", value=ausgefuehrt_von, inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)
    embed.add_field(name="Grund", value=grund, inline=False)

    await bot.get_channel(CHANNEL_QUIT_ID).send(embed=embed)
    await interaction.response.send_message(
        "✅ Suspendierung wurde erfolgreich veröffentlicht.", ephemeral=True)


@tree.command(name="kündigung", description="Fülle eine Kündigung aus.")
async def kuendigung(interaction: discord.Interaction, name: str,
                     ausgefuehrt_von: str, datum: str, grund: str):
    await log_command_use(
        interaction, "kündigung", {
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
    ausgefuehrt_von = await resolve_mentions_to_text(interaction,
                                                     ausgefuehrt_von)
    grund = await resolve_mentions_to_text(interaction, grund)

    embed = discord.Embed(title="__**Kündigung:**__ ❌",
                          color=discord.Color.red())
    embed.add_field(name="Name der gekündigten Person:",
                    value=name,
                    inline=False)
    embed.add_field(name="Ausgeführt von", value=ausgefuehrt_von, inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)
    embed.add_field(name="Grund", value=grund, inline=False)

    await bot.get_channel(CHANNEL_QUIT_ID).send(embed=embed)
    await interaction.response.send_message(
        "✅ Kündigung wurde erfolgreich veröffentlicht.", ephemeral=True)


@tree.command(name="blacklist",
              description="Füge jemanden zur Blacklist hinzu.")
async def blacklist(interaction: discord.Interaction, name: str,
                    hinzugefuegt_von: str, dauer: str, datum: str, grund: str):
    await log_command_use(
        interaction, "blacklist", {
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
    hinzugefuegt_von = await resolve_mentions_to_text(interaction,
                                                      hinzugefuegt_von)
    grund = await resolve_mentions_to_text(interaction, grund)

    embed = discord.Embed(title="__**Blacklist-Eintrag:**__ ⛔",
                          color=discord.Color.dark_purple())
    embed.add_field(name="Person", value=name, inline=False)
    embed.add_field(name="Hinzugefügt von",
                    value=hinzugefuegt_von,
                    inline=False)
    embed.add_field(name="Dauer", value=dauer, inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)
    embed.add_field(name="Grund", value=grund, inline=False)

    await bot.get_channel(CHANNEL_BLACKLIST_ID).send(embed=embed)
    await interaction.response.send_message(
        "✅ Blacklist-Eintrag wurde erfolgreich veröffentlicht.",
        ephemeral=True)


@tree.command(name="beitritt",
              description="Trage einen Spezialisierungsbeitritt ein.")
async def beitritt(interaction: discord.Interaction, name: str,
                   spezialisierung: str, ausgefuehrt_von: str, datum: str):
    await log_command_use(
        interaction, "beitritt", {
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
    spezialisierung = await resolve_mentions_to_text(interaction,
                                                     spezialisierung)
    ausgefuehrt_von = await resolve_mentions_to_text(interaction,
                                                     ausgefuehrt_von)

    embed = discord.Embed(
        title="__**Spezialisierungsbeitritt:**__ <:added:1103413152001048746>",
        color=discord.Color.blue())
    embed.add_field(name="Name der Person", value=name, inline=False)
    embed.add_field(name="Spezialisierung",
                    value=spezialisierung,
                    inline=False)
    embed.add_field(name="Ausgeführt von", value=ausgefuehrt_von, inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)

    await bot.get_channel(CHANNEL_GENERAL_ID).send(embed=embed)
    await interaction.response.send_message(
        "✅ Spezialisierungsbeitritt wurde erfolgreich veröffentlicht.",
        ephemeral=True)


@tree.command(
    name="beförderungs_sperre",
    description="Fügt eine Beförderungssperre für eine Person hinzu.")
async def befoerderungs_sperre(interaction: discord.Interaction, name: str,
                               hinzugefuegt_von: str, dauer: str, datum: str,
                               grund: str):
    if not is_allowed_channel(interaction, PROMOTES_SPERREN):
        await send_wrong_channel_response(interaction, PROMOTES_SPERREN)
        return

    await log_command_use(
        interaction, "beförderungs_sperre", {
            "name": name,
            "hinzugefuegt_von": hinzugefuegt_von,
            "dauer": dauer,
            "datum": datum,
            "grund": grund
        })

    if not has_required_role(interaction):
        await send_missing_role_response(interaction)
        return

    name = await resolve_mentions_to_text(interaction, name)
    hinzugefuegt_von = await resolve_mentions_to_text(interaction,
                                                      hinzugefuegt_von)
    grund = await resolve_mentions_to_text(interaction, grund)

    embed = discord.Embed(title="__**Beförderungssperre:**__ 🚫",
                          color=discord.Color.dark_orange())
    embed.add_field(name="Name der Person", value=name, inline=False)
    embed.add_field(name="Hinzugefügt von",
                    value=hinzugefuegt_von,
                    inline=False)
    embed.add_field(name="Dauer", value=dauer, inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)
    embed.add_field(name="Grund", value=grund, inline=False)

    await bot.get_channel(PROMOTES_SPERREN).send(embed=embed)
    await interaction.response.send_message(
        "✅ Beförderungssperre wurde erfolgreich veröffentlicht.",
        ephemeral=True)


@tree.command(name="entsperren",
              description="Hebt eine bestehende Beförderungssperre auf.")
async def entsperren(interaction: discord.Interaction, name: str,
                     entsperrt_von: str, datum: str, grund: str):
    if not is_allowed_channel(interaction, PROMOTES_SPERREN):
        await send_wrong_channel_response(interaction, PROMOTES_SPERREN)
        return

    await log_command_use(
        interaction, "entsperren", {
            "name": name,
            "entsperrt_von": entsperrt_von,
            "datum": datum,
            "grund": grund
        })

    if not has_required_role(interaction):
        await send_missing_role_response(interaction)
        return

    name = await resolve_mentions_to_text(interaction, name)
    entsperrt_von = await resolve_mentions_to_text(interaction, entsperrt_von)
    grund = await resolve_mentions_to_text(interaction, grund)

    embed = discord.Embed(title="__**Beförderungssperre aufgehoben:**__ ✅",
                          color=discord.Color.green())
    embed.add_field(name="Name der Person", value=name, inline=False)
    embed.add_field(name="Entsperrt von", value=entsperrt_von, inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)
    embed.add_field(name="Grund", value=grund, inline=False)

    await bot.get_channel(PROMOTES_SPERREN).send(embed=embed)
    await interaction.response.send_message(
        "✅ Beförderungssperre wurde erfolgreich aufgehoben.", ephemeral=True)


@tree.command(name="austritt",
              description="Trage einen spezialisierungsinternen Austritt ein.")
async def austritt(interaction: discord.Interaction, name: str,
                   spezialisierung: str, alter_rang: str, neuer_rang: str,
                   ausgefuehrt_von: str, datum: str, grund: str):
    if not has_required_role(interaction):
        await send_missing_role_response(interaction)
        return

    if not is_allowed_channel(interaction, CHANNEL_GENERAL_ID):
        await send_wrong_channel_response(interaction, CHANNEL_GENERAL_ID)
        return

    name = await resolve_mentions_to_text(interaction, name)
    spezialisierung = await resolve_mentions_to_text(interaction,
                                                     spezialisierung)
    alter_rang = await resolve_mentions_to_text(interaction, alter_rang)
    neuer_rang = await resolve_mentions_to_text(interaction, neuer_rang)
    ausgefuehrt_von = await resolve_mentions_to_text(interaction,
                                                     ausgefuehrt_von)
    grund = await resolve_mentions_to_text(interaction, grund)

    embed = discord.Embed(title="__**Spezialisierungsinterner Austritt:**__ 🟧",
                          color=discord.Color.orange())
    embed.add_field(name="Name der Person", value=name, inline=False)
    embed.add_field(name="Spezialisierung",
                    value=spezialisierung,
                    inline=False)
    embed.add_field(name="Alter Rang", value=alter_rang, inline=False)
    embed.add_field(name="Neuer Rang", value=neuer_rang, inline=False)
    embed.add_field(name="Ausgeführt von", value=ausgefuehrt_von, inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)
    embed.add_field(name="Grund", value=grund, inline=False)

    await bot.get_channel(CHANNEL_GENERAL_ID).send(embed=embed)
    await interaction.response.send_message(
        "✅ Spezialisierungsinterner Austritt wurde erfolgreich veröffentlicht.",
        ephemeral=True)


@tree.command(name="geburtsurkunde",
              description="Stellt eine Geburtsurkunde aus.")
async def geburtsurkunde(interaction: discord.Interaction, name: str,
                         geburtsdatum: str, ausgestellt_von: str, datum: str):
    if not has_required_role(interaction):
        await send_missing_role_response(interaction)
        return

    if not is_allowed_channel(interaction, CHANNEL_GEBURTSURKUNDEN_ID):
        await send_wrong_channel_response(interaction,
                                          CHANNEL_GEBURTSURKUNDEN_ID)
        return

    name = await resolve_mentions_to_text(interaction, name)
    ausgestellt_von = await resolve_mentions_to_text(interaction,
                                                     ausgestellt_von)

    embed = discord.Embed(
        title="__**Geburtsurkunde Ausgestellt**__ :green_square:",
        color=discord.Color.green())
    embed.add_field(name="Name der Person", value=name, inline=False)
    embed.add_field(name="Geburtsdatum", value=geburtsdatum, inline=False)
    embed.add_field(name="Ausgestellt von",
                    value=ausgestellt_von,
                    inline=False)
    embed.add_field(name="Geldeingang Fraktionskasse",
                    value="$200,000",
                    inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)

    await bot.get_channel(CHANNEL_GEBURTSURKUNDEN_ID).send(embed=embed)
    await interaction.response.send_message(
        "✅ Geburtsurkunde wurde erfolgreich ausgestellt.", ephemeral=True)


@tree.command(name="geburtsurkunden_sperre",
              description="Stellt eine Sperre für eine Geburtsurkunde aus.")
async def geburtsurkunden_sperre(interaction: discord.Interaction, name: str,
                                 geburtsdatum: str, ausgestellt_von: str,
                                 grund: str, datum: str):
    if not has_required_role(interaction):
        await send_missing_role_response(interaction)
        return
    if not is_allowed_channel(interaction, CHANNEL_GEBURTSURKUNDEN_ID):
        await send_wrong_channel_response(interaction,
                                          CHANNEL_GEBURTSURKUNDEN_ID)
        return

    name = await resolve_mentions_to_text(interaction, name)
    ausgestellt_von = await resolve_mentions_to_text(interaction,
                                                     ausgestellt_von)
    grund = await resolve_mentions_to_text(interaction, grund)

    embed = discord.Embed(title="__**Geburtsurkunden Sperre**__ :red_square:",
                          color=discord.Color.red())
    embed.add_field(name="Name der Person", value=name, inline=False)
    embed.add_field(name="Geburtsdatum", value=geburtsdatum, inline=False)
    embed.add_field(name="Ausgestellt von",
                    value=ausgestellt_von,
                    inline=False)
    embed.add_field(name="Dauer", value="2 Wochen", inline=False)
    embed.add_field(name="Grund", value=grund, inline=False)
    embed.add_field(name="Datum", value=datum, inline=False)

    await bot.get_channel(CHANNEL_GEBURTSURKUNDEN_ID).send(embed=embed)
    await interaction.response.send_message(
        "⛔ Sperre wurde erfolgreich veröffentlicht.", ephemeral=True)


@tree.command(name="sync",
              description="Synchronisiere Slash-Commands mit Discord.")
async def sync(interaction: discord.Interaction):
    if SYNC_ROLE_ID not in [role.id for role in interaction.user.roles]:
        await send_missing_role_response(interaction)
        return

    await interaction.response.defer(ephemeral=True)
    synced = await tree.sync()
    await interaction.edit_original_response(
        content=
        f"✅ Slash-Commands wurden synchronisiert. ({len(synced)} Befehle)")
    print(f"🔄 Slash-Commands synchronisiert: {len(synced)}")


CODE_STORAGE_FILE = 'moderation_codes.json'


def load_codes():
    try:
        with open(CODE_STORAGE_FILE, 'r') as f:
            data = json.load(f)
            return data.get("UNBAN_CODES", {}), data.get("UNMUTE_CODES", {})
    except:
        return {}, {}


def save_codes():
    with open(CODE_STORAGE_FILE, 'w') as f:
        json.dump({
            "UNBAN_CODES": UNBAN_CODES,
            "UNMUTE_CODES": UNMUTE_CODES
        },
                  f,
                  indent=4)


UNBAN_CODES, UNMUTE_CODES = load_codes()


def generate_code(prefix: str, length: int = 5) -> str:
    code = ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"{prefix}-{code}"


class UnbanButton(discord.ui.View):

    def __init__(self, code):
        super().__init__(timeout=None)
        self.code = code
        self.add_item(
            discord.ui.Button(label=f"Unban ({code})",
                              style=discord.ButtonStyle.green,
                              custom_id=f"unban:{code}"))


class UnmuteButton(discord.ui.View):

    def __init__(self, code):
        super().__init__(timeout=None)
        self.code = code
        self.add_item(
            discord.ui.Button(label=f"Unmute ({code})",
                              style=discord.ButtonStyle.blurple,
                              custom_id=f"unmute:{code}"))


@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.component:
        return

    custom_id = interaction.data.get("custom_id", "")
    if custom_id.startswith("unban:"):
        code = custom_id.split(":")[1]
        user_id = UNBAN_CODES.pop(code, None)
        save_codes()
        if not user_id:
            await interaction.response.send_message(
                "❌ Ungültiger oder abgelaufener Unban-Code.", ephemeral=True)
            return
        try:
            await interaction.guild.unban(discord.Object(id=int(user_id)))
            await interaction.response.send_message(
                f"✅ Nutzer mit ID `{user_id}` wurde entbannt.")
        except Exception as e:
            await interaction.response.send_message(f"❌ Fehler: {e}",
                                                    ephemeral=True)

    elif custom_id.startswith("unmute:"):
        code = custom_id.split(":")[1]
        user_id = UNMUTE_CODES.pop(code, None)
        save_codes()
        if not user_id:
            await interaction.response.send_message(
                "❌ Ungültiger oder abgelaufener Unmute-Code.", ephemeral=True)
            return
        member = interaction.guild.get_member(int(user_id))
        if not member:
            await interaction.response.send_message(
                "❌ Nutzer ist nicht auf dem Server.", ephemeral=True)
            return
        try:
            await member.timeout(None)
            await interaction.response.send_message(
                f"✅ Timeout für {member.mention} wurde aufgehoben.")
        except Exception as e:
            await interaction.response.send_message(f"❌ Fehler: {e}",
                                                    ephemeral=True)


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("s!löschen"):
                parts = message.content.split()
                if len(parts) != 2 or not parts[1].isdigit():
                    await message.channel.send("\u274c Benutzung: `s!löschen <Anzahl>`", delete_after=5)
                    return

                amount = int(parts[1])
                log_channel = bot.get_channel(LÖSCHEN_LOG_CHANNEL_ID)

                try:
                    deleted = await message.channel.purge(limit=amount + 1)
                    confirmation = await message.channel.send(f"\u2705 {len(deleted) - 1} Nachricht(en) gelöscht.", delete_after=5)


                    log_lines = []
                    for msg in reversed(deleted[1:]):
                        timestamp = msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
                        author = f"{msg.author} ({msg.author.id})"
                        content = msg.content or "[Leerer Inhalt]"
                        log_lines.append(f"[{timestamp}] {author}: {content}")

                    log_text = "\n".join(log_lines) or "Keine Nachrichten vorhanden."
                    filename = f"gelöschte_nachrichten_{message.channel.name}_{message.created_at.strftime('%Y%m%d_%H%M%S')}.txt"
                    file = discord.File(io.StringIO(log_text), filename=filename)

                    await log_channel.send(
                        content=f"🧹 **{len(deleted) - 1} Nachrichten gelöscht in {message.channel.mention}** von {message.author.mention}",
                        file=file
                    )

                    await asyncio.sleep(5)
                    await confirmation.delete()
                except discord.Forbidden:
                    await message.channel.send("\u274c Keine Berechtigung, Nachrichten zu löschen.", delete_after=5)



    await handle_moderation_commands(message)
    await bot.process_commands(message)


async def handle_moderation_commands(message):
    if not any(role.id in ALLOWED_ROLE_IDS for role in message.author.roles):
        return

    content = message.content
    args = content.split()
    cmd = args[0].lower()

    if cmd in ["s!ban", "s!kick", "s!timeout", "s!info"]:
        if len(args) < 2 or not args[1].isdigit():
            await message.channel.send("\u274c Ungültige Benutzer-ID.",
                                       delete_after=5)
            return

        user_id = int(args[1])
        reason = " ".join(args[3:] if cmd == "s!timeout" and len(args) > 3 else
                          args[2:]) or "Kein Grund angegeben"
        member = message.guild.get_member(user_id)
        user = member or await bot.fetch_user(user_id)
        log_channel = bot.get_channel(MOD_LOG_CHANNEL_ID)

        def build_embed(action, color, duration_str=None):
            embed = discord.Embed(title=action, color=color)
            embed.add_field(name="Name", value=str(user), inline=False)
            embed.add_field(name="ID", value=user.id, inline=False)
            if duration_str:
                embed.add_field(name="Dauer", value=duration_str, inline=False)
            embed.add_field(name="Grund", value=reason, inline=False)
            embed.add_field(name="Ausgeführt von",
                            value=message.author,
                            inline=False)
            embed.set_thumbnail(url=user.display_avatar.url)
            embed.timestamp = discord.utils.utcnow()
            return embed

        async def try_dm():
            try:
                dm_embed = discord.Embed(title="Moderationsaktion",
                                         color=discord.Color.dark_red())
                dm_embed.add_field(name="Aktion",
                                   value=cmd.replace("s!", "").capitalize(),
                                   inline=True)
                dm_embed.add_field(name="Grund", value=reason, inline=False)
                dm_embed.timestamp = discord.utils.utcnow()
                await user.send(embed=dm_embed)
            except:
                pass

        if cmd == "s!ban":
            try:
                await message.guild.ban(user, reason=reason)
                code = generate_code("BAN")
                UNBAN_CODES[code] = user.id
                embed = build_embed("🚫 Benutzer gebannt", discord.Color.red())
                embed.add_field(name="Unban Code",
                                value=f"`{code}`",
                                inline=False)
                await message.channel.send(embed=embed, delete_after=5)
                await log_channel.send(embed=embed)
                await asyncio.sleep(5)
                await message.delete()
                await try_dm()
            except Exception as e:
                await message.channel.send(f"\u274c Fehler beim Bannen: {e}",
                                           delete_after=5)

        elif cmd == "s!kick":
            if not member:
                await message.channel.send(
                    "\u274c Nutzer ist nicht auf dem Server.", delete_after=5)
                return
            try:
                await member.kick(reason=reason)
                embed = build_embed("🦶 Benutzer gekickt",
                                    discord.Color.orange())
                await message.channel.send(embed=embed, delete_after=5)
                await log_channel.send(embed=embed)
                await asyncio.sleep(5)
                await message.delete()
                await try_dm()
            except Exception as e:
                await message.channel.send(f"\u274c Fehler beim Kicken: {e}",
                                           delete_after=5)

        elif cmd == "s!timeout":
            if len(args) < 3:
                await message.channel.send(
                    "\u274c Syntax: `s!timeout <UserID> <Dauer> [Grund]`",
                    delete_after=5)
                return
            if not member:
                await message.channel.send(
                    "\u274c Nutzer ist nicht auf dem Server.", delete_after=5)
                return
            duration_text = args[2].lower()
            match = re.match(r"(\d+)([smhd])", duration_text)
            if not match:
                await message.channel.send(
                    "\u274c Ungültige Dauer. Nutze z. B. `10m`, `2h`, `1d`",
                    delete_after=5)
                return
            amount, unit = int(match[1]), match[2]
            delta = {
                's': timedelta(seconds=amount),
                'm': timedelta(minutes=amount),
                'h': timedelta(hours=amount),
                'd': timedelta(days=amount)
            }[unit]
            readable_unit = {
                's': 'Sekunden',
                'm': 'Minuten',
                'h': 'Stunden',
                'd': 'Tage'
            }[unit]
            duration_str = f"{amount} {readable_unit}"
            try:
                await member.timeout(delta, reason=reason)
                code = generate_code("TM")
                UNMUTE_CODES[code] = member.id
                embed = build_embed(f"⏳ Timeout für {duration_str}",
                                    discord.Color.gold(), duration_str)
                embed.add_field(name="Unmute Code",
                                value=f"`{code}`",
                                inline=False)
                await message.channel.send(embed=embed, delete_after=5)
                await log_channel.send(embed=embed)
                await asyncio.sleep(5)
                await message.delete()
                await try_dm()
            except Exception as e:
                await message.channel.send(f"\u274c Fehler beim Timeout: {e}",
                                           delete_after=5)

        elif cmd == "s!info":
            try:
                embed = discord.Embed(title="👤 Benutzerinfo",
                                      color=discord.Color.blurple())
                embed.add_field(name="Name", value=f"{user}", inline=True)
                embed.add_field(name="ID", value=user.id, inline=True)
                embed.set_thumbnail(url=user.display_avatar.url)
                if isinstance(user, discord.Member):
                    embed.add_field(
                        name="Serverbeitritt",
                        value=user.joined_at.strftime('%d.%m.%Y %H:%M:%S'),
                        inline=False)
                    embed.add_field(
                        name="Account erstellt",
                        value=user.created_at.strftime('%d.%m.%Y %H:%M:%S'),
                        inline=False)
                    embed.add_field(name="Rollen",
                                    value=", ".join([
                                        r.name for r in user.roles
                                        if r.name != "@everyone"
                                    ]),
                                    inline=False)
                else:
                    embed.add_field(
                        name="Account erstellt",
                        value=user.created_at.strftime('%d.%m.%Y %H:%M:%S'),
                        inline=False)
                embed.timestamp = discord.utils.utcnow()
                await message.channel.send(embed=embed)
            except Exception as e:
                await message.channel.send(
                    f"\u274c Fehler beim Abrufen der Infos: {e}",
                    delete_after=5)

    elif cmd == "s!stats":
        await message.delete(delay=5)

        def get_role_count(role_name):
            role = discord.utils.get(message.guild.roles, name=role_name)
            return len(role.members) if role else 0

        stats = {
            "Los Santos Medical Department Stats 📊": {
                "Gesamte Mitglieder": get_role_count("@everyone"),
                "LSMD Mitglieder": get_role_count("Los Santos Medical Department")
            },
            "Leitungsebene": [
                ("Chief Medical Director", get_role_count("Chief Medical Director")),
                ("Deputy Chief Medical Director", get_role_count("Deputy Chief Medical Director")),
                ("Commissioner", get_role_count("Commissioner"))
            ],
            "Führungsebene": [
                ("Captain", get_role_count("Captain")),
                ("Lieutenant", get_role_count("Lieutenant"))
            ],
            "Attending Physician": [
                ("Attending Physician", get_role_count("Attending Physician"))
            ],
            "Ärztliches Personal": [
                ("Senior Fellow Physician", get_role_count("Senior Fellow Physician")),
                ("Fellow Physician", get_role_count("Fellow Physician")),
                ("Senior Resident", get_role_count("Senior Resident")),
                ("Resident", get_role_count("Resident"))
            ],
            "Notfallmedizinabteilung": [
                ("Senior Paramedic", get_role_count("Senior Paramedic")),
                ("Paramedic", get_role_count("Paramedic")),
                ("Advanced EMT", get_role_count("Advanced EMT")),
                ("Emergency Medical Responser", get_role_count("Emergency Medical Responser")),
                ("Emergency Medical Technician", get_role_count("Emergency Medical Technician")),
                ("Trainee EMT", get_role_count("Trainee EMT"))
            ],
            "Abteilungen": [
                ("🏫| Leitung Medical Education", get_role_count("🏫| Leitung Medical Education")),
                ("🔪| Leitung General Surgery", get_role_count("🔪| Leitung General Surgery")),
                ("🧠| Leitung Psychiatric Department", get_role_count("🧠| Leitung Psychiatric Department")),
                ("🚁| Leitung Search and Resuce", get_role_count("🚁| Leitung Search and Resuce")),
                ("🚁| SAR  - Instructor", get_role_count("🚁| SAR  - Instructor")),
                ("🏫| Medical Education Department", get_role_count("🏫| Medical Education Department")),
                ("🔪| General Surgery", get_role_count("🔪| General Surgery")),
                ("🔪| Operative License", get_role_count("🔪| Operative License")),
                ("🧠| Psychiatric Department", get_role_count("🧠| Psychiatric Department")),
                ("🚁| Search and Resuce", get_role_count("🚁| Search and Resuce")),
                ("🚤| SAR-Bootsausbildung", get_role_count("🚤| SAR-Bootsausbildung")),
                ("Los Santos Medical Department", get_role_count("Los Santos Medical Department")),
                ("🏝️ | Abgemeldet", get_role_count("🏝️ | Abgemeldet"))
            ],
            "Extras": [
                ("Dispatch Operations", get_role_count("Dispatch Operations")),
                ("Erfahrender Ausbilder", get_role_count("Erfahrender Ausbilder")),
                ("Ausbilder", get_role_count("Ausbilder")),
                ("Test-Ausbilder", get_role_count("Test-Ausbilder")),
                ("Externe Aushilfe", get_role_count("Externe Aushilfe"))
            ],
            "Nebenfunktionen": [
                ("Titelgremium", get_role_count("Titelgremium")),
                ("Pressesprecher", get_role_count("Pressesprecher")),
                ("Personalverwaltung", get_role_count("Personalverwaltung")),
                ("Social-Media Verwalter", get_role_count("Social-Media Verwalter")),
                ("Fuhrparkverwaltung", get_role_count("Fuhrparkverwaltung")),
                ("Parlamentsvertretung", get_role_count("Parlamentsvertretung"))
            ],
            "Sonstiges": [
                ("LSPD - FE", get_role_count("LSPD - FE")),
                ("DOJ - FE", get_role_count("DOJ - FE")),
                ("FIB - FE", get_role_count("FIB - FE")),
                ("NG - FE", get_role_count("NG - FE")),
                ("Neutral - FE", get_role_count("Neutral - FE")),
                ("Ehrenrang", get_role_count("Ehrenrang")),
                ("Server Booster", get_role_count("Server Booster"))
            ],
            "Staatsbürger": [
                ("Staatsbürger", get_role_count("Staatsbürger"))
            ],
            "Bot´s": [
                ("Bot", get_role_count("Bot"))
            ]
        }

        embed = discord.Embed(title="📊 Los Santos Medical Department Stats", color=discord.Color.blurple())
        embed.add_field(
            name="**Gesamte Mitglieder**",
            value=str(stats["Los Santos Medical Department Stats 📊"]["Gesamte Mitglieder"]),
            inline=True
        )
        embed.add_field(
            name="**LSMD Mitglieder**",
            value=str(stats["Los Santos Medical Department Stats 📊"]["LSMD Mitglieder"]),
            inline=True
        )
        embed.add_field(name="\u200b", value="\u200b", inline=False)  # Spacer

        for section, roles in stats.items():
            if isinstance(roles, list):
                value = "\n".join([f"{role}: {count}" for role, count in roles]) or "Keine Rollen gefunden"
                embed.add_field(name=f"__{section}__", value=value, inline=False)

        await message.channel.send(embed=embed)
    
    elif cmd == "s!unban":
        if len(args) < 2:
            await message.channel.send("⚠️ Benutze: `s!unban <Code>`",
                                       delete_after=5)
            return
        code = args[1].upper()
        user_id = UNBAN_CODES.pop(code, None)
        if not user_id:
            await message.channel.send(
                "❌ Ungültiger oder abgelaufener Unban-Code.", delete_after=5)
            return
        try:
            await message.guild.unban(discord.Object(id=user_id))
            await message.channel.send(
                f"✅ Ban für Nutzer-ID `{user_id}` wurde aufgehoben mit Code `{code}`."
            )
        except Exception as e:
            await message.channel.send(f"❌ Fehler beim Unbannen: {e}",
                                       delete_after=5)

    elif cmd == "s!unmute":
        if len(args) < 2:
            await message.channel.send("⚠️ Benutze: `s!unmute <Code>`",
                                       delete_after=5)
            return
        code = args[1].upper()
        user_id = UNMUTE_CODES.pop(code, None)
        if not user_id:
            await message.channel.send(
                "❌ Ungültiger oder abgelaufener Unmute-Code.", delete_after=5)
            return
        member = message.guild.get_member(user_id)
        if not member:
            await message.channel.send("❌ Nutzer ist nicht auf dem Server.",
                                       delete_after=5)
            return
        try:
            await member.timeout(None)
            await message.channel.send(
                f"✅ Timeout für {member.mention} wurde aufgehoben mit Code `{code}`."
            )
        except Exception as e:
            await message.channel.send(
                f"❌ Fehler beim Aufheben des Timeouts: {e}", delete_after=5)

@bot.event
async def on_ready():
    await tree.sync()
    print(f"? Bot ist online als {bot.user}")

if __name__ == "__main__":
    bot.run("TOKEN_HERE")

   
