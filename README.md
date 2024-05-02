# Morrowind Multiplayer Custom Script Helper

This script (ChatGPT made it lol) runs a GUI application to facilitate the addition and removal of custom scripts from your tes3mp server. It does so by having you select your 'scripts/custom' directory and your CustomScripts.Lua file and then choosing the downloaded script you wish to add to your server, giving it a custom name. It then adds those entries to your customscripts.lua file and copies the script to your custom scripts folder. You are also able to remove entries from your customscripts file using this and can refresh the list as you go. As of right now it basically works, it just does not delete your copied script files but does remove the entries from CustomScripts.Lua so it still achieves its function.


I also recommend pressing the "Completely wipe" button after selecting your CustomScripts.Lua file if you havent added any scripts manually as the comments in that file by default get parsed weird by the app.


run the application by using visual studio code or by opening the folder containing the python script in terminal and running "python ./tes3mp_script_manager.py"

I made it using Python 3.12 so make sure that is installed and added to your PATH if you are on Windows
