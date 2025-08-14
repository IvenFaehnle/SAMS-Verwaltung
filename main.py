import discord
import os
from discord.ext import commands
import asyncio
import re
from datetime import timedelta
import random
import io
from discord.ext import tasks
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='>', intents=intents)
tree = bot.tree

ALLOWED_ROLE_IDS = [1401565598546133202, 943241957654814790, 993615970390261770, 950844059025539112]
CHANNEL_GENERAL_ID = 979128951723155557
CHANNEL_QUIT_ID = 979128097527976017
CHANNEL_BLACKLIST_ID = 1009520367284531220
CHANNEL_GEBURTSURKUNDEN_ID = 1389714794575040663
CHANNEL_LOG_ID = 1390077428944212118
MOD_LOG_CHANNEL_ID = 1328008745963356180
SYNC_ROLE_ID = 906845737281810443
LÖSCHEN_LOG_CHANNEL_ID = 1052369974573932626
PROMOTES_SPERREN = 1394763356023296173
ERROR_LOG_CHANNEL_ID = 1404465611811061891
ALLOWED_S_ROLE_IDS = [906845737281810443, 975473680358445136, 1165771712441364651, 1097205524690374716, 1367220175744798721, 943241957654814790]
STATUSLOG_ID = 1404430746579505232
MESSAGE_LOG_CHANNEL_ID = 1052369974573932626
ROLE_LOG_ID = 1052369993205026888
MEMBER_LOG_ID = 1052370202043621386
VOICE_LOG_ID = 1383135762052157600
EXCLUDED_CHANNELS = [1330319276154032179, 1330324925944168499, 1378484448554651781]
JOIN_RULES_ID = [1112116567556235294, 1378060409788960909]
REACTION_ROLES = 1341490927935557662 

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
    if not text:
        return text
    for user_id in [
            int(u_id)
            for u_id in set(re.findall(r'<@!?(\d+)>', text))
    ]:
        user = interaction.guild.get_member(user_id)
        if user:
            text = text.replace(f"<@{user_id}>", user.display_name)
            text = text.replace(f"<@!{user_id}>", user.display_name)

    for role_id in [
            int(r_id)
            for r_id in set(re.findall(r'<@&(\d+)>', text))
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

    await log_command_use(
        interaction, "geburtsurkunde", {
            "name": name,
            "geburtsdatum": geburtsdatum,
            "ausgestellt_von": ausgestellt_von,
            "datum": datum
        })

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

    await log_command_use(
        interaction, "geburtsurkunden_sperre", {
            "name": name,
            "geburtsdatum": geburtsdatum,
            "ausgestellt_von": ausgestellt_von,
            "grund": grund,
            "datum": datum
        })

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


@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def cmd_mute(ctx, member: discord.Member, minutes: int, *, reason: str = None):
    try:
        duration = timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await ctx.send(f"{member.mention} wurde für {minutes} Minuten stummgeschaltet. Grund: {reason}")
        code = "N/A"
        await log_mod_action(ctx.guild, "🔇 Mitglied gemutet", discord.Color.gold(), member.id, code, ctx.author, user_mention=member.mention)
    except discord.Forbidden:
        await ctx.send("Ich habe keine Berechtigung, diesen Benutzer zu stummschalten.")


@bot.command(name="unmute")
@commands.has_permissions(moderate_members=True)
async def cmd_unmute(ctx, user_id: int):
    member = ctx.guild.get_member(user_id)
    if member:
        try:
            await member.timeout(None)
            await ctx.send(f"{member.mention} wurde entstummt.")
            code = "N/A"
            await log_mod_action(ctx.guild, "🔊 Timeout aufgehoben", discord.Color.blurple(), user_id, code, ctx.author, user_mention=member.mention)
        except discord.Forbidden:
            await ctx.send("Ich habe keine Berechtigung, diesen Benutzer zu entstummen.")
    else:
        await ctx.send("Mitglied nicht gefunden.")


@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def cmd_unban(ctx, user_id: int):
    try:
        found_user = False
        async for ban_entry in ctx.guild.bans():
            if ban_entry.user.id == user_id:
                await ctx.guild.unban(ban_entry.user)
                await ctx.send(f"{ban_entry.user} wurde entbannt.")
                code = "N/A"
                await log_mod_action(ctx.guild, "🔓 Benutzer entbannt", discord.Color.green(), user_id, code, ctx.author, user_mention=str(ban_entry.user))
                found_user = True
                break

        if not found_user:
            await ctx.send("Benutzer nicht in der Ban-Liste gefunden.")
    except discord.Forbidden:
        await ctx.send("Ich habe keine Berechtigung, diesen Benutzer zu entbannen.")
    except Exception as e:
        await ctx.send(f"Fehler beim Entbannen: {e}")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return


    cmd_content = message.content.strip().lower()

    if message.content.startswith("s!löschen"):
        parts = message.content.split()
        if len(parts) != 2 or not parts[1].isdigit():
            await message.channel.send("\u274c Benutzung: `s!löschen <Anzahl>`", delete_after=5)
        else:
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

                if log_channel:
                    await log_channel.send(
                        content=f"🧹 **{len(deleted) - 1} Nachrichten gelöscht in {message.channel.mention}** von {message.author.mention}",
                        file=file
                    )

                await asyncio.sleep(5)
                await confirmation.delete()
            except discord.Forbidden:
                await message.channel.send("\u274c Keine Berechtigung, Nachrichten zu löschen.", delete_after=5)
            except Exception as e:
                await message.channel.send(f"\u274c Fehler beim Löschen: {e}", delete_after=5)


    if cmd_content == "s!stats":
        if not any(role.id in ALLOWED_S_ROLE_IDS for role in message.author.roles):
            await log_error(
                f"Unerlaubter Befehl `{message.content}` von {message.author.mention} in {message.channel.mention}"
            )
            return

        try:
            await message.delete(delay=5)
        except Exception:
            pass

        def get_role_count(role_name: str) -> int:
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
        embed.add_field(name="\u200b", value="\u200b", inline=False)

        for section, roles in stats.items():
            if isinstance(roles, list):
                value = "\n".join([f"{role}: {count}" for role, count in roles]) or "Keine Rollen gefunden"
                embed.add_field(name=f"__{section}__", value=value, inline=False)

        await message.channel.send(embed=embed)
        return


    if not cmd_content.startswith("s!"):
        return

    if not any(role.id in ALLOWED_S_ROLE_IDS for role in message.author.roles):
        await log_error(
            f"Unerlaubter Befehl `{message.content}` von {message.author.mention} in {message.channel.mention}"
        )
        return

    parts = message.content.split()
    cmd = parts[0].lower()

    try:
        if cmd == "s!ban" and len(parts) >= 2:
            try:
                user_id = int(parts[1].strip("<@!>"))
            except ValueError:
                await message.channel.send("\u274c Ungültige Nutzer-ID.", delete_after=5)
                await log_error(f"Ban fehlgeschlagen: Ungültige Nutzer-ID `{parts[1]}` von {message.author.mention}")
                return
            reason = " ".join(parts[2:]) or "Kein Grund angegeben"
            member = message.guild.get_member(user_id)
            if not member:
                await message.channel.send("\u274c Nutzer nicht gefunden.", delete_after=5)
                await log_error(f"Ban fehlgeschlagen: Nutzer-ID `{user_id}` nicht gefunden von {message.author.mention}")
                return
            await member.ban(reason=reason)
            await message.channel.send(f"{member.mention} wurde gebannt. Grund: {reason}")
            code = "N/A"
            await log_mod_action(message.guild, "🔨 Benutzer gebannt", discord.Color.dark_red(), user_id, code, message.author, user_mention=member.mention)

        elif cmd == "s!kick" and len(parts) >= 2:
            try:
                user_id = int(parts[1].strip("<@!>"))
            except ValueError:
                await message.channel.send("\u274c Ungültige Nutzer-ID.", delete_after=5)
                await log_error(f"Kick fehlgeschlagen: Ungültige Nutzer-ID `{parts[1]}` von {message.author.mention}")
                return
            reason = " ".join(parts[2:]) or "Kein Grund angegeben"
            member = message.guild.get_member(user_id)
            if not member:
                await message.channel.send("\u274c Nutzer nicht gefunden.", delete_after=5)
                await log_error(f"Kick fehlgeschlagen: Nutzer-ID `{user_id}` nicht gefunden von {message.author.mention}")
                return
            await member.kick(reason=reason)
            await message.channel.send(f"{member.mention} wurde gekickt. Grund: {reason}")
            code = "N/A"
            await log_mod_action(message.guild, "👢 Benutzer gekickt", discord.Color.orange(), user_id, code, message.author, user_mention=member.mention)

        elif cmd == "s!mute" and len(parts) >= 3:
            try:
                user_id = int(parts[1].strip("<@!>"))

                time_str = parts[2].lower()
                if time_str.endswith('s'):
                    duration_minutes = int(time_str[:-1]) / 60
                elif time_str.endswith('m'):
                    duration_minutes = int(time_str[:-1])
                elif time_str.endswith('h'):
                    duration_minutes = int(time_str[:-1]) * 60
                elif time_str.endswith('d'):
                    duration_minutes = int(time_str[:-1]) * 60 * 24
                else:
                    duration_minutes = int(time_str)

                if duration_minutes <= 0:
                    await message.channel.send("\u274c Dauer muss größer als 0 sein.", delete_after=5)
                    return

            except ValueError:
                await message.channel.send("\u274c Ungültige Eingabe. Format: `s!mute @user 10m [Grund]`", delete_after=5)
                await log_error(f"Mute fehlgeschlagen: Ungültige Eingabe `{parts[1:3]}` von {message.author.mention}")
                return

            reason = " ".join(parts[3:]) or "Kein Grund angegeben"
            member = message.guild.get_member(user_id)
            if not member:
                await message.channel.send("\u274c Nutzer nicht gefunden.", delete_after=5)
                await log_error(f"Mute fehlgeschlagen: Nutzer-ID `{user_id}` nicht gefunden von {message.author.mention}")
                return

            await member.timeout(timedelta(minutes=duration_minutes), reason=reason)
            await message.channel.send(f"{member.mention} wurde für {parts[2]} gemuted. Grund: {reason}")
            code = "N/A"
            await log_mod_action(message.guild, "🔇 Mitglied gemutet", discord.Color.gold(), user_id, code, message.author, user_mention=member.mention)

        elif cmd == "s!info" and len(parts) == 2:
            try:
                user_input = parts[1].strip()
                if user_input.startswith('<@') and user_input.endswith('>'):
                    user_id = int(user_input.strip('<@!>'))
                else:
                    user_id = int(user_input)
            except ValueError:
                await message.channel.send("\u274c Ungültige Nutzer-ID oder Mention.", delete_after=5)
                return
            member = message.guild.get_member(user_id)
            if not member:
                await message.channel.send("\u274c Nutzer nicht gefunden.", delete_after=5)
                await log_error(f"Info fehlgeschlagen: Nutzer-ID `{user_id}` nicht gefunden von {message.author.mention}")
                return

            joined_at = member.joined_at.strftime("%d.%m.%Y %H:%M:%S") if member.joined_at else "Unbekannt"
            created_at = member.created_at.strftime("%d.%m.%Y %H:%M:%S")

            roles = [role.name for role in member.roles if role.name != "@everyone"]
            roles_text = ", ".join(roles) if roles else "Keine Rollen"

            embed = discord.Embed(title="👤 Benutzerinfo", color=discord.Color.blurple())
            embed.add_field(name="**Name**", value=str(member), inline=False)
            embed.add_field(name="**ID**", value=str(member.id), inline=False)
            embed.add_field(name="**Serverbeitritt**", value=joined_at, inline=False)
            embed.add_field(name="**Account erstellt**", value=created_at, inline=False)
            embed.add_field(name="**Rollen**", value=roles_text, inline=False)

            if member.avatar:
                embed.set_thumbnail(url=member.avatar.url)
            embed.timestamp = discord.utils.utcnow()

            await message.channel.send(embed=embed)

        elif cmd == "s!unban" and len(parts) == 2:
            try:
                user_id = int(parts[1])
            except ValueError:
                await message.channel.send("\u274c Ungültige Nutzer-ID.", delete_after=5)
                return

            found_user = False
            async for ban_entry in message.guild.bans():
                if ban_entry.user.id == user_id:
                    await message.guild.unban(ban_entry.user)
                    await message.channel.send(f"{ban_entry.user} wurde entbannt.")
                    code = "N/A"
                    await log_mod_action(message.guild, "🔓 Benutzer entbannt", discord.Color.green(), user_id, code, message.author, user_mention=str(ban_entry.user))
                    found_user = True
                    break

            if not found_user:
                await message.channel.send("\u274c Nutzer nicht gefunden.", delete_after=5)
                await log_error(f"Unban fehlgeschlagen: Nutzer-ID `{user_id}` nicht in Ban-Liste gefunden von {message.author.mention}")

        elif cmd == "s!unmute" and len(parts) == 2:
            try:
                user_input = parts[1].strip()
                if user_input.startswith('<@') and user_input.endswith('>'):
                    user_id = int(user_input.strip('<@!>'))
                else:
                    user_id = int(user_input)
            except ValueError:
                await message.channel.send("\u274c Ungültige Nutzer-ID oder Mention.", delete_after=5)
                return
            member = message.guild.get_member(user_id)
            if not member:
                await message.channel.send("\u274c Nutzer nicht gefunden.", delete_after=5)
                await log_error(f"Unmute fehlgeschlagen: Nutzer-ID `{user_id}` nicht gefunden von {message.author.mention}")
                return
            await member.timeout(None)
            await message.channel.send(f"{member.mention} wurde entmutet.")
            code = "N/A"
            await log_mod_action(message.guild, "🔊 Timeout aufgehoben", discord.Color.blurple(), user_id, code, message.author, user_mention=member.mention)

        else:
            await log_error(f"Unbekannter s! Befehl `{message.content}` von {message.author.mention} in {message.channel.mention}")
            await message.channel.send("\u274c Unbekannter Befehl.", delete_after=5)

    except Exception as exc:

        await log_error(f"Fehler bei moderativen Befehl `{message.content}` von {message.author} in {message.channel.mention}", exc)
        try:
            await message.channel.send("\u274c Es ist ein Fehler aufgetreten.", delete_after=5)
        except Exception:
            pass


    await bot.process_commands(message)


async def log_error(message: str, exception: Exception = None):
    channel = bot.get_channel(ERROR_LOG_CHANNEL_ID)
    if not channel:
        print("❌ Fehlerlog-Channel nicht gefunden.")
        if exception:
            print("Exception:", exception)
        return

    embed = discord.Embed(
        title="⚠️ Fehler oder unerlaubter Zugriff",
        description=message,
        color=discord.Color.red()
    )
    if exception:
        embed.add_field(name="Fehler", value=str(exception), inline=False)
    embed.timestamp = discord.utils.utcnow()
    await channel.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):

    try:
        if isinstance(ctx, commands.Context):
            await log_error(f"Fehler bei Command `{ctx.message.content}` von {ctx.author} in {ctx.channel.mention}", error)
    except Exception:

        await log_error("Fehler beim Verarbeiten eines Befehls.", error)


