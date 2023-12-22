import os
import discord
from discord.ext import tasks
from discord import app_commands
from server import keep_alive  # 追加
import traceback

TOKEN = os.environ['discord']

intents = discord.Intents.default()  #適当に。
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="color", description="10進数で色を設定します。")
async def test_command(interaction: discord.Interaction, color: int):
  try:
    #そのロール名が既に存在するかどうかを確認
    check_for_duplicate = discord.utils.get(interaction.guild.roles,
                                            name=str(interaction.user.id))
    if check_for_duplicate is None:  #そのロールが存在しない場合
      print("{}が存在しないため、新たにロールを作成します。".format(interaction.user.id))
      #ロールを作成する
      role = await interaction.guild.create_role(name=interaction.user.id,
                                                 colour=discord.Colour(color))
      await interaction.user.add_roles(role)
      count = len(interaction.guild.roles) - 1
      print(count)
      positions = {role: count}
      await interaction.guild.edit_role_positions(positions=positions)
      await interaction.response.send_message("色を**{}**に変更しました。".format(color))
    else:
      print("{}が存在するため、既存のロールを編集します。".format(interaction.user.id))
      await check_for_duplicate.edit(colour=color)
      count = len(interaction.guild.roles) - 1
      print(count)
      positions = {check_for_duplicate: count}
      await interaction.guild.edit_role_positions(positions=positions)
      await interaction.response.send_message("色を**{}**に変更しました。".format(color))
  except Exception as e:
    print(e)
    print(traceback.format_exc())
    await interaction.response.send_message("https://i.imgur.com/DVvMZqC.gif")


@client.event
async def on_ready():
  print("起動完了")
  await tree.sync()  #スラッシュコマンドを同期
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
