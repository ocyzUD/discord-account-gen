import discord
import random
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

BLACKLIST_FILE = 'blacklist.txt'

def is_user_blacklisted(user_id):
    """Check if a user is blacklisted based on their user ID."""
    try:
        with open(BLACKLIST_FILE, 'r') as file:
            blacklisted_users = file.readlines()
            if str(user_id) + "\n" in blacklisted_users:
                return True
    except FileNotFoundError:
        pass
    return False

async def is_not_blacklisted(ctx):
    if is_user_blacklisted(ctx.author.id):
        await ctx.send("You are blacklisted from using any commands.")
        return False
    return True

@bot.command(name="gen")
async def gen(ctx, service: str):
    if not await is_not_blacklisted(ctx):
        return

    file_path = f'stock/{service}.txt'

    if not os.path.exists(file_path):
        await ctx.send(f"Error: The account type \"{service}\" does not exist.")
        return

    try:
        with open(file_path, 'r') as file:
            accounts = file.readlines()

        if len(accounts) == 0:
            await ctx.send(f"Error: No accounts found for {service}.")
            return

        random_account = random.choice(accounts).strip()
        username, password = random_account.split(":")

        accounts.remove(f"{random_account}\n")

        with open(file_path, 'w') as file:
            file.writelines(accounts)

        embed = discord.Embed(
            title=f"**Generator Bot**",
            description=f"Here is your generated **{service}** account:\n**Username/Email**: `{username}`\n**Password**: `{password}`",
            color=discord.Color.green()
        )

        try:
            await ctx.author.send(embed=embed)
            await ctx.send("I’ve sent your generated account to your DMs!")
        except discord.Forbidden:
            await ctx.send("I can't DM you! Please make sure your DMs are open.")

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command(name="clear")
async def clear(ctx, service: str):
    if not await is_not_blacklisted(ctx):
        return

    file_path = f'stock/{service}.txt'

    if not os.path.exists(file_path):
        await ctx.send(f"Error: The account type \"{service}\" does not exist.")
        return

    try:
        with open(file_path, 'w') as file:
            file.truncate(0)  
        await ctx.send(f"All accounts in {service} have been cleared.")

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command(name="blacklist")
async def blacklist(ctx, user: discord.User):
    if ctx.author.id != YOUR_USER_ID:
        await ctx.send("You do not have permission to blacklist users.")
        return

    try:
        with open(BLACKLIST_FILE, 'a') as file:
            file.write(str(user.id) + '\n')  
        await ctx.send(f"User {user.name} has been blacklisted from using commands.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command(name="unblacklist")
async def unblacklist(ctx, user: discord.User):
    if ctx.author.id != YOUR_USER_ID:  
        await ctx.send("You do not have permission to unblacklist users.")
        return

    try:
        with open(BLACKLIST_FILE, 'r') as file:
            blacklisted_users = file.readlines()

        user_id_str = str(user.id) + "\n"
        if user_id_str not in blacklisted_users:
            await ctx.send(f"User {user.name} is not blacklisted.")
            return

        blacklisted_users.remove(user_id_str)

        with open(BLACKLIST_FILE, 'w') as file:
            file.writelines(blacklisted_users)

        await ctx.send(f"User {user.name} has been removed from the blacklist.")

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command(name="add")
async def add(ctx, service: str, account_info: str):
    if not await is_not_blacklisted(ctx):
        return

    file_path = f'stock/{service}.txt'

    if not os.path.exists(file_path):
        await ctx.send(f"Error: The account type \"{service}\" does not exist.")
        return

    try:
        with open(file_path, 'a') as file:
            file.write(account_info + '\n')
        await ctx.send(f"Account {account_info} has been added to {service}.")

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command(name="create")
async def create(ctx, service: str):
    if not await is_not_blacklisted(ctx):
        return

    file_path = f'stock/{service}.txt'

    if os.path.exists(file_path):
        await ctx.send(f"Error: The account type \"{service}\" already exists.")
        return

    try:
        with open(file_path, 'w') as file:
            pass  
        await ctx.send(f"Service file {service} has been created.")

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command(name="delete")
async def delete(ctx, file: str):
    if not await is_not_blacklisted(ctx):
        return

    file_path = f'stock/{file}.txt'

    if not os.path.exists(file_path):
        await ctx.send(f"Error: The file \"{file}\" does not exist.")
        return

    try:
        os.remove(file_path)
        await ctx.send(f"File {file} has been deleted.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

bot.run('YOUR_TOKEN_HERE')
