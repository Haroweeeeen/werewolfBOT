import discordddd
from discord import app_commands
import json
import random
from flask import Flask
from threading import Thread
import os
import datetime
import time
import asyncio
import itertools
app = Flask('')
@app.route('/')
def hello_world():
    return 'Hello, World!'
@app.route('/')
def main():
    return 'Bot is aLive!'
def run():
    app.run(host="0.0.0.0", port=8080)
def keep_alive():
    server = Thread(target=run)
    server.start()

intents = discord.Intents.default()#適当に。
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print("起動完了")
    await tree.sync()#スラッシュコマンドを同期

@client.event
async def on_message(message):
    if message.author.bot:
        return

        await channel.send("時間ではないが、答えを聞こう\n追放する人に投票してください。\nスキップに入れると夜になり、人狼がキルします。")
        await this.discussionTime(channel)
        return
    for i in nowbjs:
        if (not message.author in i.aliveMembers):
            message.delete()

nowbjs = []
nowkinos = []
def nowPlayingGamble(user):
    for bj in nowbjs:
        if (user in bj.players.keys()):
            return True
roles = {
    "somura":"村人",
    "werewolf":"人狼",
    "uranai":"村人",
    "jester":"第三陣営",
    "madder":"村人",#クルー判定だけどwolf陣営
    "defender":"村人"#守る人

}
rolejapanese = {
    "somura":"素村",
    "werewolf":"人狼",
    "uranai":"占い師",
    "jester":"てるてる",
    "madder":"マッドメイト",#クルー判定だけどwolf陣営
    "defender":"守護者"#守る人

}
haiyakus = {#人数:{RoleName}
        1:["werewolf","uranai","madder","defender","jester"],
        2:["werewolf"],
        3:["werewolf"],
        4:["werewolf"],
        5:["werewolf","uranai","jester"],
        6:["werewolf","uranai"],
        7:["werewolf","uranai","defender"],
        8:["werewolf","werewolf","uranai","defender","madder"],
        9:["werewolf","werewolf","uranai","defender","madder"],
        10:["werewolf","werewolf","uranai","defender","madder","jester"],
    }
