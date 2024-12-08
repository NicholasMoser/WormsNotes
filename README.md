# Worms 3D Notes

- [Overview](#Overview)
- [Files](#Files)
  - [XOM](#XOM)
  - [TGA](#TGA)
  - [Lua](#Lua)
  - [CSH](#CSH)
  - [DOL](#DOL)
- [Text Modification](#Text-Modification)
- [Weapon Modification](#Weapon-Modification)
  - [WeapTwk.xom](#WeapTwk.xom)
- [Campaign Modification](#CampaignModification)
- [Challenge Modification](#Challenge-Modification)

## Overview

This page contains notes found in the internals of Worms 3D on the
GameCube.

There appears to be an unofficial patch for the PC version that may
be learned from [Worms 3D Anniversary Patch](https://github.com/heatray/W3DPatch)

The cutting room floor pages for the [console](https://tcrf.net/Worms_3D_(GameCube,_PlayStation_2,_Xbox)
and [Windows](https://tcrf.net/Worms_3D_(Windows)) release also have some interesting notes.

## Files

### XOM

XOM files contain 3D geometry, textures, colors, and effects.
They are used to show in-game worm, weapon, and map objects.

May be able to be viewed with [xom-import](https://github.com/Psycrow101/Blender-3D-XOM-plugin).
Can be converted to XML for modification with [Xom2Xml](https://github.com/AlexBond2/Xom2Xml).

Here is an [example of a XOM file converted to XML](https://gist.github.com/NicholasMoser/38a5f0284f038f744de088f7f48f7506).

I can see that the artists used Maya as their editor based on this path in one of the bundle files:

```
C:/Documents and Settings/amorriss/My Documents/maya/projects/Worms3d/boggyb all clips.mb
```

### TGA

[Truevision TGA](https://en.wikipedia.org/wiki/Truevision_TGA) graphics files are textures
that can be opened and modified in Photoshop.

![TGA File](/tga.png?raw=true "TGA File")

### Lua

Worms 3D seems to utilize some lua scripting, which would make modding the game and creating
custom scenarios much easier.

### CSH

Currently unknown. Seems to accompany every map file for each time of day, for example:

```
countingsheep.xom
countingsheepDAY.csh
countingsheepEVENING.csh
countingsheepNIGHT.csh
```

### DOL

Like all GameCube games, the actual logic of the game is found in the `main.dol` file which is in PowerPC assembly.
You can disassemble the code using [Ghidra](https://ghidra-sre.org/) and
[Ghidra GameCube Loader](https://github.com/Cuyler36/Ghidra-GameCube-Loader).

## Text Modification

You can find all of the game text in `files\Language`. It looks like the developers originally created
csv files, such as `NGCMessages.csv`, and then converted them to XOM objects in the `files\Language\NGC`
directory. You therefore can modify these messages by modifying the respective XOM object, such as `American.xom`.

![Example of replacing text](/text_mod.png?raw=true "Example of replacing text")

## Weapon Modification

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

### WeapTwk.xom

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

Weapon damage is determined by this entry:

```xml
<WormDamageMagnitude>30</WormDamageMagnitude>
```

Here is an example of modifying this value to 100:

![Fire punch damage mod](compressed.gif?raw=true)

## Campaign Modification

Each campaign level seems to have its own lua file, making modification incredibly simple.
The first campaign level, D-Day, has the file `files\Scripts\dday.lua`.
You can for example easily change the names of each worm:

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

## Challenge Modification

The first challenge, Shotgun Challenge 1, can be found in the file `files\Scripts\TargetHunt.lua`.
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
