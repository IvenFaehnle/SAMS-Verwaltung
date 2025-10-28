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

import typing



intents = discord.Intents.default()

intents.message_content = True

intents.members = True



bot = commands.Bot(command_prefix='!', intents=intents)

tree = bot.tree



ALLOWED_ROLE_IDS = [1401565598546133202, 943241957654814790, 993615970390261770, 950844059025539112]

CHANNEL_GENERAL_ID = 979128951723155557

CHANNEL_QUIT_ID = 979128097527976017

CHANNEL_BLACKLIST_ID = 1009520367284531220

CHANNEL_GEBURTSURKUNDEN_ID = 1389714794575040663

CHANNEL_LOG_ID = 1390077428944212118

MOD_LOG_CHANNEL_ID = 1184582395316416512

SYNC_ROLE_ID = 906845737281810443

LÖSCHEN_LOG_CHANNEL_ID = 1052369974573932626

PROMOTES_SPERREN = 1394763356023296173

ERROR_LOG_CHANNEL_ID = 1404465611811061891

ALLOWED_S_ROLE_IDS = [906845737281810443, 975473680358445136, 1165771712441364651, 1097205524690374716, 1367220175744798721, 906845737281810443]

STATUSLOG_ID = 1404430746579505232

MESSAGE_LOG_CHANNEL_ID = 1052369974573932626

ROLE_LOG_ID = 1052369993205026888

MEMBER_LOG_ID = 1052370202043621386

VOICE_LOG_ID = 1383135762052157600

EXCLUDED_CHANNELS = [1330319276154032179, 1330324925944168499, 1378484448554651781]

JOIN_RULES_ID = [1112116567556235294, 1378060409788960909]

REACTION_ROLES = 1341490927935557662

TICKET_CHANNEL_ID = 1054774394112712846

TICKET_TRANSCRIPT_CHANNEL_ID = 1335257248729137202

PROMOTION_RESIGNATION_CHANNEL_ID = 1378332187140821043

DEPARTMENT_APPLICATION_CHANNEL_ID = 1378184190469869619

APPLICATION_CHANNEL_ID = 1201487339940220928

SAMS_INFO_CHANNEL_ID = 1153812556029378691





TICKET_CATEGORIES = {

    "leitungsebene": {

        "category_id": 1378409619298451488,

        "allowed_roles": [1367220175744798721, 1097205524690374716, 1165771712441364651, 906845737281810443]

    },

    "fuehrungsebene": {

        "category_id": 1112346307777011842,

        "allowed_roles": [943241957654814790, 1367220175744798721, 1097205524690374716, 1165771712441364651, 906845737281810443]

    },

    "beschwerde": {

        "category_id": 1112346307777011842,

        "allowed_roles": [943241957654814790, 1367220175744798721, 1097205524690374716, 1165771712441364651, 906845737281810443]

    },

    "titel": {

        "category_id": 1120420638616727644,

        "allowed_roles": [1331579941321703464, 1367220175744798721, 1097205524690374716, 1165771712441364651, 906845737281810443]

    },

    "geburtsurkunde": {

        "category_id": 1378398361346113586,

        "allowed_roles": [993615970390261770, 943241957654814790, 1367220175744798721, 1097205524690374716, 1165771712441364651, 906845737281810443]

    },

    "behandlung": {

        "category_id": 1341485372714258515,

        "allowed_roles": [906902211769016421, 993615970390261770, 943241957654814790, 1367220175744798721, 1097205524690374716, 1165771712441364651, 906845737281810443, 993615970390261770]

    },

    "wiedereinstellung": {

        "category_id": 1112346307777011842,

        "allowed_roles": [943241957654814790, 1367220175744798721, 1097205524690374716, 1165771712441364651, 906845737281810443]

    },

    "discord_verwaltung": {

        "category_id": 1378409619298451488,

        "allowed_roles": [906845737281810443]

    },

    "befoerderungs_antrag": {

        "category_id": 1149274277468721172,

        "allowed_roles": [993615970390261770, 943241957654814790, 1367220175744798721, 1097205524690374716, 1165771712441364651, 906845737281810443]

    },

    "kuendigungs_antrag": {

        "category_id": 1149274277468721172,

        "allowed_roles": [993615970390261770, 943241957654814790, 1367220175744798721, 1097205524690374716, 1165771712441364651, 906845737281810443]

    },

    "medical_education_bewerbung": {

        "category_id": 1378079771514114088,

        "allowed_roles": [1377743930690506845, 950844061810565170, 1367220175744798721, 1097205524690374716, 1165771712441364651, 906845737281810443]

    },

    "general_surgery_bewerbung": {

        "category_id": 1378079771514114088,

        "allowed_roles": [991398406088048650, 1367220175744798721, 1097205524690374716, 1165771712441364651, 906845737281810443]

    },

    "psychiatric_bewerbung": {

        "category_id": 1378079771514114088,

        "allowed_roles": [991397474549895258, 1367220175744798721, 1097205524690374716, 1165771712441364651, 906845737281810443]

    },

    "sar_bewerbung": {

        "category_id": 1378079771514114088,

        "allowed_roles": [991398084447830117, 1367220175744798721, 1097205524690374716, 1165771712441364651, 906845737281810443]

    },

    "bewerbung": {

        "category_id": 1117471787735851028,

        "allowed_roles": [1377743800155246602, 1377743883064184903, 1377743883064184903, 1377743930690506845, 943241957654814790,950844061810565170, 1367220175744798721, 1097205524690374716, 1165771712441364651, 906845737281810443]

    }

}


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

        f"\U0000274C Dieser Befehl darf nur in {channels} verwendet werden.",

        ephemeral=True)





async def send_missing_role_response(interaction: discord.Interaction):

    await interaction.response.send_message(

        "\U0000274C Du hast keine Berechtigung, diesen Befehl zu verwenden.",

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

        print(f"\U000026A0 Log-Kanal mit ID {CHANNEL_LOG_ID} nicht gefunden!")

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





async def log_error(error_message: str):

    """Log errors to the error log channel"""

    error_channel = bot.get_channel(ERROR_LOG_CHANNEL_ID)

    if error_channel:

        embed = discord.Embed(

            title="Bot Error",

            description=error_message,

            color=discord.Color.red()

        )

        embed.timestamp = discord.utils.utcnow()

        await error_channel.send(embed=embed)

    else:

        print(f"Error: {error_message}")





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

        title="__**Interne Weiterbildung:**__ \U0001F393",

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

        "\U00002705 Interne Weiterbildung wurde erfolgreich veröffentlicht.",

        ephemeral=True)


@tree.command(name="beförderung", description="Fülle eine Beförderung aus.")

async def befoerderung(interaction: discord.Interaction, name: str,

                       alter_rang: str, neuer_rang: str, ausgefuehrt_von: str, datum: str, grund: str):

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



    embed = discord.Embed(title="__**Beförderung:**__ \U0001F7E2",

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

        "\U00002705 Beförderung wurde erfolgreich veröffentlicht.", ephemeral=True)





@tree.command(name="degradierung", description="Fülle eine Degradierung aus.")