@bot.event
async def on_message_edit(before, after):

    if before.author.bot or before.channel.id in EXCLUDED_CHANNELS:
        return


    if before.content == after.content:
        return

    log_channel = bot.get_channel(MESSAGE_LOG_CHANNEL_ID)
    if not log_channel:
        return


    timestamp = int(before.created_at.timestamp())
    time_since = f"<t:{timestamp}:R>"

    embed = discord.Embed(title="Message edited", color=discord.Color.orange())
    embed.add_field(name="Channel", value=f"{before.channel.name} ({before.channel.mention})", inline=False)


    message_link = f"https://discord.com/channels/{before.guild.id}/{before.channel.id}/{before.id}"
    embed.add_field(name="Message ID", value=f"[`{before.id}`]({message_link})", inline=False)

    embed.add_field(name="Message author", value=f"@{before.author.name} ({before.author.mention})", inline=False)
    embed.add_field(name="Message created", value=time_since, inline=False)


    before_content = before.content[:1024] if before.content else "[Leerer Inhalt]"
    after_content = after.content[:1024] if after.content else "[Leerer Inhalt]"

    embed.add_field(name="Before", value=before_content, inline=True)
    embed.add_field(name="After", value=after_content, inline=True)

    embed.timestamp = discord.utils.utcnow()

    await log_channel.send(embed=embed)


