# Dol Header

Here are the header entries for the Worms 3D DOL file along with their respective values.

| Start |  End  |  Length |  Description                    |  Value              |
|-------|-------|---------|---------------------------------|---------------------|
| 0x0   |  0x3  |  4      |  File offset to start of Text0  |  0x100 (256)        |
| 0x4   |  0x7  |  4      |  File offset to start of Text1  |  0x300 (768)        |
| 0x8   |  0xB  |  4      |  File offset to start of Text2  |  0x0 **NOT USED**   |
| 0xC   |  0xF  |  4      |  File offset to start of Text3  |  0x0 **NOT USED**   |
| 0x10  |  0x13 |  4      |  File offset to start of Text4  |  0x0 **NOT USED**   |
| 0x14  |  0x17 |  4      |  File offset to start of Text5  |  0x0 **NOT USED**   |
| 0x18  |  0x1B |  4      |  File offset to start of Text6  |  0x0 **NOT USED**   |
| 0x1C  |  0x1F |  4      |  File offset to start of Data0  |  0x35B520 (3519776) |
| 0x20  |  0x23 |  4      |  File offset to start of Data1  |  0x364DE0 (3558880) |
| 0x24  |  0x27 |  4      |  File offset to start of Data2  |  0x3E7900 (4094208) |
| 0x28  |  0x2B |  4      |  File offset to start of Data3  |  0x418EA0 (4296352) |
| 0x2C  |  0x2F |  4      |  File offset to start of Data4  |  0x41B180 (4305280) |
| 0x30  |  0x33 |  4      |  File offset to start of Data5  |  0x0 **NOT USED**   |
| 0x34  |  0x37 |  4      |  File offset to start of Data6  |  0x0 **NOT USED**   |
| 0x38  |  0x3B |  4      |  File offset to start of Data7  |  0x0 **NOT USED**   |
| 0x3C  |  0x3F |  4      |  File offset to start of Data8  |  0x0 **NOT USED**   |
| 0x40  |  0x43 |  4      |  File offset to start of Data9  |  0x0 **NOT USED**   |
| 0x44  |  0x47 |  4      |  File offset to start of Data10 |  0x0 **NOT USED**   |
| 0x48  |  0x4B |  4      |  Loading address for Text0      |  0x80003100         |
| 0x4C  |  0x4F |  4      |  Loading address for Text1      |  0x80003300         |
| 0x50  |  0x53 |  4      |  Loading address for Text2      |  0x0 **NOT USED**   |
| 0x54  |  0x57 |  4      |  Loading address for Text3      |  0x0 **NOT USED**   |
| 0x58  |  0x5B |  4      |  Loading address for Text4      |  0x0 **NOT USED**   |
| 0x5C  |  0x5F |  4      |  Loading address for Text5      |  0x0 **NOT USED**   |
| 0x60  |  0x63 |  4      |  Loading address for Text6      |  0x0 **NOT USED**   |
| 0x64  |  0x67 |  4      |  Loading address for Data0      |  0x8035E520         |
| 0x68  |  0x6B |  4      |  Loading address for Data1      |  0x80367DE0         |
| 0x6C  |  0x6F |  4      |  Loading address for Data2      |  0x803EA900         |
| 0x70  |  0x73 |  4      |  Loading address for Data3      |  0x804A9880         |
| 0x74  |  0x77 |  4      |  Loading address for Data4      |  0x804B0C80         |
| 0x78  |  0x7B |  4      |  Loading address for Data5      |  0x0 **NOT USED**   |
| 0x7C  |  0x7F |  4      |  Loading address for Data6      |  0x0 **NOT USED**   |
| 0x80  |  0x83 |  4      |  Loading address for Data7      |  0x0 **NOT USED**   |
| 0x84  |  0x87 |  4      |  Loading address for Data8      |  0x0 **NOT USED**   |
| 0x88  |  0x8B |  4      |  Loading address for Data9      |  0x0 **NOT USED**   |
| 0x8C  |  0x8F |  4      |  Loading address for Data10     |  0x0 **NOT USED**   |
| 0x90  |  0x93 |  4      |  Section sizes for Text0        |  0x200 (512)        |
| 0x94  |  0x97 |  4      |  Section sizes for Text1        |  0x35B220 (3519008) |
| 0x98  |  0x9B |  4      |  Section sizes for Text2        |  0x0 **NOT USED**   |
| 0x9C  |  0x9F |  4      |  Section sizes for Text3        |  0x0 **NOT USED**   |
| 0xA0  |  0xA3 |  4      |  Section sizes for Text4        |  0x0 **NOT USED**   |
| 0xA4  |  0xA7 |  4      |  Section sizes for Text5        |  0x0 **NOT USED**   |
| 0xA8  |  0xAB |  4      |  Section sizes for Text6        |  0x0 **NOT USED**   |
| 0xAC  |  0xAF |  4      |  Section sizes for Data0        |  0x98C0 (39104)     |
| 0xB0  |  0xB3 |  4      |  Section sizes for Data1        |  0x82B20 (535328)   |
| 0xB4  |  0xB7 |  4      |  Section sizes for Data2        |  0x315A0 (202144)   |
| 0xB8  |  0xBB |  4      |  Section sizes for Data3        |  0x22E0 (8928)      |
| 0xBC  |  0xBF |  4      |  Section sizes for Data4        |  0x1940 (6464)      |
| 0xC0  |  0xC3 |  4      |  Section sizes for Data5        |  0x0 **NOT USED**   |
| 0xC4  |  0xC7 |  4      |  Section sizes for Data6        |  0x0 **NOT USED**   |
| 0xC8  |  0xCB |  4      |  Section sizes for Data7        |  0x0 **NOT USED**   |
| 0xCC  |  0xCF |  4      |  Section sizes for Data8        |  0x0 **NOT USED**   |
| 0xD0  |  0xD3 |  4      |  Section sizes for Data9        |  0x0 **NOT USED**   |
| 0xD4  |  0xD7 |  4      |  Section sizes for Data10       |  0x0 **NOT USED**   |
| 0xD8  |  0xDB |  4      |  BSS address                    |  0x8041BEA0         |
| 0xDC  |  0xDF |  4      |  BSS size                       |  0x94DD4 (609748)   |
| 0xE0  |  0xE3 |  4      |  Entry point                    |  0x80003100         |
| 0xE4  |  0xFF |  28     |  padding                        |  0x0                |

Reverse engineering shows these sections to correspond to each data section:

- Data0 = .data
  - Also contains .ctors at the start
- Data1 = .rodata
- Data2 = .dtors
- Data3 = .sdata
- Data4 = .sdata2

The reverse engineering was accomplished by comparing to the symbol map in the European
Worms 3D version on the PS2, which is included with the ELF file.
