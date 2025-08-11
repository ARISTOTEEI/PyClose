import disnake
import disnake as dis
from disnake.ext import commands
from disnake.ext.commands import Cog

from app.client import CloseBot
from app.entryMessage import update_message
from app.utils.schemas import UserSchema,TeamType

class CloseWinnerSelect(Cog):
    def __init__(self,bot:CloseBot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_dropdown(self,inter:dis.MessageInteraction):
        if inter.component.custom_id.startswith("closewinner"):
            await inter.response.defer(with_message=True,ephemeral=True)
            if inter.guild.get_role(self.bot.settings.roles.closemod) in inter.author.roles:
                raw_data = inter.component.custom_id.split('.')
                close_id = int(raw_data[-1])
                close = await self.bot.clm.getCloseById(close_id)
                if close.creator == inter.author.id:
                    await inter.edit_original_message("Клоз успешно закрыт")
                    team_win = inter.values[0]
                    members = await self.bot.clm.get_members(close_id)
                                
                    for member in members:
                        user = await self.bot.clm.get_user(member.discord_id)
                        user = user.model_dump()
                        if member.team == team_win:
                            user['pos'+ f'{member.pos}' + 'wins'] += 1
                            user['pos'+ f'{member.pos}' + 'games'] += 1
                        else:
                            user['pos'+ f'{member.pos}' + 'games'] += 1
                        user = UserSchema.model_validate(user)
                        await self.bot.clm.update_user(user)

                    embed = dis.Embed.from_dict(
                        {
                        "title": "Dota 2 ・ Запись  ᅠ  ᅠ  ᅠ  ᅠ  ᅠ  ᅠ",
                        "color": 3092790,
                        "fields": [
                        {
                            "name": f"{'🏆' if team_win == "light" else ''} Силы тьмы",
                            "value": f'{self.bot.settings.emojis.Knife}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 1 and x.team == TeamType.DARK),"Лёгкая")} \n\n{self.bot.settings.emojis.Onion}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 2 and x.team == TeamType.DARK),"Центр")} \n\n{self.bot.settings.emojis.Security}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 3 and x.team == TeamType.DARK),"Сложная")} \n\n{self.bot.settings.emojis.Conhand}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 4 and x.team == TeamType.DARK),"Частичная поддержка")} \n\n{self.bot.settings.emojis.Conhands}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 5 and x.team == TeamType.DARK),"Полная поддержка")}',
                            "inline": True
                        },
                        {
                            "name": f"{'🏆' if team_win == "dark" else ''} Силы света",
                            "value": f'{self.bot.settings.emojis.Knife}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 1 and x.team == TeamType.LIGHT),"Лёгкая")} \n\n{self.bot.settings.emojis.Onion}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 2 and x.team == TeamType.LIGHT),"Центр")} \n\n{self.bot.settings.emojis.Security}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 3 and x.team == TeamType.LIGHT),"Сложная")} \n\n{self.bot.settings.emojis.Conhand}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 4 and x.team == TeamType.LIGHT),"Частичная поддержка")}\n\n{self.bot.settings.emojis.Conhands}・{next((f'<@{x.discord_id}>' for x in members if x.pos == 5 and x.team == TeamType.LIGHT),"Полная поддержка")}',
                            "inline": True
                        }
                        ]
                    }
                        )
                    category = inter.guild.get_channel(close.managechannel).category
                    
                    for channel in category.channels:
                        await channel.delete()
                    await category.delete()
                    await self.bot.clm.delete_close(close.creator)
                    channel = inter.guild.get_channel(self.bot.settings.channels.win_channel)
                    await channel.send(embed = embed)
                else:
                    await inter.edit_original_message("Вы не создатель клоза")
            else:
                await inter.edit_original_message("Вы не клозмод")

def setup(bot:CloseBot):
    bot.add_cog(CloseWinnerSelect(bot))