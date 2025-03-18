import discord
from discord.commands import permissions, Option
from discord.commands.context import ApplicationContext
from discord.ext import commands, tasks
from datetime import datetime
import platform
import psutil
import uptime
import datetime
import random
import time
import os
import json
import requests
import asyncio

"""
Permission Cheatsheet (by TrueMLGPro)
- For calculating an integer value for multiple role permission -
- Please refer to https://discordapi.com/permissions.html -

* = Bot owner must have 2FA enabled if the guild requires 2FA

General Permissions:
View Channels - 1024
* Manage Channels - 16
* Manage Roles - 268435456
* Manage Emojis and Stickers - 1073741824
View Audit Log - 128
View Server Insights - 524288
* Manage Webhooks - 536870912
* Manage Server - 32
Create Invite - 1
Change Nickname - 67108864
Manage Nicknames - 134217728
* Kick Members - 2
* Ban Members - 4
* Manage Events - 8589934592
* Administrator - 8

Text Permissions:
# TODO

"""

commandPrefix = "??" # Obsolete

role_os_id = 925794916469203046
role_programming_id = 925794916439818245
role_member_id = 925794916469203048
role_bot_id = 925794916469203047
server_id = 925794916418859068

if os.name == 'nt':
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

intents = discord.Intents.all()
intents.members = True
intents.presences = True

Client = discord.Client()
client = commands.Bot(command_prefix = commandPrefix, intents = intents)

@client.event
async def on_ready():
	print ("Coding Paradise Bot is connected successfully!")
	print ("Username : " + client.user.name)
	print ("ID : {}".format(client.user.id))
	print ("Version : 1.0")
	print ("[LOGGED IN]")
	update_status.start()

@tasks.loop(seconds=20)
async def update_status():
	statuses = [
        "Status 1",
        "Status 2",
        "Status 3",
        "Status 4",
        "Status 5",
        "Status 6",
    ]
	now = datetime.datetime.now()
	current_time = now.strftime("%H:%M:%S")
	print(f"[{current_time}] [i] Status Updater Task is running...")
	guild = client.get_guild(server_id)
	current_status = random.choice(statuses)
	# await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{guild.member_count} members | v1.0.1"))
	await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=current_status))

##################RANKING SYSTEM#######################

#async def update_data(user):
#    with open ("data.json", "r") as f:
#        data = json.load(f)
#    
#    if str(user.id) in data:
#        pass
#    else:
#        data[str(user.id)] = {}
#        data[str(user.id)]["messages"] = 0
#        data[str(user.id)]["points"] = 0
#    
#    with open("data.json", "w") as f:
#        json.dump(data, f)
#

#async def add_stats(user):
#	with open ("data.json", "r") as f:
#		data = json.load(f)
	
#	if not user.bot:
#		data[str(user.id)]["messages"] += 1
#	
#	with open("data.json", "w") as f:
#		json.dump(data, f)

#async def level_up(users, user, channel):
#	if user.bot:
#		pass
#	else:
#		points_per_level = 20
#		
#		points = users["members"][str(user.id)]["points"]
#		level = users["members"][str(user.id)]["level"]
#		
#		level_given = int(points / points_per_level)
#		
#		if level == level_given:
#			pass
#		else:
#			print("{} Leveled up {}".format(user.mention, level))
#			users["members"][str(user.id)]["level"] = level_given
#
##################//RANKING SYSTEM//#######################

### EVENTS ###

@client.event
async def on_member_join(member):
	role_operating_system = discord.utils.get(member.guild.roles, id=925794916469203046)
	role_programming = discord.utils.get(member.guild.roles, id=925794916439818245)
	role_member = discord.utils.get(member.guild.roles, id=925794916469203048)
	role_bot = discord.utils.get(member.guild.roles, id=925794916469203047)

	if not member.bot:
		await member.add_roles(role_operating_system)
		await member.add_roles(role_programming)
		await member.add_roles(role_member)
	else:
		await member.add_roles(role_bot)

