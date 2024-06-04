This repository is developed in Lapland UAS Arctic Beekeeping project

https://www.facebook.com/Arktinenmehilainen/

https://www.lapinamk.fi/fi/Yrityksille-ja-yhteisoille/Lapin-AMKin-hankkeet?RepoProject=4208000101

---

# tequ-bee-nest-scale

This is repository of Bee Nest scale prototype device. Prototype is developed for Pycom Lopyv4 development board and each prototype can monitor weight of the single bee nest. Each unit is connected LoRaWAN network where data is also sent every 6 hours.

Collected sensor data can be found and accessed using Bee-Apps, Datatool found from https://dash.tequ.fi.

## Hardware
List of the hardware used in prototype

| Hardware               | Model         | Placement       | Link          |
| -------------          |:-------------:| :-------------: | :-------------:|
| Board                  | Lopy v4       | Control box     | <a href="https://docs.pycom.io/datasheets/development/lopy4/">Link</a>|
| Sparkfun OpenScale     | SEN-13261     | Control box     | <a href="https://www.sparkfun.com/products/13261">Link</a>|
| Temperature sensor     | DS18B20       | Control box     | <a href="https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf">Data sheet</a>|
| Scale unit             | Zemic L6W-C3-200kg-3G6   | Control box    | <a href="https://www.zemiceurope.com/media/Documentation/L6W_Datasheet.pdf">Data sheet</a>|
| Adafruit MiniBoost 5V @ 1A        | TPS61023       | Control box     | <a href="https://www.adafruit.com/product/4654">Data sheet</a>| |
| Battery holder         | CA 3 GS       | Control box     | |
| Batteries              | 3 x 1.5 AA    | Control box     | |
| Antenna                | 868 MHz    | Control box     | |

## Example mechanics for scale platform

Profican aluminium parts:

- 8 pieces of 40x25-N1102
- 45x90- N 0166, 2 pieces of 35 cm aluminium profiles
- 45x45- N 0165, 4 pieces of 56 cm aluminium profiles
- N 1205, 4 pieces, adjustment of platform
- 2 cm thick plywood, 60 x 60 cm, attached to aluminium frame

## Connections
Connections of the hardware used in prototype.
| Device                 | PIN           | Device         | PIN            | 
| -------------          |:-------------:| :-------------:| :-------------:|
| Lopy v4                | Vin           |  Battery                           | +              |
| Lopy v4                | GND           |  Battery                           | -              |
| Lopy v4                | TX            |  SEN-13261                         | TX             |
| Lopy v4                | RX            |  SEN-13261                         | RX             |
| Lopy v4                | P2            |  TPS61023                          | EN             |
| 868 MHz antenna        | uFl plug      |  Lopy v4                           | 868 MHz connector |
| DS18B20                | 5V SIG GND    |  SEN-13261                         | TEMP connector    |
| TPS61023               | OUT           |  SEN-13261                         | 5V             |
| Battery                | -             |  SEN-13261                         | GND            |
| SEN-13261              | E+            |  Zemic L6W-C3-200kg-3G6            | Input (+)      |
| SEN-13261              | E-            |  Zemic L6W-C3-200kg-3G6            | Input (-)      |
| SEN-13261              | A+            |  Zemic L6W-C3-200kg-3G6            | Output (+)     |
| SEN-13261              | A-            |  Zemic L6W-C3-200kg-3G6            | Output (-)     |
| SEN-13261              | SHD           |  Zemic L6W-C3-200kg-3G6            | Shield         |


## Development

### 1. Clone this repository
```
git clone https://github.com/Lapland-UAS-Tequ/tequ-bee-nest-heater.git
```

### 2. Create config.json file to local directory

```
{
  "SSID": "",
  "SIGFOX": false,
  "WLAN": false,
  "LORA_APP_KEY": "",
  "SERVER_URL": "",
  "LORAWAN": true,
  "LORA_APP_EUI": "",
  "PASSWORD": "",
  "DCDC_ENABLE_PIN":"P2"
}

```
- ssid = (not used)
- password = (not used)
- SIGFOX = (not used)
- WLAN =  (not used)
- LORA_APP_KEY = LoRaWAN application key
- LORA_APP_EUI = LoRaWAN APP EUI
- SERVER_URL = (not used)
- LORAWAN = false/true, enable or disable LORAWAN 
- WLAN = false/true, enable or disable WLAN (not used)
- DCDC_ENABLE_PIN = PIN ID that TPS61023 control signal is connected


### 3. Install development environment

https://docs.pycom.io/gettingstarted/software/atom/

### 4. Update LoPy firmware

https://docs.pycom.io/updatefirmware/

### 5. Build connections

### 6. Configure Sparkfun OpenScale

See image "scale_asetukset.PNG" in this repository and configure your scale with same settings.

### 7. Upload project to Lopy v4 and test its working

### 8. Start developing!

### OPTIONAL Register device to Digita´s LoRaWAN portal

https://i5u4t3.internetofthings.ibmcloud.com/dashboard/

### OPTIONAL Register device to Tequ´s IBM Cloud Watson IoT Platform

https://i5u4t3.internetofthings.ibmcloud.com/dashboard/

Device Type = bee-scale
Device ID = <LORAWAN DEV EUI>
mqtt_authtoken = generate randomly