@bot.event
async def on_message_delete(message):

    if message.author.bot or message.channel.id in EXCLUDED_CHANNELS:
        return

    log_channel = bot.get_channel(MESSAGE_LOG_CHANNEL_ID)
    if not log_channel:
        return


    timestamp = int(message.created_at.timestamp())
    time_since = f"<t:{timestamp}:R>"

    embed = discord.Embed(title="Message deleted", color=discord.Color.red())
    embed.add_field(name="Channel", value=f"{message.channel.name} ({message.channel.mention})", inline=False)


    message_link = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
    embed.add_field(name="Message ID", value=f"[`{message.id}`]({message_link})", inline=False)

    embed.add_field(name="Message author", value=f"@{message.author.name} ({message.author.mention})", inline=False)
    embed.add_field(name="Message created", value=time_since, inline=False)


    content = message.content[:1024] if message.content else "[Leerer Inhalt]"


    if message.attachments:
        attachments_info = "\n".join([f"Anhang: {att.filename}" for att in message.attachments])
        content += f"\n\n**Anhänge:**\n{attachments_info}"

    embed.add_field(name="Message", value=content, inline=False)

    embed.timestamp = discord.utils.utcnow()

    await log_channel.send(embed=embed)


async def handle_role_connections(member: discord.Member):
    if not member:
        return

    
    role_connections = {
        1405336711889817600: [
            1405336830634627144, 1405336827770175539, 1405336824523788451,
            1405336821424066580, 1405336818739707978, 1405336815522680862,
            1405336812494262335, 1405336809705050172
        ],
        1405337883963035698: [
            1405337895476138004, 1405337894687604757, 1405337892993372291,
            1405337890808004718, 1405337887809081447
        ],
        1405337896310800464: [
            1405338740318146600, 1405338739307450579, 1405337901306220665,
            1405337900408766524, 1405337897049002044
        ],
        1405338740955545780: [
            1405338744055402657, 1405338743312744558, 1405338742503243796,
            1405338742218293248
        ]
    }

    member_roles = {role.id for role in member.roles}

    for target_role_id, source_role_ids in role_connections.items():
        if any(source_role_id in member_roles for source_role_id in source_role_ids):
            target_role = member.guild.get_role(target_role_id)
            if target_role and target_role not in member.roles:
                try:
                    await member.add_roles(target_role, reason="Automatische Rollenzuweisung (Verknüpfung)")
                    print(f"Assigned role {target_role.name} to {member.name} due to role connection.")
                except discord.Forbidden:
                    print(f"Failed to assign role {target_role.name} to {member.name}: Missing permissions.")
                except Exception as e:
                    print(f"Error assigning role {target_role.name} to {member.name}: {e}")
        else:
            target_role = member.guild.get_role(target_role_id)
            if target_role and target_role in member.roles:
                try:
                    await member.remove_roles(target_role, reason="Automatische Rollenentfernung (Verknüpfung)")
                    print(f"Removed role {target_role.name} from {member.name} due to role connection.")
                except discord.Forbidden:
                    print(f"Failed to remove role {target_role.name} from {member.name}: Missing permissions.")
                except Exception as e:
                    print(f"Error removing role {target_role.name} from {member.name}: {e}")


