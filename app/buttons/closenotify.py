import disnake as dis
from disnake.ext import commands
from disnake.ext.commands import Cog

from app.client import CloseBot


class CloseNotifyButton(Cog):
    def __init__(self, bot: CloseBot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_button_click(self, inter: dis.MessageInteraction):
        if inter.component.custom_id.startswith("closenotify"):
            raw_data = inter.component.custom_id.split(".")
            close_id = raw_data[-1]
            close = await self.bot.clm.getCloseById(int(close_id))
            creator = inter.guild.get_member(close.creator)
            if inter.guild.get_role(self.bot.settings.roles.closemod) in inter.author.roles:
                if creator == inter.author:
                    embed = dis.Embed.from_dict(
                        {
                            "title": "<:freeiconbell8262174:1393538484731510794>  Dota 2 Клоз ・ [RU] Dota 2",
                            "description": f'Участвуй в игре 5 на 5 против ребят нашего сервера. Улучшай свою статистику ( /stats ), попадай в топы, знакомься с ребятами и получай опыт в игре! Главная цель игры - защитить свою крепость и разрушить крепость противника! СБОР В:{inter.guild.get_channel(close.waitingchannel).mention}',
                            "color": 3092790,
                            # "fields": [
                            #   {
                            #     "name": "<:freeiconcoins359920:1111875709732933643> Участие",
                            #     "value": "```50 ```",
                            #     "inline": True
                            #   },
                            #   {
                            #     "name": "<:freeiconcoins359920:1111875709732933643> Победа",
                            #     "value": "```100```",
                            #     "inline": True
                            #   },
                            #   {
                            #     "name": "<:freeiconskull556158:1115273145448935494> Клановые",
                            #     "value": "```-2 и +3```",
                            #     "inline": True
                            #   }
                            # ],
                            "footer": {
                                "text": "Ведущий: " + creator.display_name,
                                "icon_url": creator.display_avatar.url
                            },
                            "image": {
                                "url": "https://cdn.discordapp.com/attachments/745563237805981787/1393591367590215805/image.png?ex=6873ba99&is=68726919&hm=e25b2fc981bdd0366bd87a2616e2420a7c8e024648641767bc9d5415ba8fb35e&"
                            }
                        }
                    )
                    role = inter.guild.get_role(
                        self.bot.settings.roles.closenotify)
                    await inter.guild.get_channel(self.bot.settings.channels.notification_channel).send(role.mention, embed=embed)
                    await inter.response.send_message("Вы успешно отпраили уведомление", ephemeral=True)
                else:
                    await inter.response.send_message("Вы не создатель клоза", ephemeral=True)
            else:
                await inter.response.send_message("Вы не являетесь клозмодом", ephemeral=True)


def setup(bot: CloseBot):
    bot.add_cog(CloseNotifyButton(bot))
