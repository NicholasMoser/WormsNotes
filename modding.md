# Modding

This page contains details on how to go about modding the game.

## Export Files

In order to modify the game easier, it's best to export all of the files from the disc to your local file system.
Dolphin is able to launch the game from these files, so you can easily modify the files to quickly test changes.

First make sure that Dolphin has access to your .iso/.ciso/.nkit.iso/.rvz file and right click on it in Dolphin and select **Properties**:

![Dolphin Right Click](/img/dolphin_right_click.png?raw=true "Dolphin Right Click")

Then go to the right-most tab **Filesystem**, right click on the Disc at the top and
select **Extract Entire Disc**. Extract it to the directory of your choosing.

![Dolphin Right Click](/img/dolphin_export_files.png?raw=true "Dolphin Right Click")

Now if you navigate to the location you exported to, you'll find two directories.

![Extracted Files](/img/extracted_files.png?raw=true "Extracted Files")

- **files** contains most of the actual files for the game, such as graphics, audio,
  maps, etc.
- **sys** contains the code for the game and the disc header information.

## Launch Game from Exported Files

As we modify files, we'll want to test our changes. You can do so by launching the game
from these exported files.

To do so, open the **sys** directory you'll find the following:

![Sys Files](/img/sys_files.png?raw=true "Sys Files")

The `main.dol` file here is the main code for the game. We can launch the game by doing
one of the following:

- Right click `main.dol`, select **Open with...** and select Dolphin
- Drag `main.dol` directly onto a running version of Dolphin
- Open Dolphin and go to **File->Open..** at the top left and select `main.dol`

## Modifying Files

To modify the files, you will need specific software based on which file you wish to
modify. I've listed descriptions of each file type you may encounter below:

### XOM

XOM files contain most of the interesting data for the game. You can think of them
like a zip file that contain configuration values, 3D geometry, textures, colors,
and effects.

Here are some of the more notable XOM files to modify:

- `files/Language/NGC/American.xom` contains all of the text displayed in-game for the
  American locale.
- `files/AITwk.xom` contains tweaks to enemy AI, dictating how smart they are.
- `files/DefSave.xom` contains metadata on what data in the game is locked and needs
  to be unlocked by the player.
- `files/WeapTwk.xom` contains most of the weapon data, such as weapon damage.

#### Xomview

I've had the most success with reading and writing XOM files using
[xomview](https://gitlab.com/w4tweaks/xomview). If you open a .xom file with it you'll
see a GUI like this:

![xomview American.xom](/img/xomview_american.png?raw=true "xomview American.xom")

Here I have the file `files/Language/NGC/American.xom` open, which contains all of the
displayed text in-game for the American locale. You can right click a value and select
**Change [Value]** to modify it.

When you are done making changes to the file you can hit the **Save Xom** button to
save your changes, and when relaunching the game you should see your changes active.

You can use the Search bar to help find specific configurations you may be looking for,
such as specific text you'd like to replace.

#### Xom Import

Models may also be viewed in blender with
[xom-import](https://github.com/Psycrow101/Blender-3D-XOM-plugin).

#### Xom2xml

I've also tried using [Xom2Xml](https://github.com/AlexBond2/Xom2Xml) to modify
these files, but it currently fails on many xom files in the console verisons of
Worms 3D. Here is an
[example of a XOM file converted to XML](https://gist.github.com/NicholasMoser/38a5f0284f038f744de088f7f48f7506).

#### CrateModGames

There is a C# app used for game randomizers that appears to have some Worms 3D support.
It has some bindings for Worms 3D files:
[CrateModGames/GameSpecific/Worms/Common](https://github.com/TheBetaM/CrateModLoader/tree/master/CrateModGames/GameSpecific/Worms/Common).

Although [GameCube may not be fully supported](https://github.com/TheBetaM/CrateModLoader/blob/master/CrateModGames/GameSpecific/Worms/Worms3D/Game_Worms3D.cs#L12).

### TGA

[Truevision TGA](https://en.wikipedia.org/wiki/Truevision_TGA) graphics files are textures
that can be opened and modified in Photoshop.

![TGA File](img/tga.png?raw=true "TGA File")

The format for the PS2 and GameCube TGA files is slightly different than in the PC version.

![TGA Modes](img/tga_modes.png?raw=true "TGA Modes")

This is the reason that opening TGA files with XomView shows the images as corrupted:

![XomView TGA](img/xomview_tga.png?raw=true "XomView TGA")

Unfortunately because of this you cannot currently replace these files, even
with unmodified versions of TGA files.

### Lua

[Lua scripts](https://en.wikipedia.org/wiki/Lua_(programming_language)) are programming
code files primarily used for Challenges and the Campaign. These scripts are in the
`files/Scripts` folder and can be modified like any programming language. I personally 
recommend using [Visual Studio Code](https://code.visualstudio.com/), which has plugins
for developing Lua.

### CSH

Currently unknown. Seems to accompany every map file for each time of day, for example:

```
countingsheep.xom
countingsheepDAY.csh
countingsheepEVENING.csh
countingsheepNIGHT.csh
```

### DSP

[.dsp](https://www.metroid2002.com/retromodding/wiki/DSP_(File_Format)) files are
audio. You can listen to the audio using [foobar2000](https://www.foobar2000.org/) 
and [foo_input_vgmstream](https://github.com/stuerp/foo_input_vgmstream).

I'm not entirely sure how to modify these files yet. For Naruto GNT4, it uses
`.trk` files which are actually `.adp` files. You can replace them using
[ffmpeg](https://www.ffmpeg.org/) and **dtkmake.exe** from the Gamecube SDK.
More information can be found here:
[Create TRK File from Music File](https://github.com/NicholasMoser/GNTool/blob/main/docs/audio.md#create-trk-file-from-music-file)

I do think that `.adp` files and `.dsp` files may be different based on this
[hackernews post](https://news.ycombinator.com/item?id=34625573). It links to
[this page](http://web.archive.org/web/20080420105759/https://hcs64.com/mboard/gcstreamdb.php)
which seems to indicate that different games use ADP and DSP and are handled
differently.

### DOL

Like all GameCube games, the actual logic of the game is found in the `main.dol` file 
which is in PowerPC assembly. You can disassemble the code using
[Ghidra](https://ghidra-sre.org/) and
[Ghidra GameCube Loader](https://github.com/Cuyler36/Ghidra-GameCube-Loader).

Modifying the DOL can be difficult. Replacing a single instruction with a different
one is easy, as you simply replace the bytes as-is, but if you wish to add new code
you'll need to utilize [code caves](https://en.wikipedia.org/wiki/Code_cave).
I've written some tools in [Xombie](https://github.com/NicholasMoser/Xombie) to help
create code caves.

#### Symbol Map

There is a [symbol map](https://refspecs.linuxbase.org/elf/gabi4+/ch4.symtab.html)
in the PS2 EU version of the game, making it much easier to understand the underlying 
code of the game: https://www.retroreversing.com/ps2-unstripped/

After extracting files from the ISO dump, you can simply run the Linux command `readelf -Ws sles_518.43 >> symbol.map`
to get a symbol map from the binary.

The symbol map will tell you the names of every function in the game as well as many
variables. Ghidra will automatically use it if you open the PS2 code with the
[Ghidra PS2 plugin](https://github.com/chaoticgd/ghidra-emotionengine-reloaded).