@bot.event
async def on_member_update(before, after):
    if before.roles == after.roles:
        return

    await handle_role_connections(after)

    log_channel = bot.get_channel(ROLE_LOG_ID)
    if not log_channel:
        return


    before_roles = set(before.roles)
    after_roles = set(after.roles)

    added_roles = after_roles - before_roles
    removed_roles = before_roles - after_roles


    if added_roles or removed_roles:
        embed = discord.Embed(
            title="User roles update",
            color=discord.Color.blue()
        )

        display_name = after.display_name if after.display_name != after.name else after.name
        embed.add_field(
            name="User",
            value=f"{after.mention} (@{display_name})",
            inline=False
        )

        if added_roles:
            added_role_mentions = ", ".join([role.mention for role in added_roles])
            embed.add_field(
                name="Added",
                value=f"{added_role_mentions}",
                inline=False
            )

        if removed_roles:
            removed_role_mentions = ", ".join([role.mention for role in removed_roles])
            embed.add_field(
                name="Removed",
                value=f"{removed_role_mentions}",
                inline=False
            )

        try:
            audit_logs = [entry async for entry in after.guild.audit_logs(action=discord.AuditLogAction.member_role_update, limit=5)]

            executor_info = "Unbekannt"
            reason_info = None

            for entry in audit_logs:
                if entry.target and entry.target.id == after.id:
                    time_diff = discord.utils.utcnow() - entry.created_at
                    if time_diff.total_seconds() <= 10:
                        executor_info = f"{entry.user.mention} (@{entry.user.name})"
                        if entry.reason:
                            reason_info = entry.reason
                        break

            embed.add_field(
                name="Ausgeführt von",
                value=f"{executor_info}",
                inline=False
            )

            if reason_info:
                embed.add_field(
                    name="Reason",
                    value=f"{reason_info}",
                    inline=False
                )

        except discord.Forbidden:
            embed.add_field(
                name="Ausgeführt von",
                value="Keine Berechtigung für Audit-Logs",
                inline=False
            )
        except Exception:
            embed.add_field(
                name="Ausgeführt von",
                value="Fehler beim Abrufen",
                inline=False
            )

        if after.avatar:
            embed.set_thumbnail(url=after.avatar.url)

        embed.timestamp = discord.utils.utcnow()

        await log_channel.send(embed=embed)

    if before.nick != after.nick:
        log_channel = bot.get_channel(MEMBER_LOG_ID)
        if not log_channel:
            return

        embed = discord.Embed(
            title="User nickname update",
            color=discord.Color.orange()
        )

        display_name = after.display_name if after.display_name != after.name else after.name
        embed.add_field(
            name="User",
            value=f"{after.mention} (@{display_name})",
            inline=False
        )

        user_link = f"https://discord.com/users/{after.id}"
        embed.add_field(name="ID", value=f"[`{after.id}`]({user_link})", inline=False)

        current_nickname = after.nick if after.nick else "/"
        previous_nickname = before.nick if before.nick else "/"

        embed.add_field(name="Nickname", value=current_nickname, inline=False)
        embed.add_field(name="Previous nickname", value=previous_nickname, inline=False)

        if after.avatar:
            embed.set_thumbnail(url=after.avatar.url)

        embed.timestamp = discord.utils.utcnow()

        await log_channel.send(embed=embed)


