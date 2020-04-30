import discord

token = ''
prefix = '~~'
game = discord.Game(f"Follow the rules. {prefix}help")

oauth = "https://discordapp.com/api/oauth2/authorize?client_id=696124534679535728&permissions=268561591&scope=bot"
server = "https://discord.gg/PVTBgK6"
srccode = "https://github.com/spergmoment/law-enforcer"
restart = "pm2 restart 3"

ids = [
    694643777146454096,
    296182065949573121
]

staticinfo = f"```Owner: literal monkey#9193\nOwner ID: 694643777146454096\n"
f"Running on: 5.6.3-arch1-1 x86_64 64 bit\nProcessors: 4 × Intel Core i5-3210M CPU @ 2.50GHz\nMemory: 7.7 GB"
endinfo = f"Join the official support server: {server}\nSee the code for yourself: {srccode}"

botlower = "I am at a lower level on the role hierarchy than this member."
userlower = 'This member has a higher role than you.'

owneronly = "You must be a bot owner to use this command."

def userperms(perm):
    return f"You must have the `{perm.upper()}` permission to do this."

def botperms(perm):
    return f"I lack the permissions to {perm}."

def helpCmd(emb, cmd, desc, syntax, ex1, ex2, notes, reqperms):
    emb.title = cmd
    emb.description = desc
    emb.add_field(name="Usage", value=f"\\{prefix}{cmd} {syntax}", inline=False)
    if ex1 and ex2: 
        emb.add_field(name="Examples", value=f"\\{prefix}{cmd} {ex1}\n\\{prefix}{cmd} {ex2}", inline=False)
    if notes: 
        emb.add_field(name="Extra Notes", value=notes)
    return emb.add_field(name="Required Permissions", value=reqperms)
