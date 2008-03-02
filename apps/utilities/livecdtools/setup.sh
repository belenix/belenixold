#! /usr/bin/bash


#
# Do not execute keyboard selection here for now
# We are using kbd -s.
#
if [ `/usr/bin/false` ]
then

kbd_type=`/usr/bin/kbd -t`
DIALOG=/usr/bin/dialog

tag_values="33 US-English 32 UK-English 6 Danish 18 Dutch 8 French 9 German 14 Italian 15 Japanese(106) 271 Japanese-type6 16 Korean 19 Norwegian 22 Portuguese 25 Spanish 26 Swedish 27 Swiss-French 28 Swiss-German 30 Taiwanese 23 Russian 264 Albanian 261 Belarusian 2 Belgian 260 Bulgarian 259 Croatian 5 Czech 34 Czech(Qwerty) 7 Finnish 4 French-Canadian 12 Hungarian 10 Greek 258 Icelandic 17 Latin-American 265 Lithuanian 266 Latvian 267 Macedonian 263 Malta_UK 262 Malta_US 21 Polish 257 Serbia-And-Montenegro 256 Slovenian 24 Slovakian 31 TurkishQ 35 TurkishF"

labels["33"]="US-English"
labels["32"]="UK-English"
labels["6"]="Danish"
labels["18"]="Dutch"
labels["8"]="French"
labels["9"]="German"
labels["14"]="Italian"
labels["15"]="Japanese(106)"
labels["16"]="Korean"
labels["19"]="Norwegian"
labels["22"]="Portuguese"
labels["25"]="Spanish"
labels["26"]="Swedish"
labels["27"]="Swiss-French"
labels["28"]="Swiss-German"
labels["30"]="Taiwanese"
labels["23"]="Russian"
labels["271"]="Japanese-type6"
labels["264"]="Albanian"
labels["261"]="Belarusian"
labels["2"]="Belgian"
labels["260"]="Bulgarian"
labels["259"]="Croatian"
labels["5"]="Czech"
labels["7"]="Finnish"
labels["4"]="French-Canadian"
labels["12"]="Hungarian"
labels["10"]="Greek"
labels["258"]="Icelandic"
labels["17"]="Latin-American"
labels["265"]="Lithuanian"
labels["266"]="Latvian"
labels["267"]="Macedonian"
labels["263"]="Malta_UK"
labels["262"]="Malta_US"
labels["21"]="Polish"
labels["257"]="Serbia-And-Montenegro"
labels["256"]="Slovenian"
labels["24"]="Slovakian"
labels["31"]="TurkishQ"
labels["25"]="TurkishF"


cat > /tmp/xkbmap <<EOF
US-English:us
UK-English:gb
Czech:cz
Danish:dk
Dutch:nl
French:fr
French-Canadian:ca(fr)
German:de
Greek:gr
Hungarian:hu
Italian:it
Japanese(106):jp
Japanese-type6:jp
Latvian:lv
Lithuanian:lt
Polish:pl:us
Korean:us
Norwegian:no
Portuguese:pt
Russian:ru
Spanish:es
Swedish:se
Swiss-French:ch
Swiss-German:ch
Taiwanese:vn
TurkishQ:tr
TurkishF:tr
Albanian:al
Belarusian:be
Belgian:be
Bulgarian:bg
Croatian:hr
Czech(Qwerty):cz_qwerty
Finnish:fi
Icelandic:is
Latin-American:la
Macedonian:mk
Malta_UK:gb
Malta_US:us
Serbia-And-Montenegro:us
Slovenian:si
Slovakian:sk
EOF

$DIALOG --nocancel --menu 'Please select your keyboard layout from the list...' 20 70 12 $tag_values 2> /tmp/kb

if [ -f /tmp/kb ]
then
	type=`cat /tmp/kb`
	if [ "$type" = "" ]
	then
		type="1"
	fi
else
	type="1"
fi

if [ "$type" = "34" ]
then
		type="7"
fi

desc=${labels[$type]}
#/usr/sbin/eeprom keyboard-layout=$desc
echo "LAYOUT=$desc" >> /etc/default/kbd

xkblayout=`/usr/bin/grep "$desc" /tmp/xkbmap | /usr/bin/head -n 1 | /usr/bin/cut -f2 -d":"`

echo -n $xkblayout > /.xkblayout

fi
# Keyboard selection commented here for now.



if [ ! -f /.lg3d ]
then
	tag_values="A \"Xfce Desktop\" B \"KDE Desktop\" C \"Command Line Login\" D \"Compiz 3D Manager + Xfce (Nvidia/Intel)\" E \"Compiz 3D Manager + KDE (Nvidia/Intel)\""
else
	tag_values="A \"Xfce Desktop\" B \"Looking Glass 3D Desktop\" C \"Command Line Login\""
fi
eval "$DIALOG --nocancel --menu 'Desktop UI Selection' 20 70 12 $tag_values 2> /.desk"

type="1"
if [ -f /.desk ]
then
	type=`/usr/bin/cat /.desk`

	if [ "$type" = "E" ]
	then
		type="5"

	elif [ "$type" = "D" ]
	then
		type="4"

	elif [ "$type" = "C" ]
	then
		type="3"

	elif [ "$type" = "B" ]
	then
		type="2"
	else
		type="1"
	fi
fi

echo $type > /.desk