class Game:
    class SelectButton(discord.ui.Button):
        def __init__(self,txt:str,style,bj):
            super().__init__(label=txt,style=style)
            self.bj = bj
        async def callback(self, interaction: discord.Interaction):
            if (self.bj.commandSelecting == False): return
            if (self.label == "参加する"):
                this = self.bj
                if (not interaction.user in this.poll.joinMembers):
                    await this.poll.joinmember(interaction.user)
                    await interaction.response.send_message(f'<@{interaction.user.id}>が参加しました')
                else:await interaction.response.send_message(f'既に参加しています。',ephemeral=True)
            elif (self.label == "抜ける"):
                this = self.bj
                if (interaction.user in this.poll.joinMembers):
                    await this.poll.outmember(interaction.user)
                    await interaction.response.send_message(f'<@{interaction.user.id}>が抜けました')
                else:await interaction.response.send_message(f'既に参加しています。',ephemeral=True)
            elif (self.label == "メンバー決定"):
                this = self.bj
                if (len(this.poll.joinMembers) > 0):
                    this.commandSelecting = False
                    await interaction.response.send_message("では、開始します。")
                    await this.startGame(interaction.channel)
            if (self.bj.discussion):
                if (self.label == "スキップ"):
                        if (interaction.user in self.bj.votedPlayer):
                            await interaction.response.send_message(embed=discord.Embed(title=f"既に投票しています。"),ephemeral=True)    
                            return
                        if (not interaction.user in list(self.bj.players.keys())):
                            await interaction.response.send_message(embed=discord.Embed(title=f"お前そもそも参加してないやろ殺すぞ",),ephemeral=True)    
                            return
                        if (not interaction.user in self.bj.aliveMembers):
                            await interaction.response.send_message(embed=discord.Embed(title=f"死者は投票はできません"),ephemeral=True)    
                            return
                        self.bj.isVotedUser["skip"] = self.bj.isVotedUser["skip"] + 1
                        self.bj.votedPlayer.append(interaction.user)
                        await interaction.response.send_message(embed=discord.Embed(title=f"スキップしました"),ephemeral=True)
                        if (len(self.bj.votedPlayer) == len(self.bj.aliveMembers)): await self.bj.eject(interaction.channel)
                for i in self.bj.aliveMembers:
                    if (self.label == i.name):
                        if (interaction.user in self.bj.votedPlayer):
                            await interaction.response.send_message(embed=discord.Embed(title=f"既に投票しています。",),ephemeral=True) 
                            return
                        if (not interaction.user in list(self.bj.players.keys())):
                            await interaction.response.send_message(embed=discord.Embed(title=f"お前そもそも参加してないやろ殺すぞ",),ephemeral=True)    
                            return
                        if (not interaction.user in self.bj.aliveMembers):
                            await interaction.response.send_message(embed=discord.Embed(title=f"死者は投票はできません"),ephemeral=True)    
                            return
                        self.bj.isVotedUser[i.id] = self.bj.isVotedUser[i.id] + 1
                        self.bj.votedPlayer.append(interaction.user)
                        await interaction.response.send_message(embed=discord.Embed(title="投票しました",description=f"<@{i.id}>に投票しました",),ephemeral=True)
                        if (len(self.bj.votedPlayer) == len(self.bj.aliveMembers)):await self.bj.eject(interaction.channel)

                
    class SelectButtons(discord.ui.View):
        def __init__(self,buttontxtcolorlist,bj):#,discord.ButtonStyle.red
            super().__init__()
            for i in buttontxtcolorlist:
                self.add_item(Game.SelectButton(i[0],i[1],bj))
    class Poll:
        def __init__(this,user:discord.User,channel,message):
            this.maker = user
            this.message = message
            this.joinMembers = []
        async def outmember(this,member):
            if (member in this.joinMembers):
                this.joinMembers.remove(member)
            joinmemberstring = ""
            for i in this.joinMembers:
                joinmemberstring += "<@" + str(i.id) + ">\n"
            newembed = discord.Embed(title="人狼のメンバー募集", description="")
            newembed.add_field(name="・参加メンバー",value=joinmemberstring)
            await this.message.edit(embed=newembed)
            
        async def joinmember(this,member):
            if (member in this.joinMembers): return
            else: this.joinMembers.append(member)
            joinmemberstring = ""
            for i in this.joinMembers:
                joinmemberstring += "<@" + str(i.id) + ">\n"
            newembed = discord.Embed(title="人狼のメンバー募集", description="")
            newembed.add_field(name="・参加メンバー",value=joinmemberstring)
            await this.message.edit(embed=newembed)
    class VotePoll:
        def __init__(this,user:discord.User,channel,message):
            this.maker = user
            this.message = message
            this.members = []
        async def outmember(this,member):
            if (member in this.joinMembers):
                this.joinMembers.remove(member)
            joinmemberstring = ""
            for i in this.joinMembers:
                joinmemberstring += "<@" + str(i.id) + ">\n"
            newembed = discord.Embed(title="人狼のメンバー募集", description="")
            newembed.add_field(name="・参加メンバー",value=joinmemberstring)
            await this.message.edit(embed=newembed)
            
        async def joinmember(this,member):
            if (member in this.joinMembers): return
            else: this.joinMembers.append(member)
            joinmemberstring = ""
            for i in this.joinMembers:
                joinmemberstring += "<@" + str(i.id) + ">\n"
            newembed = discord.Embed(title="人狼のメンバー募集", description="")
            newembed.add_field(name="・参加メンバー",value=joinmemberstring)
            await this.message.edit(embed=newembed)

    def __init__(this,user:discord.User,channel):
        this.makeuser = user
        this.commandSelecting = False
        this.poll = None
        this.winjester = False
        this.winners = []
        this.aliveMembers = []
        this.targetpoll = None
        this.players = {}
        this.didUranaiPlayers = []
        this.DefensePlayer = {}#user:defenseしたtarget
        this.isNight = False
        this.endGame = False
        this.discussion = False
        this.isVotedUser = {}#id:投票された数
        this.votedPlayer = []#id
        this.killNightPlayer = {}#user:killしたuser
    async def startpoll(this,channel):#channel→こまんどじっこうしたちゃんねる
        global nowbjs
        message = await channel.send(embed=discord.Embed(title="人狼のメンバー募集", description=""))
        this.poll = Game.Poll(this.makeuser,channel,message)
        nowbjs.append(this)
        await asyncio.sleep(1)
        await channel.send("参加する人を募集します。")
        buttons = Game.SelectButtons([["参加する",discord.ButtonStyle.success]
        ,["抜ける",discord.ButtonStyle.gray]
        ,["メンバー決定",discord.ButtonStyle.blurple]],this)

        await channel.send(f"コマンドを選択してください",view=buttons)
        this.commandSelecting = True

    async def startGame(this,channel):

        await asyncio.sleep(1)

        randomplayerslist = random.sample(this.poll.joinMembers, len(this.poll.joinMembers))
        rolecounts = [0,0,0,0,0,0]#むら、じんろう、うらない、マッドメイト、しゅごしゃ、ジェスター

        for i in range(0,len(randomplayerslist)):#ランダムに役職付与
            rolename = ""
            this.aliveMembers = this.poll.joinMembers
            try:
                rolename = haiyakus[len(randomplayerslist)][i]
                if (rolename == "werewolf"): rolecounts[1] += 1
                if (rolename == "uranai"): rolecounts[2] += 1
                if (rolename == "madder"): rolecounts[3] += 1
                if (rolename == "defender"): rolecounts[4] += 1
                if (rolename == "jester"): rolecounts[5] += 1
                this.players[randomplayerslist[i].id] = rolename
            except:
                rolename = "somura"
                rolecounts[0] += 1
                this.players[randomplayerslist[i].id] = "somura"
                
            senduser = await client.fetch_user(randomplayerslist[i].id)     
            await senduser.send(f"あなたの役職は「{rolejapanese[rolename]}」です。")
        await channel.send("全員に役職を送りました。確認してください。")
        await asyncio.sleep(8)
        await channel.send("・この村の配役\n" + f"素村:{rolecounts[0]}人\n人狼:{rolecounts[1]}\n占い師:{rolecounts[2]}人\nマッドメイト:{rolecounts[3]}人\n守護者:{rolecounts[4]}\nてるてる:{rolecounts[5]}")
        await asyncio.sleep(3)
        await this.startMorning(channel,None,isfirst=True)

    async def startMorning(this,channel,killtargets,isfirst = False):
        if (this.endGame): return
        this.isNight = False
        this.didUranaiPlayers = []
        this.DefensePlayer = []

        if (random.randint(1,10) == 1): await channel.send("はよ起きろカスども、朝になったぞ")
        else:await channel.send("起きてください。朝になりました")
        await asyncio.sleep(3)
        if (killtargets != None):
            sendtext = f"今日の夜に、"
            for i in range(0,len(killtargets)):
                if (i == 1): sendtext += "と"
                sendtext += f"「{killtargets[i]}」さん"
            sendtext += "が死亡しました。"
            if (random.randint(1,10) == 1): await channel.send(sendtext + "やったね。")
            else: await channel.send(sendtext)
        else:
            if (isfirst == False): await channel.send("今日は死人がでませんでした")
        await asyncio.sleep(3)
        await channel.send("では、人外を追放するために議論してください。\n5分間待ってやる。\n/endと送ることで議論を強制終了できます\n※役職一覧、役職説明は/roleinfoコマンドで確認できます。")
        await asyncio.sleep(60 * 5)
        if (this.discussion or this.isNight): return
        await channel.send("時間だ、答えを聞こう\n追放する人に投票してください。\nスキップに入れると夜になり、人狼がキルします。")
        await this.discussionTime(channel)
    async def discussionTime(this,channel):
        this.discussion = True
        this.isVotedUser = {}
        this.votedPlayer = []
        message = await channel.send(embed=discord.Embed(title="投票", description=""))
        this.poll = Game.Poll(this.makeuser,channel,message)
        nowbjs.append(this)
        await asyncio.sleep(1)
        votetargets = []
        for i in this.aliveMembers:
            this.isVotedUser[i.id] = 0
            votetargets.append([i.name,discord.ButtonStyle.success])
        votetargets.append(["スキップ",discord.ButtonStyle.gray])
        buttons = Game.SelectButtons(votetargets,this)
        this.isVotedUser["skip"] = 0
        await channel.send(f"コマンドを選択してください",view=buttons)
        this.commandSelecting = True
    async def eject(this,channel):
        this.discussion = False
        this.killNightPlayer = {}
        this.commandSelecting = False
        await asyncio.sleep(3)
        embed = discord.Embed(title="投票結果", description="")
        for i in this.aliveMembers:
            embed.add_field(name="・" + i.name, value=str(this.isVotedUser[i.id]) + "票",inline=True)
        embed.add_field(name="・スキップ", value=str(this.isVotedUser["skip"]) + "票",inline=True)
        await channel.send(embed=embed)
        ejectid = None
        skip = False
        mostVoteCount = 0
        await asyncio.sleep(4)
        for i in this.aliveMembers:
            if (mostVoteCount < this.isVotedUser[i.id]):
                mostVoteCount = this.isVotedUser[i.id]
                ejectid = i.id
                skip = False
            elif (mostVoteCount == this.isVotedUser[i.id]):
                ejectid = None
                skip = True
        if (mostVoteCount == this.isVotedUser["skip"] or mostVoteCount < this.isVotedUser["skip"]):
                ejectid = None
                skip = True
        if (skip == False):
            ejectPlayer =  await client.fetch_user(ejectid)
            this.aliveMembers.remove(ejectPlayer)
            await channel.send(ejectPlayer.name + "が追放された")
            await asyncio.sleep(3)
            if (this.players[ejectid] == "jester"):
                this.winjester = True
            await this.checkEndGame(channel)
            await this.startNight(channel)
        else:
            await channel.send("スキップとなりました")
            await asyncio.sleep(3)
            await this.startNight(channel)
    async def startNight(this,channel):
        if (this.endGame): return
        await channel.send("夜になりました。\n人狼の方は/killコマンドを使ってキルするターゲットを決めて下さい")
        this.isNight = True
    async def checkEverywolfKill(this,channel):
        werewolfs = []
        for i in this.aliveMembers:
            if (this.players[i.id] == "werewolf"): werewolfs.append(i)
        killed = True
        killtargets = []
        for i in werewolfs:
            if (not i in this.killNightPlayer.keys()):
                killed = False
            else: killtargets.append(this.killNightPlayer[i])
        if (not killed): return
        for i in killtargets:
            if (list(this.DefensePlayer.keys()) is not [] and i in list(this.DefensePlayer.keys())):
                killtargets.remove(i)
                continue
            this.aliveMembers.remove(i)#ぶっころ作業            
        await asyncio.sleep(2)
        await this.checkEndGame(channel)
        await this.startMorning(channel,killtargets)
    async def checkEndGame(this,channel,reason = "eject"):
        werewolfs = []
        humans = []
        madders = []
        jester = []
        for i in this.aliveMembers:
            if (this.players[i.id] == "werewolf"): werewolfs.append(i)
            elif (this.players[i.id] == "madder"):madders.append(i) 

            elif (this.players[i.id] == "somura"):humans.append(i)            
            elif (this.players[i.id] == "uranai"):humans.append(i) 
            elif (this.players[i.id] == "defender"):humans.append(i)   

            elif (this.players[i.id] == "jester"):jester.append(i)
        everywerewolfs = []
        everyhumans = []
        everymadders = []
        everyjester = []
        for i, role in this.players.items():
            if (role == "werewolf"): everywerewolfs.append(i)
            elif (role == "madder"):everymadders.append(i) 

            elif (role == "somura"):everyhumans.append(i)            
            elif (role == "uranai"):everyhumans.append(i) 
            elif (role == "defender"):everyhumans.append(i)   

            elif (role == "jester"):everyjester.append(i) 
        everyUsers = [everywerewolfs,everymadders,everyhumans,everyjester]
        if (this.winjester):
            this.winners = [everyjester[0]]
            await this.endgame(channel,this.winners)
            return
        if (len(werewolfs) == 1 and len(madders) + len(humans) + len(jester) <= 1):#人狼1の場合は1,1となった場合勝利
            this.winners = [everywerewolfs,everymadders]
            await this.endgame(channel,this.winners,everyUsers)
            return
        if (len(werewolfs) == 2 and len(madders) + len(humans) + len(jester) <= 4):#人狼2の場合は4,2となった場合勝利
            this.winners = [everywerewolfs,everymadders]
            await this.endgame(channel,this.winners,everyUsers)
            return
        if (len(werewolfs) == 0):
            this.winners = [everyhumans]
            await this.endgame(channel,this.winners,everyUsers)
    def toTeamTextList(this,lis):
        result = ""
        if (lis is None):
            return "エラーです"
        for winner in lis:
            result += "\n・<@" + str(winner) + ">"
        return result
    async def endgame(this,channel,winners:[],everyUsers):
        this.endGame = True
        nowbjs.remove(this)
        await asyncio.sleep(1)
        description = ""
        team = roles[this.players[winners[0][0]]]
        if (team == "人狼"): description = "村が人狼によって破壊されました"
        if (team == "村人"): description = "村に平和が訪れました"
        if (team == "第三陣営"): description = "村が人狼ではない何者かによって破壊されました。"
        embed=discord.Embed(title=roles[this.players[winners[0][0]]] + "の勝利！！", description=description)
        winnerstext = ""
        for winners1 in winners:
            for winner in winners1:
                winnerstext += "<@" + str(winner) + ">"
        if (everyUsers[1] is not []):
            wolfTeam = everyUsers[0].extend(everyUsers[1])
        else: wolfTeam = everyUsers[0]
        humanTeam = everyUsers[2]
        neutralTeam = everyUsers[3]
        embed.add_field(name="・勝者", value=winnerstext)
        embed.add_field(name="・人狼陣営", value=this.toTeamTextList(wolfTeam))
        embed.add_field(name="・村人陣営", value=this.toTeamTextList(humanTeam))
        embed.add_field(name="・第三陣営", value=this.toTeamTextList(neutralTeam))
        await channel.send(embed=embed)
