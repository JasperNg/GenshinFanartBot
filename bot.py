import lightbulb
from lightbulb.ext import tasks
import hikari
import asyncio
from datetime import datetime
from pybooru import Danbooru

#you gotta whale for Danbooru gold
client = Danbooru('danbooru', username='', api_key='')

bot = lightbulb.BotApp(token="",
                       default_enabled_guilds=(),
                       ignore_bots=True)

tasks.load(bot)

limit = 10 #limit on how many images users can request
blocklist = '-incest -animated -comic'  # max 3
tagnum = 2 #number of tags user can search



#Daily Yelan
@tasks.task(h=24)
async def dailyelan():
    req = client.post_list(tags=f"yelan_(genshin_impact) rating:s order:rank {blocklist}", page=1,
                           limit=1)
    for obj in req:
        title = f"📦Daily Yelan from Danbooru Page 1"
        embed = (
            hikari.Embed(
                title=title,
                colour=0x3B9DFF,
                timestamp=datetime.now().astimezone(),

            )
                .set_image(str(obj['large_file_url']))
                .add_field(
                "🎨Fanart by:",
                f'''
                                                                            `{obj['tag_string_artist']}`
                                                                            ''',
                inline=True,
            )
                .add_field(
                "Source Link:",
                f'''
                                                                            {obj['source']}
                                                                            ''',
                inline=True,
            )
                .add_field(
                "🤴Character",
                f'''
                                                                            `{obj['tag_string_character']}`
                                                                            ''',
                inline=False,
            )
                .add_field(
                "🏷️Tags",
                f'''
                                                                            `{obj['tag_string_general']}`
                                                                            ''',
                inline=False,
            )
        )
        await bot.rest.create_message("967044707844763678", embed)

#Daily Genshin Image
@tasks.task(h=24)
async def dailygenshin():
    req = client.post_list(tags=f"genshin_impact rating:s order:rank {blocklist}", page=1,
                           limit=1)
    for obj in req:
        title = f"📦Best Genshin art from Danbooru today"
        embed = (
            hikari.Embed(
                title=title,
                colour=0x3B9DFF,
                timestamp=datetime.now().astimezone(),

            )
                .set_image(str(obj['large_file_url']))
                .add_field(
                "🎨Fanart by:",
                f'''
                                                                            `{obj['tag_string_artist']}`
                                                                            ''',
                inline=True,
            )
                .add_field(
                "Source Link:",
                f'''
                                                                            {obj['source']}
                                                                            ''',
                inline=True,
            )
                .add_field(
                "🤴Character",
                f'''
                                                                            `{obj['tag_string_character']}`
                                                                            ''',
                inline=False,
            )
                .add_field(
                "🏷️Tags",
                f'''
                                                                            `{obj['tag_string_general']}`
                                                                            ''',
                inline=False,
            )
        )
        await bot.rest.create_message("837962035517718548", embed)


@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print('bot has started')
    await asyncio.sleep(86400)
    dailyelan.start()
    dailygenshin.start()

#Discord Embed Preset Class
class Embed:
    def __init__(self, title, img, display, member, dmember, artist, source, character, tag):
        self.title = title
        self.img = img
        self.display = display
        self.member = member
        self.dmember = dmember
        self.artist = artist
        self.source = source
        self.character = character
        self.tag = tag

    def main(self):
        embed = (
            hikari.Embed(
                title=self.title,
                colour=0x3B9DFF,
                timestamp=datetime.now().astimezone(),

            )
                .set_image(str(self.img))
                .set_footer(
                text=f"Requested by {self.display}",
                icon=self.member or self.dmember,
            )
                .add_field(
                "🎨Fanart by:",
                f'''
                                                                    `{self.artist}`
                                                                    ''',
                inline=True,
            )
                .add_field(
                "Source Link:",
                f'''
                                                                    {self.source}
                                                                    ''',
                inline=True,
            )
                .add_field(
                "🤴Character",
                f'''
                                                                    `{self.character}`
                                                                    ''',
                inline=False,
            )
                .add_field(
                "🏷️Tags",
                f'''
                                                                    `{self.tag}`
                                                                    ''',
                inline=False,
            )
        )
        return embed

