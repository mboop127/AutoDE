This is a automatic game runner for Age of Empires 2: DE. **This runs via screen capture, it cannot run in the background.**

Before running:
- backup your AI folder
  - (this **will** overwrite all .ai files in your ai directory. .per files will be untouched. A backup of all .ai files will be saved to /ai_backup, but to be safe I suggest you backup your ai folder before running)
- confirm your monitor and game are both at 1080x1920p. No other resolutions are supported.
- confirm your graphical settings are all default - ie, no smooth text

How to run:
- download and extract git code to anywhere on your computer
- update settings file to match your game directory (may work as-is, but good to check).
  - you can also enable debugging in this file, and change the macro delay in case your machine struggles.
- run AOE2 DE at full screen, see resolution requirements above
- either:
  - enter ai names (eg Bambi_v030.per) matching their .per name in your directory (case senstitive)
  - enter ai civs
  - set timeout time and game count
  - set speedup hotkey for sped up games or leave blank.
  - Make sure DE is on screen, open to main menu, and the auto-DE GUI is not blocking the single player button.
  - Press run and wait!
- or:
  - edit the "parameters.csv" file to list every matchup you would like tested

The results will both print in the CMD window and save to a new csv in the outputs folder; if the program crashes mid run, it should save the results from each matchup as they happen.

Debugging:
- check the logs for details on what went wrong. Enable debug mode in the setttings file for more information next run.
- confirm that your resolution matches the above
- try lowering the command delay in the settings folder
- check AI names, check debug log to see if it is getting stuck trying to find a button