@tree.command(name="werewolf",description="ルールはわかるだろ、察しろ")
async def bj_command(interaction: discord.Interaction):
    self = interaction.user
    if (nowPlayingGamble(user=self)): interaction.response.send_message(embed=discord.Embed(color=discord.Colour.yellow(),title=f'現在プレイ中です'),ephemeral=True)
    #プレイヤーチェック

    bj = Game(self,interaction.channel)
    await interaction.response.send_message("投票を始めます",ephemeral=False)
    await bj.startpoll(interaction.channel)
@tree.command(name="kill",description="プレイヤーをキルします(夜に一回だけ使用可能)")
async def kill_command(interaction: discord.Interaction,target:discord.User):
    self = interaction.user
    for i in nowbjs:
        if (self in i.aliveMembers and i.players[self.id] == "werewolf" and i.isNight and not self in i.killNightPlayer.keys()):
            if (target in i.aliveMembers and i.players[target.id] != "werewolf" and i.isNight and not target in i.killNightPlayer.values()):
                i.killNightPlayer[self] = target
                await interaction.response.send_message(embed=discord.Embed(color=discord.Colour.yellow(),title=f'{target.name}をキルしました'),ephemeral=True)
                await i.checkEverywolfKill(interaction.channel) 
            else:
                await interaction.response.send_message(embed=discord.Embed(color=discord.Colour.red(),title=f'選択したユーザーはゲームに参加していない、または人狼、または他のプレイヤーが既にキルターゲットとして選んでいます。'),ephemeral=True)