@client.event
async def on_message(ctx):
	await client.process_commands(ctx) # This is really important otherwise all the commands won't work at all if there is an on_message thingy.
	# await update_data(ctx.author) # Calls function to check if user is in database
	# await add_stats(ctx.author) # Calls function to add message count to user in database

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed = discord.Embed(description = f'**{ctx.author.name}, this command doesn\'t exist.**', color=0xff2500))

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed = discord.Embed(description = f'**Required argument is missing.**', color=0xff2500))

    if isinstance(error, commands.BadArgument):
        await ctx.send(embed = discord.Embed(description = f'**Invalid argument.**', color=0xff2500))

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed = discord.Embed(description = f'**You have no rights to use this command.**', color=0xff2500))

    print("\n")
    print(error)
    print("\n")

### COMMANDS ###
# For permission cheatsheet, go to line 18

### Moderation Commands ###

'''
@permissions.has_any_role(*items, guild_id=None)

The method used to specify multiple application command role restrictions.
- The application command runs if the invoker has any of the specified roles.

Parameters
	- *items (Union[int, str]) – The integers or strings that represent the ids or names of the roles that the permission is tied to.
	- guild_id (int) – The integer which represents the id of the guild that the permission may be tied to.

--------

discord.InteractionResponse.send_message(content=None, *, embed=None, embeds=None,
	view=None, tts=False, ephemeral=False, allowed_mentions=None,
	file=None, files=None, delete_after=None)

This function is a coroutine.
- Responds to this interaction by sending a message.

Parameters:
	- content (Optional[str]) – The content of the message to send.
	- embeds (List[Embed]) – A list of embeds to send with the content. Maximum of 10. This cannot be mixed with the embed parameter.
	- embed (Embed) – The rich embed for the content to send. This cannot be mixed with embeds parameter.
	- tts (bool) – Indicates if the message should be sent using text-to-speech.
	- view (discord.ui.View) – The view to send with the message.
	- ephemeral (bool) – Indicates if the message should only be visible to the user who started the interaction. If a view is sent with an ephemeral message and it has no timeout set then the timeout is set to 15 minutes.
	- allowed_mentions (AllowedMentions) – Controls the mentions being processed in this message. See abc.Messageable.send() for more information.
	- delete_after (float) – If provided, the number of seconds to wait in the background before deleting the message we just sent.
	- file (File) – The file to upload.
	- files (List[File]) – A list of files to upload. Must be a maximum of 10.

Raises:
	- HTTPException – Sending the message failed.
	- TypeError – You specified both embed and embeds.
	- ValueError – The length of embeds was invalid.
	- InteractionResponded – This interaction has already been responded to before.
'''
@client.slash_command(
    name = "clear",
    description = "[Moderation] Purges a specified amount of messages",
    guild_ids = [925794916418859068]
)
@permissions.has_any_role("Chefs", "Staff")
async def clear_slash(ctx: ApplicationContext, amount: Option(int, "Enter the amount of messages to purge", required = True, min=1, max=1000, default=10)):
	if isinstance(amount, int):
		if amount > 1:
			await ctx.channel.purge(limit=amount)
			await discord.InteractionResponse.send_message(f":white_check_mark: {amount} messages were deleted successfully!", ephemeral=True, delete_after=5)
			print("Command 'clear' succeed")
		else:
			raise discord.ext.commands.errors.BadArgument
	else:
		raise discord.ext.commands.errors.BadArgument

@client.slash_command(
    name = "kick",
    description = "[Moderation] Kicks specified member",
    guild_ids = [925794916418859068]
)
@permissions.has_any_role("Chefs", "Staff")
async def kick_slash(ctx: ApplicationContext, user: Option(discord.Member, "Enter target user's name", required = True)):
	username = user.name
	await discord.Member.kick(user)
	await discord.InteractionResponse.send_message(f":white_check_mark: {username} was kicked successfully!", ephemeral=True, delete_after=10)
	print("Command 'kick' succeed")
	print(f"{username} was kicked!")

