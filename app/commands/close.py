import disnake as dis
from disnake.ext.commands import Cog, Param, InteractionBot
from disnake.ext import commands
from disnake import PermissionOverwrite,Embed
from ..client import CloseBot
from ..closemanager import CloseSource

class CloseCommand(Cog):
    def __init__(self,bot:CloseBot) -> None:
        self.bot = bot
        super().__init__()

    @commands.slash_command(name="close",description="Create close Dota 2")
    async def close_command(self,inter:dis.ApplicationCommandInteraction,type:str = Param(choices={"random":"random","team":"team"})):
        await inter.response.defer(with_message=True)
        if not(inter.guild):
            await inter.edit_original_message("Не используйте в личных сообщениях")
            return
        closemod = inter.guild.get_role(self.bot.settings.roles.closemod)
        
        if closemod not in inter.author.roles:
            await inter.edit_original_message("У вас нету роли клозмейкера")
            return
        
        if (await self.bot.clm.getCloseByCreator(inter.author.id)):
            await inter.edit_original_message("У вас уже запущен клоз")
            return
        
        closeban = inter.guild.get_role(self.bot.settings.roles.closeban)
        everyone = inter.guild.default_role

        category = await inter.guild.create_category(
            name="Close",
            overwrites={
                everyone:PermissionOverwrite(view_channel=True),
                closeban:PermissionOverwrite(view_channel=False)
            }
        )

        managechannel = await inter.guild.create_text_channel(
            name = "Управление",
            category=category,
            position=0,
            overwrites={
                everyone:PermissionOverwrite(view_channel=False),
                closemod:PermissionOverwrite(view_channel=True),
                closeban:PermissionOverwrite(view_channel=False)
            }
        )

        messagechannel = await inter.guild.create_text_channel(
            name = "Запись",
            category=category,
            position=1,
            overwrites={
                everyone:PermissionOverwrite(view_channel=True),
                closemod:PermissionOverwrite(view_channel=True),
                closeban:PermissionOverwrite(view_channel=False)
            }            
        )

        waitingchannel = await inter.guild.create_voice_channel(
            name="Ожидание",
            category=category,
            position=2,
            overwrites={
                everyone:PermissionOverwrite(view_channel=True),
                closemod:PermissionOverwrite(view_channel=True,kick_members=True,mute_members=True,move_members=True),
                closeban:PermissionOverwrite(view_channel=False)
            }
        )
        source = CloseSource(
            type=type,
            managechannel=managechannel.id,
            waitingchannel=waitingchannel.id,
            creator=inter.author.id,
            messagechannel=messagechannel.id
        )
        close = await self.bot.clm.create_close(source)

        if type == "team":
            message = Embed.from_dict(
                {
                        "title": "Dota 2 ・ Запись  ᅠ  ᅠ  ᅠ  ᅠ  ᅠ  ᅠ",
                        "color": 3092790,
                        "fields": [
                        {
                            "name": "Силы тьмы",
                            "value": f'{self.bot.settings.emojis.Knife}・Лёгкая \n\n{self.bot.settings.emojis.Onion}・Центр \n\n{self.bot.settings.emojis.Security}・Сложная \n\n{self.bot.settings.emojis.Conhand}・Частичная поддержка\n\n{self.bot.settings.emojis.Conhands}・Полная поддержка',
                            "inline": True
                        },
                        {
                            "name": "Силы света",
                            "value": f'{self.bot.settings.emojis.Knife}・Лёгкая \n\n{self.bot.settings.emojis.Onion}・Центр \n\n{self.bot.settings.emojis.Security}・Сложная \n\n{self.bot.settings.emojis.Conhand}・Частичная поддержка\n\n{self.bot.settings.emojis.Conhands}・Полная поддержка',
                            "inline": True
                        }
                        ]
                }
            )
            row = dis.ui.ActionRow.with_message_components()
            row.add_button(
                style=dis.ButtonStyle.primary,
                label='Силы тьмы',
                emoji=self.bot.settings.emojis.dark,
                custom_id=f"team.dark.{close.id}"
            )
            row.add_button(
                style=dis.ButtonStyle.primary,
                label="Силы света",
                emoji=self.bot.settings.emojis.light,
                custom_id=f"team.light.{close.id}"
            )
            row.add_button(
                style=dis.ButtonStyle.danger,
                label="Выйти из записи",
                emoji=self.bot.settings.emojis.light,
                custom_id=f'closeexit.{close.id}'
            )
            await messagechannel.send(embed = message,components=row)

        else:
            pass

        message = Embed.from_dict(
        {
			"title": "Dota 2 ・ Управление клозом ᅠ  ᅠ  ᅠ  ᅠ  ᅠ  ᅠ",
			"description": "**<:freeiconnotificationbell9479257:1393538487139041280> - Уведомить о сборе на клоз\n\n<:freeiconbell8262174:1393538484731510794> - Позвать ребят на свободные позиции \n\n<:freeiconforbiddensign799546:1393538481820663898> - Удалить игрока из записи \n\n<:freeiconarrow11917347:1393538479274590248> - Запустить клоз\n\n<:freeiconmultiply6401653:1393538476640571442> - Отменить клоз**\n\n**Dota 2 ・Вспомогательные команды**\n\n/swap - заменить игрока или поменять местами игроков",
			"color": 3092790
		}
        )
        row = dis.ui.ActionRow.with_message_components()
        row.add_button(
            style=dis.ButtonStyle.primary,
            label="Уведомить",
            custom_id=f"closenotify.{close.id}"
        )
        row.add_button(
            style=dis.ButtonStyle.primary,
            label="Позвать",
            custom_id=f"closecall.{close.id}"
        )
        row.add_button(
            style=dis.ButtonStyle.primary,
            label="Кикнуть",
            custom_id=f"closeremove.{close.id}"
        )
        row.add_button(
            style=dis.ButtonStyle.primary,
            label="Начать",
            custom_id=f"closestart.{close.id}"
        )
        row.add_button(
            style=dis.ButtonStyle.primary,
            label="Отменить",
            custom_id=f"closecancel.{close.id}"
        )
        await managechannel.send(embed = message,components=row)
        await inter.edit_original_message("Клоз создан")

    @commands.slash_command(name="removeclose")
    async def close_remove(self,inter:dis.AppCmdInter):
        await inter.response.defer(with_message=True,ephemeral=True)
        close = await self.bot.clm.getCloseByCreator(inter.author.id)
        if close:
            channel = inter.guild.get_channel(close.managechannel)

            for channel in channel.category.channels:
                await channel.delete()
            
            await inter.edit_original_message("Успешно")
        else:
            await inter.edit_original_message("Нету каналов")
        

def setup(bot:InteractionBot):
    bot.add_cog(CloseCommand(bot))

