from pyrogram import Client as Clients


def create_pyrogram(name: str, **args):
    return Clients(name, **args)