@client.slash_command(
    name = "ban",
    description = "[Moderation] Bans specified member",
    guild_ids = [925794916418859068]
)
@permissions.has_any_role("Chefs", "Staff")
async def ban_slash(ctx: ApplicationContext, user: Option(discord.Member, "Enter target user's name", required = True)):
	username = user.name
	await discord.Member.ban(user)
	await discord.InteractionResponse.send_message(f":white_check_mark: {username} was banned successfully!", ephemeral=True, delete_after=10)
	print("Command 'ban' succeed")
	print(f"{username} was banned!")

### Utility commands ###

@client.slash_command(
    name = "member_stats",
    description = "Displays the member count of this guild",
    guild_ids = [925794916418859068],
)
async def member_stats_slash(ctx: ApplicationContext):
	total_users_count = ctx.guild.member_count
	member_count = len([m for m in ctx.guild.members if not m.bot])
	bot_count = len([m for m in ctx.guild.members if m.bot])
	
	author = ctx.author
	value = random.randint(0, 0xffffff)
	embed = discord.Embed(
	colour = value
	)
	
	embed.set_author(name="Member Stats")
	embed.add_field(name="Total Users", value=total_users_count)
	embed.add_field(name="Members", value=member_count)
	embed.add_field(name="Bots", value=bot_count)
	embed.set_footer(text=f'Requested by {author}')
	await ctx.respond(embed = embed)

@client.slash_command(
    name = "bot_info",
    description = "Responds with bot usage statistics",
    guild_ids = [925794916418859068],
)
async def bot_info_slash(ctx: ApplicationContext):
	value = random.randint(0, 0xffffff)
	system = platform.system()
	architecture = platform.machine()
	release = platform.release()
	sys_version = platform.version()
	cpu_percent = psutil.cpu_percent()

	if os.name == 'nt':
		uptime_sys = uptime._uptime_windows()
	elif os.name == 'posix':
		uptime_sys = uptime._uptime_linux()

	mem_total = psutil.virtual_memory()[0]
	mem_used = psutil.virtual_memory()[3]

	info = discord.Embed(
	colour = value
	)

	info.set_author(name="Bot Statistics")
	info.add_field(name="System", value=system + " " + architecture + " " + release)
	info.add_field(name="System Version", value=sys_version)
	info.add_field(name="CPU Usage", value=str(cpu_percent) + "%")
	info.add_field(name="RAM Usage", value=str(int(mem_used / 1024 / 1024)) + "MB" + " / " + str(int(mem_total / 1024 / 1024)) + "MB")
	info.add_field(name="Uptime", value=str(datetime.timedelta(seconds=round(uptime_sys))))
	info.set_footer(text=f'Requested by {ctx.author}')

	await ctx.respond(embed=info)

@client.slash_command(
    name = "avatar",
    description = "Responds with your avatar or specified member's avatar",
    guild_ids = [925794916418859068]
)
async def avatar_slash(ctx: ApplicationContext, user: Option(discord.Member, "Enter target user's name (optional)", required = False)):
	if user is None:
		value = random.randint(0, 0xffffff)
		avatar_embed = discord.Embed(
			colour = value,
		)

		# See: https://docs.pycord.dev/en/master/api.html?highlight=interaction#discord.Interaction
		author = ctx.interaction.user
		pfp = author.avatar.url

		avatar_embed.set_author(name="Avatar")
		avatar_embed.set_image(url=pfp)
		avatar_embed.set_footer(text=author.name)
		
		await ctx.respond(embed = avatar_embed)
	else:
		value = random.randint(0, 0xffffff)
		avatar_embed = discord.Embed(
			colour = value
		)
		pfp = user.avatar.url

		avatar_embed.set_author(name="Avatar")
		avatar_embed.set_image(url=pfp)
		avatar_embed.set_footer(text=user.name)
		
		await ctx.respond(embed = avatar_embed)

