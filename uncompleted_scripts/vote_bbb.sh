#!/bin/bash

rm word.jpg
wget -ct0 "http://votacao.globo.com/rsvotacao/word.jpg?x=&y=1" -O word.jpg --save-cookies=cookies.txt --keep-session-cookies \
    --header='Host: votacao.globo.com' \
    --header='User-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2' \
    --header='Accept: image/png,image/*;q=0.8,*/*;q=0.5' \
    --header='Accept-Language: pt-br,en-us;q=0.7,en;q=0.3' \
    --header='Accept-Encoding: gzip,deflate' \
    --header='Accept-Charset: UTF-8,*' \
    --header='Keep-Alive: 115' \
    --header='Connection: keep-alive' \
    --header='Referer: http://bbb.globo.com/BBB10/Paredao/Votacao/0,,17411-p-2849,00.html' \
    --header='Pragma: no-cache' \
    --header='Cache-Control: no-cache'

# break
# mv word.jpg {decoded}.jpg
# echo Palavra Decodificada: {decoded}
# open -W decoded.jpg
# rm {decoded}.jpg

open -W word.jpg
echo -n "Palavra: "
read answer

wget -ct0 "http://votacao.globo.com/rsvotacao/vote" -O voto.html --save-headers --load-cookies=cookies.txt --max-redirect=0 \
    --header='Host: votacao.globo.com' \
    --header='User-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2' \
    --header='Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
    --header='Accept-Language: pt-br,en-us;q=0.7,en;q=0.3' \
    --header='Accept-Encoding: gzip,deflate' \
    --header='Accept-Charset: UTF-8,*' \
    --header='Keep-Alive: 115' \
    --header='Connection: keep-alive' \
    --header='Referer: http://bbb.globo.com/BBB10/Paredao/Votacao/0,,17411-p-2849,00.html' \
    --header='Content-Type: application/x-www-form-urlencoded' \
    --post-data="poll_id=2849&success_url=http%3A%2F%2Fbbb.globo.com%2FBBB10%2FParedao%2FVotacao%2F0%2C%2C17411-p-2849-1%2C00.html&error_url=http%3A%2F%2Fbbb.globo.com%2FBBB10%2FParedao%2FVotacao%2F0%2C%2C17411-p-2849-2-2%2C00.html&opt=2&answer=${answer}"

