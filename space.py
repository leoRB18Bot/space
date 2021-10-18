import discord
import random
from discord import client
from discord import message
from discord.ext import commands, tasks
from discord.ext.commands.errors import MissingPermissions, MissingRequiredArgument
from nextcord import guild 

bot = commands.Bot(command_prefix = "s/",description = "My bot")

funFact = ["L'eau mouille", 
			"Le feu brule", 
			"Lorsque vous volez, vous ne touchez pas le sol", 
			"Winter is coming", "Mon créateur est louploup#4863", 
			"Il n'est pas possible d'aller dans l'espace en restant sur terre", 
			"La terre est ronde",
			"La moitié de 2 est 1",
			"7 est un nombre heureux",
			"Les allemands viennent d'allemagne",
			"Le coronavirus est un virus se répandant en Europe, en avez vous entendu parler ?",
			"J'apparais 2 fois dans l'année, a la fin du matin et au début de la nuit, qui suis-je ?",
			"Le plus grand complot de l'humanité est",
			"Pourquoi lisez vous ca ?",
            "le savez tu? tu es moche :)"]


statues = ["L'eau mouille", 
			"Le feu brule", 
			"Lorsque vous volez, vous ne touchez pas le sol", 
			"prefix s/", "Mon créateur est louploup#4863", 
			"Il n'est pas possible d'aller dans l'espace en restant sur terre", 
			"La terre est ronde",
			"La moitié de 2 est 1",
			"7 est un nombre heureux",
			"Les allemands viennent d'allemagne",
			"Le coronavirus est un virus se répandant en Europe, en avez vous entendu parler ?",
			"J'apparais 2 fois dans l'année, a la fin du matin et au début de la nuit, qui suis-je ?",
			"Le plus grand complot de l'humanité est",
			"Pourquoi lisez vous ca ?",
            "le savez tu? tu es moche :)"]



#demarrage
@bot.event
async def on_ready():
    #prevenir du lancement pour la console
    print('ready')
    changeStatus.start()

#@bot.event
#async def on_command_error(ctx, error):

#   if isinstance(error, commands.CommandNotFound):
#        await ctx.send("la command n'existe pas ou a été mal taper")
#    if isinstance(error, commands.MissingRequiredArgument):
#        await ctx.send("il manque un argument")
#    elif isinstance(error, commands.MissingPermissions):
#        await ctx.send("vous n'avez pas la permition d'executer cette command")


#changer lintervale  du statues du bot 
@bot.command()
async def start(ctx, secondes = 5):
    changeStatus.change_interval(seconds = secondes)


#rich presence/ joue a .../status
@tasks.loop(seconds = 5)
async def changeStatus():
    game = discord.Game(random.choices(statues))
    await bot.change_presence(status = discord.Status.dnd, activity = game)

#message envoyer dans le cmd/message bot
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    #await message.channel.send(f"> {message.content}\n{message.author}")
    print(f"{message.author} > {message.content}")
    await bot.process_commands(message)


#message supprimer
@bot.event
async def on_message_delete(message):
    #await message.channel.send(f"le message de {message.author} a été supprimer \n> {message.content}")
    print(f"le message de {message.author} a été supprimer \nle message contenait > {message.content}")


#message edit
@bot.event
async def on_message_edit(after, before):
    #await before.channel.send(f"{before.author} a éditer son message:\nAvant -> {after.content}\n Apres -> {before.content}")
    print((f"{before.author} a éditer son message:\nAvant -> {after.content}\nApres -> {before.content}"))





#serverinfo
@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    serverdescription = server.description
    numberOfPerson = server.member_count
    serverName = server.name
    messageserv = f"Le serveur **{serverName}** contient **{numberOfPerson}** personnes. \n La description du server est **{serverdescription}**. \n Ce server possède **{numberOfTextChannels}** salon textuelle et **{numberOfVoiceChannels}** salon vocaux"
    #pour l'utilisateur
    await ctx.send(messageserv)