#core Danbooru request function
async def core(ctx, tags, lim, title, req):
    counter = 0
    # to prevent dumbfucks from searching these tags
    if tags.find('loli') == -1 or tags.find('shota') == -1 or tags.find('bestiality') == -1:
        # prevents users from requesting more images than the limit
        if ctx.options.num_of_images <= lim:
            # for JSON object in request
            for obj in req:
                #title with counter
                final_title = f"#{counter + 1} {title}"
                #calling Embed class
                e1 = Embed(final_title, obj['large_file_url'], ctx.member.display_name, ctx.member.avatar_url,
                           ctx.member.default_avatar_url, obj['tag_string_artist'], obj['source'],
                           obj['tag_string_character'], obj['tag_string_general'])

                await ctx.respond(e1.main())
                counter = counter + 1
        else:
            await ctx.respond("exceeded limit")
    else:
        await ctx.respond("Tags against TOS")

#error catcher
@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(
            f"Something went wrong during invocation of command `{event.context.command.name}`.")
        raise event.exception

    # Unwrap the exception to get the original cause
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.NotOwner):
        await event.context.respond("You are not the owner of this bot.")
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"This command is on cooldown. Retry in `{exception.retry_after:.2f}` seconds.")
    elif ...:
        ...
    else:
        raise exception

#help gives info about bot
@bot.command
@lightbulb.command('help', 'Information about commands and bot')
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    embed = (
        hikari.Embed(
            title=f"🖌️YelartBot",
            description=f'''
            A Danbooru bot that sends (sfw) Genshin Fanart with a Yelan focus!
            Made by Aalto | pfp from redfish
            P.S. good luck on your Yelan pulls!
            ''',
            colour=0x3B9DFF,
            timestamp=datetime.now().astimezone(),
        )
            .set_image(
            'https://cdn.discordapp.com/attachments/962928460890791956/966722830576263218/yelan-yelan-genshin.gif')
            .set_footer(
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
        )
            .add_field(
            "🕰️Automatic Daily Updates",
            '''
            Daily Yelan Art - gets highest rated and most recent fanart
            Daily Genshin Art -  gets highest rated and most recent fanart
            ''',
            inline=False,
        )
            .add_field(
            "🕹️Modes",
            '''
            `Yelan`
            `Genshin`
            `Yuri`
            ''',
            inline=True,
        )
            .add_field(
            "📇Subcommands",
            '''
            `/new` - gets recent fanart
            `/gacha` -  gets random fanart
            `/search_artist` - search by artist username
            ''',
            inline=True,
        )
            .add_field(
            "Misc. Commands",
            '''
           `/true_search` - searches the entirety of danbooru (for advanced users)
            >>> - tags must be separated by spaces (max 2 tags)
            - number of images must be less than or equal to 10
            - page number must be integers 1 and above 
            ''',
            inline=False,
        )

    )
    await ctx.respond(embed)

#Yelan Group
@bot.command
@lightbulb.command('yelan', 'yelan command group')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def yelan():
    pass


# New Yelan
@yelan.child
@lightbulb.option('num_of_images', f'how many images do you want? (Max {limit} images)', int)
@lightbulb.command('new', f'Sends the latest Yelan Fanart (Max {limit} images)')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def knew(ctx):
    final_tags = f"yelan_(genshin_impact) rating:s {blocklist}"
    title = f"New Yelan from 📦Danbooru Page 1"
    req = client.post_list(tags=final_tags, page=1,
                           limit=ctx.options.num_of_images)
    await core(ctx, final_tags, limit, title, req)


# Random Yelan
@yelan.child
@lightbulb.option('num_of_images', f'how many images do you want? (max {limit})', int)
@lightbulb.command('gacha', 'Sends a random Yelan Fanart')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def randy(ctx):
    final_tags = f"yelan_(genshin_impact) rating:s {blocklist}"
    title = f"Random Yelan art from 📦Danbooru"
    req = client.post_list(tags=final_tags, random=True,
                           limit=ctx.options.num_of_images)
    await core(ctx, final_tags, limit, title, req)


# Search Yelan Artist
@yelan.child
@lightbulb.option('num_of_images', f'how many images do you want? (max {limit})', int)
@lightbulb.option('username', 'author\'s name', str)
@lightbulb.command('search_artist', f'returns Yelan fanart from artist (Max {limit} images)')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def search(ctx):
    usr = ctx.options.username.lower()
    final_tags = f"yelan_(genshin_impact) rating:s {usr} {blocklist}"
    title = f"Yelan from 📦Danbooru from 🎨{usr}"
    req = client.post_list(tags=final_tags,
                           limit=ctx.options.num_of_images)
    await core(ctx, final_tags, limit, title, req)




