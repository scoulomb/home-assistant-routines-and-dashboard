# SLZB buying guide

Optimisez votre Domotique zigbee: Découverte du dongle PoE SLZB-06 pour Zigbee2mqtt et ZHA
https://www.domo-blog.fr/optimisez-domotique-zigbee-avantages-dongle-poe-slzb-06-zigbee2mqtt-zha/

## MR1, 2 or 3


![](./media/SLZB-MR-Series-Evolution-of-Power.jpg)

Chip info
https://haade.fr/en/blog/efr32mg21-silabs-compatible-multiprotocol-zigbee-openthread-matter


CC2652P
Rank: 1
CC2652P (48Mhz, 88Kb RAM) is the Top 1 on our list. Reliability has been tested over the years and by many users. CC2652* chips are fully supported in Zigbee2MQTT (EFR32 has an “experimental” support status), and are also fully supported in ZHA. That is, it is a universal coordinator for both ZHA and Zigbee2MQTT. Zigbee firmware supports up to 200 end devices. Even with the maximum number of Zigbee devices, the chip parameters (processor 48Mhz and 88Kb RAM) are not even close to the maximum, so there is no difference in speed compared to other chips in the series (CC2652P7: 48Mhz+152Kb RAM, CC2674P10: 48Mhz+264Kb RAM). So, CC2652P is #1.

CC2652P7 [https://www.ti.com/product/CC2652P7]
Rank: 2
The CC2652P7 (48Mhz + 152 Kb RAM) has the same processor (48Mhz) as the CC2652P chips, but a slightly larger amount of RAM – 152Kb (CC2652P: 88Kb). At the same time, neither the processor nor the memory is used even by 30% when the chip is operating in coordinator mode with the maximum possible number of connected end devices. Therefore, this chip is more of a marketing ploy. Our recommendation is to pay attention to CC2652P. It is cheaper, more reliable (because it has been tested by a large number of users), and supports +20dB of gain at the firmware level. That is, If you like marketing gimmicks, the CC2652P7 is your choice. The CC2652P7 chip is ranked #2 in our rating.

CC2674P10 [https://www.ti.com/product/CC2674P10]
Rank: 4
The CC2674P7 (48Mhz + 264Kb RAM) has the same processor (48Mhz) as the CC2652P and CC2652P7 chips, but a slightly larger amount of RAM – 264Kb (CC2652P: 88Kb, CC2652P: 152Kb,). At the same time, neither the processor nor the memory is used even by 30% when the chip is operating in coordinator mode with the maximum possible number of connected end devices. Therefore, this chip is more of a marketing ploy. In addition, the firmware for this chip is in test mode. As of February 2024, we recommend that you buy these coordinators at your own risk, or if you are a firmware developer and you need a test device on this chip. Our recommendation is to pay attention to the CC2652P. It is cheaper, more reliable (as it has been tested by a large number of users), and supports +20 dB of gain at the firmware level. That is, if you like marketing gimmicks, CC2674P10 is your choice. The CC2674P10 chip takes the 4th place in our rating.

EFR32MG21 https://www.silabs.com/wireless/zigbee/efr32mg21-series-2-socs]
Rank: 1
The EFR32MG21 (80Mhz + 96Kb RAM) does not differ significantly from the CC2652P chips in terms of technical characteristics. However, there are a few things that the user should know: (1) This chip is ideal for working with ZHA (since the native Home Assistant coordinator is built on the same chip), but it is listed in the “experimental” section for Zigbee2MQTT. In practice, these chips show more stable operation than CC26** in Zigbee coordinator mode. In addition, although both EFR32MG21 and CC2652P chips have a +20dB amplifier, EFR32 chips usually show higher LQI with end devices. We put this chip on the 1st place along with the CC2652P chip in our rating.

EFR32MG24 [https://www.silabs.com/wireless/zigbee/efr32mg24-series-2-socs]
Rank: 3
EFR32MG24 (80Mhz + 256KbRAM) does not differ significantly from EFR32MG21 chip in terms of technical characteristics, except for the size of RAM: 256Kb versus 96Kb in EFR32MG21. The amount of RAM is at the level of the CC2674P10 chip. However, as in the case of the CC2674P10 chip, even with the maximum connection, the processor and RAM are not loaded to the maximum in EFR32MG21. So whether it makes sense to overpay for EFR32MG24 is a rhetorical question. Therefore, here we would say the same as with CC2652P7 and CC2674P10 – if you like marketing gimmicks, CC2674P10 is your choice. This chip takes the 3rd place in our rating.



MR2 chip regression?  
https://www.reddit.com/r/homeassistant/comments/1l08o4i/which_to_get_slzbmr1_mr3/

=> Decision to go for MR3 as not more expensive and more performant  
But customs duty: https://novapost.com/en-fr/international/receive-from-ukraine/  
Can consider MR1 then  
Price on AliExpress same as:  
- https://www.domadoo.fr/fr/produits-de-domotique/7773-smlight-slzb-mr1-adaptateur-usb-ethernet-poe-zigbee-thread-matter.html?srsltid=AfmBOoq-Q_HOiTYfwCSuK-8mVjkfQssO7iSDoqMLu9JaMErzn8zwQqz6  
- https://fr.aliexpress.com/item/1005008814854495.html?gatewayAdapt=glo2fra  

Note: MR series has one of SL and TI chip  
Unlike 06 series (which has a single chip)

## MRW10

Also bought MRW10 with Zwave proto

## Achats Zigbee Accessories

- 18,02€ | Tuya ZigBee 3.0 Smart Hub  
- 17,10€ | MOES Tuya Zigbee3.0 Smart IR Remote  
- 12,75€ | MOES Tuya WiFi IR RF Remote  
- 11,09€ | MOES Tuya Zigbee Smart Light Sensor  
- 8,47€ | SONOFF SNZB 02P ZigBee Temperature Sensor  
- ZigBee Smart Vibration Sensor  
- 6,35€ | Rain Sensor Alert Wifi Zigbee  
- 4,19€ | Tuya Wifi/Zigbee Temperature And Humidity Sensor  
- 12,75€ | Tuya ZigBee Smart IR Remote Control  
- 14,52€ | Haozee Tuya Smart Zigbee Rain Sensor  
- 6,58€ | MOES Tuya ZigBee WiFi Smart IR Remote Control  
- 12,70€ | UFO-R11 Zigbee Air Conditioner TV IR Remote  
- 12,14€ | SONOFF SNZB 02D Zigbee Temperature Humidity Sensor