@bot.event
async def on_member_join(member):
    auto_roles = JOIN_RULES_ID

    await handle_role_connections(member)

    log_channel = bot.get_channel(MEMBER_LOG_ID)
    if not log_channel:
        return

    embed = discord.Embed(
        title="User joined",
        color=discord.Color.green()
    )

    display_name = member.display_name if member.display_name != member.name else member.name
    embed.add_field(
        name="User",
        value=f"{member.mention} (@{display_name})",
        inline=False
    )

    user_link = f"https://discord.com/users/{member.id}"
    embed.add_field(name="ID", value=f"[`{member.id}`]({user_link})", inline=False)


    timestamp = int(member.created_at.timestamp())
    age_text = f"<t:{timestamp}:R>"

    embed.add_field(name="Created", value=age_text, inline=False)
    embed.add_field(name="Members", value=str(member.guild.member_count), inline=False)

    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)

    embed.timestamp = discord.utils.utcnow()

    await log_channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    log_channel = bot.get_channel(MEMBER_LOG_ID)
    if not log_channel:
        return

    embed = discord.Embed(
        title="User left",
        color=discord.Color.red()
    )

    display_name = member.display_name if member.display_name != member.name else member.name
    embed.add_field(
        name="User",
        value=f"@{member.name} (<@{member.id}>)",
        inline=False
    )

    user_link = f"https://discord.com/users/{member.id}"
    embed.add_field(name="ID", value=f"[`{member.id}`]({user_link})", inline=False)


    if member.joined_at:
        time_on_server = discord.utils.utcnow() - member.joined_at
        if time_on_server.days >= 1:
            joined_text = f"vor {time_on_server.days} Tag{'en' if time_on_server.days > 1 else ''}"
        elif time_on_server.seconds >= 3600:
            hours = time_on_server.seconds // 3600
            joined_text = f"vor {hours} Stunde{'n' if hours > 1 else ''}"
        else:
            joined_text = "vor wenigen Minuten"
    else:
        joined_text = "Unbekannt"

    embed.add_field(name="Joined", value=joined_text, inline=False)


    roles = [role.mention for role in member.roles if role.name != "@everyone"]
    roles_text = " ".join(roles) if roles else "Keine Rollen"
    embed.add_field(name="Roles", value=roles_text, inline=False)

    embed.add_field(name="Members", value=str(member.guild.member_count), inline=False)

    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)

    embed.timestamp = discord.utils.utcnow()

    await log_channel.send(embed=embed)



