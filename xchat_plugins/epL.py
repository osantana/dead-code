import xchat

__module_name__ = "* epx L" 
__module_version__ = "0.1.0" 
__module_description__ = "Ensina como usar /clear"


def clear_cb(word, word_eol, userdata):
    ctx = xchat.get_context()
    ctx.command("me acha que limpar a tela eh para os fracos!")
    return xchat.EAT_ALL

xchat.hook_command("clear", clear_cb, help="Usage: CLEAR, Clears the current text window")
