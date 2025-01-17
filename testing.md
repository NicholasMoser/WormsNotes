# Testing

To test weapons, you can just load a singleplayer
campaign or mission and modify the Lua file to add
all weapons. Here's the full list:

## WeaponInventory

- Bazooka
- Grenade
- ClusterGrenade
- Airstrike
- Dynamite
- HolyHandGrenade
- BananaBomb
- Landmine
- Shotgun
- BaseballBat
- Prod
- VikingAxe
- FirePunch
- HomingMissile
- Mortar
- HomingPidgeon
- Earthquake
- Sheep
- MineStrike
- PetrolBomb
- GasCanister
- SheepStrike
- MadCow
- OldWoman
- ConcreteDonkey
- NuclearBomb
- Armageddon
- MagicBullet
- SuperSheep
- Girder
- BridgeKit
- NinjaRope
- Parachute
- ScalesOfJustice
- LowGravity
- QuickWalk
- LaserSight
- Teleport
- Jetpack
- SkipGo
- Surrender
- ChangeWorm
- Freeze
- Blowpipe
- LotteryStrike
- DoctorsStrike
- MegaMine
- StickyBomb
- Binoculars
- Redbull

## Code to Add All Weapons

```lua
    lock, inventory = EditContainer("Inventory.Team00") 
    inventory.Bazooka = -1
    inventory.Grenade = -1
    inventory.ClusterGrenade = -1
    inventory.Airstrike = -1
    inventory.Dynamite = -1
    inventory.HolyHandGrenade = -1
    inventory.BananaBomb = -1
    inventory.Landmine = -1
    inventory.Shotgun = -1
    inventory.BaseballBat = -1
    inventory.Prod = -1
    inventory.VikingAxe = -1
    inventory.FirePunch = -1
    inventory.HomingMissile = -1
    inventory.Mortar = -1
    inventory.HomingPidgeon = -1
    inventory.Earthquake = -1
    inventory.Sheep = -1
    inventory.MineStrike = -1
    inventory.PetrolBomb = -1
    inventory.GasCanister = -1
    inventory.SheepStrike = -1
    inventory.MadCow = -1
    inventory.OldWoman = -1
    inventory.ConcreteDonkey = -1
    inventory.NuclearBomb = -1
    inventory.Armageddon = -1
    inventory.MagicBullet = -1
    inventory.SuperSheep = -1
    inventory.Girder = -1
    inventory.BridgeKit = -1
    inventory.NinjaRope = -1
    inventory.Parachute = -1
    inventory.ScalesOfJustice = -1
    inventory.LowGravity = -1
    inventory.QuickWalk = -1
    inventory.LaserSight = -1
    inventory.Teleport = -1
    inventory.Jetpack = -1
    inventory.SkipGo = -1
    inventory.Surrender = -1
    inventory.ChangeWorm = -1
    inventory.Freeze = -1
    inventory.Blowpipe = -1
    inventory.LotteryStrike = -1
    inventory.DoctorsStrike = -1
    inventory.MegaMine = -1
    inventory.StickyBomb = -1
    inventory.Binoculars = -1
    inventory.Redbull = -1
    CloseContainer(lock)
```

![All Weapons](img/all_weapons.png?raw=true)
