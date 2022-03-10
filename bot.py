import discord
from discord.ext import commands, tasks
from discord.file import File
from discord import Game
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

commandPrefix = "??"

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
client.remove_command('help')

@client.event
async def on_ready():
	print ("Coding Paradise Bot is connected successfully!")
	print ("Username : " + client.user.name)
	print ("ID : {}".format(client.user.id))
	print ("Version : 1.0")
	print ("[LOGGED IN]")
	update_status.start()

@tasks.loop(seconds=1)
async def update_status():
	print("[i] Status Updater Task is running...")
	guild = client.get_guild(server_id)
	await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{guild.member_count} members | {commandPrefix} | v1.0"))
	#await client.change_presence(status=discord.Status.online, activity=discord.Streaming(type=discord.ActivityType.streaming, name=f"how I code xD", url="https://twitch.tv/truemlgprooo"))

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




###MEMBER JOIN###

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
	#await update_data(ctx.author) #calls function to check if user is in database
	#await add_stats(ctx.author) #calls function to add message count to user in database



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


@client.slash_command(
    name = "member_stats",
    description= "Command to display member count.",
    guild_ids = [925794916418859068],
)
async def member_stats_slash(ctx):
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
	print ("Command 'member_stats' succeed")

@client.slash_command(
    name = "bot_info",
    description= "Command to display informations about the bot.",
    guild_ids = [925794916418859068],
)
async def bot_info(ctx):
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
	info.set_footer(text=f'Requested by {ctx.author.mention}')

	await ctx.respond(embed=info)





@client.command(pass_context = True, aliases=["c"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
	if isinstance(amount, int):
		if amount > 1:
			await ctx.channel.purge(limit=amount)
			await ctx.send(f":white_check_mark: {amount} messages were deleted successfully!", delete_after = 5)
			print("Command 'clear' succeed")
		else:
			raise discord.ext.commands.errors.BadArgument
	else:
		raise discord.ext.commands.errors.BadArgument

@client.command(pass_context = True, aliases=["k"])
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member):
	username = user.name
	await ctx.send(f":white_check_mark: {username} was kicked successfully!")
	await discord.Member.kick(user)
	print ("Command 'kick' succeed")
	print (f"{username} was kicked!")

@client.command(pass_context = True, aliases=["b"])
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member):
	username = user.name
	await ctx.send(f":white_check_mark: {username} was banned successfully!")
	await discord.Member.ban(user)
	print ("Command 'ban' succeed")
	print (f"{username} was banned!")

@client.command(pass_context = True)
async def avatar(ctx, user: discord.Member=None):
	if user is None:
		value = random.randint(0, 0xffffff)
		embed = discord.Embed(
		colour = value
		)
		author = ctx.message.author
		pfp = author.avatar_url_as(format="png")

		embed.set_author(name="Avatar")
		embed.set_image(url=pfp)
		embed.set_footer(text=author.name)
		
		await ctx.send(embed = embed)
		return
	else:
		value = random.randint(0, 0xffffff)
		embed = discord.Embed(
		colour = value
		)
		pfp = user.avatar_url_as(format="png")

		embed.set_author(name="Avatar")
		embed.set_image(url=pfp)
		embed.set_footer(text=user.name)

		await ctx.send(embed = embed)

@client.command(pass_context = True, aliases=["u", "user"])
async def user_info(ctx, user: discord.Member=None):
	if user is None:
		author = ctx.author

		roles = [role for role in author.roles]

		embed = discord.Embed(
				colour = author.color
		)

		embed.set_author(name=f'User Info - {author}')
		embed.set_thumbnail(url=author.avatar_url)
		embed.set_footer(text=f'Requested by {author}', icon_url=author.avatar_url)

		embed.add_field(name='ID', value=author.id)
		embed.add_field(name='Guild Name', value=author.display_name)
		embed.add_field(name='Status', value=author.status)
		embed.add_field(name='Activity', value=author.activity)
		embed.add_field(name='Is on Mobile?', value=author.is_on_mobile())
		
		embed.add_field(name='Created at', value=author.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
		embed.add_field(name='Joined at', value=author.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

		embed.add_field(name=f'Roles ({len(roles)})', value=' '.join([role.mention for role in roles]))
		embed.add_field(name='Top Role', value=author.top_role.mention)

		embed.add_field(name='Bot?', value=author.bot)

		await ctx.send(embed=embed)
		return
	else:
		author = ctx.author
		roles = [role for role in user.roles]

		embed = discord.Embed(
				colour = user.color
		)

		embed.set_author(name=f'User Info - {user}')
		embed.set_thumbnail(url=user.avatar_url)
		embed.set_footer(text=f'Requested by {author}', icon_url=author.avatar_url)

		embed.add_field(name='ID', value=user.id)
		embed.add_field(name='Guild Name', value=user.display_name)
		embed.add_field(name='Status', value=user.status)
		embed.add_field(name='Activity', value=user.activity)
		embed.add_field(name='Is on Mobile?', value=user.is_on_mobile())

		embed.add_field(name='Created at', value=user.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
		embed.add_field(name='Joined at', value=user.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

		embed.add_field(name=f'Roles ({len(roles)})', value=' '.join([role.mention for role in roles]))
		embed.add_field(name='Top Role', value=user.top_role.mention)

		embed.add_field(name='Bot?', value=user.bot)

		await ctx.send(embed=embed)



@client.command(pass_context = True, aliases=["chk_rls", "c_r"])
async def check_roles(ctx):
	member_count=len([m for m in ctx.guild.members if not m.bot])
	bot_count=len([m for m in ctx.guild.members if m.bot])
	await ctx.send("Checking roles for {} members including {} bots...".format(member_count, bot_count))
	await ctx.send("It may take up to {} minutes.".format(round(((member_count*2)/60), 2)))
	for guild in client.guilds:
		for member in guild.members:
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
	print ("Command 'check_roles' succeed!")
	#rewrite


with open("token.txt", "r") as file:
	token=file.readline()

client.run(f"{token}")