@bot.event
async def on_voice_state_update(member, before, after):
    """Handle voice channel join, leave, and switch events"""
    log_channel = bot.get_channel(VOICE_LOG_ID)
    if not log_channel:
        return

    if before.channel is None and after.channel is not None:
        embed = discord.Embed(
            title="User joined channel",
            color=discord.Color.green()
        )

        display_name = member.display_name if member.display_name != member.name else member.name
        embed.add_field(
            name="User",
            value=f"{member.mention} (@{display_name})",
            inline=False
        )

        embed.add_field(
            name="Channel",
            value=f"{after.channel.mention}",
            inline=False
        )

        user_count = len(after.channel.members)
        user_limit = after.channel.user_limit if after.channel.user_limit > 0 else "∞"
        embed.add_field(
            name="Users",
            value=f"{user_count}/{user_limit}",
            inline=False
        )

        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)

        embed.timestamp = discord.utils.utcnow()
        await log_channel.send(embed=embed)

    elif before.channel is not None and after.channel is None:
        embed = discord.Embed(
            title="User left channel",
            color=discord.Color.red()
        )

        display_name = member.display_name if member.display_name != member.name else member.name
        embed.add_field(
            name="User",
            value=f"{member.mention} (@{display_name})",
            inline=False
        )

        embed.add_field(
            name="Channel",
            value=f"{before.channel.mention}",
            inline=False
        )

        user_count = len(before.channel.members)
        user_limit = before.channel.user_limit if before.channel.user_limit > 0 else "∞"
        embed.add_field(
            name="Users",
            value=f"{user_count}/{user_limit}",
            inline=False
        )

        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)

        embed.timestamp = discord.utils.utcnow()
        await log_channel.send(embed=embed)


    elif before.channel is not None and after.channel is not None and before.channel != after.channel:
        was_moved = False
        moved_by = None

        try:
            await asyncio.sleep(1.0)

            audit_logs = [entry async for entry in member.guild.audit_logs(action=discord.AuditLogAction.member_move, limit=20)]

            for entry in audit_logs:
                if entry.target and entry.target.id == member.id:
                    time_diff = discord.utils.utcnow() - entry.created_at
                    if (time_diff.total_seconds() <= 30 and
                        hasattr(entry.changes, 'before') and hasattr(entry.changes, 'after') and
                        entry.changes.before.channel and entry.changes.after.channel and
                        entry.changes.before.channel.id == before.channel.id and
                        entry.changes.after.channel.id == after.channel.id):
                        was_moved = True
                        moved_by = entry.user
                        break
                    elif time_diff.total_seconds() <= 15 and entry.user.id != member.id:
                        was_moved = True
                        moved_by = entry.user
                        break

        except Exception as e:
            print(f"Audit log error: {e}")
            pass

        if was_moved and moved_by:
            embed = discord.Embed(
                title="User moved channel",
                color=discord.Color.purple()
            )

            display_name = member.display_name if member.display_name != member.name else member.name
            embed.add_field(
                name="User",
                value=f"{member.mention} (@{display_name})",
                inline=False
            )

            embed.add_field(
                name="Channel",
                value=f"{after.channel.mention}",
                inline=False
            )

            user_count_new = len(after.channel.members)
            user_limit_new = after.channel.user_limit if after.channel.user_limit > 0 else "∞"
            embed.add_field(
                name="Users",
                value=f"{user_count_new}/{user_limit_new}",
                inline=False
            )

            embed.add_field(
                name="Previous channel",
                value=f"{before.channel.mention}",
                inline=False
            )

            user_count_prev = len(before.channel.members)
            user_limit_prev = before.channel.user_limit if before.channel.user_limit > 0 else "∞"
            embed.add_field(
                name="Previous users",
                value=f"{user_count_prev}/{user_limit_prev}",
                inline=False
            )

            moved_by_display = moved_by.display_name if moved_by.display_name != moved_by.name else moved_by.name
            embed.add_field(
                name="Moved by",
                value=f"{moved_by.mention} (@{moved_by_display})",
                inline=False
            )

        else:
            embed = discord.Embed(
                title="User switched channel",
                color=discord.Color.blue()
            )

            display_name = member.display_name if member.display_name != member.name else member.name
            embed.add_field(
                name="User",
                value=f"{member.mention} (@{display_name})",
                inline=False
            )

            embed.add_field(
                name="Channel",
                value=f"{after.channel.mention}",
                inline=False
            )

            user_count_new = len(after.channel.members)
            user_limit_new = after.channel.user_limit if after.channel.user_limit > 0 else "∞"
            embed.add_field(
                name="Users",
                value=f"{user_count_new}/{user_limit_new}",
                inline=False
            )

            embed.add_field(
                name="Previous channel",
                value=f"{before.channel.mention}",
                inline=False
            )

            user_count_prev = len(before.channel.members)
            user_limit_prev = before.channel.user_limit if before.channel.user_limit > 0 else "∞"
            embed.add_field(
                name="Previous users",
                value=f"{user_count_prev}/{user_limit_prev}",
                inline=False
            )

        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)

        embed.timestamp = discord.utils.utcnow()
        await log_channel.send(embed=embed)


