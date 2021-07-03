# Fitxategi hau entrenamendurako datuak lortzen eta preprozesatzen ditu.

import csv
import tweepy
import time
import configparser

# Twitter API-aren konexioa
# info.properties fitxategia irakurri
config = configparser.ConfigParser()
config.read('../info.properties')

consumer_key = config.get('APIkey', 'consumer_key')
consumer_secret = config.get('APIkey', 'consumer_secret')


auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

"""  
TWEEPY-REN KONEXIOA PROBATZEKO 
for tweet in tweepy.Cursor(api.search, q = 'tweepy').items(10):
    print(tweet.text)    
"""


def datuak_transformatu():
    # Metodo hau datuak preprozesatzen ditu (id-tik datuetara pasatu eta berriro .csv batean gorde)

    # Denboraren kontrola eramateko
    hasiera_denbora = time.time()

    # Lehenengo, sarrerako datuak lortuko dira
    with open('twitter_human_bots_dataset.csv') as sarrera_datuak:
        # Irakurtzailea objetua sortu
        csv_reader = csv.reader(sarrera_datuak, delimiter=',')
        # Datuak berriro idazteko
        with open('datu_eguneratuak.csv', mode='w', newline='') as datueguneratuak:
            # Idazlea objetua sortu
            datuak_writer = csv.writer(datueguneratuak)

            # Zenbat erabiltzaile topatu ez diren zenbatzeko
            user_not_found = 0

            for kont, row in enumerate(csv_reader):
                # 100 iterazio behin abisatzen du
                if (kont % 100) == 0:
                    print("############################################# " + str(kont) + ". ITERAZIOA ##############################################")
                    # denbora kalkulatu
                    exekuzio_denbora = time.time() - hasiera_denbora
                    denbora_erakutsi(exekuzio_denbora)

                # Erabiltzaile bakoitzaren data lortu
                userdata = idtik_datara(row[0], row[1])
                # Erabilzailea aurkitu bada
                if len(userdata) != 0:
                    datuak_writer.writerow(userdata)
                # Bestela zenbat txarto dauden zenbatu
                else:
                    user_not_found += 1


    # Amaierako datuak hobeto ikusteko
    print("##############################################################################################")
    print()
    print()
    print()

    # denbora totala kalkulatu
    exekuzio_denbora = time.time() - hasiera_denbora
    print("DATUEN PREPROZESAMENDUAREN DENBORA TOTALA: ")
    denbora_erakutsi(exekuzio_denbora)
    print()

    # Zenbat erabiltzaile topatu ez diren aurkeztu
    print("ZENBAT ERABILTZAILE EZ DIRA TOPATU: " + str(user_not_found))


def idtik_datara(user_id, klasea):
    # Metodo hau erabiltzaile baten id-a emanda erabiltzaileri buruzko informazioa lortzen du

    userdata = []

    try:
        user = api.get_user(user_id)

        #atributuak lortu
        userdata.append(informazioa_dauka(user.location))
        userdata.append(informazioa_dauka(user.profile_location))
        userdata.append(informazioa_dauka(user.description))
        userdata.append(informazioa_dauka(user.url))
        userdata.append(1 if user.protected else 0)
        userdata.append(user.followers_count)
        userdata.append(user.friends_count)
        userdata.append(user.listed_count)
        userdata.append(informazioa_dauka(user.favourites_count))
        userdata.append(informazioa_dauka(user.utc_offset))
        userdata.append(informazioa_dauka(user.geo_enabled))
        userdata.append(1 if user.verified else 0)
        userdata.append(informazioa_dauka(user.statuses_count))
        userdata.append(informazioa_dauka(user.lang))
        userdata.append(1 if user.contributors_enabled else 0)
        userdata.append(informazioa_dauka(user.profile_background_image_url))
        userdata.append(informazioa_dauka(user.profile_image_url))
        #userdata.append(informazioa_dauka(user.profile_banner_url))

        #klasea
        userdata.append(1 if klasea == "human" else 0)

    except tweepy.RateLimitError:
        # Tweepy-ren rate limit salbuespena kudeatu: 15 minutu itxaron
        print("Tweepy-ren 'rate limit' salbuespena: 15 minutu itxaron dei gehiago egiteko.")
        print("Itxaroten ... ")
        time.sleep(15 * 60)
        print("Jarraitu!")

    except tweepy.TweepError as e:
        print(str(user_id) + " Erabiltzailea ez da topatu!")

    return userdata


def informazioa_dauka(info):
    # Metodo hau 0 bueltatzen du informazioa ematen ez bazaio, 1 beztela
    if info is None:
        return 0
    else:
        return 1


def denbora_erakutsi(exekuzio_denbora):
    # Metodo hau programaren exekuzio denbora txukun inprimatzen du
    egun = exekuzio_denbora // (24 * 3600)
    exekuzio_denbora %= (24 * 3600)
    ordu = exekuzio_denbora // 3600
    exekuzio_denbora %= 3600
    minutu = exekuzio_denbora // 60
    exekuzio_denbora %= 60
    segundu = exekuzio_denbora
    print("Egun:Ordu:Minutu:Segundu --> %d:%d:%d:%d" % (egun, ordu, minutu, segundu))


datuak_transformatu()
