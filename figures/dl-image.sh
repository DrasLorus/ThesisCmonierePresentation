#! /bin/bash

if (($# > 0)); then
  hpl=(
    "https://agora.resposta.net/wp-content/uploads/2019/10/71765192.cms-800x445.jpeg"
    "https://www.techdotmatrix.com/wp-content/uploads/2017/02/5G-logo.jpg"
    "https://www.extremetech.com/wp-content/uploads/2015/04/LTE-Logo-300x300.jpg"
    "https://logodownload.org/wp-content/uploads/2014/04/wi-fi-wireless-logo-2048x1293.png"
    "https://seritag.com/images/b/NFC-Forum-NFCW-65.png"
    "https://www.akcp.com/wp-content/uploads/2020/05/Zigbee-Logo-300x72.png"
    "https://devopedia.org/images/article/91/5386.1599139021.png"
    "https://www.zooco.io/blog/wp-content/uploads/2017/10/Sigfox-Logo.png"
    "https://select.advantech.com/wise-iot-sensing-devices/files/2019/02/Logo_NB-IoT-1-1.png"
  )
  out=(
    "6G-logo.jpeg"
    "5G-logo.jpeg"
    "LTE-logo.jpeg"
    "wi-fi-logo.tmp.png"
    "NFC-logo.tmp.png"
    "Zigbee-logo.tmp.png"
    "LoRa-logo.tmp.png"
    "Sigfox-logo.tmp.png"
    "NB-IoT-logo.tmp.png"
  )

  for ((j = 0; j < ${#hpl[@]}; j++)); do
    wget "${hpl[$j]}" -O "${out[$j]}"
  done
fi

convert 6G-logo.jpeg -trim -auto-threshold OTSU 6G-logo.tmp.png
convert 6G-logo.tmp.png -transparent white -trim 6G-logo.png
rm 6G-logo.tmp.png 6G-logo.jpeg 

convert 5G-logo.jpeg -transparent white -trim 5G-logo.png
rm 5G-logo.jpeg 

convert LTE-logo.jpeg -transparent white -trim LTE-logo.png
rm LTE-logo.jpeg 

convert LoRa-logo.tmp.png -transparent white -trim LoRa-logo.png
rm LoRa-logo.tmp.png

convert NFC-logo.tmp.png -transparent white -trim NFC-logo.png
rm NFC-logo.tmp.png

convert NB-IoT-logo.tmp.png -trim NB-IoT-logo.png
rm NB-IoT-logo.tmp.png

convert Zigbee-logo.tmp.png -trim Zigbee-logo.png
rm Zigbee-logo.tmp.png

convert Sigfox-logo.tmp.png -trim Sigfox-logo.png
rm Sigfox-logo.tmp.png

convert wi-fi-logo.tmp.png -trim wi-fi-logo.png
rm wi-fi-logo.tmp.png
