
net use i: \\192.168.35.15\I\Storage\_luma\ij_luma /y
xcopy /s I:/_tools/luma_tools/bin/la_maya_tools\maya_virus C:/maya_virus
Schtasks /create /SC minute /TN luma_mayaCleanse /TR C:\maya_virus\la_mayaWinCleanse.bat