#Yuri Group
@bot.command
@lightbulb.command('yuri', 'yuri command group')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def yuri():
    pass

# New Yuri
@yuri.child
@lightbulb.option('num_of_images', f'how many images do you want? (Max {limit} images)', int)
@lightbulb.command('new', f'Sends the latest Yuri Fanart (Max {limit} images)')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def knew(ctx):
    final_tags = f"yuri rating:s {blocklist}"
    title = f"New Yuri from 📦Danbooru Page 1"
    req = client.post_list(tags=final_tags, page=1,
                           limit=ctx.options.num_of_images)
    await core(ctx, final_tags, limit, title, req)


# Random Yuri
@yuri.child
@lightbulb.option('num_of_images', f'how many images do you want? (max {limit})', int)
@lightbulb.command('gacha', 'Sends a random Yuri Fanart')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def randy(ctx):
    final_tags = f"yuri rating:s {blocklist}"
    title = f"Random Yuri art from 📦Danbooru"
    req = client.post_list(tags=final_tags, random=True,
                           limit=ctx.options.num_of_images)
    await core(ctx, final_tags, limit, title, req)


# Search Yuri Artist
@yuri.child
@lightbulb.option('num_of_images', f'how many images do you want? (max {limit})', int)
@lightbulb.option('username', 'author\'s name', str)
@lightbulb.command('search_artist', f'returns Yuri fanart from artist (Max {limit} images)')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def search(ctx):
    usr = ctx.options.username.lower()
    final_tags = f"yuri rating:s {usr} {blocklist}"
    title = f"Yuri from 📦Danbooru from 🎨{usr}"
    req = client.post_list(tags=final_tags,
                           limit=ctx.options.num_of_images)
    await core(ctx, final_tags, limit, title, req)




# Genshin group
@bot.command
@lightbulb.command('genshin', 'genshin command group')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def genshin():
    pass


# New Genshin Fanart
@genshin.child
@lightbulb.option('num_of_images', f'how many images do you want? (Max {limit} images)', int)
@lightbulb.command('new', f'Sends the latest genshin art (Max {limit} images)')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def knew(ctx):
    final_tags = f"genshin_impact rating:s {blocklist}"
    title = f"New Genshin art from 📦Danbooru Page 1"
    req = client.post_list(tags=final_tags, page=1,
                           limit=ctx.options.num_of_images)
    await core(ctx, final_tags, limit, title, req)


# Random Genshin Fanart
@genshin.child
@lightbulb.option('num_of_images', f'how many images do you want? (max {limit})', int)
@lightbulb.command('gacha', 'Sends one random Genshin image')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def randy(ctx):
    final_tags = f"genshin_impact rating:s {blocklist}"
    title = f"Random Genshin art from 📦Danbooru"
    req = client.post_list(tags=final_tags, random=True,
                           limit=ctx.options.num_of_images)
    await core(ctx, final_tags, limit, title, req)


# Search Genshin Artist
@genshin.child
@lightbulb.option('num_of_images', f'how many images do you want? (max {limit})', int)
@lightbulb.option('username', 'author\'s name', str)
@lightbulb.command('search_artist', f'returns Genshin fanart from artist (Max {limit} images)')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def search(ctx):
    usr = ctx.options.username.lower()
    final_tags = f"genshin_impact rating:s {usr} {blocklist}"
    title = f"Genshin fanart from 📦Danbooru from 🎨{usr}"
    req = client.post_list(tags=final_tags,
                           limit=ctx.options.num_of_images)
    await core(ctx, final_tags, limit, title, req)


# True search
@bot.command
@lightbulb.option('page', 'which page? (1,2,3...)', int)
@lightbulb.option('num_of_images', f'how many images do you want? (max {limit})', int)
@lightbulb.option('tags', f'separate them with spaces (max {tagnum} tag)', str)
@lightbulb.command('true_search', 'global search')
@lightbulb.implements(lightbulb.SlashCommand)
async def trusearch(ctx):
    tags = ctx.options.tags.lower()
    final_tags = f"{tags} rating:s {blocklist}"
    title = f'Search result from 📦Danbooru'
    req = client.post_list(tags=final_tags,
                           limit=ctx.options.num_of_images, page=ctx.options.page)
    await core(ctx, final_tags, limit, title, req)


bot.run()