@bot.event
async def on_ready():
    try:
        await tree.sync()
    except Exception:
        pass
    print(f"\u2705 Bot ist online als {bot.user}")

    if not status_log.is_running():
        status_log.start()
    
    
    await setup_reaction_roles()


async def setup_reaction_roles():
    """Setup reaction role message in the specified channel"""
    channel = bot.get_channel(REACTION_ROLES)
    if not channel:
        print("❌ Reaction Role Channel nicht gefunden!")
        return
    
    existing_message = None
    try:
        async for message in channel.history(limit=100):
            if (message.author == bot.user and 
                message.embeds and 
                message.embeds[0].title == "Optionale Rollen"):
                existing_message = message
                break
    except Exception as e:
        print(f"Fehler beim Überprüfen vorhandener Nachrichten: {e}")
    
    if existing_message:
        print("✅ Reaction Role System bereits vorhanden - kein neues Setup erforderlich!")
        return
    
    embed = discord.Embed(
        title="Optionale Rollen",
        description=(
            "Um die Pings ein Wenig zu reduzieren, gibt es jetzt für Module oder Interesse an Spezialisierungen, "
            "sogenannte \"Reaction Roles\" Solltet ihr also dementsprechend Interesse an einer Spezialisierung, "
            "Fortbildung oder einem Modul haben holt euch hier einfach die Rolle ab und wenn sie durch Ausbilder "
            "Gepingt wird, absolviert Ihr jene und könnt euch jene Rolle nach erfolgreichem Absolvieren durch "
            "erneutes Anklicken der Reaktion wieder Entfernen.\n\n"
            "**Bitte klicke auf die benötigten Rollen, um diese zu erhalten.**"
        ),
        color=discord.Color.blue()
    )
    
    role_info = [
        ("1️⃣", "Modul 1 benötigt", 1341491722961682543),
        ("2️⃣", "Modul 2 benötigt", 1341491806734651514),
        ("3️⃣", "Modul 3 benötigt", 1341491907724972122),
        ("🎓", "Interesse Medical Education", 1374491251482558545),
        ("🥼", "Interesse General Surgery", 1374490464119554159),
        ("🧠", "Interesse Psychiatric", 1374491124349141002),
        ("🚁", "Interesse Search and Rescue", 1374490266706120845),
        ("🚤", "Interesse SAR-Bootsausbildung", 1374505941038530663),
        ("🚨", "Interesse Dispatch Operations", 1377037664087183420)
    ]
    
    role_text = ""
    for emoji, role_name, role_id in role_info:
        role_text += f"{emoji} - <@&{role_id}>\n"
    
    embed.add_field(name="Verfügbare Rollen:", value=role_text, inline=False)
    
    message = await channel.send(embed=embed)
    
    reactions = ["1️⃣", "2️⃣", "3️⃣", "🎓", "🥼", "🧠", "🚁", "🚤", "🚨"]
    for reaction in reactions:
        try:
            await message.add_reaction(reaction)
        except Exception as e:
            print(f"Fehler beim Hinzufügen der Reaktion {reaction}: {e}")
    
    print("✅ Reaction Role System eingerichtet!")


