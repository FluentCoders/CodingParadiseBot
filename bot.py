import discord
import discord.utils
from discord.ext.commands import Bot
from discord.ext import commands, tasks
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

if os.name == 'nt':
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

intents = discord.Intents.all()
intents.members = True
intents.presences = True

Client = discord.Client()
client = commands.Bot(command_prefix = "!", intents = intents)
client.remove_command('help')

@client.event
async def on_ready():
	print ("Coding Paradise Bot is connected successfully!")
	print ("Username : " + client.user.name)
	print ("ID : {}".format(client.user.id))
	print ("Version : 1.0")
	print ("[LOGGED IN]")
	update_status.start()

@tasks.loop(seconds=10)
async def update_status():
	print("[i] Status Updater Task is running...")
	guild = client.get_guild(834081696915783721)
	await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{guild.member_count} members | ! | v1.0"))

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

@client.command(pass_context=True, aliases=["m_s"])
async def member_stats(ctx):
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
	embed.set_footer(text=f'Requested by {author}', icon_url=author.avatar_url)
	await ctx.send(embed = embed)
	print ("Command 'member_stats' succeed")

@client.command(pass_context = True)
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

	await ctx.send(embed=info)

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

# Pog, I am just copying basic stuff if that's ok - TrueMLGPro
# I don't wanna rewrite it xD so yeah - TrueMLGPro
# Alright I'm sharing my terminal - TrueMLGPro
# Please don't fuck up my system - TrueMLGPro
# lmao - TrueMLGPro
# You hacked me - TrueMLGPro
# We are just building a lego thing - TrueMLGPro

# now i can code ahah - andre

# Well, gonna continue copying basic stuff - TrueMLGPro

# ye same from place bot - andre

# lmao pog - TrueMLGPro
# This leveling thing looks cool - TrueMLGPro

# I'm done copying stuff - TrueMLGPro

##################RANKING SYSTEM#######################

async def update_data(users, user):
	if str(user.id) in users["members"]:
		pass
	elif user.bot:
		pass
	else:
		users["members"][str(user.id)] = {}
		users["members"][str(user.id)]["messages"] = 0
		users["members"][str(user.id)]["points"] = 0

async def add_stats(users, user, message):
	if not user.bot:
		users["members"][str(user.id)]["messages"] += message

async def level_up(users, user, channel):
	if user.bot:
		pass
	else:
		points_per_level = 20
		
		points = users["members"][str(user.id)]["points"]
		level = users["members"][str(user.id)]["level"]			# Hello there, just checking xD, alr back to hw :)
		
		level_given = int(points / points_per_level)
		
		if level == level_given:
			pass
		else:
			print("{} Leveled up {}".format(user.mention, level))
			users["members"][str(user.id)]["level"] = level_given

##################//RANKING SYSTEM//#######################

@client.event
async def on_message(ctx):
	await client.process_commands(ctx) # This is really important otherwise all the commands won't work at all if there is an on_message thingy.

	with open("users.json", 'r') as f:
		users = json.load(f)

	await update_data(users, ctx.author)
	await add_stats(users, ctx.author, ctx)
	await level_up(users, ctx.author, ctx.channel)

	with open("users.json", 'w') as f:
		json.dump(users, f)


with open("token.txt", "r") as file:
	token=file.readline()

client.run(f"{token}")