async def degradierung(interaction: discord.Interaction, name: str,

                       alter_rang: str, neuer_rang: str, ausgefuehrt_von: str, datum: str,

                       grund: str):

    await log_command_use(

        interaction, "degradierung", {

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



    embed = discord.Embed(title="__**Degradierung:**__ \U0001F7E5",

                          color=discord.Color.dark_red())

    embed.add_field(name="Name der degradierten Person",

                    value=name,

                    inline=False)

    embed.add_field(name="Alter Rang", value=alter_rang, inline=False)

    embed.add_field(name="Neuer Rang", value=neuer_rang, inline=False)

    embed.add_field(name="Ausgeführt von", value=ausgefuehrt_von, inline=False)

    embed.add_field(name="Datum", value=datum, inline=False)

    embed.add_field(name="Grund", value=grund, inline=False)



    await bot.get_channel(CHANNEL_GENERAL_ID).send(embed=embed)

    await interaction.response.send_message(

        "\U00002705 Degradierung wurde erfolgreich veröffentlicht.", ephemeral=True)

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



    embed = discord.Embed(title="__**Suspendierung:**__ \U0001F550",

                          color=discord.Color.gold())

    embed.add_field(name="Name der Suspendierten Person:",

                    value=name,

                    inline=False)

    embed.add_field(name="Ausgeführt von", value=ausgefuehrt_von, inline=False)

    embed.add_field(name="Datum", value=datum, inline=False)

    embed.add_field(name="Grund", value=grund, inline=False)



    await bot.get_channel(CHANNEL_QUIT_ID).send(embed=embed)

    await interaction.response.send_message(

        "\U00002705 Suspendierung wurde erfolgreich veröffentlicht.", ephemeral=True)





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



    embed = discord.Embed(title="__**Kündigung:**__ \U0001F7E5",

                          color=discord.Color.red())

    embed.add_field(name="Name der gekündigten Person:",

                    value=name,

                    inline=False)

    embed.add_field(name="Ausgeführt von", value=ausgefuehrt_von, inline=False)

    embed.add_field(name="Datum", value=datum, inline=False)

    embed.add_field(name="Grund", value=grund, inline=False)



    await bot.get_channel(CHANNEL_QUIT_ID).send(embed=embed)

    await interaction.response.send_message(

        "\U00002705 Kündigung wurde erfolgreich veröffentlicht.", ephemeral=True)



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



    embed = discord.Embed(title="__**Blacklist-Eintrag:**__ \U0001F534",

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

        "\U00002705 Blacklist-Eintrag wurde erfolgreich veröffentlicht.",

        ephemeral=True)





@tree.command(name="beitritt",

              description="Trage einen spezialisierungsbeitritt ein.")

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

    spezialisierung = await resolve_mentions_to_text(

        interaction, spezialisierung)

    ausgefuehrt_von = await resolve_mentions_to_text(interaction,

                                                     ausgefuehrt_von)



    embed = discord.Embed(

        title="__**Spezialisierungsbeitritt:**__ \U00002795",

        color=discord.Color.blue())

    embed.add_field(name="Name der Person", value=name, inline=False)

    embed.add_field(name="Spezialisierung",

                    value=spezialisierung,

                    inline=False)

    embed.add_field(name="Ausgeführt von", value=ausgefuehrt_von, inline=False)

    embed.add_field(name="Datum", value=datum, inline=False)



    await bot.get_channel(CHANNEL_GENERAL_ID).send(embed=embed)

    await interaction.response.send_message(

        "\U00002705 Spezialisierungsbeitritt wurde erfolgreich veröffentlicht.",

        ephemeral=True)





@tree.command(

    name="befoerderungs_sperre",

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



    embed = discord.Embed(title="__**Beförderungssperre:**__ \U0001F6AB",

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

        "\U00002705 Beförderungssperre wurde erfolgreich veröffentlicht.",

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



    embed = discord.Embed(title="__**Beförderungssperre aufgehoben:**__ \U00002705",

                          color=discord.Color.green())

    embed.add_field(name="Name der Person", value=name, inline=False)

    embed.add_field(name="Entsperrt von", value=entsperrt_von, inline=False)

    embed.add_field(name="Datum", value=datum, inline=False)

    embed.add_field(name="Grund", value=grund, inline=False)



    await bot.get_channel(PROMOTES_SPERREN).send(embed=embed)

    await interaction.response.send_message(

        "\U00002705 Beförderungssperre wurde erfolgreich aufgehoben.", ephemeral=True)


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



    embed = discord.Embed(title="__**Spezialisierungsinterner Austritt:**__ \U0000274C ",

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

        "\U00002705 Spezialisierungsinterner Austritt wurde erfolgreich veröffentlicht.",

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

        title="__**Geburtsurkunde Ausgestellt**__ \U0001F7E2",

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

        "\U00002705 Geburtsurkunde wurde erfolgreich ausgestellt.", ephemeral=True)





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



    embed = discord.Embed(title="__**Geburtsurkunden Sperre**__ \U0001F7E5",

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

        "\U00002705 Sperre wurde erfolgreich veröffentlicht.", ephemeral=True)

@tree.command(name="add", description="Füge einen Benutzer oder eine Rolle zum aktuellen Ticket hinzu.")

async def add_to_ticket(

    interaction: discord.Interaction,

    target: typing.Union[discord.Member, discord.Role]

):

    if not is_ticket_channel(interaction.channel.id):

        await interaction.response.send_message("\U0000274C Dieser Befehl kann nur in Ticket-Kanälen verwendet werden!", ephemeral=True)

        return



    ticket_info = bot.ticket_channels.get(interaction.channel.id, {})

    ticket_type = ticket_info.get('type')



    if not ticket_type:

        channel = interaction.channel

        for t_type, config in TICKET_CATEGORIES.items():

            if channel.category_id == config["category_id"]:

                ticket_type = t_type

                bot.ticket_channels[interaction.channel.id] = {

                    'type': ticket_type,

                    'creator': None,

                    'created_at': channel.created_at,

                    'transcript_messages': []

                }

                break



    if not ticket_type or ticket_type not in TICKET_CATEGORIES:

        await interaction.response.send_message("\U0000274C Ticket-Typ nicht erkannt!", ephemeral=True)

        return



    ticket_config = TICKET_CATEGORIES[ticket_type]

    user_roles = [role.id for role in interaction.user.roles]



    if not any(role_id in user_roles for role_id in ticket_config["allowed_roles"]):

        await interaction.response.send_message("\U0000274C Sie haben keine Berechtigung, dieses Ticket zu verwalten!", ephemeral=True)

        return



    await interaction.response.defer()



    if isinstance(target, discord.Member):

        await interaction.channel.set_permissions(target, read_messages=True, send_messages=True)

        embed = discord.Embed(

            title="\U00002795 Benutzer hinzugefügt",

            description=f"{target.mention} wurde zum Ticket hinzugefügt",

            color=discord.Color.green()

        )

    elif isinstance(target, discord.Role):

        await interaction.channel.set_permissions(target, read_messages=True, send_messages=True)

        embed = discord.Embed(

            title="\U00002795 Rolle hinzugefügt",

            description=f"Rolle {target.mention} wurde zum Ticket hinzugefügt",

            color=discord.Color.green()

        )



    embed.add_field(name="Hinzugefügt von", value=f"{interaction.user.mention}", inline=False)

    await interaction.followup.send(embed=embed)




@tree.command(name="out", description="Entferne einen Benutzer oder eine Rolle aus dem aktuellen Ticket.")

async def remove_from_ticket(

    interaction: discord.Interaction,

    target: typing.Union[discord.Member, discord.Role]

):

    if not is_ticket_channel(interaction.channel.id):

        await interaction.response.send_message("\U0000274C Dieser Befehl kann nur in Ticket-Kanälen verwendet werden!", ephemeral=True)

        return



    ticket_info = bot.ticket_channels.get(interaction.channel.id, {})

    ticket_type = ticket_info.get('type')



    if not ticket_type:

        channel = interaction.channel

        for t_type, config in TICKET_CATEGORIES.items():

            if channel.category_id == config["category_id"]:

                ticket_type = t_type

                bot.ticket_channels[interaction.channel.id] = {

                    'type': ticket_type,

                    'creator': None,

                    'created_at': channel.created_at,

                    'transcript_messages': []

                }

                break



    if not ticket_type or ticket_type not in TICKET_CATEGORIES:

        await interaction.response.send_message("\U0000274C Ticket-Typ nicht erkannt!", ephemeral=True)

        return



    ticket_config = TICKET_CATEGORIES[ticket_type]

    user_roles = [role.id for role in interaction.user.roles]



    if not any(role_id in user_roles for role_id in ticket_config["allowed_roles"]):

        await interaction.response.send_message("\U0000274C Sie haben keine Berechtigung, dieses Ticket zu verwalten!", ephemeral=True)

        return



    await interaction.response.defer()



    if isinstance(target, discord.Member):

        if target.id == ticket_info.get('creator'):

            embed = discord.Embed(

                title="\U0000274C Fehler",

                description="Der Ticket-Ersteller kann nicht entfernt werden!",

                color=discord.Color.red()

            )

            await interaction.followup.send(embed=embed)

            return



        await interaction.channel.set_permissions(target, overwrite=None)

        embed = discord.Embed(

            title="\U00002796 Benutzer entfernt",

            description=f"{target.mention} wurde aus dem Ticket entfernt",

            color=discord.Color.red()

        )



    elif isinstance(target, discord.Role):

        if target.id in ticket_config["allowed_roles"]:

            embed = discord.Embed(

                title="\U0000274C Fehler",

                description="Diese Rolle ist standardmäßig für diesen Ticket-Typ berechtigt und kann nicht entfernt werden!",

                color=discord.Color.red()

            )

            await interaction.followup.send(embed=embed)

            return



        await interaction.channel.set_permissions(target, overwrite=None)

        embed = discord.Embed(

            title="\U00002796 Rolle entfernt",

            description=f"Rolle {target.mention} wurde aus dem Ticket entfernt",

            color=discord.Color.red()

        )



    embed.add_field(name="Entfernt von", value=f"{interaction.user.mention}", inline=False)

    await interaction.followup.send(embed=embed)



@tree.command(name="move", description="Verschiebe das aktuelle Ticket in eine andere Kategorie.")
async def move_ticket(interaction: discord.Interaction, kategorie: str):
    if not is_ticket_channel(interaction.channel.id):
        await interaction.response.send_message("\U0000274C Dieser Befehl kann nur in Ticket-Kanälen verwendet werden!", ephemeral=True)
        return

    ticket_info = bot.ticket_channels.get(interaction.channel.id, {})
    current_ticket_type = ticket_info.get('type')

    if not current_ticket_type or current_ticket_type not in TICKET_CATEGORIES:
        await interaction.response.send_message("\U0000274C Aktueller Ticket-Typ nicht erkannt!", ephemeral=True)
        return

   
    current_config = TICKET_CATEGORIES[current_ticket_type]
    user_roles = [role.id for role in interaction.user.roles]

    if not any(role_id in user_roles for role_id in current_config["allowed_roles"]):
        await interaction.response.send_message("\U0000274C Sie haben keine Berechtigung, dieses Ticket zu verwalten!", ephemeral=True)
        return

   
    if kategorie not in TICKET_CATEGORIES:
        available_categories = ", ".join(TICKET_CATEGORIES.keys())
        await interaction.response.send_message(f"\U0000274C Unbekannte Kategorie! Verfügbare Kategorien: {available_categories}", ephemeral=True)
        return

   
    if kategorie == current_ticket_type:
        await interaction.response.send_message("\U0000274C Das Ticket befindet sich bereits in dieser Kategorie!", ephemeral=True)
        return

    await interaction.response.defer()

    try:
        target_config = TICKET_CATEGORIES[kategorie]
        target_category = bot.get_channel(target_config["category_id"])

        if not target_category:
            await interaction.followup.send("\U0000274C Zielkategorie nicht gefunden!", ephemeral=True)
            return

      
        await interaction.channel.edit(category=target_category)

        
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            bot.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

       
        if ticket_info.get('creator'):
            creator = interaction.guild.get_member(ticket_info['creator'])
            if creator:
                overwrites[creator] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

       
        for role_id in target_config["allowed_roles"]:
            role = interaction.guild.get_role(role_id)
            if role:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        
        await interaction.channel.edit(overwrites=overwrites)

       
        bot.ticket_channels[interaction.channel.id]['type'] = kategorie

        
        await log_ticket_message_event(
            interaction.channel.id,
            "TICKET VERSCHOBEN",
            f"Von '{current_ticket_type}' zu '{kategorie}' durch {interaction.user.display_name}"
        )

      
        new_close_view = get_ticket_close_view(kategorie)

        embed = discord.Embed(
            title="\U0001F4E6 Ticket verschoben",
            description=f"Ticket wurde erfolgreich von `{current_ticket_type}` zu `{kategorie}` verschoben",
            color=discord.Color.blue()
        )
        embed.add_field(name="Verschoben von", value=f"{interaction.user.mention}", inline=False)
        embed.add_field(name="Neue Kategorie", value=f"{target_category.name}", inline=False)

        await interaction.followup.send(embed=embed)
        await interaction.channel.send("**Neue Ticket-Verwaltung für diese Kategorie:**", view=new_close_view)

    except Exception as e:
        embed = discord.Embed(
            title="\U0000274C Fehler",
            description=f"Fehler beim Verschieben des Tickets: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)


@tree.command(name="rename", description="Ändere den Namen des aktuellen Tickets.")

async def rename_ticket(interaction: discord.Interaction, neuer_name: str):

    if not is_ticket_channel(interaction.channel.id):

        await interaction.response.send_message("\U0000274C Dieser Befehl kann nur in Ticket-Kanälen verwendet werden!", ephemeral=True)

        return



    ticket_info = bot.ticket_channels.get(interaction.channel.id, {})

    ticket_type = ticket_info.get('type')



    if not ticket_type:

        channel = interaction.channel

        for t_type, config in TICKET_CATEGORIES.items():

            if channel.category_id == config["category_id"]:

                ticket_type = t_type

                bot.ticket_channels[interaction.channel.id] = {

                    'type': ticket_type,

                    'creator': None,

                    'created_at': channel.created_at,

                    'transcript_messages': []

                }

                break



    if not ticket_type or ticket_type not in TICKET_CATEGORIES:

        await interaction.response.send_message("\U0000274C Ticket-Typ nicht erkannt!", ephemeral=True)

        return



    ticket_config = TICKET_CATEGORIES[ticket_type]

    user_roles = [role.id for role in interaction.user.roles]



    if not any(role_id in user_roles for role_id in ticket_config["allowed_roles"]):

        await interaction.response.send_message("\U0000274C Sie haben keine Berechtigung, dieses Ticket zu verwalten!", ephemeral=True)

        return



    if not neuer_name or len(neuer_name) > 100:

        await interaction.response.send_message("\U0000274C Der Name muss zwischen 1 und 100 Zeichen lang sein!", ephemeral=True)

        return



    import re





    clean_name = neuer_name.replace(" ", "-").replace("_", "-")

    clean_name = clean_name.lower()


    clean_name = re.sub(r"<a?:\w+:\d+>", "", clean_name)


    clean_name = re.sub(r"[^a-z0-9äöüß\-\U0001F000-\U0001FFFF\u2600-\u27BF]", "", clean_name)



    if not clean_name:

        clean_name = "ticket"



    try:

        old_name = interaction.channel.name

        await interaction.channel.edit(name=clean_name, reason=f"Ticket umbenannt von {interaction.user}")



        embed = discord.Embed(

            title="\U0001F3F7 Ticket umbenannt",

            description=f"Ticket wurde zu `{clean_name}` umbenannt",

            color=discord.Color.blue()

        )

        embed.add_field(name="Umbenannt von", value=f"{interaction.user.mention}", inline=False)



        await interaction.response.send_message(embed=embed)



        await log_ticket_message_event(

            interaction.channel.id,

            "TICKET UMBENANNT",

            f"Von '{old_name}' zu '{clean_name}' durch {interaction.user.display_name}"

        )



    except Exception as e:

        embed = discord.Embed(

            title="\U0000274C Fehler",

            description=f"Fehler beim Umbenennen: {str(e)}",

            color=discord.Color.red()

        )

        await interaction.response.send_message(embed=embed, ephemeral=True)



@tree.command(name="sync",

              description="Synchronisiere Slash-Commands mit Discord.")

async def sync(interaction: discord.Interaction):
    if SYNC_ROLE_ID not in [role.id for role in interaction.user.roles]:
        await send_missing_role_response(interaction)
        return

    await interaction.response.defer(ephemeral=True)

    
    synced_global = await tree.sync()
    synced_guild = await tree.sync(guild=interaction.guild)

    await interaction.edit_original_response(
        content=
        f"\U00002705 Slash-Commands wurden synchronisiert.\nGlobal: {len(synced_global)} Befehle\nServer-spezifisch: {len(synced_guild)} Befehle")
    print(f"\U0001F501 Slash-Commands synchronisiert - Global: {len(synced_global)}, Guild: {len(synced_guild)}")

@bot.command(name="mute")

@commands.has_permissions(moderate_members=True)

async def cmd_mute(ctx, member: discord.Member, minutes: int, *, reason: str = None):

    try:

        duration = timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)


        try:
            embed = discord.Embed(
                title="Sie wurden stummgeschaltet",
                description=f"Sie wurden auf dem Server **{ctx.guild.name}** stummgeschaltet.",
                color=discord.Color.orange()
            )
            embed.add_field(name="Grund", value=reason or "Kein Grund angegeben", inline=False)
            embed.add_field(name="Dauer", value=f"{minutes} Minuten", inline=False)
            embed.add_field(name="Ausgeführt von", value=str(ctx.author), inline=False)
            embed.timestamp = discord.utils.utcnow()
            await member.send(embed=embed)
        except Exception as e:
            print(f"Konnte keine DM an {member.name} senden: {e}")

        await ctx.send(f"{member.mention} wurde für {minutes} Minuten stummgeschaltet. Grund: {reason}")
        code = "N/A"
        await log_mod_action(ctx.guild, "\U0001F507 Mitglied gemutet", discord.Color.gold(), member.id, code, ctx.author, user_mention=member.mention)
    except discord.Forbidden:
        await ctx.send("Ich habe keine Berechtigung, diesen Benutzer zu stummschalten.")

@bot.command(name="unmute")

@commands.has_permissions(moderate_members=True)

async def cmd_unmute(ctx, user_id: int):

    member = ctx.guild.get_member(user_id)

    if member:

        try:

            await member.timeout(None)


            try:
                embed = discord.Embed(
                    title="Ihre Stummschaltung wurde aufgehoben",
                    description=f"Ihre Stummschaltung auf dem Server **{ctx.guild.name}** wurde aufgehoben.",
                    color=discord.Color.green()
                )
                embed.add_field(name="Ausgeführt von", value=str(ctx.author), inline=False)
                embed.timestamp = discord.utils.utcnow()
                await member.send(embed=embed)
            except Exception as e:
                print(f"Konnte keine DM an {member.name} senden: {e}")

            await ctx.send(f"{member.mention} wurde entstummt.")

            code = "N/A"

            await log_mod_action(ctx.guild, "\U0001F50A Timeout aufgehoben", discord.Color.blurple(), user_id, code, ctx.author, user_mention=member.mention)

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


                try:
                    embed = discord.Embed(
                        title="Sie wurden entbannt",
                        description=f"Sie wurden vom Server **{ctx.guild.name}** entbannt.",
                        color=discord.Color.green()
                    )
                    embed.add_field(name="Ausgeführt von", value=str(ctx.author), inline=False)
                    embed.timestamp = discord.utils.utcnow()
                    await ban_entry.user.send(embed=embed)
                except Exception as e:
                    print(f"Konnte keine DM an {ban_entry.user.name} senden: {e}")

                await ctx.send(f"{ban_entry.user} wurde entbannt.")

                code = "N/A"

                await log_mod_action(ctx.guild, "\U0001F528 Benutzer entbannt", discord.Color.green(), user_id, code, ctx.author, user_mention=str(ban_entry.user))

                found_user = True

                break

        if not found_user:

            await ctx.send("Benutzer nicht in der Ban-Liste gefunden.")

    except discord.Forbidden:

        await ctx.send("Ich habe keine Berechtigung, diesen Benutzer zu entbannen.")

    except Exception as e:

        await ctx.send(f"Fehler beim Entbannen: {e}")



async def close_ticket_with_reason(ticket_channel, closed_by, reason):

    """Close ticket with reason and send DM to creator"""

    try:

        ticket_info = getattr(bot, 'ticket_channels', {}).get(ticket_channel.id, {})


        transcript_file_for_dm = await generate_ticket_transcript_file(ticket_channel, closed_by, reason)

        transcript_file_for_channel = await generate_ticket_transcript_file(ticket_channel, closed_by, reason)





        if ticket_info.get('creator'):

            try:

                creator = bot.get_user(ticket_info['creator'])

                if creator:

                    embed = discord.Embed(

                        title="Ihr Ticket wurde geschlossen",

                        description=f"**Ticket:** {ticket_channel.name}\n**Grund:** {reason}",

                        color=discord.Color.red()

                    )

                    embed.add_field(name="Geschlossen von", value=closed_by.mention, inline=True)

                    embed.add_field(name="Geschlossen am", value=discord.utils.format_dt(discord.utils.utcnow(), style='F'), inline=True)

                    embed.timestamp = discord.utils.utcnow()



                    if transcript_file_for_dm:

                        await creator.send(embed=embed, file=transcript_file_for_dm)

                    else:

                        await creator.send(embed=embed)

            except Exception as e:

                print(f"Konnte keine DM an Ticket-Ersteller senden: {e}")



        transcript_channel = bot.get_channel(TICKET_TRANSCRIPT_CHANNEL_ID)

        if transcript_channel and transcript_file_for_channel:

            try:

                embed = discord.Embed(

                    title="Ticket Transkript",

                    description=f"Vollständiges Transkript für **{ticket_channel.name}**",

                    color=discord.Color.blue()

                )

                embed.add_field(name="Ticket-Typ", value=ticket_info.get('type', 'Unbekannt'), inline=True)

                embed.add_field(name="Ersteller", value=f"<@{ticket_info.get('creator', 0)}>", inline=True)

                embed.add_field(name="Geschlossen von", value=closed_by.mention, inline=True)

                embed.add_field(name="Grund", value=reason, inline=False)

                embed.timestamp = discord.utils.utcnow()



                await transcript_channel.send(embed=embed, file=transcript_file_for_channel)

            except Exception as e:

                print(f"Konnte Transkript nicht in Channel senden: {e}")



    except Exception as e:

        print(f"Fehler beim Schließen des Tickets mit Grund: {e}")



async def generate_ticket_transcript_file(ticket_channel, closed_by, reason="Kein Grund angegeben"):

    """Generate a transcript file that can be sent via DM"""

    try:

        ticket_info = getattr(bot, 'ticket_channels', {}).get(ticket_channel.id, {})



        transcript_text = f"=== TICKET TRANSKRIPT ===\n"

        transcript_text += f"Ticket: {ticket_channel.name}\n"

        transcript_text += f"Ersteller: {bot.get_user(ticket_info.get('creator', 0)) if ticket_info.get('creator') else 'Unbekannt'}\n"

        transcript_text += f"Geschlossen von: {closed_by}\n"

        transcript_text += f"Grund: {reason}\n"

        transcript_text += f"Erstellt: {ticket_info.get('created_at', 'Unbekannt')}\n"

        transcript_text += f"Geschlossen: {discord.utils.utcnow()}\n"

        transcript_text += f"{'='*50}\n\n"

        messages = []

        async for message in ticket_channel.history(limit=None, oldest_first=True):

            messages.append(message)



        for message in messages:

            timestamp = message.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')

            author = f"{message.author.display_name} ({message.author.name})"



            transcript_text += f"[{timestamp}] {author}:\n"



            if message.content:

                transcript_text += f"  {message.content}\n"



            if message.attachments:

                for attachment in message.attachments:

                    transcript_text += f"  \U0001F4AC Anhang: {attachment.filename}\n"



            if message.embeds:

                for embed in message.embeds:

                    transcript_text += f"  \U0001F4AC Embed: {embed.title or 'Untitled'}\n"



            transcript_text += "\n"



        filename = f"transcript_{ticket_channel.name}_{discord.utils.utcnow().strftime('%Y%m%d_%H%M%S')}.txt"

        return discord.File(io.StringIO(transcript_text), filename=filename)



    except Exception as e:

        print(f"\U0000274C Fehler beim Erstellen des Transcript-Files: {e}")

        return None




async def generate_ticket_transcript(ticket_channel, closed_by, reason="Kein Grund angegeben"):

    """Generate a complete transcript of the ticket"""

    try:

        transcript_channel = bot.get_channel(TICKET_TRANSCRIPT_CHANNEL_ID)

        if not transcript_channel:

            print(f"\U0000274C Transcript Channel {TICKET_TRANSCRIPT_CHANNEL_ID} nicht gefunden!")

            return



        ticket_info = getattr(bot, 'ticket_channels', {}).get(ticket_channel.id, {})

        transcript_text = f"=== TICKET TRANSKRIPT ===\n"

        transcript_text += f"Ticket: {ticket_channel.name}\n"

        transcript_text += f"Ersteller: {bot.get_user(ticket_info.get('creator', 0)) if ticket_info.get('creator') else 'Unbekannt'}\n"

        transcript_text += f"Geschlossen von: {closed_by}\n"

        transcript_text += f"Grund: {reason}\n"

        transcript_text += f"Erstellt: {ticket_info.get('created_at', 'Unbekannt')}\n"

        transcript_text += f"Geschlossen: {discord.utils.utcnow()}\n"

        transcript_text += f"{'='*50}\n\n"



        messages = []

        async for message in ticket_channel.history(limit=None, oldest_first=True):

            messages.append(message)



        for message in messages:

            timestamp = message.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')

            author = f"{message.author.display_name} ({message.author.name})"



            transcript_text += f"[{timestamp}] {author}:\n"



            if message.content:

                transcript_text += f"  {message.content}\n"



            if message.attachments:

                for attachment in message.attachments:

                    transcript_text += f"  \U0001F4AC Anhang: {attachment.filename}\n"



            if message.embeds:

                for embed in message.embeds:

                    transcript_text += f"  \U0001F4AC Embed: {embed.title or 'Untitled'}\n"



            transcript_text += "\n"



        filename = f"transcript_{ticket_channel.name}_{discord.utils.utcnow().strftime('%Y%m%d_%H%M%S')}.txt"

        file = discord.File(io.StringIO(transcript_text), filename=filename)



        embed = discord.Embed(

            title="\U0001F3AB Ticket Transkript",

            description=f"Vollständiges Transkript für **{ticket_channel.name}**",

            color=discord.Color.blue()

        )

        embed.add_field(name="Ticket-Typ", value=ticket_info.get('type', 'Unbekannt'), inline=True)

        embed.add_field(name="Ersteller", value=f"<@{ticket_info.get('creator', 0)}>", inline=True)

        embed.add_field(name="Geschlossen von", value=closed_by.mention, inline=True)

        embed.add_field(name="Anzahl Nachrichten", value=str(len(messages)), inline=True)

        embed.timestamp = discord.utils.utcnow()



        await transcript_channel.send(embed=embed, file=file)



        if hasattr(bot, 'ticket_channels') and ticket_channel.id in bot.ticket_channels:

            del bot.ticket_channels[ticket_channel.id]



        print(f"\U00002705 Transcript für {ticket_channel.name} erstellt")



    except Exception as e:

        print(f"\U0000274C Fehler beim Erstellen des Transcripts: {e}")





async def log_ticket_message_event(channel_id, event_type, message_data):

    """Log ticket message events for transcript"""

    if not hasattr(bot, 'ticket_channels'):

        return



    if channel_id in bot.ticket_channels:

        timestamp = discord.utils.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

        bot.ticket_channels[channel_id]['transcript_messages'].append({

            'timestamp': timestamp,

            'event': event_type,

            'content': message_data

        })



def is_ticket_channel(channel_id):

    """Check if a channel is a ticket channel"""

    if not hasattr(bot, 'ticket_channels'):

        bot.ticket_channels = {}



    if channel_id in bot.ticket_channels:

        return True



    channel = bot.get_channel(channel_id)

    if not channel or not channel.category_id:

        return False



    for ticket_type, config in TICKET_CATEGORIES.items():

        if channel.category_id == config["category_id"]:



            bot.ticket_channels[channel_id] = {

                'type': ticket_type,

                'creator': None,

                'created_at': channel.created_at,

                'transcript_messages': []

            }

            return True



    return False

@bot.event

async def on_message(message):

    if message.author.bot:

        return



    cmd_content = message.content.strip().lower()





    if is_ticket_channel(message.channel.id):

        content = f"Nachricht von {message.author.display_name}: {message.content}"

        if message.attachments:

            content += f" [Anhänge: {', '.join([att.filename for att in message.attachments])}]"

        await log_ticket_message_event(message.channel.id, "NACHRICHT GESENDET", content)





    if cmd_content.startswith("s!löschen"):

        if not any(role.id in ALLOWED_S_ROLE_IDS for role in message.author.roles):

            await log_error(

                f"Unerlaubter Befehl `{message.content}` von {message.author.mention} in {message.channel.mention}"

            )

            return
        parts = message.content.split()
        if len(parts) != 2 or not parts[1].isdigit():

            try:

                await message.delete()
            except Exception:
                pass
            await message.channel.send("\U0000274C Benutzung: `s!löschen <Anzahl>`", delete_after=5)
            return

        amount = int(parts[1])
        log_channel = bot.get_channel(LÖSCHEN_LOG_CHANNEL_ID)

        try:

            messages_to_delete = []
            async for msg in message.channel.history(limit=amount + 1):
                messages_to_delete.append(msg)


            attachments_to_download = []
            for msg in messages_to_delete:
                for att in msg.attachments:
                    try:

                        data = await att.read()
                        attachments_to_download.append({
                            'filename': att.filename,
                            'data': data,
                            'message_id': msg.id,
                            'author': str(msg.author)
                        })
                    except Exception as e:
                        print(f"Fehler beim Herunterladen von {att.filename}: {e}")


            if messages_to_delete:
                try:

                    valid_messages = []
                    for msg in messages_to_delete:
                        age = discord.utils.utcnow() - msg.created_at
                        if age.days < 14:
                            valid_messages.append(msg)

                    if len(valid_messages) > 1:
                        await message.channel.delete_messages(valid_messages)
                    elif len(valid_messages) == 1:
                        await valid_messages[0].delete()

                    deleted = messages_to_delete
                except discord.NotFound:

                    deleted = messages_to_delete
                except discord.HTTPException as e:
                    if e.code == 10008:
                        deleted = messages_to_delete
                    else:
                        print(f"HTTP Fehler beim Löschen: {e}")
                        deleted = messages_to_delete
                except Exception as e:
                    print(f"Fehler beim Löschen der Nachrichten: {e}")
                    deleted = messages_to_delete
            else:
                deleted = []

            confirmation = await message.channel.send(
                f"\U00002705 {amount} Nachricht(en) gelöscht.",
                delete_after=5
            )

            log_lines = []
            files_to_send = []

            for msg in reversed(deleted):
                timestamp = msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
                author = f"{msg.author} ({msg.author.id})"
                content = msg.content or "[Leerer Inhalt]"

                if msg.attachments:
                    attachments_info = []
                    for att in msg.attachments:
                        attachments_info.append(att.filename)


                        for downloaded in attachments_to_download:
                            if downloaded['message_id'] == msg.id and downloaded['filename'] == att.filename:
                                try:
                                    buf = io.BytesIO(downloaded['data'])
                                    buf.seek(0)

                                    safe_author = "".join(c for c in downloaded['author'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                                    prefix_filename = f"[{safe_author}]_{downloaded['filename']}"
                                    files_to_send.append(discord.File(buf, filename=prefix_filename))
                                except Exception as e:
                                    print(f"Fehler beim Erstellen der Datei: {e}")
                                break

                    content += f" [Anhänge: {', '.join(attachments_info)}]"

                log_lines.append(f"[{timestamp}] {author}: {content}")

            log_text = "\n".join(log_lines) or "Keine Nachrichten vorhanden."
            filename = f"gelöschte_nachrichten_{message.channel.name}_{message.created_at.strftime('%Y%m%d_%H%M%S')}.txt"
            file = discord.File(io.StringIO(log_text), filename=filename)

            if log_channel:
                await log_channel.send(
                    content=f"\U0001F5D1\uFE0F **{len(deleted)} Nachrichten gelöscht in {message.channel.mention}** von {message.author.mention}",
                    files=[file, *files_to_send]
                )



            await asyncio.sleep(5)

            await confirmation.delete()



        except discord.Forbidden:

            await message.channel.send("\U0000274C Ich habe keine Berechtigung, Nachrichten zu löschen.", delete_after=5)

        except Exception as e:

            await message.channel.send(f"\U0000274C Fehler beim Löschen: {e}", delete_after=5)



        return





    if cmd_content == "s!stats":

        if not any(role.id in ALLOWED_S_ROLE_IDS for role in message.author.roles):

            await log_error(

                f"Unerlaubter Befehl `{message.content}` von {message.author.mention} in {message.channel.mention}"

            )

            return
        try:
            await message.delete()
        except Exception:
            pass

        def get_role_count(role_name: str) -> int:

            role = discord.utils.get(message.guild.roles, name=role_name)

            return len(role.members) if role else 0



        stats = {

            "San Andreas Medical Services Stats \U0001F4CA": {

                "Gesamte Mitglieder": get_role_count("@everyone"),

                "SAMS Mitglieder": get_role_count("San Andreas Medical Services")

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

                ("\U0001F3EB| Leitung Medical Education", get_role_count("\U0001F3EB| Leitung Medical Education")),

                ("\U0001F52A| Leitung General Surgery", get_role_count("\U0001F52A| Leitung General Surgery")),

                ("\U0001F9E0| Leitung Psychiatric Department", get_role_count("\U0001F9E0| Leitung Psychiatric Department")),

                ("\U0001F681| Leitung Search and Resuce", get_role_count("\U0001F681| Leitung Search and Resuce")),

                ("\U0001F681| SAR  - Instructor", get_role_count("\U0001F681| SAR  - Instructor")),

                ("\U0001F3EB| Medical Education Department", get_role_count("\U0001F3EB| Medical Education Department")),

                ("\U0001F52A| General Surgery", get_role_count("\U0001F52A| General Surgery")),

                ("\U0001F52A| Operative License", get_role_count("\U0001F52A| Operative License")),

                ("\U0001F9E0| Psychiatric Department", get_role_count("\U0001F9E0| Psychiatric Department")),

                ("\U0001F681| Search and Rescue", get_role_count("\U0001F681| Search and Rescue")),

                ("\U0001F6A4| SAR-Bootsausbildung", get_role_count("\U0001F6A4| SAR-Bootsausbildung")),

                ("San Andreas Medical Services", get_role_count("San Andreas Medical Services")),

                ("\U0001F3DD | Abgemeldet", get_role_count("\U0001F3DD | Abgemeldet"))

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

        embed = discord.Embed(title="\U0001F4CA San Andreas Medical Services Stats", color=discord.Color.blurple())

        embed.add_field(

            name="**Gesamte Mitglieder**",

            value=str(stats["San Andreas Medical Services Stats \U0001F4CA"]["Gesamte Mitglieder"]),

            inline=True

        )

        embed.add_field(

            name="**SAMS Mitglieder**",

            value=str(stats["San Andreas Medical Services Stats \U0001F4CA"]["SAMS Mitglieder"]),

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

        await bot.process_commands(message)

        return



    if not any(role.id in ALLOWED_S_ROLE_IDS for role in message.author.roles):

        await log_error(

            f"Unerlaubter Befehl `{message.content}` von {message.author.mention} in {message.channel.mention}"

        )

        return



    parts = message.content.split()

    cmd = parts[0].lower()



    async def send_confirmation(channel, action, member_mention, reason, duration=None):

        embed = discord.Embed(title=action, color=discord.Color.green())

        embed.add_field(name="Nutzer", value=member_mention, inline=False)

        embed.add_field(name="Grund", value=reason or "Kein Grund angegeben", inline=False)

        if duration:

            embed.add_field(name="Dauer", value=duration, inline=False)

        embed.timestamp = discord.utils.utcnow()

        await channel.send(embed=embed)



    async def log_mod_action(guild, action, color, user_id, code, moderator, user_mention=None, reason=None, duration=None):

        channel = guild.get_channel(MOD_LOG_CHANNEL_ID)

        if not channel:

            print(f"Mod-Log Channel mit ID {MOD_LOG_CHANNEL_ID} nicht gefunden!")

            return



        embed = discord.Embed(title=action, color=color)

        embed.add_field(name="Nutzer", value=user_mention or f"ID: {user_id}", inline=False)

        embed.add_field(name="Nutzer-ID", value=str(user_id), inline=False)

        embed.add_field(name="Code", value=code, inline=False)

        embed.add_field(name="Ausgeführt von", value=moderator.mention, inline=False)

        if reason:

            embed.add_field(name="Grund", value=reason, inline=False)

        if duration:

            embed.add_field(name="Dauer", value=duration, inline=False)

        embed.timestamp = discord.utils.utcnow()

        await channel.send(embed=embed)



    try:

        if cmd == "s!ban" and len(parts) >= 2:

            args = parts[1:]

            banned_users = []

            failed_users = []



            def is_user_id(token: str) -> bool:

                try:

                    int(token.strip("<@!>"))

                    return True

                except ValueError:

                    return False



            i = 0

            while i < len(args):

                if not is_user_id(args[i]):

                    failed_users.append((args[i], "Ungültige Nutzer-ID"))

                    i += 1

                    continue



                user_id = int(args[i].strip("<@!>"))

                reason_parts = []

                j = i + 1

                while j < len(args) and not is_user_id(args[j]):

                    reason_parts.append(args[j])

                    j += 1

                reason = " ".join(reason_parts) or "Kein Grund angegeben"

                try:
                    member = message.guild.get_member(user_id)
                    if member:

                        try:
                            embed = discord.Embed(
                                title="Sie wurden gebannt",
                                description=f"Sie wurden vom Server **{message.guild.name}** gebannt.",
                                color=discord.Color.red()
                            )
                            embed.add_field(name="Grund", value=reason, inline=False)
                            embed.add_field(name="Dauer", value="Permanent", inline=False)
                            embed.add_field(name="Ausgeführt von", value=str(message.author), inline=False)
                            embed.timestamp = discord.utils.utcnow()
                            await member.send(embed=embed)
                        except Exception as e:
                            print(f"Konnte keine DM an {member.name} senden: {e}")

                        await member.ban(reason=reason)
                        banned_users.append(f"{member.mention} (Grund: {reason})")
                        await log_mod_action(
                            message.guild,
                            "Benutzer gebannt \U0001F528",
                            discord.Color.dark_red(),
                            user_id,
                            "N/A",
                            message.author,
                            user_mention=member.mention,
                            reason=reason,
                            duration="Permanent"
                        )
                        await send_confirmation(message.channel, "Ban bestätigt \U0001F528", member.mention, reason, "Permanent")
                    else:
                        user = await bot.fetch_user(user_id)

                        try:
                            embed = discord.Embed(
                                title="Sie wurden gebannt",
                                description=f"Sie wurden vom Server **{message.guild.name}** gebannt.",
                                color=discord.Color.red()
                            )
                            embed.add_field(name="Grund", value=reason, inline=False)
                            embed.add_field(name="Dauer", value="Permanent", inline=False)
                            embed.add_field(name="Ausgeführt von", value=str(message.author), inline=False)
                            embed.timestamp = discord.utils.utcnow()
                            await user.send(embed=embed)
                        except Exception as e:
                            print(f"Konnte keine DM an {user.name if user else user_id} senden: {e}")

                        await message.guild.ban(user, reason=reason)
                        mention = user.mention if user else f"ID: {user_id}"
                        banned_users.append(f"{mention} (Grund: {reason})")
                        await log_mod_action(
                            message.guild,
                            "Benutzer gebannt (Force Ban) \U0001F528",
                            discord.Color.dark_red(),
                            user_id,
                            "N/A",
                            message.author,
                            user_mention=mention,
                            reason=reason,
                            duration="Permanent"
                        )
                        await send_confirmation(message.channel, "Force Ban bestätigt \U0001F528", mention, reason, "Permanent")
                except Exception as e:
                    failed_users.append((user_id, str(e)))
                i = j



            if failed_users:

                error_msg = "\n".join([f"\U0000274C `{uid}` → {err}" for uid, err in failed_users])

                await message.channel.send(f"Fehlgeschlagene Banns:\n{error_msg}")




        elif cmd == "s!kick" and len(parts) >= 2:

            try:

                user_id = int(parts[1].strip("<@!>"))

            except ValueError:

                await message.channel.send("\U0000274C Ungültige Nutzer-ID.")

                return
            reason = " ".join(parts[2:]) or "Kein Grund angegeben"
            member = message.guild.get_member(user_id)
            if not member:
                await message.channel.send("\U0000274C Nutzer nicht gefunden.")
                return
            await member.kick(reason=reason)
            await log_mod_action(
                message.guild,
                "Benutzer gekickt \U0001F528",
                discord.Color.orange(),
                user_id,
                "N/A",
                message.author,
                user_mention=member.mention,
                reason=reason
            )
            await send_confirmation(message.channel, "Kick bestätigt \U0001F528", member.mention, reason)




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

                    await message.channel.send("\U0000274C Dauer muss größer als 0 sein.")

                    return

            except ValueError:

                await message.channel.send("\U0000274C Ungültige Eingabe. Format: `s!mute @user 10m [Grund]`")

                return



            reason = " ".join(parts[3:]) or "Kein Grund angegeben"

            member = message.guild.get_member(user_id)

            if not member:

                await message.channel.send("\U0000274C Nutzer nicht gefunden.")

                return

            try:
                embed = discord.Embed(
                    title="Sie wurden stummgeschaltet",
                    description=f"Sie wurden auf dem Server **{message.guild.name}** stummgeschaltet.",
                    color=discord.Color.orange()
                )
                embed.add_field(name="Grund", value=reason or "Kein Grund angegeben", inline=False)
                embed.add_field(name="Dauer", value=parts[2], inline=False)
                embed.add_field(name="Ausgeführt von", value=str(message.author), inline=False)
                embed.timestamp = discord.utils.utcnow()
                await member.send(embed=embed)
            except Exception as e:
                print(f"Konnte keine DM an {member.name} senden: {e}")

            await member.timeout(timedelta(minutes=duration_minutes), reason=reason)
            await log_mod_action(
                message.guild,
                "Mitglied gemutet \U0001F528",
                discord.Color.gold(),
                user_id,
                "N/A",
                message.author,
                user_mention=member.mention,
                reason=reason,
                duration=parts[2]
            )
            await send_confirmation(message.channel, "Mute bestätigt \U000023F3", member.mention, reason, parts[2])




        elif cmd == "s!info" and len(parts) == 2:

            try:

                user_input = parts[1].strip()

                if user_input.startswith('<@') and user_input.endswith('>'):

                    user_id = int(user_input.strip('<@!>'))

                else:

                    user_id = int(user_input)

            except ValueError:

                await message.channel.send("\U0000274C Ungültige Nutzer-ID oder Mention.")

                return



            member = message.guild.get_member(user_id)

            if not member:

                await message.channel.send("\U0000274C Nutzer nicht gefunden.")

                return



            joined_at = member.joined_at.strftime("%d.%m.%Y %H:%M:%S") if member.joined_at else "Unbekannt"

            created_at = member.created_at.strftime("%d.%m.%Y %H:%M:%S")

            roles = [role.name for role in member.roles if role.name != "@everyone"]

            roles_text = ", ".join(roles) if roles else "Keine Rollen"



            embed = discord.Embed(title="\U0001F464 Benutzerinfo", color=discord.Color.blurple())

            embed.add_field(name="Name", value=str(member), inline=False)

            embed.add_field(name="ID", value=str(member.id), inline=False)

            embed.add_field(name="Serverbeitritt", value=joined_at, inline=False)

            embed.add_field(name="Account erstellt", value=created_at, inline=False)

            embed.add_field(name="Rollen", value=roles_text, inline=False)

            if member.avatar:

                embed.set_thumbnail(url=member.avatar.url)

            embed.timestamp = discord.utils.utcnow()

            await message.channel.send(embed=embed)




        elif cmd == "s!unban" and len(parts) >= 2:

            try:

                user_id = int(parts[1])

            except ValueError:

                await message.channel.send("\U0000274C Ungültige Nutzer-ID.")

                return



            reason = " ".join(parts[2:]) or None

            found_user = False

            async for ban_entry in message.guild.bans():

                if ban_entry.user.id == user_id:

                    await message.guild.unban(ban_entry.user, reason=reason)

                    try:
                        embed = discord.Embed(
                            title="Sie wurden entbannt",
                            description=f"Sie wurden vom Server **{message.guild.name}** entbannt.",
                            color=discord.Color.green()
                        )
                        embed.add_field(name="Grund", value=reason or "Kein Grund angegeben", inline=False)
                        embed.add_field(name="Ausgeführt von", value=str(message.author), inline=False)
                        embed.timestamp = discord.utils.utcnow()
                        await ban_entry.user.send(embed=embed)
                    except Exception as e:
                        print(f"Konnte keine DM an {ban_entry.user.name} senden: {e}")

                    await log_mod_action(

                        message.guild,

                        "Benutzer entbannt \U0001F528",

                        discord.Color.green(),

                        user_id,

                        "N/A",

                        message.author,

                        user_mention=str(ban_entry.user),

                        reason=reason

                    )

                    await send_confirmation(message.channel, "Unban bestätigt \U0001F528", str(ban_entry.user), reason)

                    found_user = True

                    break

            if not found_user:

                await message.channel.send("\U0000274C Nutzer nicht gefunden.")





        elif cmd == "s!unmute" and len(parts) >= 2:

            try:

                user_input = parts[1].strip()

                if user_input.startswith('<@') and user_input.endswith('>'):

                    user_id = int(user_input.strip('<@!>'))

                else:

                    user_id = int(user_input)

            except ValueError:

                await message.channel.send("\U0000274C Ungültige Nutzer-ID oder Mention.")

                return



            reason = " ".join(parts[2:]) or None

            member = message.guild.get_member(user_id)

            if not member:

                await message.channel.send("\U0000274C Nutzer nicht gefunden.")

                return



            await member.timeout(None, reason=reason)


            try:
                embed = discord.Embed(
                    title="Ihre Stummschaltung wurde aufgehoben",
                    description=f"Ihre Stummschaltung auf dem Server **{message.guild.name}** wurde aufgehoben.",
                    color=discord.Color.green()
                )
                embed.add_field(name="Grund", value=reason or "Kein Grund angegeben", inline=False)
                embed.add_field(name="Ausgeführt von", value=str(message.author), inline=False)
                embed.timestamp = discord.utils.utcnow()
                await member.send(embed=embed)
            except Exception as e:
                print(f"Konnte keine DM an {member.name} senden: {e}")

            await log_mod_action(

                message.guild,

                "Timeout aufgehoben \U0001F528",

                discord.Color.blurple(),

                user_id,

                "N/A",

                message.author,

                user_mention=member.mention,

                reason=reason

            )

            await send_confirmation(message.channel, "Unmute bestätigt \U000023F3", member.mention, reason)



        else:

            await message.channel.send("\U0000274C Unbekannter Befehl.")



    except Exception:

        try:

            await message.channel.send("\U0000274C Es ist ein Fehler aufgetreten.")

        except Exception:

            pass



    await bot.process_commands(message)





@bot.event

async def on_message_edit(before, after):



    if before.author.bot or before.channel.id in EXCLUDED_CHANNELS:

        return



    if is_ticket_channel(before.channel.id):

        edit_info = f"Nachricht bearbeitet von {before.author.display_name}: {before.content[:500]}\nNachher: {after.content[:500]}"

        await log_ticket_message_event(before.channel.id, "NACHRICHT BEARBEITET", edit_info)



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

    try:



        if message.author.bot or message.channel.id in EXCLUDED_CHANNELS:

            return



        if is_ticket_channel(message.channel.id):

            delete_info = f"Nachricht gelöscht von {message.author.display_name}: {message.content[:500]}"

            if message.attachments:

                delete_info += f" [Anhänge: {', '.join([att.filename for att in message.attachments])}]"

            await log_ticket_message_event(message.channel.id, "NACHRICHT GELÖSCHT", delete_info)



        log_channel = bot.get_channel(MESSAGE_LOG_CHANNEL_ID)

        if not log_channel:

            print(f"\u26A0 Message Delete Log-Kanal mit ID {MESSAGE_LOG_CHANNEL_ID} nicht gefunden!")

            return



        print(f"\U0000274C Message deleted in #{message.channel.name} by {message.author.name}: {message.content[:50]}...")



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

        print(f"\U00002705 Message delete logged successfully")



    except Exception as e:

        print(f"\U0000274C Fehler beim Loggen der gelöschten Nachricht: {e}")

        try:

            await log_error(f"Fehler beim Message Delete Logging: {str(e)}")

        except:

            pass





async def handle_role_connections(member: discord.Member):

    if not member:

        return





    role_connections = {

        1378044741874221056: [

            1341491722961682543, 1341491806734651514, 1341491907724972122,

            1374491251482558545, 1374490464119554159, 1374491124349141002,

            1374490266706120845, 1374505941038530663, 1377037664087183420,

            1316162018838843522, 1086619242310402069, 1351940914997628968,

            1351941009570922598, 1351941076218286184, 1351941565207281724,

            1351941619246694510

        ],

        1378086885037178960: [

            1331579941321703464, 1377668908504584224, 1396121017893785630,

            1394474415021883452, 1390090743011344414, 1389686744840011916

        ],

        1378044948749746317: [

            1090587504987607121, 1405648419040788650, 1377743800155246602,

            1377743883064184903, 1377743930690506845, 1165747504814510231

        ],

        1378086334849093683: [

            906845737281810443, 1382218511820132456, 975473680358445136,

            1165771712441364651, 1097205524690374716

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



        executor_info = "Unbekannt"

        reason_info = None



        try:

            

            await handle_role_connections(after)

            

            audit_logs = [entry async for entry in after.guild.audit_logs(

                action=discord.AuditLogAction.member_role_update,

                limit=10

            )]



            for entry in audit_logs:

                if entry.target and entry.target.id == after.id:

                    time_diff = discord.utils.utcnow() - entry.created_at

                    if time_diff.total_seconds() <= 30:

                        

                        if entry.user.id == bot.user.id:

                            executor_info = "Rollen-Connection (Bot)"

                        else:

                            executor_info = f"{entry.user.mention} (@{entry.user.name})"

                        reason_info = entry.reason

                        break



        except discord.Forbidden:

            executor_info = "Keine Berechtigung für Audit-Logs"

        except Exception as e:

            print(f"Fehler beim Abrufen der Audit-Logs: {e}")

            executor_info = "Fehler beim Abrufen"



        embed.add_field(

            name="Ausgeführt von",

            value=executor_info,

            inline=False

        )



        if reason_info:

            embed.add_field(

                name="Reason",

                value=reason_info,

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

    if hasattr(bot, 'ticket_channels'):
        tickets_to_close = []
        for channel_id, ticket_info in bot.ticket_channels.items():
            if ticket_info.get('creator') == member.id:
                tickets_to_close.append(channel_id)

        for channel_id in tickets_to_close:
            try:
                channel = bot.get_channel(channel_id)
                if channel:

                    class SystemUser:
                        def __init__(self):
                            self.mention = "System"
                            self.name = "System"
                            self.id = 0

                    system_user = SystemUser()
                    await generate_ticket_transcript(channel, system_user, "Discord verlassen")
                    await channel.delete(reason="Ticket automatisch geschlossen - Benutzer hat Discord verlassen")

                    if channel_id in bot.ticket_channels:
                        del bot.ticket_channels[channel_id]
            except Exception as e:
                print(f"Fehler beim automatischen Schließen des Tickets {channel_id}: {e}")

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

    print(f"\U00002705 Bot ist online als {bot.user}")



    if not status_log.is_running():

        status_log.start()



    if not hasattr(bot, 'ticket_channels'):

        bot.ticket_channels = {}



    bot.add_view(TicketView())

    bot.add_view(TicketSelectView())

    bot.add_view(TicketCloseConfirmView())

    bot.add_view(PromotionResignationView())

    bot.add_view(DepartmentApplicationView())

    bot.add_view(ApplicationView())



    bot.add_view(LeitungsebeneCloseView())

    bot.add_view(FuehrungsebeneCloseView())

    bot.add_view(BeschwerdeCloseView())

    bot.add_view(TitelCloseView())

    bot.add_view(GeburtsurkundeCloseView())

    bot.add_view(BehandlungCloseView())

    bot.add_view(WiedereinstellungCloseView())

    bot.add_view(DiscordVerwaltungCloseView())

    bot.add_view(PromotionCloseView())

    bot.add_view(ResignationCloseView())

    bot.add_view(MedicalEducationCloseView())

    bot.add_view(GeneralSurgeryCloseView())

    bot.add_view(PsychiatricCloseView())

    bot.add_view(SarCloseView())

    bot.add_view(ApplicationCloseView())



    await setup_reaction_roles()

    await setup_ticket_system()

    await setup_promotion_resignation_system()

    await setup_department_application_system()

    await setup_application_system()

    await setup_sams_info_embed()





async def setup_ticket_system():

    """Setup ticket system message in the specified channel"""

    channel = bot.get_channel(TICKET_CHANNEL_ID)

    if not channel:

        print("\U0000274C Ticket Channel nicht gefunden!")

        return



    existing_message = None

    try:

        async for message in channel.history(limit=100):

            if (message.author == bot.user and
                message.embeds and
                message.embeds[0].title == "San Andreas Medical Services - Ticket System"):

                existing_message = message

                break

    except Exception as e:

        print(f"Fehler beim Überprüfen vorhandener Ticket-Nachrichten: {e}")



    if existing_message:

        print("\U00002705 Ticket System bereits vorhanden - kein neues Setup erforderlich!")

        return



    embed = discord.Embed(

        title="San Andreas Medical Services - Ticket System",

        description=(

            "Hier haben Sie *über den Bot unter dieser Nachricht* die Möglichkeit mit dem San Andreas Medical Services direkten Kontakt aufzunehmen.\n"

            "**Bitte ändern Sie Ihren Nickname *vor dem Abschicken* auf Ihren IC-Namen!**\n\n"



            "> \U0001F97C **Leitungsebene-Anfragen**\n"

            "> Bei Beschwerden gegen Führungsebene Mitglieder ab Lieutenant+ und sonstigen Anliegen.\n\n"



            "> \U0001F97C **Führungsebene-Anfragen**\n"

            "> Bei dringenden Problemen, Fragen, individuellen Gesprächen usw.\n\n"



            "> \U0001F4DD **Beschwerde-Tickets**\n"

            "> Bei Beschwerden gegen Mitglieder des San Andreas Medical Services .\n\n"



            "> \U0001F4D1 **Titel-Anfragen**\n"

            "> Wenn sie eine Dissertation oder Habilitation ablegen wollen.\n"

            "> Anforderungen siehe: https://fivenet.modernv.net/wiki/ambulance/144/titel-erwerbung\n\n"



            "> \U0001F4D1 **Geburtsurkunden-Anfragen**\n"

            "> Dieses Ticket ist gemäß bei Verdacht auf § 3 BGB Abs. 2 zur Beglaubigung zu öffnen, sofern die Vermittlung durch das DoJ erfolgt ist.\n\n"



            "> \U0001FA79 **Behandlungs-Anfragen**\n"

            "> Sollten sie eine ambulante oder operative Behandlung wünschen, können sie hier ein Ticket eröffnen.\n\n"



            "> \U0001F501 **Wiedereinstellungs-Anfragen**\n"

            "> Wenn Sie bereits beim San Andreas Medical Services gearbeitet haben, haben Sie die Möglichkeit, eine Wiedereinstellungsanfrage zu stellen, sofern Ihre Kündigung auf eigenen Wunsch erfolgte.\n\n"



            "> \U0001F6E0 **Discord/Verwaltungs-Anfragen**\n"

            "> Sollten bei Fragen Fehler oder Verbesserungsvorschläge auftreten, kann eine Anfrage über Discord oder an die Verwaltung gestellt werden."

        ),

        color=discord.Color.blue()

    )



    view = TicketView()

    message = await channel.send(embed=embed, view=view)



    print("\U00002705 Ticket System eingerichtet!")

async def setup_reaction_roles():

    """Setup reaction role message in the specified channel"""

    channel = bot.get_channel(REACTION_ROLES)

    if not channel:

        print("\U0000274C Reaction Role Channel nicht gefunden!")

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

        print("\U00002705 Reaction Role System bereits vorhanden - kein neues Setup erforderlich!")

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

        ("\U00000031\U0000FE0F\U000020E3", "Modul 1 benötigt", 1341491722961682543),

        ("\U00000032\U0000FE0F\U000020E3", "Modul 2 benötigt", 1341491806734651514),

        ("\U00000033\U0000FE0F\U000020E3", "Modul 3 benötigt", 1341491907724972122),

        ("\U0001F3EB", "Interesse Medical Education", 1374491251482558545),

        ("\U0001F52A", "Interesse General Surgery", 1374490464119554159),

        ("\U0001F9E0", "Interesse Psychiatric", 1374491124349141002),

        ("\U0001F681", "Interesse Search and Rescue", 1374490266706120845),

        ("\U0001F6A4", "Interesse SAR-Bootsausbildung", 1374505941038530663),

        ("\U0001F6A8", "Interesse Dispatch Operations", 1377037664087183420)

    ]



    role_text = ""

    for emoji, role_name, role_id in role_info:

        role_text += f"> {emoji} `-` <@&{role_id}>\n"



    embed.add_field(name="Verfügbare Rollen:", value=role_text, inline=False)



    message = await channel.send(embed=embed)



    reactions = ["\U00000031\U0000FE0F\U000020E3", "\U00000032\U0000FE0F\U000020E3", "\U00000033\U0000FE0F\U000020E3", "\U0001F3EB", "\U0001F52A", "\U0001F9E0", "\U0001F681", "\U0001F6A4", "\U0001F6A8"]

    for reaction in reactions:

        try:

            await message.add_reaction(reaction)

        except Exception as e:

            print(f"Fehler beim Hinzufügen der Reaktion {reaction}: {e}")



    print("\U00002705 Reaction Role System eingerichtet!")





@bot.event

async def on_raw_reaction_add(payload):

    """Handle reaction role assignment when user adds reaction"""

    if payload.user_id == bot.user.id:

        return



    if payload.channel_id != REACTION_ROLES:

        return



    reaction_roles = {

        "\U00000031\U0000FE0F\U000020E3": 1341491722961682543,

        "\U00000032\U0000FE0F\U000020E3": 1341491806734651514,

        "\U00000033\U0000FE0F\U000020E3": 1341491907724972122,

        "\U0001F3EB": 1374491251482558545,

        "\U0001F52A": 1374490464119554159,

        "\U0001F9E0": 1374491124349141002,

        "\U0001F681": 1374490266706120845,

        "\U0001F6A4": 1374505941038530663,

        "\U0001F6A8": 1377037664087183420

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

        print(f"\U00002705 {member.name} hat die Rolle {role.name} erhalten")

    except Exception as e:

        print(f"\U0000274C Fehler beim Hinzufügen der Rolle {role.name} für {member.name}: {e}")





@bot.event

async def on_raw_reaction_remove(payload):

    """Handle reaction role removal when user removes reaction"""

    if payload.user_id == bot.user.id:

        return

    if payload.channel_id != REACTION_ROLES:

        return



    reaction_roles = {

       "\U00000031\U0000FE0F\U000020E3": 1341491722961682543,

        "\U00000032\U0000FE0F\U000020E3": 1341491806734651514,

        "\U00000033\U0000FE0F\U000020E3": 1341491907724972122,

        "\U0001F3EB": 1374491251482558545,

        "\U0001F52A": 1374490464119554159,

        "\U0001F9E0": 1374491124349141002,

        "\U0001F681": 1374490266706120845,

        "\U0001F6A4": 1374505941038530663,

        "\U0001F6A8": 1377037664087183420

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

        print(f"\U00002796 {member.name} hat die Rolle {role.name} verloren")

    except Exception as e:

        print(f"\U0000274C Fehler beim Entfernen der Rolle {role.name} für {member.name}: {e}")





class TicketView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)



    @discord.ui.button(label="Erstelle ein Ticket", style=discord.ButtonStyle.primary, emoji="\U0001F3AB", custom_id="ticket_create_button")

    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        view = TicketSelectView()

        await interaction.response.send_message("Wählen Sie den Ticket-Typ:", view=view, ephemeral=True)





class TicketSelectView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)


    @discord.ui.select(

        placeholder="Wählen Sie einen Ticket-Typ...",

        custom_id="ticket_type_select",

        options=[

            discord.SelectOption(

                label="\U0001F97C Leitungsebene-Anfragen",

                description="Bei Beschwerden gegen Führungsebene Mitglieder ab Lieutenant+ und sonstigen Anliegen",

                value="leitungsebene"

            ),

            discord.SelectOption(

                label="\U0001F97C Führungsebene-Anfragen",

                description="Bei dringenden Problemen und Fragen",

                value="fuehrungsebene"

            ),

            discord.SelectOption(

                label="\U0001F4DD Beschwerde-Tickets",

                description="Bei Beschwerden gegen Mitglieder",

                value="beschwerde"

            ),

            discord.SelectOption(

                label="\U0001F4D1 Titel-Anfragen",

                description="Für Dissertation oder Habilitation",

                value="titel"

            ),

            discord.SelectOption(

                label="\U0001F4D1 Geburtsurkunden-Anfragen",

                description="Beglaubigung von Geburtsurkunden",

                value="geburtsurkunde"

            ),

            discord.SelectOption(

                label="\U0001FA79 Behandlungs-Anfragen",

                description="Ambulante oder operative Behandlung",

                value="behandlung"

            ),

            discord.SelectOption(

                label="\U0001F501 Wiedereinstellungs-Anfragen",

                description="Wiedereinstellung nach eigener Kündigung",

                value="wiedereinstellung"

            ),

            discord.SelectOption(

                label="\U0001F6E0\U0000FE0F Discord/Verwaltungs-Anfragen",

                description="Fehler oder Verbesserungsvorschläge",

                value="discord_verwaltung"

            )

        ]

    )

    async def select_ticket_type(self, interaction: discord.Interaction, select: discord.ui.Select):

        ticket_type = select.values[0]



        if ticket_type == "geburtsurkunde":

            await create_ticket_channel(interaction, ticket_type, None)

        else:

            modal = get_ticket_modal(ticket_type)

            await interaction.response.send_modal(modal)





def get_ticket_modal(ticket_type: str):

    if ticket_type == "leitungsebene":

        return LeitungsebeneModal()

    elif ticket_type == "fuehrungsebene":

        return FuehrungsebeneModal()

    elif ticket_type == "beschwerde":

        return BeschwerdeModal()

    elif ticket_type == "titel":

        return TitelModal()

    elif ticket_type == "behandlung":

        return BehandlungModal()

    elif ticket_type == "wiedereinstellung":

        return WiedereinstellungModal()

    elif ticket_type == "discord_verwaltung":

        return DiscordVerwaltungModal()





class LeitungsebeneModal(discord.ui.Modal):

    def __init__(self):

        super().__init__(title="Leitungsebene-Anfrage")



    name_birth = discord.ui.TextInput(

        label="Name & Geburtsdatum:",

        placeholder="[Hier eintragen]",

        required=True,

        max_length=200

    )



    employer = discord.ui.TextInput(

        label="Bei welchem Arbeitgeber sind Sie beschäftigt?",

        placeholder="[Hier eintragen]",

        required=True,

        max_length=200

    )



    request = discord.ui.TextInput(

        label="Um Welches Anliegen Handelt es sich?",

        placeholder="Bitte schildern Sie Ihr Anliegen in 1 bis 2 Sätzen.",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    async def on_submit(self, interaction: discord.Interaction):

        form_data = {

            "Name & Geburtsdatum": self.name_birth.value,

            "Arbeitgeber": self.employer.value,

            "Anliegen": self.request.value

        }

        await create_ticket_channel(interaction, "leitungsebene", form_data)


class FuehrungsebeneModal(discord.ui.Modal):

    def __init__(self):

        super().__init__(title="Führungsebene-Anfrage")



    name_birth = discord.ui.TextInput(

        label="Name & Geburtsdatum:",

        placeholder="[Hier eintragen]",

        required=True,

        max_length=200

    )



    employer = discord.ui.TextInput(

        label="Bei welchem Arbeitgeber sind Sie beschäftigt?",

        placeholder="[Hier eintragen]",

        required=True,

        max_length=200

    )



    request = discord.ui.TextInput(

        label="Um Welches Anliegen Handelt es sich?",

        placeholder="Bitte schildern Sie Ihr Anliegen in 1 bis 2 Sätzen.",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    async def on_submit(self, interaction: discord.Interaction):

        form_data = {

            "Name & Geburtsdatum": self.name_birth.value,

            "Arbeitgeber": self.employer.value,

            "Anliegen": self.request.value

        }

        await create_ticket_channel(interaction, "fuehrungsebene", form_data)





class BeschwerdeModal(discord.ui.Modal):

    def __init__(self):

        super().__init__(title="Beschwerde-Ticket")



    complaint = discord.ui.TextInput(

        label="Worum geht es in Ihrer Beschwerde?",

        placeholder="Kurze Beschreibung des Vorfalls oder Problems",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    when_where = discord.ui.TextInput(

        label="Wann und wo hat sich der Vorfall ereignet?",

        placeholder="Datum, Uhrzeit, Ort oder Abteilung",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=500

    )



    persons = discord.ui.TextInput(

        label="Waren bestimmte Personen beteiligt?",

        placeholder="Optionaler Hinweis auf Mitarbeiter oder Zeugen",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=500

    )



    async def on_submit(self, interaction: discord.Interaction):

        form_data = {

            "Beschwerde": self.complaint.value,

            "Wann und wo": self.when_where.value,

            "Beteiligte Personen": self.persons.value

        }

        await create_ticket_channel(interaction, "beschwerde", form_data)





class TitelModal(discord.ui.Modal):

    def __init__(self):

        super().__init__(title="Titel-Anfrage")



    name_birth = discord.ui.TextInput(

        label="Name: & Geburtsdatum:",

        placeholder="[Hier eintragen]",

        required=True,

        max_length=200

    )



    requirements = discord.ui.TextInput(

        label="Vorraussetzungen bekannt?",

        placeholder="https://fivenet.modernv.net/wiki/ambulance/145/doktortitel",

        required=True,

        max_length=300

    )



    topic = discord.ui.TextInput(

        label="Welches Thema stellen sie sich vor?",

        placeholder="Kompliziertes Thema oder Leitfrage?",

        required=False,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    async def on_submit(self, interaction: discord.Interaction):

        form_data = {

            "Name & Geburtsdatum": self.name_birth.value,

            "Voraussetzungen": self.requirements.value,

            "Thema": self.topic.value or "Nicht angegeben"

        }

        await create_ticket_channel(interaction, "titel", form_data)



class BehandlungModal(discord.ui.Modal):

    def __init__(self):

        super().__init__(title="Behandlungs-Anfrage")



        self.complaint = discord.ui.TextInput(

            label="Name & Geburtsdatum",

            placeholder="Bitte geben Sie Ihren vollständigen Namen und Ihr Geburtsdatum ein.",

            required=True,

            style=discord.TextStyle.paragraph,

            max_length=1000

        )



        self.when_where = discord.ui.TextInput(

            label="Telefonnummer",

            placeholder="Bitte geben Sie Ihre Telefonnummer ein.",

            required=True,

            style=discord.TextStyle.paragraph,

            max_length=500

        )



        self.persons = discord.ui.TextInput(

            label="Problembeschreibung",

            placeholder="Beschreiben Sie Ihr Problem möglichst ausführlich für das ärztliche Personal.",

            required=True,

            style=discord.TextStyle.paragraph,

            max_length=500

        )

        self.add_item(self.complaint)

        self.add_item(self.when_where)

        self.add_item(self.persons)



    async def on_submit(self, interaction: discord.Interaction):

        form_data = {

            "Name & Geburtsdatum": self.complaint.value,

            "Telefonnummer": self.when_where.value,

            "Beschreibung": self.persons.value

        }

        await create_ticket_channel(interaction, "behandlung", form_data)





class WiedereinstellungModal(discord.ui.Modal):

    def __init__(self):

        super().__init__(title="Wiedereinstellungs-Anfrage")



    name = discord.ui.TextInput(

        label="Name:",

        placeholder="[Hier eintragen]",

        required=True,

        max_length=200

    )



    birth = discord.ui.TextInput(

        label="Geburtsdatum:",

        placeholder="[Hier eintragen]",

        required=True,

        max_length=200

    )



    rank = discord.ui.TextInput(

        label="Welchen Rang bekleideten Sie:",

        placeholder="Welchen Rang bekleideten Sie zum Zeitpunkt Ihrer Kündigung?",

        required=True,

        max_length=200

    )



    async def on_submit(self, interaction: discord.Interaction):

        form_data = {

            "Name": self.name.value,

            "Geburtsdatum": self.birth.value,

            "Vorheriger Rang": self.rank.value

        }

        await create_ticket_channel(interaction, "wiedereinstellung", form_data)





class DiscordVerwaltungModal(discord.ui.Modal):

    def __init__(self):

        super().__init__(title="Discord/Verwaltungs-Anfrage")



    anliegen = discord.ui.TextInput(

        label="Anliegen:",

        placeholder="[Hier eintragen]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    suggestions = discord.ui.TextInput(

        label="Vorschläge/Verbesserungen:",

        placeholder="[Hier eintragen]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    errors = discord.ui.TextInput(

        label="Fehlermeldungen:",

        placeholder="[Hier eintragen]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    async def on_submit(self, interaction: discord.Interaction):

        form_data = {

            "Anliegen": self.anliegen.value,

            "Vorschläge/Verbesserungen": self.suggestions.value,

            "Fehlermeldungen": self.errors.value

        }

        await create_ticket_channel(interaction, "discord_verwaltung", form_data)





async def create_ticket_channel(interaction: discord.Interaction, ticket_type: str, form_data: dict = None):

    """Create a ticket channel with proper permissions"""

    try:

        await interaction.response.defer(ephemeral=True)



        ticket_config = TICKET_CATEGORIES[ticket_type]

        category = bot.get_channel(ticket_config["category_id"])



        if not category:

            await interaction.followup.send("\U0000274C Ticket-Kategorie nicht gefunden!", ephemeral=True)

            return



        ticket_type_names = {

            "leitungsebene": "leitungsebene",

            "fuehrungsebene": "fuehrungsebene",

            "beschwerde": "beschwerde",

            "titel": "titel",

            "geburtsurkunde": "geburtsurkunde",

            "behandlung": "behandlung",

            "wiedereinstellung": "wiedereinstellung",

            "discord_verwaltung": "discord-verwaltung",

            "befoerderungs_antrag": "befoerderungs-antrag",

            "kuendigungs_antrag": "kuendigungs-antrag",

            "medical_education_bewerbung": "med-bewerbung",

            "general_surgery_bewerbung": "gs-bewerbung",

            "psychiatric_bewerbung": "psy-bewerbung",

            "sar_bewerbung": "sar-bewerbung",

            "bewerbung": "bewerbung"

        }


        ticket_type_name = ticket_type_names.get(ticket_type, ticket_type)

        ticket_counter = len([ch for ch in category.channels if ch.name.startswith(f"{ticket_type_name}-{interaction.user.name}")]) + 1

        channel_name = f"{ticket_type_name}-{interaction.user.name}-{ticket_counter}"



        overwrites = {

            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),

            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),

            bot.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)

        }

        for role_id in ticket_config["allowed_roles"]:

            role = interaction.guild.get_role(role_id)

            if role:

                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)





        ticket_channel = await category.create_text_channel(

            name=channel_name,

            overwrites=overwrites,

            reason=f"Ticket erstellt von {interaction.user}"

        )



        if not hasattr(bot, 'ticket_channels'):

            bot.ticket_channels = {}

        bot.ticket_channels[ticket_channel.id] = {

            'type': ticket_type,

            'creator': interaction.user.id,

            'created_at': discord.utils.utcnow(),

            'transcript_messages': []

        }



        if ticket_type == "geburtsurkunde":

            content = (

                "> Lieber Bürger,\n"

                "> das vorliegende Ticket wurde ausschließlich bei Verdacht gemäß § 3 BGB Abs. 2 eröffnet. Die Bearbeitung erfolgt nur dann, wenn die Vermittlung durch das Department of Justice (DoJ) mittels Nachweis (via FiveNet per Dokument) erfolgt ist.\n"

                "> \n"

                "> Bitte beachten Sie:\n"

                "> \n"

                "> • Für die Prüfung ist zwingend das entsprechende Dokument (DOC) erforderlich.\n"

                "> • Dieses Dokument muss im FiveNet hinterlegt sein und ist hier im Ticket durch einen direkten Link zu verknüpfen.\n"

                "> • Ohne gültige Verlinkung + dem Nachweis des DoJ, kann das Ticket nicht weiterbearbeitet werden und wird ohne Begründung geschlossen.\n"

                "> \n"

                "> Für Rückfragen stehen wir Ihnen selbstverständlich gerne zur Verfügung.\n"

                "> \n"

                "> Ihr Ocean Medical Center\n"

                "> San Andreas Medical Services."

            )

            await ticket_channel.send(f"{interaction.user.mention}\n\n{content}")



        elif ticket_type == "titel":

            await ticket_channel.send(

                f"{interaction.user.mention}\n\n"

                "Danke für ihre Anfrage.\n"

                "Stellen sie sicher das sie die Vorraussetzungen gelesen und verstanden haben!\n\n"

                "https://fivenet.modernv.net/wiki/ambulance/144/titel-erwerbung\n\n"

                "https://fivenet.modernv.net/wiki/ambulance/145/doktortitel"

            )



            if form_data:

                embed = discord.Embed(title="Titel-Anfrage Details", color=discord.Color.blue())

                for key, value in form_data.items():

                    embed.add_field(name=key, value=value, inline=False)

                await ticket_channel.send(embed=embed)



        elif ticket_type == "discord_verwaltung":

            await ticket_channel.send(

                f"{interaction.user.mention}\n\n"

                "Vielen Dank für das Erstellen dieses Discord-Verwaltungstickets. "

                "Bitte habe etwas Geduld, die Discord-Verwaltung wird sich in Kürze bei dir melden und dir eine Rückmeldung geben."

            )



            role_mentions = []

            for role_id in ticket_config["allowed_roles"]:

                role = interaction.guild.get_role(role_id)

                if role:

                    role_mentions.append(role.mention)



            if role_mentions:

                await ticket_channel.send(" ".join(role_mentions))



            if form_data:

                embed = discord.Embed(title="Discord/Verwaltungs-Anfrage Details", color=discord.Color.blue())

                for key, value in form_data.items():

                    embed.add_field(name=key, value=value, inline=False)

                await ticket_channel.send(embed=embed)



        elif ticket_type == "bewerbung":

            await ticket_channel.send(f"{interaction.user.mention}")



            if form_data:

                embed = discord.Embed(title="Bewerbungsdetails", color=discord.Color.blue())

                for key, value in form_data.items():

                    embed.add_field(name=key, value=value, inline=False)

                await ticket_channel.send(embed=embed)



        else:

            await ticket_channel.send(f"{interaction.user.mention}")



            if form_data:

                embed = discord.Embed(title=f"{ticket_type.title()}-Ticket Details", color=discord.Color.blue())

                for key, value in form_data.items():

                    embed.add_field(name=key, value=value, inline=False)

                await ticket_channel.send(embed=embed)



        close_view = get_ticket_close_view(ticket_type)

        await ticket_channel.send("**Ticket-Verwaltung**", view=close_view)



        await interaction.followup.send(f"\U00002705 Ticket erstellt: {ticket_channel.mention}", ephemeral=True)



    except Exception as e:

        print(f"\U0000274C Fehler beim Erstellen des Tickets: {e}")

        await interaction.followup.send("\U0000274C Fehler beim Erstellen des Tickets!", ephemeral=True)





class LeitungsebeneCloseView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        self.ticket_type = "leitungsebene"



    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.danger, emoji="\U0001F512", custom_id="close_leitungsebene")

    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        ticket_config = TICKET_CATEGORIES[self.ticket_type]

        user_roles = [role.id for role in interaction.user.roles]



        if not any(role_id in user_roles for role_id in ticket_config["allowed_roles"]):

            await interaction.response.send_message("\U0000274C Sie haben keine Berechtigung, dieses Ticket zu schließen!", ephemeral=True)

            return



        confirm_view = TicketCloseConfirmView()

        await interaction.response.send_message("Sind Sie sicher, dass Sie dieses Ticket schließen möchten?", view=confirm_view, ephemeral=True)

class FuehrungsebeneCloseView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        self.ticket_type = "fuehrungsebene"



    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.danger, emoji="\U0001F512", custom_id="close_fuehrungsebene")

    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        ticket_config = TICKET_CATEGORIES[self.ticket_type]

        user_roles = [role.id for role in interaction.user.roles]



        if not any(role_id in user_roles for role_id in ticket_config["allowed_roles"]):

            await interaction.response.send_message("\U0000274C Sie haben keine Berechtigung, dieses Ticket zu schließen!", ephemeral=True)

            return



        confirm_view = TicketCloseConfirmView()

        await interaction.response.send_message("Sind Sie sicher, dass Sie dieses Ticket schließen möchten?", view=confirm_view, ephemeral=True)



class BeschwerdeCloseView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        self.ticket_type = "beschwerde"



    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.danger, emoji="\U0001F512", custom_id="close_beschwerde")

    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        ticket_config = TICKET_CATEGORIES[self.ticket_type]

        user_roles = [role.id for role in interaction.user.roles]



        if not any(role_id in user_roles for role_id in ticket_config["allowed_roles"]):

            await interaction.response.send_message("\U0000274C Sie haben keine Berechtigung, dieses Ticket zu schließen!", ephemeral=True)

            return



        confirm_view = TicketCloseConfirmView()

        await interaction.response.send_message("Sind Sie sicher, dass Sie dieses Ticket schließen möchten?", view=confirm_view, ephemeral=True)



class TitelCloseView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        self.ticket_type = "titel"



    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.danger, emoji="\U0001F512", custom_id="close_titel")

    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        ticket_config = TICKET_CATEGORIES[self.ticket_type]

        user_roles = [role.id for role in interaction.user.roles]



        if not any(role_id in user_roles for role_id in ticket_config["allowed_roles"]):

            await interaction.response.send_message("\U0000274C Sie haben keine Berechtigung, dieses Ticket zu schließen!", ephemeral=True)

            return



        confirm_view = TicketCloseConfirmView()

        await interaction.response.send_message("Sind Sie sicher, dass Sie dieses Ticket schließen möchten?", view=confirm_view, ephemeral=True)



class GeburtsurkundeCloseView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        self.ticket_type = "geburtsurkunde"



    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.danger, emoji="\U0001F512", custom_id="close_geburtsurkunde")

    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        ticket_config = TICKET_CATEGORIES[self.ticket_type]

        user_roles = [role.id for role in interaction.user.roles]



        if not any(role_id in user_roles for role_id in ticket_config["allowed_roles"]):

            await interaction.response.send_message("\U0000274C Sie haben keine Berechtigung, dieses Ticket zu schließen!", ephemeral=True)

            return



        confirm_view = TicketCloseConfirmView()

        await interaction.response.send_message("Sind Sie sicher, dass Sie dieses Ticket schließen möchten?", view=confirm_view, ephemeral=True)



class BehandlungCloseView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        self.ticket_type = "behandlung"

    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.danger, emoji="\U0001F512", custom_id="close_behandlung")

    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        ticket_config = TICKET_CATEGORIES[self.ticket_type]

        user_roles = [role.id for role in interaction.user.roles]



        if not any(role_id in user_roles for role_id in ticket_config["allowed_roles"]):

            await interaction.response.send_message("\U0000274C Sie haben keine Berechtigung, dieses Ticket zu schließen!", ephemeral=True)

            return



        confirm_view = TicketCloseConfirmView()

        await interaction.response.send_message("Sind Sie sicher, dass Sie dieses Ticket schließen möchten?", view=confirm_view, ephemeral=True)


class WiedereinstellungCloseView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        self.ticket_type = "wiedereinstellung"



    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.danger, emoji="\U0001F512", custom_id="close_wiedereinstellung")

    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        ticket_config = TICKET_CATEGORIES[self.ticket_type]

        user_roles = [role.id for role in interaction.user.roles]



        if not any(role_id in user_roles for role_id in ticket_config["allowed_roles"]):

            await interaction.response.send_message("\U0000274C Sie haben keine Berechtigung, dieses Ticket zu schließen!", ephemeral=True)

            return



        confirm_view = TicketCloseConfirmView()

        await interaction.response.send_message("Sind Sie sicher, dass Sie dieses Ticket schließen möchten?", view=confirm_view, ephemeral=True)



class DiscordVerwaltungCloseView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        self.ticket_type = "discord_verwaltung"



    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.danger, emoji="\U0001F512", custom_id="close_discord_verwaltung")

    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        ticket_config = TICKET_CATEGORIES[self.ticket_type]

        user_roles = [role.id for role in interaction.user.roles]



        if not any(role_id in user_roles for role_id in ticket_config["allowed_roles"]):

            await interaction.response.send_message("\U0000274C Sie haben keine Berechtigung, dieses Ticket zu schließen!", ephemeral=True)

            return



        confirm_view = TicketCloseConfirmView()

        await interaction.response.send_message("Sind Sie sicher, dass Sie dieses Ticket schließen möchten?", view=confirm_view, ephemeral=True)



class PromotionCloseView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        self.ticket_type = "befoerderungs_antrag"



    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.danger, emoji="\U0001F512", custom_id="close_befoerderungs_antrag")

    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        allowed_roles = [993615970390261770, 943241957654814790, 1367220175744798721, 1097205524690374716, 1165771712441364651, 906845737281810443]

        user_roles = [role.id for role in interaction.user.roles]



        if not any(role_id in user_roles for role_id in allowed_roles):

            await interaction.response.send_message("\U0000274C Sie haben keine Berechtigung, dieses Ticket zu schließen!", ephemeral=True)

            return



        confirm_view = TicketCloseConfirmView()

        await interaction.response.send_message("Sind Sie sicher, dass Sie dieses Ticket schließen möchten?", view=confirm_view, ephemeral=True)



class ResignationCloseView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        self.ticket_type = "kuendigungs_antrag"



    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.danger, emoji="\U0001F512", custom_id="close_kuendigungs_antrag")

    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        allowed_roles = [993615970390261770, 943241957654814790, 1367220175744798721, 1097205524690374716, 1165771712441364651, 906845737281810443]

        user_roles = [role.id for role in interaction.user.roles]



        if not any(role_id in user_roles for role_id in allowed_roles):

            await interaction.response.send_message("\U0000274C Sie haben keine Berechtigung, dieses Ticket zu schließen!", ephemeral=True)

            return



        confirm_view = TicketCloseConfirmView()

        await interaction.response.send_message("Sind Sie sicher, dass Sie dieses Ticket schließen möchten?", view=confirm_view, ephemeral=True)



def get_ticket_close_view(ticket_type: str):

    views = {

        "leitungsebene": LeitungsebeneCloseView(),

        "fuehrungsebene": FuehrungsebeneCloseView(),

        "beschwerde": BeschwerdeCloseView(),

        "titel": TitelCloseView(),

        "geburtsurkunde": GeburtsurkundeCloseView(),

        "behandlung": BehandlungCloseView(),

        "wiedereinstellung": WiedereinstellungCloseView(),

        "discord_verwaltung": DiscordVerwaltungCloseView(),

        "befoerderungs_antrag": PromotionCloseView(),

        "kuendigungs_antrag": ResignationCloseView(),

        "medical_education_bewerbung": MedicalEducationCloseView(),

        "general_surgery_bewerbung": GeneralSurgeryCloseView(),

        "psychiatric_bewerbung": PsychiatricCloseView(),

        "sar_bewerbung": SarCloseView(),

        "bewerbung": ApplicationCloseView()

    }

    return views.get(ticket_type, LeitungsebeneCloseView())

class TicketCloseReasonModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Ticket schließen")

    reason = discord.ui.TextInput(
        label="Grund für das Schließen:",
        placeholder="Geben Sie einen Grund für das Schließen des Tickets an...",
        required=True,
        style=discord.TextStyle.paragraph,
        max_length=1000
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_message("\U0001F512 Ticket wird geschlossen...", ephemeral=True)

            await close_ticket_with_reason(interaction.channel, interaction.user, self.reason.value)

            await asyncio.sleep(3)
            await interaction.channel.delete(reason=f"Ticket geschlossen von {interaction.user}")
        except Exception as e:
            print(f"Fehler beim Schließen des Tickets: {e}")

class TicketCloseConfirmView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ja, schließen", style=discord.ButtonStyle.danger, custom_id="ticket_confirm_close")
    async def confirm_close(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = TicketCloseReasonModal()
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Abbrechen", style=discord.ButtonStyle.secondary, custom_id="ticket_cancel_close")
    async def cancel_close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("\U0000274C Vorgang abgebrochen.", ephemeral=True)





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





class PromotionResignationView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)



    @discord.ui.button(label="\U0001F7E9 Beförderungs-Antrag", style=discord.ButtonStyle.success, custom_id="promotion_request")

    async def promotion_request(self, interaction: discord.Interaction, button: discord.ui.Button):

        modal = PromotionRequestModal()

        await interaction.response.send_modal(modal)



    @discord.ui.button(label="\U0001F7E5 Kündigungs-Antrag", style=discord.ButtonStyle.danger, custom_id="resignation_request")

    async def resignation_request(self, interaction: discord.Interaction, button: discord.ui.Button):

        modal = ResignationRequestModal()

        await interaction.response.send_modal(modal)





class PromotionRequestModal(discord.ui.Modal):

    def __init__(self):

        super().__init__(title="Beförderungs-Antrag")



    name_birth = discord.ui.TextInput(

        label="Name, Geburtsdatum:",

        placeholder="[Hier eintragen]",

        required=True,

        max_length=200

    )



    employment_start = discord.ui.TextInput(

        label="Seit wann sind Sie beim SAMS angestellt:",

        placeholder="[Hier eintragen]",

        required=True,

        max_length=200

    )



    last_promotion = discord.ui.TextInput(

        label="Wann war ihre letzte Beförderung:",

        placeholder="[Hier eintragen]",

        required=True,

        max_length=200

    )



    negative_remarks = discord.ui.TextInput(

        label="Welche negativen Vermerke haben Sie?",

        placeholder="[Hier eintragen]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    service_time = discord.ui.TextInput(

        label="Dienstzeit seit letzter Beförderung:",

        placeholder="[Hier eintragen]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    async def on_submit(self, interaction: discord.Interaction):

        form_data = {

            "Name, Geburtsdatum": self.name_birth.value,

            "Seit wann beim SAMS angestellt": self.employment_start.value,

            "Letzte Beförderung": self.last_promotion.value,

            "Negative Vermerke": self.negative_remarks.value,

            "Dienstzeit seit letzter Beförderung": self.service_time.value

        }

        await create_ticket_channel(interaction, "befoerderungs_antrag", form_data)



class ResignationRequestModal(discord.ui.Modal):

    def __init__(self):

        super().__init__(title="Kündigungs-Antrag")



    name = discord.ui.TextInput(

        label="Name:",

        placeholder="[Hier eintragen]",

        required=True,

        max_length=200

    )



    birth_date = discord.ui.TextInput(

        label="Geburtsdatum:",

        placeholder="[Hier eintragen]",

        required=True,

        max_length=200

    )



    employment_start = discord.ui.TextInput(

        label="Seit wann sind Sie beim SAMS angestellt:",

        placeholder="[Hier eintragen]",

        required=True,

        max_length=200

    )


    resignation_reason = discord.ui.TextInput(

        label="Wieso möchten Sie beim SAMS Kündigen:",

        placeholder="[Hier eintragen]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    async def on_submit(self, interaction: discord.Interaction):

        form_data = {

            "Name": self.name.value,

            "Geburtsdatum": self.birth_date.value,

            "Seit wann beim SAMS angestellt": self.employment_start.value,

            "Kündigungsgrund": self.resignation_reason.value

        }

        await create_ticket_channel(interaction, "kuendigungs_antrag", form_data)





async def setup_promotion_resignation_system():

    """Setup promotion/resignation system message in the specified channel"""

    channel = bot.get_channel(PROMOTION_RESIGNATION_CHANNEL_ID)

    if not channel:

        print("\U0000274C Promotion/Resignation Channel nicht gefunden!")

        return



    existing_message = None

    try:

        async for message in channel.history(limit=100):

            if (message.author == bot.user and
                message.embeds and
                message.embeds[0].title == "Erstelle einen Beförderungs/Kündigungs-Antrag"):

                existing_message = message

                break

    except Exception as e:

        print(f"Fehler beim Überprüfen vorhandener Promotion/Resignation-Nachrichten: {e}")



    if existing_message:

        print("\U00002705 Promotion/Resignation System bereits vorhanden - kein neues Setup erforderlich!")

        return



    embed = discord.Embed(

        title="Erstelle einen Beförderungs/Kündigungs-Antrag",

        description=(

            "**\U0001F7E9 Beförderungs-Antrag**\n"

            "Reiche einen Beförderungs-Antrag ein.\n\n"

            "**\U0001F7E5 Kündigungs-Antrag**\n"

            "Reiche einen Kündigungs-Antrag ein."

        ),

        color=discord.Color.blue()

    )



    view = PromotionResignationView()

    message = await channel.send(embed=embed, view=view)



    print("\U00002705 Promotion/Resignation System eingerichtet!")





class DepartmentApplicationView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)



    @discord.ui.button(label="Erstelle eine Abteilungs-Bewerbung", style=discord.ButtonStyle.primary, emoji="\U0001F3E5", custom_id="department_application_button")

    async def create_department_application(self, interaction: discord.Interaction, button: discord.ui.Button):

        view = DepartmentSelectView()

        await interaction.response.send_message("Wählen Sie die Abteilung:", view=view, ephemeral=True)





class DepartmentSelectView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)



    @discord.ui.select(

        placeholder="Wählen Sie eine Abteilung...",

        custom_id="department_select",

        options=[

            discord.SelectOption(

                label="\U0001F3EB Medical Education – Bewerbung",

                description="Bewerbung für das Medical Education Department",

                value="medical_education_bewerbung"

            ),

            discord.SelectOption(

                label="\U0001F52A General Surgery – Bewerbung",

                description="Bewerbung für die General Surgery",

                value="general_surgery_bewerbung"

            ),

            discord.SelectOption(

                label="\U0001F9E0 Psychiatric Department – Bewerbung",

                description="Bewerbung für das Psychiatric Department",

                value="psychiatric_bewerbung"

            ),

            discord.SelectOption(

                label="\U0001F681 Search and Rescue – Bewerbung",

                description="Bewerbung für Search and Rescue",

                value="sar_bewerbung"

            )

        ]

    )

    async def select_department(self, interaction: discord.Interaction, select: discord.ui.Select):

        department_type = select.values[0]

        modal = get_department_modal(department_type)

        await interaction.response.send_modal(modal)





def get_department_modal(department_type: str):

    if department_type == "medical_education_bewerbung":

        return MedicalEducationModal()

    elif department_type == "general_surgery_bewerbung":

        return GeneralSurgeryModal()

    elif department_type == "psychiatric_bewerbung":

        return PsychiatricModal()

    elif department_type == "sar_bewerbung":

        return SarModal()





class MedicalEducationModal(discord.ui.Modal):

    def __init__(self):

        super().__init__(title="Medical Education – Bewerbung")



    name_birth_employment = discord.ui.TextInput(

        label="Name, Geburtsdatum sowie Einstellungs Datum",

        placeholder="[Hier eintragen]",

        required=True,

        max_length=500

    )



    promotion_remarks = discord.ui.TextInput(

        label="Letzte Beförderung & negative Vermerke",

        placeholder="[Hier eintragen – Datum ihrer letzen Beförderung sowie negativen Vermerke die Sie erhalten haben]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    why_join = discord.ui.TextInput(

        label="Wieso möchten Sie dem MED beitreten?",

        placeholder="[Hier eintragen]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    previous_member = discord.ui.TextInput(

        label="Waren Sie schon einmal Mitglied des MED?",

        placeholder="[Ja/Nein – bitte ggf. mit Zeitraum und Grund für das Ausscheiden angeben]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    async def on_submit(self, interaction: discord.Interaction):

        form_data = {

            "Name, Geburtsdatum sowie Einstellungs Datum": self.name_birth_employment.value,

            "Datum ihrer letzen Beförderung sowie negativen Vermerke": self.promotion_remarks.value,

            "Wieso möchten Sie dem MED beitreten?": self.why_join.value,

            "Waren Sie schon einmal Mitglied des MED?": self.previous_member.value

        }

        await create_ticket_channel(interaction, "medical_education_bewerbung", form_data)





class GeneralSurgeryModal(discord.ui.Modal):

    def __init__(self):

        super().__init__(title="General Surgery – Bewerbung")



    name_birth_employment = discord.ui.TextInput(

        label="Name, Geburtsdatum & Einstellungs Datum",

        placeholder="[Hier eintragen]",

        required=True,

        max_length=500

    )



    promotion_remarks = discord.ui.TextInput(

        label="Letzte Beförderung & negative Vermerke",

        placeholder="[Hier eintragen – Datum ihrer letzen Beförderung sowie negativen Vermerke die Sie erhalten haben]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    why_join = discord.ui.TextInput(

        label="Wieso möchten Sie der GS beitreten?",

        placeholder="[Hier eintragen]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    weekly_overview = discord.ui.TextInput(

        label="Aktuelle Wochenübersicht Dienstzeit?",

        placeholder="[Hier eintragen – z. B. in Stunden oder Schichten]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    async def on_submit(self, interaction: discord.Interaction):

        form_data = {

            "Name, Geburtsdatum sowie Einstellungs Datum": self.name_birth_employment.value,

            "Datum ihrer letzen Beförderung sowie negativen Vermerke": self.promotion_remarks.value,

            "Wieso möchten Sie der GS beitreten?": self.why_join.value,

            "Was ist Ihre aktuelle Wochenübersicht in Dienstzeit?": self.weekly_overview.value

        }

        await create_ticket_channel(interaction, "general_surgery_bewerbung", form_data)





class PsychiatricModal(discord.ui.Modal):

    def __init__(self):

        super().__init__(title="Psychiatric Department – Bewerbung")



    name_birth_employment = discord.ui.TextInput(

        label="Name, Geburtsdatum & Einstellungs Datum",

        placeholder="[Hier eintragen]",

        required=True,

        max_length=500

    )



    promotion_remarks = discord.ui.TextInput(

        label="Letzte Beförderung & negative Vermerke",

        placeholder="[Hier eintragen – Datum ihrer letzen Beförderung sowie negativen Vermerke die Sie erhalten haben]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    why_join = discord.ui.TextInput(

        label="Wieso möchten Sie der PSY beitreten?",

        placeholder="[Hier eintragen]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    weekly_overview = discord.ui.TextInput(

        label="Aktuelle Wochenübersicht Dienstzeit?",

        placeholder="[Hier eintragen – z. B. in Stunden oder Schichten]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    async def on_submit(self, interaction: discord.Interaction):

        form_data = {

            "Name, Geburtsdatum sowie Einstellungs Datum": self.name_birth_employment.value,

            "Datum ihrer letzen Beförderung sowie negativen Vermerke": self.promotion_remarks.value,

            "Wieso möchten Sie der PSY beitreten?": self.why_join.value,

            "Was ist Ihre aktuelle Wochenübersicht in Dienstzeit?": self.weekly_overview.value

        }

        await create_ticket_channel(interaction, "psychiatric_bewerbung", form_data)

class SarModal(discord.ui.Modal):

    def __init__(self):

        super().__init__(title="Search and Rescue – Bewerbung")



    name_birth_employment = discord.ui.TextInput(

        label="Name, Geburtsdatum & Einstellungs Datum",

        placeholder="[Hier eintragen]",

        required=True,

        max_length=500

    )



    promotion_remarks = discord.ui.TextInput(

        label="Letzte Beförderung & negative Vermerke",

        placeholder="[Hier eintragen – Datum ihrer letzen Beförderung sowie negativen Vermerke die Sie erhalten haben]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    previous_member = discord.ui.TextInput(

        label="Waren Sie schon einmal Mitglied der SAR?",

        placeholder="[Ja/Nein – bitte ggf. mit Zeitraum und Grund für das Ausscheiden angeben]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    weekly_overview = discord.ui.TextInput(

        label="Aktuelle Wochenübersicht Dienstzeit?",

        placeholder="[Hier eintragen – z. B. in Stunden oder Schichten]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    async def on_submit(self, interaction: discord.Interaction):

        form_data = {

            "Name, Geburtsdatum sowie Einstellungs Datum": self.name_birth_employment.value,

            "Datum ihrer letzen Beförderung sowie negativen Vermerke": self.promotion_remarks.value,

            "Waren Sie schon einmal Mitglied der SAR?": self.previous_member.value,

            "Was ist Ihre aktuelle Wochenübersicht in Dienstzeit?": self.weekly_overview.value

        }

        await create_ticket_channel(interaction, "sar_bewerbung", form_data)





class MedicalEducationCloseView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        self.ticket_type = "medical_education_bewerbung"



    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.danger, emoji="\U0001F512", custom_id="close_medical_education_bewerbung")

    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        ticket_config = TICKET_CATEGORIES[self.ticket_type]

        user_roles = [role.id for role in interaction.user.roles]



        if not any(role_id in user_roles for role_id in ticket_config["allowed_roles"]):

            await interaction.response.send_message("\U0000274C Sie haben keine Berechtigung, dieses Ticket zu schließen!", ephemeral=True)

            return



        confirm_view = TicketCloseConfirmView()

        await interaction.response.send_message("Sind Sie sicher, dass Sie dieses Ticket schließen möchten?", view=confirm_view, ephemeral=True)


class GeneralSurgeryCloseView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        self.ticket_type = "general_surgery_bewerbung"



    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.danger, emoji="\U0001F512", custom_id="close_general_surgery_bewerbung")

    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        ticket_config = TICKET_CATEGORIES[self.ticket_type]

        user_roles = [role.id for role in interaction.user.roles]



        if not any(role_id in user_roles for role_id in ticket_config["allowed_roles"]):

            await interaction.response.send_message("\U0000274C Sie haben keine Berechtigung, dieses Ticket zu schließen!", ephemeral=True)

            return



        confirm_view = TicketCloseConfirmView()

        await interaction.response.send_message("Sind Sie sicher, dass Sie dieses Ticket schließen möchten?", view=confirm_view, ephemeral=True)





class PsychiatricCloseView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        self.ticket_type = "psychiatric_bewerbung"



    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.danger, emoji="\U0001F512", custom_id="close_psychiatric_bewerbung")

    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        ticket_config = TICKET_CATEGORIES[self.ticket_type]

        user_roles = [role.id for role in interaction.user.roles]



        if not any(role_id in user_roles for role_id in ticket_config["allowed_roles"]):

            await interaction.response.send_message("\U0000274C Sie haben keine Berechtigung, dieses Ticket zu schließen!", ephemeral=True)

            return



        confirm_view = TicketCloseConfirmView()

        await interaction.response.send_message("Sind Sie sicher, dass Sie dieses Ticket schließen möchten?", view=confirm_view, ephemeral=True)





class SarCloseView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        self.ticket_type = "sar_bewerbung"



    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.danger, emoji="\U0001F512", custom_id="close_sar_bewerbung")

    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        ticket_config = TICKET_CATEGORIES[self.ticket_type]

        user_roles = [role.id for role in interaction.user.roles]



        if not any(role_id in user_roles for role_id in ticket_config["allowed_roles"]):

            await interaction.response.send_message("\U0000274C Sie haben keine Berechtigung, dieses Ticket zu schließen!", ephemeral=True)

            return



        confirm_view = TicketCloseConfirmView()

        await interaction.response.send_message("Sind Sie sicher, dass Sie dieses Ticket schließen möchten?", view=confirm_view, ephemeral=True)





async def setup_department_application_system():

    """Setup department application system message in the specified channel"""

    channel = bot.get_channel(DEPARTMENT_APPLICATION_CHANNEL_ID)

    if not channel:

        print("\U0000274C Department Application Channel nicht gefunden!")

        return



    existing_message = None

    try:

        async for message in channel.history(limit=100):

            if (message.author == bot.user and
                message.embeds and
                message.embeds[0].title == "Erstelle eine Abteilungs-Bewerbung"):

                existing_message = message

                break

    except Exception as e:

        print(f"Fehler beim Überprüfen vorhandener Department Application-Nachrichten: {e}")



    if existing_message:

        print("\U00002705 Department Application System bereits vorhanden - kein neues Setup erforderlich!")

        return



    embed = discord.Embed(

        title="Erstelle eine Abteilungs-Bewerbung",

        description=(

            "\U0001F3EB **Medical Education – Bewerbung**\n"

            "Du hast Lust, Leuten neue Dinge beizubringen und sehnst dich nach neuen Aufgaben und Zielen im San Andreas Medical Services? Dann bewirb dich hier für das Medical Education Department.\n\n"



            "\U0001F52A **General Surgery – Bewerbung**\n"

            "Du hast Interesse an operativen Eingriffen und möchtest im OP aktiv sein? Dann bewirb dich hier für die General Surgery.\n\n"



            "\U0001F9E0 **Psychiatric Department – Bewerbung**\n"

            "Du möchtest dich auf psychologische Betreuung und Gespräche spezialisieren? Dann bewirb dich hier für das Psychiatric Department.\n\n"



            "\U0001F681 **Search and Rescue – Bewerbung**\n"

            "Du willst bei Luft- und Wasserrettungseinsätzen helfen und Leben retten? Dann bewirb dich hier für die Search and Rescue."

        ),

        color=discord.Color.blue()

    )



    view = DepartmentApplicationView()

    message = await channel.send(embed=embed, view=view)



    print("\U00002705 Department Application System eingerichtet!")





class ApplicationView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)



    @discord.ui.button(label="Erstelle ein Bewerbungs-Ticket", style=discord.ButtonStyle.primary, emoji="\U0001F4DD", custom_id="application_ticket_button")

    async def create_application_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        modal = ApplicationModal()

        await interaction.response.send_modal(modal)





class ApplicationModal(discord.ui.Modal):

    def __init__(self):

        super().__init__(title="Bewerbung für das SAMS")



    name_birth_age_job = discord.ui.TextInput(

        label="IC Name, Geburtsdatum, Alter & Beruf:",

        placeholder="[Hier eintragen]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    strengths_weaknesses = discord.ui.TextInput(

        label="2 Stärken und 2 Schwächen:",

        placeholder="[Hier eintragen]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )

    medical_experience = discord.ui.TextInput(

        label="Medizinische Erfahrungen:",

        placeholder="[Hier eintragen]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    about_yourself = discord.ui.TextInput(

        label="Über sich (mind. 2 Sätze):",

        placeholder="[Hier eintragen]",

        required=True,

        style=discord.TextStyle.paragraph,

        max_length=1000

    )



    async def on_submit(self, interaction: discord.Interaction):

        form_data = {

            "IC Name, Geburtsdatum, Alter & aktueller Beruf": self.name_birth_age_job.value,

            "2 passende Stärken und Schwächen": self.strengths_weaknesses.value,

            "Erfahrungen im Medizinischen Bereich": self.medical_experience.value,

            "Ein paar Sätze über sich": self.about_yourself.value

        }

        await create_ticket_channel(interaction, "bewerbung", form_data)





class ApplicationCloseView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        self.ticket_type = "bewerbung"



    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.danger, emoji="\U0001F512", custom_id="close_bewerbung")

    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        ticket_config = TICKET_CATEGORIES[self.ticket_type]

        user_roles = [role.id for role in interaction.user.roles]



        if not any(role_id in user_roles for role_id in ticket_config["allowed_roles"]):

            await interaction.response.send_message("\U0000274C Sie haben keine Berechtigung, dieses Ticket zu schließen!", ephemeral=True)

            return



        confirm_view = TicketCloseConfirmView()

        await interaction.response.send_message("Sind Sie sicher, dass Sie dieses Ticket schließen möchten?", view=confirm_view, ephemeral=True)





async def setup_application_system():

    """Setup application system message in the specified channel"""

    channel = bot.get_channel(APPLICATION_CHANNEL_ID)

    if not channel:

        print("\U0000274C Application Channel nicht gefunden!")

        return



    existing_message = None

    try:

        async for message in channel.history(limit=100):

            if (message.author == bot.user and
                message.embeds and
                "Willkommen im Bewerbungsprozess" in message.embeds[0].title):

                existing_message = message

                break

    except Exception as e:

        print(f"Fehler beim Überprüfen vorhandener Application-Nachrichten: {e}")



    if existing_message:

        print("\U00002705 Application System bereits vorhanden - kein neues Setup erforderlich!")

        return



    embed = discord.Embed(

        title="Willkommen im Bewerbungsprozess des San Andreas Medical Services!",

        description=(

            "## Mündliche Ausbildungen finden jeden Freitag um 18 Uhr am San Andreas Medical Services bei der Postleitzahl 7011/7015 statt!\n\n"

            "Um eine **schriftliche Bewerbung** abzusenden klicken Sie unter dieser Nachricht auf das Feld des Bots.\n"

            "Es gelten folgende Richtlinien:\n\n"

            "## Richtlinien für Bewerbungen - Bewerber\n"

            "- Straffreiheit seit min. 2 Wochen\n"

            "- Kein eingetragenes Hausverbot auf dem SAMS Discord.\n"

            "- **Vor** Absenden des Tickets **spätestens** nach Erstellung muss der **Discord Nickname** auf den **IC-Namen** geändert werden.\n"

            " - Bei Nicht-Einhaltung kann das Ticket kommentarlos geschlossen werden.\n"

            "- Bei unangebrachtem Verhalten des Bewerbers schließen wir das Ticket und verhängen eine Sperrfrist von min. 1 Woche.\n"

            "- Nennen Sie min. 2 Stärken und 2 Schwächen!\n"

            "- Einzelne Wörter sind nicht aussagekräftig. Bitte schreiben Sie in vollständigen Sätzen.\n"

            "- Das Benutzen von Hilfsmitteln wie ChatGPT o. ä. ist nicht erlaubt und kann zur Ablehnung führen.\n"

            "- Rechtschreibung / Grammatik kann in Ausnahmefällen zur Ablehnung führen.\n"

            "- Sofern sich der Bewerber nicht nach **48h** meldet, nachdem er **gepingt** wurde, wird das Ticket geschlossen."

        ),

        color=discord.Color.blue()

    )



    view = ApplicationView()

    message = await channel.send(embed=embed, view=view)



    print("\U00002705 Application System eingerichtet!")





async def setup_sams_info_embed():

    """Setup SAMS info embed in the specified channel"""

    channel = bot.get_channel(SAMS_INFO_CHANNEL_ID)

    if not channel:

        print("\U0000274C SAMS Info Channel nicht gefunden!")

        return



    existing_message = None

    try:

        async for message in channel.history(limit=100):

            if (message.author == bot.user and
                message.embeds and
                "San Andreas Medical Services" in message.embeds[0].title):

                existing_message = message

                break

    except Exception as e:

        print(f"Fehler beim Überprüfen vorhandener SAMS Info-Nachrichten: {e}")



    if existing_message:

        print("\U00002705 SAMS Info Embed bereits vorhanden - kein neues Setup erforderlich!")

        return



    embed = discord.Embed(

        title="\U0001F3E5 Informationen über die San Andreas Medical Services",

        description=(

            "Wir sind die **staatliche Organisation**, wenn es um **zivile Hilfe** geht.\n"

            "Egal ob **Schießerei**, **Unfall**, **Epidemie** oder **Unterstützung** – **wir sind da**."

        ),

        color=discord.Color.blue()

    )



    embed.add_field(

        name="\U0001F4E9 **Kontakt**",

        value=(

            "\U0001F4E7 **E-Mail:** `info@sams.fivenet.ls`\n"

            "\U0001F4CD **Hauptstandort:** PLZ 7011/7015, Los Santos\n"

            "\U0001F310 **Webseite:** *SAMS Wiki*"

        ),

        inline=False

    )





    embed.add_field(

        name="\U0001F468\u200D\U00002695\ufe0f **Führungsebene**",

        value=(

            "**Office of the Chief Medical Director**\n"

            "*Verwaltung & strategische Leitung des SAMS*\n\n"

            "• Dr. Kevin S. Gordon – Chief Medical Director\n"

            "• Dr. Sam Hill – Deputy Chief Medical Director\n\n"

            "**Commissioner**\n"

            "*Verwaltung, Personalstrukturen & Organisation*\n\n"

            "• Ben Schmit – Commissioner\n\n"

            "**Spezialisierungsleitungen**\n\n"

            "• Max Wolf – Captain of Search and Rescue\n"

      "• Lea Majors – Lieutenant of Search and Rescue\n"

            "• Daniela Novan – Captain of Psychiatric Department\n"

      "• Lucy Mitsch - Lieutenant of Psychiatric Department\n"

            "• Dr. Sam Hill – Captain of General Surgery of Los Santos\n"

      "• Aktuell Unbesetzt - Lieutenant of General Surgery of Los Santos"

        ),

        inline=False

    )

    embed.add_field(

        name="\U0001F393 **Titelgremium**",

        value=(

            "*Abnahme & Prüfung von Dr.- und Prof.-Titeln*\n"

            "**Mitglieder:** Dr. Kevin S. Gordon · Prof. Dr. Fiona H. Knusper · Prof. Dr. Tobias Bergmann · Prof. Dr. Sebastian Grey · Prof. Dr. Aiden Jones"

        ),

        inline=False

    )



    embed.add_field(

        name="\U0001F4F0 **Presse & Öffentlichkeitsarbeit**",

        value=(

            "*Kommunikation mit Presse, Bürgern & externen Partnern*\n\n"

            "• Ben Schmit\n"

            "• Max Wolf"

        ),

        inline=False

    )



    embed.add_field(

        name="\U0001F4DA **Ausbildung & Bewerbung**",

        value=(

            "**Leitung:** Yannick Baum\n\n"

            "\U0001F5E3 **Mündliche Bewerbungen:**\n"

            "\U0001F4C5 Jeden **Mittwoch & Samstag um 19:30 Uhr**\n"

            "\U0001F4CD SAMS Hauptgebäude, PLZ 7011/7015 Playa Vista\n\n"

            "\U0001F4DD **Schriftliche Bewerbungen:**\n"

            "\U0001F4CC Via Ticket im [Bewerbungs-Channel](https://discord.com/channels/906650031132672010/1201487339940220928)"

        ),

        inline=False

    )



    embed.add_field(

        name="\U000026A0 **Beschwerdeverfahren**",

        value=(

            "\U0001F3AB Beschwerde Ticket eröffnen\n"

            "\U0001F4AC Direkte Ansprache im Staat möglich"

        ),

        inline=False

    )



    embed.add_field(

        name="\U0001F44D \U0001F44E**Feedback**",

        value=(

            "Feedback zu **Mitarbeitern & Organisation** im \U0001F44D \U0001F44E-feedback Channel\n"

            "*(Beschwerden bitte weiterhin über ein Ticket)*"

        ),

        inline=False

    )



    embed.add_field(

        name="\U0001F4DC **Hausordnung**",

        value=(

            "\U0001F4C4 Die aktuelle Hausordnung findest du hier:\n"

            "\U0001F517 [SAMS Hausordnung](https://fivenet.modernv.net/wiki/ambulance/147/hausordnung)"

        ),

        inline=False

    )



    try:

        await channel.send(embed=embed)

        print("\U00002705 SAMS Info Embed eingerichtet!")

    except Exception as e:

        print(f"\U0000274C Fehler beim Erstellen des SAMS Info Embeds: {e}")





version_file = "version.txt"



def load_version():

    if os.path.exists(version_file):

        with open(version_file, "r") as f:

            raw = f.read()


            clean = raw.replace("\x00", "").strip()



            parts = clean.split(".")

            if len(parts) == 3 and all(p.isdigit() for p in parts):

                return clean

            else:


                return "1.0.0"

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

            title="__SAMS Verwaltung__",

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

            title="__SAMS Verwaltung__",

            description="Sync completed!",

            color=discord.Color.green()

        )

        complete_embed.add_field(name="Zeitpunkt", value=now, inline=True)

        complete_embed.add_field(name="Neue Version", value=bot_version, inline=True)

        complete_embed.timestamp = discord.utils.utcnow()



        await channel.send(embed=complete_embed)



        await setup_sams_info_embed()



@status_log.before_loop

async def before_status_log():

    await bot.wait_until_ready()



if __name__ == '__main__':

    bot.run('MTQwNjI4MzM5MjIyNzczNzcwMQ.GJmhjO.MIxzxAUZ1q23SA2pXxggeaqQI8kpG_MWDpH3fM')
