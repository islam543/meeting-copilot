"""Create Windows shortcuts for the meeting copilot. Run once: python make_shortcuts.py

- Desktop and Start menu: "Meeting Copilot" (pin it to the taskbar from either)
- This folder: "Meeting Copilot (sample)" plays the sample meeting, no mic or Soniox key needed
Shortcuts run pythonw.exe, so no console window opens.
"""

import sys
from pathlib import Path

import pythoncom
from win32com.propsys import propsys, pscon
from win32com.shell import shell, shellcon

from copilot import APP_ICON, APP_ID

HERE = Path(__file__).resolve().parent
PYTHONW = Path(sys.executable).with_name("pythonw.exe")
SCRIPT = HERE / "copilot.py"


def make_link(path, args, description):
    link = pythoncom.CoCreateInstance(shell.CLSID_ShellLink, None, pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
    link.SetPath(str(PYTHONW if PYTHONW.exists() else sys.executable))
    link.SetArguments(args)
    link.SetWorkingDirectory(str(HERE))
    link.SetIconLocation(*APP_ICON)
    link.SetDescription(description)
    store = link.QueryInterface(propsys.IID_IPropertyStore)
    store.SetValue(pscon.PKEY_AppUserModel_ID, propsys.PROPVARIANTType(APP_ID))
    store.Commit()
    link.QueryInterface(pythoncom.IID_IPersistFile).Save(str(path), 0)
    print("Created", path)


def main():
    desktop = Path(shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOPDIRECTORY, None, 0))
    programs = Path(shell.SHGetFolderPath(0, shellcon.CSIDL_PROGRAMS, None, 0))
    about = "Live copilot for in-person meetings"
    for folder in (desktop, programs):
        make_link(folder / "Meeting Copilot.lnk", f'"{SCRIPT}"', about)
    make_link(HERE / "Meeting Copilot (sample).lnk",
              f'"{SCRIPT}" --replay sample_meeting.txt --brief sample_brief.md', "Play the sample meeting")


if __name__ == "__main__":
    main()