@tree.command(name="defense",description="プレイヤーが人狼によってキルされるのを防ぎます(昼に一回だけ使用可能)")
async def defense_command(interaction: discord.Interaction,target:discord.User):
    self = interaction.user
    for i in nowbjs:
        if (self in i.aliveMembers and i.players[self.id] == "defender" and not i.isNight and not self in list(i.DefensePlayer.keys())):
            if (target in i.aliveMembers and not i.isNight):
                i.DefensePlayer[self] = target
                await interaction.response.send_message(embed=discord.Embed(color=discord.Colour.cyan(),title=f'{target.name}を防衛しました'),ephemeral=True)
            else:
                await interaction.response.send_message(embed=discord.Embed(color=discord.Colour.red(),title=f'選択したユーザーはゲームに参加していない、または人狼、または他のプレイヤーが既にキルターゲットとして選んでいます。'),ephemeral=True)

            
@tree.command(name="uranai",description="プレイヤーを占います(昼に一回だけ使用可能)")
async def uranai_command(interaction: discord.Interaction,target:discord.User):
    self = interaction.user
    for i in nowbjs:
        if (self in i.aliveMembers and i.players[self.id] == "uranai" and not i.isNight and not self in i.didUranaiPlayers):
            if (target in i.aliveMembers and not i.isNight):
                
                await interaction.response.send_message(embed=discord.Embed(color=discord.Colour.yellow(),title=f'{target.name}の役職は{i.players[target.id]}です'),ephemeral=True)
                await i.didUranaiPlayers.append(self) 
            else:
                await interaction.response.send_message(embed=discord.Embed(color=discord.Colour.red(),title=f'選択したユーザーはゲームに参加していない、または死んでいます'),ephemeral=True)

@tree.command(name="end",description="議論を強制終了します")
async def end_command(interaction: discord.Interaction):
    self = interaction.user
    for i in nowbjs:
        if (self in list(i.players.keys()) and i.discussion):
            await i.discussionTime(interaction.channel)
            return
    interaction.response.send_message(embed=discord.Embed(color=discord.Colour.red(),title="あなたはゲームに参加していません"))
    
keep_alive()

client.run(os.getenv("TOKEN"))