@bot.event
async def on_raw_reaction_add(payload):
    """Handle reaction role assignment when user adds reaction"""
    if payload.user_id == bot.user.id:
        return
    
    if payload.channel_id != REACTION_ROLES:
        return
    
    reaction_roles = {
        "1️⃣": 1341491722961682543,  
        "2️⃣": 1341491806734651514,  
        "3️⃣": 1341491907724972122,  
        "🎓": 1374491251482558545, 
        "🥼": 1374490464119554159,  
        "🧠": 1374491124349141002,  
        "🚁": 1374490266706120845,  
        "🚤": 1374505941038530663,  
        "🚨": 1377037664087183420   
    }
    
    emoji = str(payload.emoji)
    if emoji not in reaction_roles:
        return
    
    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return
    
    member = guild.get_member(payload.user_id)
    if not member:
        return
    
    role_id = reaction_roles[emoji]
    role = guild.get_role(role_id)
    if not role:
        return
    
    try:
        await member.add_roles(role, reason="Reaction Role hinzugefügt")
        print(f"✅ {member.name} hat die Rolle {role.name} erhalten")
    except Exception as e:
        print(f"❌ Fehler beim Hinzufügen der Rolle {role.name} für {member.name}: {e}")


@bot.event
async def on_raw_reaction_remove(payload):
    """Handle reaction role removal when user removes reaction"""
    if payload.user_id == bot.user.id:
        return
    
    
    if payload.channel_id != REACTION_ROLES:
        return
    
    reaction_roles = {
        "1️⃣": 1341491722961682543, 
        "2️⃣": 1341491806734651514,  
        "3️⃣": 1341491907724972122, 
        "🎓": 1374491251482558545, 
        "🥼": 1374490464119554159,  
        "🧠": 1374491124349141002,  
        "🚁": 1374490266706120845,  
        "🚤": 1374505941038530663,  
        "🚨": 1377037664087183420  
    }
    
    emoji = str(payload.emoji)
    if emoji not in reaction_roles:
        return
    
    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return
    
    member = guild.get_member(payload.user_id)
    if not member:
        return
    
    role_id = reaction_roles[emoji]
    role = guild.get_role(role_id)
    if not role:
        return
    
    try:
        await member.remove_roles(role, reason="Reaction Role entfernt")
        print(f"➖ {member.name} hat die Rolle {role.name} verloren")
    except Exception as e:
        print(f"❌ Fehler beim Entfernen der Rolle {role.name} für {member.name}: {e}")


async def log_mod_action(guild, title, color, user_id, code, executor, user_mention=None):

    log_channel = guild.get_channel(MOD_LOG_CHANNEL_ID)
    if not log_channel:
        return

    embed = discord.Embed(title=title, color=color)
    embed.add_field(name="Nutzer", value=user_mention if user_mention else f"`{user_id}`", inline=False)
    embed.add_field(name="Nutzer-ID", value=str(user_id), inline=False)
    embed.add_field(name="Code", value=str(code), inline=False)
    embed.add_field(name="Ausgeführt von", value=str(executor), inline=False)
    embed.timestamp = discord.utils.utcnow()

    await log_channel.send(embed=embed)


version_file = "version.txt"

def load_version():
    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            return f.read().strip()
    return "1.0.0"

def save_version(version):
    with open(version_file, "w") as f:
        f.write(version)

bot_version = load_version()

@tasks.loop(minutes=10)
async def status_log():
    global bot_version
    channel = bot.get_channel(STATUSLOG_ID)
    if channel:
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        start_embed = discord.Embed(
            title="__LSMD Verwaltung__",
            description="Starting sync...",
            color=discord.Color.orange()
        )
        start_embed.add_field(name="Zeitpunkt", value=now, inline=True)
        start_embed.add_field(name="Version", value=bot_version, inline=True)
        start_embed.timestamp = discord.utils.utcnow()

        await channel.send(embed=start_embed)

        major, minor, patch = map(int, bot_version.split('.'))
        patch += 1
        if patch >= 100:
            patch = 0
            minor += 1
        if minor >= 100:
            minor = 0
            major += 1
        bot_version = f"{major}.{minor}.{patch}"

        save_version(bot_version)

        await asyncio.sleep(2)

        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")


        complete_embed = discord.Embed(
            title="__LSMD Verwaltung__",
            description="Sync completed!",
            color=discord.Color.green()
        )
        complete_embed.add_field(name="Zeitpunkt", value=now, inline=True)
        complete_embed.add_field(name="Neue Version", value=bot_version, inline=True)
        complete_embed.timestamp = discord.utils.utcnow()

        await channel.send(embed=complete_embed)

@status_log.before_loop
async def before_status_log():
    await bot.wait_until_ready()

if __name__ == "__main__":
    bot.run("TOKEN_HERE")
