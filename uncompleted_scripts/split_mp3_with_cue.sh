#!/bin/bash

mpg123="/usr/bin/mpg123"
bchunk="/usr/bin/bchunk"
cdrecord="/usr/bin/cdrecord"
device="0,0,0"

if [ "$#" != "3" ]; then
	echo "Uso: $0 arquivo.mp3 arquivo.cue diretorio_de_trabalho" >&2
	exit 1
fi

if [ "`id -u`" != "0" ]; then
	echo "É necessário ser root para usar esse script." >&2
	exit 2
fi

mp3file="$1"

if [ ! -f "$mp3file" ]; then
	echo "Arquivo $mp3file não encontrado." >&2
	exit 3
fi

cuefile="$2"

if [ ! -f "$cuefile" ]; then
	echo "Arquivo $cuefile não encontrado." >&2
	exit 3
fi

workdir="$3"

if [ ! -d "$workdir" ]; then
	echo "Diretório de trabalho $workdir não existe." >&2
	exit 3
fi

cd $workdir
echo "Gerando arquivo de audio..."
$mpg123 -sv "$mp3file" > alldisk.pcm 2> record.log
echo "Quebrando arquivo de audio de acordo com cuesheet..."
$bchunk alldisk.pcm "$cuefile" tracks >> record.log 2>&1
rm -f alldisk.pcm >> record.log 2>&1
echo "Gravando o CD (device: $device)..."

while true; do
	$cdrecord dev=$device -swab -v -dao -audio tracks??.cdr >> record.log 2>&1
	if [ "$?" != "0" ]; then
		echo -n "Insira o CD no drive e confirme o processo de gravação. [S/n]?"
		read resp
		if [ "$resp" == "n" || "$resp" == "N" ]; then
			rm -f tracks??.cdr >> record.log 2>&1
			exit 4
		fi
	else
		break
	fi
done

rm -f tracks??.cdr >> record.log 2>&1
cd -
