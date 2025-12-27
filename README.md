# 🛠️ HOST-MASTER (SysAdmin Practice Tool)

![Python](https://img.shields.io/badge/python-3.x-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Focus](https://img.shields.io/badge/focus-Hosting%20Diagnostics-orange?style=for-the-badge)
![Platform](https://img.shields.io/badge/stack-LAMP%20%2F%20LEMP-green?style=for-the-badge)

**CLI diagnosztikai eszköz, amelyet a Web Hosting és VPS hibaelhárítási folyamatok gyakorlására és automatizálására fejlesztettem.**

Ezt a projektet azzal a céllal hoztam létre, hogy mélyebben megértsem a szerverüzemeltetés során felmerülő leggyakoribb L1/L2 szintű hibajegyek (ticketek) technikai hátterét. A script a manuális parancssori ellenőrzéseket (permission fix, service restart, mailq check) fogja össze egyetlen Python logikába.

## 🎯 MIÉRT KÉSZÜLT?

Egy nagy szolgáltatónál (mint pl. ATW, Telekom) elengedhetetlen, hogy a rendszergazda ne csak használja a belső eszközöket, hanem értse is a mögöttes Linux folyamatokat.

A **Host-Master** bizonyítja, hogy rendelkezem az alábbi ismeretekkel:
* **Szolgáltatás menedzsment:** Hogyan kell kezelni a leállt `Nginx`, `Apache` vagy `MySQL` folyamatokat.
* **Jogosultsági körök:** A `644` (fájl) és `755` (mappa) szabványok ismerete és automatizált javítása.
* **Levelezés diagnosztika:** A `Postfix` sorban álló levelek (`mailq`) elemzése és spam-gyanú felismerése.
* **Rendszerfelügyelet:** Lemezterület és SSL tanúsítványok kritikus állapotának monitorozása.

## 🛠️ FUNKCIÓK A GYAKORLATBAN

A script az alábbi gyakori "Ticket-szituációkat" szimulálja és oldja meg:

### 1. "Nem tölt be az oldal" (Service Check)
A script ellenőrzi a futó processzeket. Ha az `Nginx` vagy `PHP-FPM` váratlanul leállt, a rendszer naplózza az eseményt és megkísérli az újraindítást.

### 2. "Nem tudok képet feltölteni / 403 Forbidden" (Permission Fixer)
Gyakori hiba, amikor az ügyfél FTP-n rossz jogokkal tölt fel fájlokat. A script rekurzívan beállítja a helyes Linux jogosultságokat a webgyökérben.

### 3. "Nem mennek ki a levelek" (Mail Queue)
Lekérdezi a Postfix állapotát. Ha a várakozó levelek száma átlép egy küszöbértéket, az potenciális SPAM-támadásra vagy feltört fiókra utal.

### 4. "Nem biztonságos az oldal" (SSL Check)
Python `ssl` modullal ellenőrzi a tanúsítvány lejárati dátumát közvetlenül a porton keresztül.

## 📥 TELEPÍTÉS ÉS KIPRÓBÁLÁS

```bash
# 1. Letöltés
wget [https://raw.githubusercontent.com/aaron-devop/host-master/main/host_master.py](https://raw.githubusercontent.com/aaron-devop/host-master/main/host_master.py)

# 2. Futtatás (Root jogosultság szükséges a rendszerműveletekhez)
sudo python3 host_master.py
```

## 🖥️ MINTA KIMENET

```text
HostMaster > 1

[OK] nginx fut.
[HIBA] mysql LEÁLLT! Újraindítás...
[OK] php8.1-fpm fut.
```

## 📜 LICENC
MIT License
