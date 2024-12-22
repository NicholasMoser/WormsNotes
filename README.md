# Worms 3D Notes

<!-- vscode-markdown-toc -->
* 1. [Overview](#Overview)
* 2. [Files](#Files)
	* 2.1. [XOM](#XOM)
	* 2.2. [TGA](#TGA)
	* 2.3. [Lua](#Lua)
	* 2.4. [CSH](#CSH)
	* 2.5. [DOL](#DOL)
* 3. [Symbol Map](#SymbolMap)
* 4. [Text Modification](#TextModification)
* 5. [Weapon Modification](#WeaponModification)
	* 5.1. [WeapTwk.xom](#WeapTwk.xom)
* 6. [Campaign Modification](#CampaignModification)
* 7. [Challenge Modification](#ChallengeModification)
* 8. [Skip Intro Cutscenes](#SkipIntroCutscenes)
* 9. [Unlock Levels by Default](#UnlockLevelsbyDefault)
* 10. [Navigate Deathmatch Maps Faster](#NavigateDeathmatchMapsFaster)
* 11. [Add More Maps to Multiplayer](#AddMoreMapstoMultiplayer)
	* 11.1. [Campaign Level Alien](#CampaignLevelAlien)
	* 11.2. [Deathmatch Level Alien](#DeathmatchLevelAlien)
	* 11.3. [Adding Levels](#AddingLevels)
* 12. [Change Controller](#ChangeController)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

##  1. <a name='Overview'></a>Overview

This page contains notes found in the internals of Worms 3D on the GameCube.
I've been able to make some modifications to the game which are shown in below sections.

There appears to be an unofficial patch for the PC version that may
be learned from [Worms 3D Anniversary Patch](https://github.com/heatray/W3DPatch)

The cutting room floor pages for the [console](https://tcrf.net/Worms_3D_(GameCube,_PlayStation_2,_Xbox))
and [Windows](https://tcrf.net/Worms_3D_(Windows)) release also have some interesting notes.

Even better is that there appear to be C# bindings for working with Worms related files:
[CrateModGames/GameSpecific/Worms/Common](https://github.com/TheBetaM/CrateModLoader/tree/master/CrateModGames/GameSpecific/Worms/Common).
Although [GameCube may not be fully supported](https://github.com/TheBetaM/CrateModLoader/blob/master/CrateModGames/GameSpecific/Worms/Worms3D/Game_Worms3D.cs#L12).

##  2. <a name='Files'></a>Files

###  2.1. <a name='XOM'></a>XOM

XOM files contain 3D geometry, textures, colors, and effects.
They are used to show in-game worm, weapon, and map objects.

I've had the most success with viewing XOM files using [xomview](https://gitlab.com/w4tweaks/xomview).
Models may also be viewed in blender with [xom-import](https://github.com/Psycrow101/Blender-3D-XOM-plugin).
Last, they can be converted to XML for modification with [Xom2Xml](https://github.com/AlexBond2/Xom2Xml).
Although not every xom file on the GameCube version can be converted currently.

Here is an [example of a XOM file converted to XML](https://gist.github.com/NicholasMoser/38a5f0284f038f744de088f7f48f7506).

###  2.2. <a name='TGA'></a>TGA

[Truevision TGA](https://en.wikipedia.org/wiki/Truevision_TGA) graphics files are textures
that can be opened and modified in Photoshop.

![TGA File](/tga.png?raw=true "TGA File")

###  2.3. <a name='Lua'></a>Lua

Worms 3D seems to utilize some lua scripting, which would make modding the game and creating
custom scenarios much easier.

###  2.4. <a name='CSH'></a>CSH

Currently unknown. Seems to accompany every map file for each time of day, for example:

```
countingsheep.xom
countingsheepDAY.csh
countingsheepEVENING.csh
countingsheepNIGHT.csh
```

###  2.5. <a name='DOL'></a>DOL

Like all GameCube games, the actual logic of the game is found in the `main.dol` file which is in PowerPC assembly.
You can disassemble the code using [Ghidra](https://ghidra-sre.org/) and
[Ghidra GameCube Loader](https://github.com/Cuyler36/Ghidra-GameCube-Loader).

##  3. <a name='SymbolMap'></a>Symbol Map

There is a symbol map in the PS2 EU version of the game, making it much easier to understand the underlying code of the game:
https://www.retroreversing.com/ps2-unstripped/

After extracting files from the ISO dump, you can simply run the Linux command `readelf -Ws sles_518.43 >> symbol.map`
to get a symbol map from the binary.

##  4. <a name='TextModification'></a>Text Modification

You can find all of the game text in `files/Language`. It looks like the developers originally created
csv files, such as `NGCMessages.csv`, and then converted them to XOM objects in the `files/Language/NGC`
directory. You therefore can modify these messages by modifying the respective XOM object, such as `American.xom`.

![Example of replacing text](/text_mod.png?raw=true "Example of replacing text")

##  5. <a name='WeaponModification'></a>Weapon Modification

This section details my efforts to find where weapon damage is set. If you'd prefer to avoid the technical parts,
skip to the next section.

Health is set at instruction 0x80140f3c in the `main.dol`.
If a worm has taken damage, the damage will be set to `worm->new_health` (offset 0x24).

Damage is subtracted from total health at instruction 0x80149598. Damage is set at 0x80148f3c which is passed in as the
second parameter of the method starting at 0x80148e8c.

Damage is calculated at the function at 0x80143bdc, which will be called `calculate_damage`.
Blast damage is calculated at the function at 0x80148a58, which will be called `calculate_blast_damage`.
Somewhere in these methods, it must account for the weapon being used. Let's start by just looking at Fire Punch,
which appears to always do 30 damage. The 30 must be stored somewhere we can modify.

Unfortunately, the call stack above this point looks like this code is determined via an interpreter of some sort.
After [doing some research](https://t17forum.worms2d.info/index.php/t-39070.html), I can see that it is interpreted
from XOM files.

###  5.1. <a name='WeapTwk.xom'></a>WeapTwk.xom

This file contains most of the weapon data, and appears to be easy to configure after conversion with
[Xom2Xml](https://github.com/AlexBond2/Xom2Xml). For example, here is data for fire punch:

```xml
    <MeleeWeaponPropertiesContainer id="kWeaponFirePunch-0">
      <IsAimedWeapon>false</IsAimedWeapon>
      <DamageIsPercentage>false</DamageIsPercentage>
      <WormIsWeapon>true</WormIsWeapon>
      <RetreatTimeOverride>0</RetreatTimeOverride>
      <Radius>8</Radius>
      <MinAimAngle>0</MinAimAngle>
      <MaxAimAngle>0</MaxAimAngle>
      <DischargeFX></DischargeFX>
      <DischargeSoundFX></DischargeSoundFX>
      <WormCollisionFX>WeaponFirePunch</WormCollisionFX>
      <LandCollisionFX></LandCollisionFX>
      <LogicalPositionOffset x="16" y="0" z="4"/>
      <ImpulseDirection x="70" y="0" z="0"/>
      <LogicalLaunchYOffset>-8</LogicalLaunchYOffset>
      <WormDamageMagnitude>30</WormDamageMagnitude>
      <LandDamageMagnitude>0</LandDamageMagnitude>
      <ImpulseMagnitude>0.22</ImpulseMagnitude>
      <WormDamageRadius>0</WormDamageRadius>
      <LandDamageRadius>0</LandDamageRadius>
      <ImpulseRadius>0.1</ImpulseRadius>
      <DisplayName>Text.kWeaponFirePunch</DisplayName>
      <AnimDraw>DrawFirepunch</AnimDraw>
      <AnimAim>HoldFirepunch</AnimAim>
      <AnimFire>FireFirepunch</AnimFire>
      <AnimHolding></AnimHolding>
      <AnimEndFire></AnimEndFire>
      <WeaponGraphicsResourceID>Dummy</WeaponGraphicsResourceID>
      <WeaponType>0</WeaponType>
      <DefaultPreference>0</DefaultPreference>
      <CurrentPreference>0</CurrentPreference>
      <LaunchDelay>300</LaunchDelay>
      <PostLaunchDelay>0</PostLaunchDelay>
      <FirstPersonOffset x="0" y="0" z="0"/>
      <FirstPersonScale x="0" y="0" z="0"/>
      <FirstPersonFiringParticleEffect></FirstPersonFiringParticleEffect>
      <FirstPersonDrawAnim></FirstPersonDrawAnim>
      <FirstPersonWindUpAnim></FirstPersonWindUpAnim>
      <FirstPersonFireAnim></FirstPersonFireAnim>
      <FirstPersonWindDownAnim></FirstPersonWindDownAnim>
      <FirstPersonReloadAnim></FirstPersonReloadAnim>
      <FirstPersonHideAnim></FirstPersonHideAnim>
      <FirstPersonIdleAnim></FirstPersonIdleAnim>
      <FirstPersonHandDrawAnim></FirstPersonHandDrawAnim>
      <FirstPersonHandWindUpAnim></FirstPersonHandWindUpAnim>
      <FirstPersonHandFireAnim></FirstPersonHandFireAnim>
      <FirstPersonHandWindDownAnim></FirstPersonHandWindDownAnim>
      <FirstPersonHandReloadAnim></FirstPersonHandReloadAnim>
      <FirstPersonHandHideAnim></FirstPersonHandHideAnim>
      <FirstPersonHandIdleAnim></FirstPersonHandIdleAnim>
      <DisplayInFirstPerson>false</DisplayInFirstPerson>
      <CanBeFiredWhenWormMoving>true</CanBeFiredWhenWormMoving>
      <RumbleLight>0</RumbleLight>
      <RumbleHeavy>150</RumbleHeavy>
    </MeleeWeaponPropertiesContainer>
```

Some enum values can be found matching to [Worms Ultimate Mayhem](https://github.com/AlexBond2/Xom2Xml/blob/main/XOMSCHM/WUM/XEnum.md).

Weapon damage is determined by this entry:

```xml
<WormDamageMagnitude>30</WormDamageMagnitude>
```

Here is an example of modifying this value to 100:

![Fire punch damage mod](compressed.gif?raw=true)

##  6. <a name='CampaignModification'></a>Campaign Modification

Each campaign level seems to have its own lua file, making modification incredibly simple.
The first campaign level, D-Day, has the file `files/Scripts/dday.lua`. Here's an example
of the definition of an enemy worm:

```lua
   -- Worm 6, Team 1
   CopyContainer("Worm.Data04", "Worm.Data06")
   lock, worm = EditContainer("Worm.Data06")
   CopyContainer("AIParams.Worm04", "AIParams.Worm06")
   worm.Energy = 30  
   worm.Spawn = "spawn7"
   worm.Name = "Scutze"
   CloseContainer(lock)
```

You can easily change things like the name of the worm:

![Campaign mod](campaign_mod.png?raw=true)

##  7. <a name='ChallengeModification'></a>Challenge Modification

The first challenge, Shotgun Challenge 1, can be found in the file `files/Scripts/TargetHunt.lua`.
Any lua files are trivial to modify, so for this challenge I changed it from having only the
shotgun to having all weapons from the D-Day campaign:

So I changed the inventory from:

```lua
function SetupInventories()
   -- sets up a default container and adds our selection to it
   lock, inventory = EditContainer("Inventory.Team.Default") 
   inventory.Shotgun = -1
   CloseContainer(lock) -- must close the container ASAP

   CopyContainer("Inventory.Team.Default", "Inventory.Team00")
   CopyContainer("Inventory.Team.Default", "Inventory.Team01")

   lock, delays = EditContainer("Inventory.WeaponDelays") 
   CloseContainer(lock)

end
```

to:

```lua
function SetupInventories()
   -- sets up a default container and adds our selection to it
   lock, inventory = EditContainer("Inventory.Team.Default") 
   inventory.Bazooka = -1
   inventory.Grenade = -1
   inventory.ClusterGrenade = 5
   inventory.Uzi = -1
   inventory.Landmine = 5
   inventory.FirePunch = -1
   inventory.Shotgun = -1
   inventory.SkipGo = -1
   
   CloseContainer(lock) -- must close the container ASAP

   -- Copies this selection into each worm

   CopyContainer("Inventory.Team.Default", "Inventory.Team00")
   CopyContainer("Inventory.Team.Default", "Inventory.Team01")

   -- Sets allies to have extra airstrikes and no clusters
   lock, inventory = EditContainer("Inventory.Team00") 
   inventory.Airstrike = 1
   inventory.ClusterGrenade = 0
   inventory.Mortar = 4
   inventory.Landmine = 0
   inventory.HomingMissile = 1
   --inventory.FlameThrower = 2
   inventory.Girder = 0

   CloseContainer(lock)
   lock, inventory = EditContainer("Inventory.Team01") 
   
    inventory.HomingMissile = 0
   
    CloseContainer(lock)
   
   -- Sets up some delays
   lock, delays = EditContainer("Inventory.WeaponDelays") 
   delays.Airstrike = 4
   CloseContainer(lock)
end
```

And you can see the results here:

![Challenge mod](challenge_mod.gif?raw=true)

##  8. <a name='SkipIntroCutscenes'></a>Skip Intro Cutscenes

The method `main()` is at 0x8015b1a8, so the calls to the cutscenes should be somewhat early in that method.
But upon further inspection, main appears to jump to interpreted code fairly early on. A better way of finding
the intro video cutscene definitions might be to search for the video titles.

Turns out it's even easier than that, you can simply delete or rename `files/FMV/NTSC/acclaim.thp` and
`files/FMV/NTSC/t17logo.thp` to remove them from the intro. The MusyX splash screen is a combination of
static images though. Specifically it's a combination of:

- `files/Logos/License.tga`
- `files/Frontend/Icons/musyxdolby.tga`
- `files/Logos/musyxdolbytext.tga`

These three are defined in `files/Bundles/bundle03.xom`. They're actually the only things defined in bundle03.
To modify them, you must modify them **in** bundle03.xom, not the file paths under `Logos/` and `Frontend/`.
The file bundle03.xom unfortunately cannot be renamed or deleted without causing runtime errors.

If we look at the file load order:

```
23:03:603 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:      67 kB Local.xom
23:03:792 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:       9 kB DefSave.xom
23:03:903 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:      13 kB Tweak.xom
23:04:044 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:      20 kB WeapTwk.xom
23:04:158 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:      96 kB MenuTwk.xom
23:04:365 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:       6 kB CamTwk.xom
23:04:492 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:      18 kB Scripts.xom
23:04:612 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:       7 kB HudTwk.xom
23:04:720 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:       8 kB LvlSetup.xom
23:04:837 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:       1 kB Persist.xom
23:04:945 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:      12 kB AITwk.xom
23:05:102 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:      17 kB MenuTwkGC.xom
23:05:267 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:     192 kB PartTwk.xom
23:05:481 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:     244 kB Language/NGC/American.xom
23:05:768 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:     588 kB Bundles/bundle05.xom
23:06:330 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:     138 kB Bundles/bundle03.xom
23:07:125 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:       7 kB Audio/NGCSFX/NGCSFX.pool
23:08:542 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:       1 kB Audio/NGCSFX/NGCSFX.proj
23:08:543 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:   2,400 kB Audio/NGCSFX/NGCSFX.samp
23:09:586 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:      10 kB Audio/NGCSFX/NGCSFX.sdir
23:09:705 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:      18 kB Bundles/Bundle02.xom
23:13:815 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:   2,903 kB FMV/NTSC/acclaim.thp
23:23:986 Core\HW\DVD\FileMonitor.cpp:86 W[FileMon]:   2,075 kB FMV/NTSC/t17logo.thp
```

bundle05.xom seems to have icons, the loading animation, boxes, buttons, and bars. So mostly UI.
Looks like bundle03.xom is loaded from the DOL most likely, will be easier to remove at a later time.
For now, just override the existing images with some mod related info.

##  9. <a name='UnlockLevelsbyDefault'></a>Unlock Levels by Default

The file `DefSave.xom` contains metadata on which files are locked by default. You can force it to be
unlocked by default by removing a locked entry like so:

```xml
  <ContainerResources href="L.L.Leek"/>
  ...
  <XContainerResourceDetails id="L.L.Leek">
    <Value href="L.L.Leek-0"/>
    <Name>L.L.Leek</Name>
    <Flags>17</Flags>
  </XContainerResourceDetails>
  <LockedContainer id="L.L.Leek-0">
    <Locked>true</Locked>
    <LockedTitle>Text.Level.Leek</LockedTitle>
    <LockedIcon>5</LockedIcon>
  </LockedContainer>
```

You can also then update Scripts.xom to remove the <lock>, for example changing:

```xml
<Lock>L.L.Leek</Lock>
```

to

```xml
<Lock></Lock>
```

##  10. <a name='NavigateDeathmatchMapsFaster'></a>Navigate Deathmatch Maps Faster

It would be nice to be able to scroll through the deathmatch map list faster, especially if and when we
add more maps.

However it looks like the Delay value for this is in MultiplayerMenu which may be defined in MenuTwk.xom
which currently cannot be extracted with xom2xml.

##  11. <a name='AddMoreMapstoMultiplayer'></a>Add More Maps to Multiplayer

Multiplayer currently contains [a number of accessible maps](maps.md). Some levels are playable in both
campaign and deathmatch mode. For example in Scripts.xom:

###  11.1. <a name='CampaignLevelAlien'></a>Campaign Level Alien

```xml
<LevelDetails id="FE.Level.Alien-0">
  <LevelName>Text.Level.Alien</LevelName>
  <ScriptName>ALIEN</ScriptName>
  <Theme>LUNAR</Theme>
  <CustomTheme></CustomTheme>
  <LandFile>alien.xom</LandFile>
  <TimeOfDay>EVENING</TimeOfDay>
  <Particles></Particles>
  <LevelType>0</LevelType>
  <Brief>Miss.Alien.brief</Brief>
  <Image>Mission_AJS.tga</Image>
  <LevelNumber>34</LevelNumber>
  <Lock></Lock>
  <LongestWins>true</LongestWins>
  <AIPathNodeStartYOffset>0</AIPathNodeStartYOffset>
  <AIPathNodeCollisionStep>20</AIPathNodeCollisionStep>
</LevelDetails>
```

###  11.2. <a name='DeathmatchLevelAlien'></a>Deathmatch Level Alien

```xml
<LevelDetails id="FE.Unlocked.Alien-0">
  <LevelName>Text.Level.Alien</LevelName>
  <ScriptName>stdvs,wormpot</ScriptName>
  <Theme>LUNAR</Theme>
  <CustomTheme></CustomTheme>
  <LandFile>alien.xom</LandFile>
  <TimeOfDay>EVENING</TimeOfDay>
  <Particles></Particles>
  <LevelType>5</LevelType>
  <Brief></Brief>
  <Image>Mission_AJS.tga</Image>
  <LevelNumber>0</LevelNumber>
  <Lock>L.L.Alien</Lock>
  <LongestWins>true</LongestWins>
  <AIPathNodeStartYOffset>0</AIPathNodeStartYOffset>
  <AIPathNodeCollisionStep>20</AIPathNodeCollisionStep>
</LevelDetails>
```

###  11.3. <a name='AddingLevels'></a>Adding Levels

Levels don't seem to be stored by LevelNumber in memory. Instead they are added by file and
sorted by name. So to add a level you just need to add an entry to Scripts.xom with:

- id starting with "FE.Unlocked."
- `<LevelType>` set to 5
- `<ScriptName>` set to "stdvs,wormpot"

##  12. <a name='ChangeController'></a>Change Controller

Multiplayer normally follows a "hotseat" pattern, where only 1 controller is used.
This controller is passed between players as they take their turns.

While all controllers are polled in memory, only controller 1 is written out to a useful location.
Thankfully, we can easily hijack the controller port this is pointing to at 0x80301548.

You can simply change the 0 in:

```asm
li  r25, 0
```

to the respective controller port.

Here is a Gecko Code to swap the current active controller to the team matching the current team index. In other words,
when it's Player 1's turn, controller 1 is active. When it's player 2's turn, controller 2 is active. Etc.

```gecko
C21563BC 00000007
7C040378 7C030378
3D20800F 6129CB5C
7D2903A6 4E800421
80630034 2C030000
4082000C 3D208040
9089352C 807F0130
38810024 00000000
C2301548 00000002
3F208040 8339352C
60000000 00000000
```

and here's the annotated assembly code for this gecko code:

```asm
loc_0x801563BC:
  ; Get the currently active team's data via GetTeamData() at 0x800fcb5c.
  ; This clobbers r0, r3, and r9. r3 will need to be restored by the end of the code
  ; since it is used in the function call in the next instruction at 0x801563c0.
  ; We have r4 free since we overwrite it at the end, so let's move r0 (active team) to it.
  ; We also must move r0 (active team) to r3 as part of the function call to GetTeamData().
  mr r4, r0
  mr r3, r0
  lis   r9, 0x800f
  ori   r9, r9, 0xCB5C
  mtctr r9
  bctrl
  ; Check if the current active team is AI
  lwz r3,  0x34(r3)
  cmpwi r3, 0
  bne end
  ; If it's not AI, store r4 (the active team) into 0x8040352C
  lis r9, 0x8040
  stw r4, 13612(r9)
end:
  ; Restore r3 and run original replaced instruction
  lwz	r3, 0x0130 (r31)
  addi r4, r1, 0x24

...

loc_0x80301548:
  # Load 0x8040352C into r25 as the controller to be read from
  lis r25, 0x8040
  lwz r25, 13612(r25)
```
