import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    class Bot(commands.Bot):
        def __init__(self, intents: discord.Intents, **kwargs):
            super().__init__(command_prefix="!", intents=intents, case_insensitive=True)

        async def on_ready(self):
            print(f'Bot đã kết nối thành công: {self.user.name}')
            await self.tree.sync()

    intents = discord.Intents.all()
    bot = Bot(intents=intents)

    leaderboard_url = 'https://adventofcode.com/2023/leaderboard/private/view/1763801.json'
    session_id = os.getenv("SESSION_ID")

    @bot.event
    async def on_member_join(member):
        guild = member.guild
        if guild.system_channel is not None:
            detailMessage = 'Chao mung {0.mention} den voi {1.name}!'.format(member, guild)
            await guild.system_channel.send(detailMessage)

    @bot.hybrid_command(name='hello', description = 'Tự kỷ')
    async def hello(interaction: discord.Integration):
        author = interaction.message.author
        await interaction.reply(content=f'Xin chào, {author.mention}!')

    @bot.hybrid_command(name='info', description='Thông tin bot, mã nguồn')
    async def info(interaction: discord.Integration):
        embed = discord.Embed(title="Thông tin về Bot",
                            description="AoC BOT",
                            color=0x00ff00)
        embed.add_field(name="Tác giả", value="Nguyen Van An")
        embed.add_field(name="Ngôn ngữ", value="Python")
        embed.add_field(name="Mã nguồn", value="https://github.com/21010647AnNV/AoCBOT")
        embed.set_footer(text="© 2023 AoCBOT")
        await interaction.reply(embed=embed)
        
    @bot.hybrid_command(name='ping', description='Ping mạng')
    async def ping(interaction: discord.Integration):
        latency = round(bot.latency * 1000)  
        await interaction.reply(f'Độ trễ hiện tại của bot là {latency} ms.')

    @bot.hybrid_command(name='leaderboard', description='Flex nhẹ cái điểm')
    async def leaderboard(interaction: discord.Integration):
        headers = {'Cookie': f'session={session_id}'}
        response = requests.get(leaderboard_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            members = data['members']

            sorted_members = sorted(members.items(), key=lambda x: x[1]['local_score'], reverse=True)

            embed = discord.Embed(title="Leaderboard", color=0x00ff00)

            leaderboard_info = "Leaderboard:\n"
            for member_id, member_data in sorted_members:
                member_name = member_data['name']
                local_score = member_data['local_score']
                embed.add_field(name=member_name, value=f"Score: {local_score}★", inline=False)

            await interaction.reply(embed=embed)
        else:
            await interaction.reply(f"Failed to fetch leaderboard. Status code: {response.status_code}")

    @bot.hybrid_command(name='menu', description='Hiển thị danh sách câu lệnh')
    async def menu(interaction: discord.Integration):
        help_message = """
    Danh sách câu lệnh:
    `!menu`: Hiển thị danh sách câu lệnh
    `!leaderboard`: Flex nhẹ cái điểm
    `!hello`: Tự kỷ
    `!ping`: Ping mạng
    `!info`: Thông tin bot, mã nguồn
    `!shorttime`: The flash of AoC
    """
        await interaction.reply(help_message)

    @bot.hybrid_command(name='shorttime', description='Thời gian ngắn nhất')
    async def shorttime(interaction: discord.Integration, day: str):
        headers= {'Cookie': f'session={session_id}'}
        response = requests.get(leaderboard_url, headers=headers)

        # http debug
        if response.status_code == 200:
            data = response.json()
            members = data['members']

            sorted_members = sorted(
            members.items(),
            key=lambda x: x[1]['completion_day_level'].get(str(day), {}).get('1', {}).get('get_star_ts', float('inf')) or float('inf')
            )

            for member_id, member_data in sorted_members:
                star_ts = member_data['completion_day_level'].get(str(day), {}).get('1', {}).get('get_star_ts')
                if star_ts:
                    fastest_member_id = member_id
                    fastest_member_data = member_data
                    break
            else:
                await interaction.reply(f"No completed data !")
                return

            fastest_member_name = fastest_member_data['name']
            fastest_timestamp = fastest_member_data['completion_day_level'].get(str(day), {}).get('1', {}).get('get_star_ts', 0)

            if fastest_timestamp:
                fastest_timestamp = datetime.utcfromtimestamp(fastest_timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')
            else:
                fastest_timestamp = "Not completed"

            embed = discord.Embed(title=f'The flash ngày: {day}', color=0x00ffff)
            embed.add_field(name="Member", value=fastest_member_name, inline=False)
            embed.add_field(name="Completion Time", value=fastest_timestamp, inline=False)

            await interaction.reply(embed=embed)
        else:
            await interaction.reply(f'Fail to fetch!. Status code: {response.status_code}')

    @bot.hybrid_command(name='poop', description='Ẩu lên đìa')
    async def poop(interaction: discord.Integration, target_user: discord.User = None):
        author_name = interaction.author.name
        poop_message = f"""``` 
    ⠀⠀⠀⠀⠀⢀⣤⣶⣶⣤⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⡄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⡿⠁⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣦⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀
⠀⠀⠀⠀⢠⣿⣿⣿⣿⡿⣿⣿⣧⣀⠀⠀
⠀⠀⠀⠀⢺⣿⣿⣿⣿⣧⣬⣻⢿⣿⣿⡦
⠀⠀⠀⠀⠀⠙⠻⠿⢿⣿⣿⣿⣿⡏⠛⠁
⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⣽⣿⡿⠁⠀⠀
⠀⢀⡠⣿⣷⣤⡀⠀⠀⢸⣿⣿⠃⠀⠀⠀
⠰⠿⠿⠿⠿⠿⠇⠀⠠⠿⠿⠏⠀⠀⠀⠀```"""
        if target_user:
            poop_message += f"\n**" + "Ẩu lên đìa  " + f"{target_user.mention}**"
        
        await interaction.reply(content=f"{author_name}\n" + poop_message)
        
    bot.run(os.getenv("TOKEN"))

