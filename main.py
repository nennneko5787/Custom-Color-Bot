import os
import discord
from discord.ext import tasks
from discord import app_commands
from server import keep_alive  # 追加
import traceback

TOKEN = os.environ['discord']

intents = discord.Intents.default()  # 適当に。
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="color", description="16進数で色を設定します。")
async def color(interaction: discord.Interaction, hex: str):
	try:
		color = int(hex, 16)
		# そのロール名が既に存在するかどうかを確認
		check_for_duplicate = discord.utils.get(interaction.guild.roles,
		                                        name=str(interaction.user.id))
		if check_for_duplicate is None:  # そのロールが存在しない場合
			print("{}が存在しないため、新たにロールを作成します。".format(interaction.user.id))
			# ロールを作成する
			role = await interaction.guild.create_role(name=interaction.user.id,
			                                           colour=discord.Colour(color))
			await interaction.user.add_roles(role)
			count = len(interaction.guild.roles) - 1
			print(count)
			positions = {role: count}
			await interaction.guild.edit_role_positions(positions=positions)
			await interaction.response.send_message("色を**{}**に変更しました。".format(hex))
		else:
			print("{}が存在するため、既存のロールを編集します。".format(interaction.user.id))
			await check_for_duplicate.edit(colour=color)
			count = len(interaction.guild.roles) - 1
			print(count)
			positions = {check_for_duplicate: count}
			await interaction.guild.edit_role_positions(positions=positions)
			await interaction.response.send_message("色を**{}**に変更しました。".format(hex))
	except ValueError:
		await interaction.response.send_message("無効な16進数が入力されました。")
	except Exception as e:
		print(e)
		print(traceback.format_exc())
		await interaction.response.send_message("https://i.imgur.com/DVvMZqC.gif")


@tree.command(name="color_from_rgb", description="RGBで色を設定します。")
async def color_from_rgb(interaction: discord.Interaction, r: app_commands.Range[int, 255], g: app_commands.Range[int, 255], b: app_commands.Range[int, 255]):
	try:
		# そのロール名が既に存在するかどうかを確認
		check_for_duplicate = discord.utils.get(interaction.guild.roles,
		                                        name=str(interaction.user.id))
		if check_for_duplicate is None:  # そのロールが存在しない場合
			print("{}が存在しないため、新たにロールを作成します。".format(interaction.user.id))
			# ロールを作成する
			role = await interaction.guild.create_role(name=interaction.user.id,
			                                           colour=discord.Colour.from_rgb(r, g, b))
			await interaction.user.add_roles(role)
			count = len(interaction.guild.roles) - 1
			print(count)
			positions = {role: count}
			await interaction.guild.edit_role_positions(positions=positions)
			await interaction.response.send_message("色を**{},{},{}**に変更しました。".format(r, g, b))
		else:
			print("{}が存在するため、既存のロールを編集します。".format(interaction.user.id))
			await check_for_duplicate.edit(colour=color)
			count = len(interaction.guild.roles) - 1
			print(count)
			positions = {check_for_duplicate: count}
			await interaction.guild.edit_role_positions(positions=positions)
			await interaction.response.send_message("色を**{},{},{}**に変更しました。".format(r, g, b))
	except Exception as e:
		print(e)
		print(traceback.format_exc())
		await interaction.response.send_message("https://i.imgur.com/DVvMZqC.gif")


@tree.command(name="delete", description="色の設定を削除します。")
async def color(interaction: discord.Interaction):
	try:
		# そのロール名が既に存在するかどうかを確認
		check_for_duplicate = discord.utils.get(interaction.guild.roles,
		                                        name=str(interaction.user.id))
		if check_for_duplicate is not None:
			await check_for_duplicate.delete()
			await interaction.response.send_message("色の設定を削除しました。")
		else:
			await interaction.response.send_message("色の設定が存在しません。", ephemeral=True)
	except Exception as e:
		print(e)
		print(traceback.format_exc())
		await interaction.response.send_message("https://i.imgur.com/DVvMZqC.gif")


@client.event
async def on_ready():
	print("起動完了")
	await tree.sync()  # スラッシュコマンドを同期
	myLoop.start()


@tasks.loop(seconds=20)  # repeat after every 10 seconds
async def myLoop():
	# work
	await client.change_presence(activity=discord.Game(
		name="{} Servers / Program by nennneko5787 / Server by render.com".
		format(len(client.guilds))))


keep_alive()
try:
	client.run(TOKEN)
except:
	os.system("kill 1")
