# Worms 3D Notes

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

You can find all of the game text in `Worms3D\files\Language`. It looks like the developers originally created
csv files, such as `NGCMessages.csv`, and then converted them to XOM objects in the `Worms3D\files\Language\NGC`
directory. You therefore can modify these messages by modifying the respective XOM object, such as `American.xom`.

![Example of replacing text](/text_mod.png?raw=true "Example of replacing text")

## Weapon Modification

Health is set at instruction 0x80140f3c in the `main.dol`:

```c
undefined4 update_health(Worm *worm,int param_2)
{
  float fVar1;
  double dVar2;
  double local_10;
  
  if ((int)worm->health != worm->new_health) {
                    /* Worm has taken damage.
                       Convert param_2 - worm->field35_0x2c and worm->new_health from ints to
                       doubles */
    local_10 = (double)CONCAT44(0x43300000,param_2 - worm->field35_0x2c ^ 0x80000000);
    dVar2 = local_10 - _DAT_8039f5f0;
    local_10 = (double)CONCAT44(0x43300000,worm->new_health);
    fVar1 = (float)dVar2 * _DAT_8039f5f8 + worm->health;
                    /* Set whichever is smaller, not sure what the other number is */
    if (fVar1 <= (float)(local_10 - _DAT_8039f600)) {
      worm->health = fVar1;
    }
    else {
      worm->health = (float)(local_10 - _DAT_8039f600);
    }
    zz_80141410_(worm);
  }
  worm->field35_0x2c = param_2;
  return 0;
}
```

If a worm has taken damage, the damage will be set to `worm->new_health` (offset 0x24).

Damage is subtracted from total health at instruction 0x80149598. Damage is set at 0x80148f3c which is passed in as the
second parameter of the method starting at 0x80148e8c.

Damage is calculated at the function at 0x80143bdc, which will be called `calculate_damage`.
Blast damage is calculated at the function at 0x80148a58, which will be called `calculate_blast_damage`.
Somewhere in these methods, it must account for the weapon being used. Let's start by just looking at Fire Punch,
which appears to always do 30 damage. The 30 must be stored somewhere we can modify.

Unfortunately, the call stack above this point looks like this code is determined via an interpreter of some sort.
Therefore, it may be related to the lua files included on the disk. I searched each lua file but didn't see any relevant
references to the number 30 in decimal or hex.

It could also be related to the "Weap" files in the root directory of the disk:

- WeapLvl2.xom
- WeapLvl3.xom
- WeapLvl4.xom
- WeapLvl5.xom
- WeapTwk.xom

Googling this file seems to reveal that this is exactly what I was looking for: https://t17forum.worms2d.info/index.php/t-39070.html

WeapTwk.xom has values such as:

```
file Tweak\WeapTwk.xml
#Bomber.NumBombs = 20
edit kWeaponBazooka-0
IsLowGravity = false
quick * Bomblet
Num*s = 5
*MaxConeAngle = 0.90
*MaxSpeed = -0.2
*MinSpeed = -0.1
*WeaponName = kWeaponGrenade
quick $ Magnitude
quick % Radius
WormDamage$ = 35
LandDamage% = 30
edit kWeaponClusterGrenade-0
NumBomblets = 20
BombletMaxSpeed = 0.75
BombletMaxConeAngle = 0.05
file Tweak\Tweak.xml
#Ninja.NumShots *= 2
#Ninja.MaxLength = 9999
#Ninja.WormMass = 0.8
```
