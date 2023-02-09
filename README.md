# FLOPS4
## FLOPS4 Loader Of Profiles (Sims 4)

A helper to use multiple profiles for The Sims 4, and/or to allow it to use a profile outside of "Documents".

Thanks to the amazing work over at <https://github.com/ModOrganizer2/usvfs> and <https://github.com/pwssnk/py-usvfs>, we have a way to redirect a program's filesystem access selectively.

If building or running from source, you need to use Python 3.7.
Anything higher or lower is currently incompatible.

### First Steps:
1. Create a directory where you want to put your profiles.
   *For example:* `C:\Games\TS4Data`
2. Place `flops4.py` or `flops4.exe` in that directory.
3. Run the script for the first time. This will generate flops4.ini.
4. In the INI:
-- Set `launch_command` to point to your `TS4_x64.exe`, along with any command line options.
-- Change any other paths and settings as needed.

### Usage:
`python.exe flops4.py [profile_name]`
*or*
`flops4.exe [profile_name]`

### Note:
**If there is any existing data**, it will be moved to a new profile named `backup_[current_datetime]`.
