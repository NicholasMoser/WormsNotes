'''
Creates C# class files from XOMSCHM.dat
'''
import os
import sys
from lxml import objectify

def main():
    if not os.path.isfile('XOMSCHM.dat'):
        print('Missing XOMSCHM.dat')
        sys.exit(1)

    with open('XOMSCHM.dat', 'r') as xomschm:
        text = xomschm.read()
        tree = objectify.fromstring(text)

    for element in tree.XContainer.getchildren():
        handle_container(element)

def handle_container(element):
    print(f'XContainer {element.tag}')
    name = element.tag
    code = get_code_header(name)
    types = []
    for entry in element.getchildren():
        attrib = entry.attrib
        text = entry.text
        if 'id' in attrib and attrib['id'] == 'XRef':
            handle_container(entry)
        elif 'Xtype' in attrib and attrib['Xtype'] == 'XClass':
            handle_container(entry)
        elif 'Xtype' in attrib and attrib['Xtype'] == 'XCollection':
            print(f'XCollection {entry.tag}')
        elif text == 'XString':
            print(f'XString {entry.tag}')
        elif text == 'XBool':
            print(f'XBool {entry.tag}')
        elif text == 'XUInt':
            print(f'XUInt {entry.tag}')
        elif text == 'XInt':
            print(f'XInt {entry.tag}')
        elif text == 'XUInt16':
            print(f'XUInt16 {entry.tag}')
        elif text == 'XInt16':
            print(f'XInt16 {entry.tag}')
        elif text == 'XUInt8':
            print(f'XUInt8 {entry.tag}')
        elif text == 'XInt8':
            print(f'XInt8 {entry.tag}')
        elif text == 'XFloat':
            print(f'XFloat {entry.tag}')
        elif text == 'XEnum':
            print(f'XEnum {entry.tag}')
        elif text == 'XUIntHex':
            print(f'XUIntHex {entry.tag}')
        elif text == 'XBoundBox':
            print(f'XBoundBox {entry.tag}')
        elif text == 'XVector4f':
            print(f'XVector4f {entry.tag}')
        elif text == 'XMatrix':
            print(f'XMatrix {entry.tag}')
        elif text == 'XMatrix34':
            print(f'XMatrix34 {entry.tag}')
        elif 'x' in attrib and 'y' in attrib and attrib['x'] == 'XFloat':
            print(f'Vector2 {entry.tag}')
        elif 'x' in attrib and 'y' in attrib and 'z' in attrib and attrib['x'] == 'XFloat':
            print(f'Vector3 {entry.tag}')
        elif 'r' in attrib and 'g' in attrib and 'b' in attrib and 'a' in attrib and attrib['r'] == 'XUInt8':
            print(f'Color {entry.tag}')
        elif 'href' in attrib:
            href = attrib['href']
            print(f'XReference {entry.tag} to {href}')
        elif entry.tag == 'comment':
            print(f'Skip comment')
        else:
            print(f'error {entry.tag}')
            sys.exit(1)

def get_code_header(name):
    return f'''using System;
using System.Collections.Generic;
using System.IO;
using CrateModLoader.GameSpecific.WormsForts;
using CrateModLoader.GameSpecific.WormsForts.XOM;

namespace Xombie.CrateModGames.GameSpecific.Worms.Common.API.XOM.Containers.Worms3D
{{
    [XOM_TypeName("{name}")]
    public class {name} : Container
    {{
'''

if __name__ == "__main__":
    main()