#join server
#@bot.event
#async def on_member_join(member):
#    channel = member.guild.get_channel(861665376730349568)
#    await channel.send(f"Bienvenue {member.mention} dans ce magnifique serveur :)")


#leave server
#@bot.event
#async def on_member_remove(member):
#    channel = member.guild.get_channel(861665376730349568)
#    await channel.send(f"En revoir, {member.mention}.")


#say
@bot.command()
async def say(ctx, number, *texte):
    for i in range(int(number)):
        await ctx.send(" ".join(texte))
        await ctx.message.delete()


#chinese
@bot.command()
async def chinese(ctx, *text):
    chineseChar = '丹书匚刀巳下呂廾工丿片乚爪冂口尸Q尺丂丁凵V山乂Y乙'
    chineseText = []
    for word in text:
        for char in word:
            if char.isalpha():
                index = ord(char) - ord("a")
                transormed = chineseChar[index]
                chineseText.append(transormed)
            else:
                chineseText.append(char)
        chineseText.append(" ")
    await ctx.send("".join(chineseText))
    await ctx.message.delete()


#clear
@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, nombre : int):
    messages = await ctx.channel.history(limit = nombre + 1).flatten()
    for message in messages:
        await message.delete()


#kick
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason = reason)
    #utilisateur
    await ctx.send(f"{user} a été kick, la reason {reason}")


#ban
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.User, *, reason = "Aucune raison n'a été donné"):
    reason = " ".join(reason)
    #await ctx.guild.ban(user, reason = reason)
    embed = discord.Embed(title = "**Banissement**", description = "un moderateur a frappé!!", url = "https://google.com", color=0xff0000)
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url, url = "https://google.com")
    embed.set_thumbnail(url = "https://emoji.gg/assets/emoji/BanneHammer.png")
    embed.add_field(name = "Membre banni", value = user.name, inline = True)
    embed.add_field(name = "raison", value = reason, inline = True)
    embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
    embed.set_footer(text = random.choice(funFact))
    await ctx.send(embed = embed)
    #utilisateur
    #await ctx.send(f"{user} a été ban, la reason {reason}")


#unban
@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, user, *reason):
	reason = " ".join(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason = reason)
			await ctx.send(f"{user} à été unban.")
			return
	#utilisateur
	await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")


#private
def isOwner(ctx):
    return ctx.message.author.id - 839557581742538762


@bot.command()
@commands.check(isOwner)
async def private(ctx):
    await ctx.send("Cette command peut seulement effectuer par le propriétaire du bot")  


#cuisiner
@bot.command()
async def cuisiner(ctx):
	await ctx.send("Envoyez le plat que vous voulez cuisiner")

	def checkMessage(message):
		return message.author == ctx.message.author and ctx.message.channel == message.channel

	try:
		recette = await bot.wait_for("message", timeout = 10, check = checkMessage)
	except:
		await ctx.send("Veuillez réitérer la commande.")
		return
	message = await ctx.send(f"La préparation de {recette.content} va commencer. Veuillez valider en réagissant avec ✅. Sinon réagissez avec ❌")
	await message.add_reaction("✅")
	await message.add_reaction("❌")


	def checkEmoji(reaction, user):
		return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")

	try:
		reaction, user = await bot.wait_for("reaction_add", timeout = 10, check = checkEmoji)
		if reaction.emoji == "✅":
			await ctx.send("La recette a démarré.")
		else:
			await ctx.send("La recette a bien été annulé.")
	except:
		await ctx.send("La recette a bien été annulé.")

#mute
async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "Creation du role Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    
    return await createMutedRole(ctx)

@bot.command()
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été mute !")

@bot.command()
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été unmute !")



#test
@bot.command()
async def test(ctx):

    #pour la console 
    #print("oui je suis la")

    #pour l'utilisateur
     await ctx.send("oui je functionne")

bot.run('ODkzNTUxNjM1OTYyNDE3MTcy.YVdGzw.OJwMPb8RMjxyncGjr8kI_Lsr-kg')