@client.slash_command(
	name = "user_info",
	description = "Displays information about your or other member's account",
	guild_ids = [925794916418859068]
)
async def user_info(ctx: ApplicationContext, user: Option(discord.Member, "Enter target user's name (optional)", required = False)):
	if user is None:
		author = ctx.author
		roles = [role for role in author.roles]

		info_embed = discord.Embed(
			colour = author.color
		)

		info_embed.set_author(name=f'User Info - {author}')
		info_embed.set_thumbnail(url=author.avatar.url)
		info_embed.set_footer(text=f'Requested by {author}', icon_url=author.avatar.url)

		info_embed.add_field(name='ID', value=author.id)
		info_embed.add_field(name='Guild Name', value=author.display_name)
		info_embed.add_field(name='Status', value=author.status)
		info_embed.add_field(name='Custom Status', value=author.activity)
		info_embed.add_field(name='Is on Mobile?', value=author.is_on_mobile())
		
		info_embed.add_field(name='Created at', value=author.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
		info_embed.add_field(name='Joined at', value=author.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

		info_embed.add_field(name=f'Roles ({len(roles)})', value=' '.join([role.mention for role in roles]))
		info_embed.add_field(name='Top Role', value=author.top_role.mention)

		await ctx.respond(embed=info_embed)
	else:
		author = ctx.interaction.user
		roles = [role for role in user.roles]

		info_embed = discord.Embed(
			colour = user.color
		)

		info_embed.set_author(name=f'User Info - {user}')
		info_embed.set_thumbnail(url=user.avatar.url)
		info_embed.set_footer(text=f'Requested by {author}', icon_url=author.avatar.url)

		info_embed.add_field(name='ID', value=user.id)
		info_embed.add_field(name='Guild Name', value=user.display_name)
		info_embed.add_field(name='Status', value=user.status)
		info_embed.add_field(name='Custom Status', value=user.activity)
		info_embed.add_field(name='Is on Mobile?', value=user.is_on_mobile())

		info_embed.add_field(name='Created at', value=user.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
		info_embed.add_field(name='Joined at', value=user.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

		info_embed.add_field(name=f'Roles ({len(roles)})', value=' '.join([role.mention for role in roles]))
		info_embed.add_field(name='Top Role', value=user.top_role.mention)

		info_embed.add_field(name='Bot?', value=user.bot)

		await ctx.respond(embed = info_embed)

@client.slash_command(
	name = "check_roles",
	description = "Checks for missing roles for all the users present in the guild",
	guild_ids = [925794916418859068]
)
async def check_roles_slash(ctx: ApplicationContext):
	member_count=len([m for m in ctx.guild.members if not m.bot])
	bot_count=len([m for m in ctx.guild.members if m.bot])
	await ctx.respond("Checking roles for {} members including {} bots...".format(member_count, bot_count) + "\n" +
        ("It may take up to {} minutes.".format(round(((member_count * 2) / 60), 2))))
	
	for member in ctx.guild.members:
		roles = [role.name for role in ctx.guild.roles]
		role_operating_system = discord.utils.get(ctx.guild.roles, id=role_os_id)
		role_programming = discord.utils.get(ctx.guild.roles, id=role_programming_id)
		role_member = discord.utils.get(ctx.guild.roles, id=role_member_id)
		role_bot = discord.utils.get(ctx.guild.roles, id=role_bot_id)
		if not member.bot:
			if role_operating_system not in roles:
				await member.add_roles(role_operating_system)
			if role_programming not in roles:
				await member.add_roles(role_programming)
			if role_member not in roles:
				await member.add_roles(role_member)
		else:
			if role_bot not in roles:
				await member.add_roles(role_bot)

			if role_operating_system in roles:
				await member.remove_roles(role_operating_system)
			if role_programming in roles:
				await member.remove_roles(role_programming)
			if role_member in roles:
				await member.remove_roles(role_member)

	await ctx.send("Missing roles were added successfully!")

with open("token.txt", "r") as file:
	token=file.readline()

client.run(f"{token}")