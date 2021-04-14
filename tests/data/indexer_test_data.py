from service_classes.indexer import IndexerResult

tests = [
    {
        "name": "OPM - seeders",
        "enable": True,
        "data": {
            IndexerResult("[Judas] One Punch Man (Seasons 1-2 + OVAs + Specials) [BD 1080p][HEVC x265 10bit][Dual-Audio][Multi-Subs] (Batch)", "", 100, "10 GiB"): 0,
            IndexerResult("[HorribleSubs] One Punch Man S2 - 07 [1080p].mkv", "", 10, "10 GiB"): None,
            IndexerResult("One-Punch Man Season 02 [1080p] (Dual Audio)", "", 10, "10 GiB"): None,
            IndexerResult("[HorribleSubs] One Punch Man - 01 [720p].mkv", "", 10, "10 GiB"): None,
            IndexerResult("[GJM] One Punch Man S2 - OVA1 (BD 1080p) [F2CD9816].mkv", "", 10, "10 GiB"): None,
            IndexerResult("[HorribleSubs] One-Punch Man (01-12) [1080p] (Batch)", "", 30, "10 GiB"): 1,
            IndexerResult("[Erai-raws] One Punch Man (2019) - 01 ~ 12 [1080p][Multiple Subtitle]", "", 10, "10 GiB"): 2,
            IndexerResult("[0x539] One Punch Man S01 (Season 1 + OVAs + OAD) (Dual Audio BD 1080p x264 10bit FLAC)", "", 1, "10 GiB"): None,
            IndexerResult("[EMBER] One Punch Man (2019) (Season 2+Specials) [BDRip] [1080p Dual Audio HEVC 10 bits] (OPM 2)", "", 10, "10 GiB"): None,
            IndexerResult("[bonkai77] One Punch Man + OVA [1080p] [DUAL-AUDIO] [x265] [HEVC] [AAC] [10bit]", "", 4, "10 GiB"): None
        },
        "rank_settings": {"titles": ["One Punch Man", "One-Punch Man"], "pref_groups": ["HorribleSubs", "Erai-raws"],
                          "pref_quality": "1080p", "season": 1, "min_gib": 1, "min_seeders": 5, "seeders_importance": 1}
    },
    {
        "name": "OPM - seeders importance 0",
        "enable": True,
        "data": {
            IndexerResult("[Judas] One Punch Man (Seasons 1-2 + OVAs + Specials) [BD 1080p][HEVC x265 10bit][Dual-Audio][Multi-Subs] (Batch)", "", 100, "10 GiB"): 0,
            IndexerResult("[HorribleSubs] One Punch Man S2 - 07 [1080p].mkv", "", 10, "10 GiB"): None,
            IndexerResult("One-Punch Man Season 02 [1080p] (Dual Audio)", "", 10, "10 GiB"): None,
            IndexerResult("[HorribleSubs] One Punch Man - 01 [720p].mkv", "", 10, "10 GiB"): None,
            IndexerResult("[GJM] One Punch Man S2 - OVA1 (BD 1080p) [F2CD9816].mkv", "", 10, "10 GiB"): None,
            IndexerResult("[HorribleSubs] One-Punch Man (01-12) [1080p] (Batch)", "", 10, "10 GiB"): 1,
            IndexerResult("[Erai-raws] One Punch Man (2019) - 01 ~ 12 [1080p][Multiple Subtitle]", "", 10, "10 GiB"): 1,
            IndexerResult("[0x539] One Punch Man S01 (Season 1 + OVAs + OAD) (Dual Audio BD 1080p x264 10bit FLAC)", "", 10, "10 GiB"): 0,
            IndexerResult("[EMBER] One Punch Man (2019) (Season 2+Specials) [BDRip] [1080p Dual Audio HEVC 10 bits] (OPM 2)", "", 10, "10 GiB"): None,
        },
        "rank_settings": {"titles": ["One Punch Man", "One-Punch Man"], "pref_groups": ["HorribleSubs", "Erai-raws"],
                          "pref_quality": "1080p", "season": 1, "min_gib": 1, "min_seeders": 5, "seeders_importance": 0}
    },
    {
        "name": "Wonder egg priority",
        "enable": False,
        "data": {
            IndexerResult("[SubsPlease] Wonder Egg Priority - 12 (1080p) [33854763].mkv", "", 668, "1.2 GiB"): None,
            IndexerResult("[Erai-raws] Wonder Egg Priority - 12 END [1080p].mkv", "", 194, "1.2 GiB"): None,
            IndexerResult("[Erai-raws] Wonder Egg Priority - 01 [1080p].mkv", "", 158, "1.2 GiB"): None,
            IndexerResult("[Erai-raws] Wonder Egg Priority - 12 END [1080p HEVC].mkv", "", 89, "408.2 MiB"): None,
            IndexerResult("[Erai-raws] Wonder Egg Priority - 06 [1080p HEVC].mkv", "", 85, "422.6 MiB"): None,
            IndexerResult("[Erai-raws] Wonder Egg Priority - 08 [v0][1080p].mkv", "", 81, "1.2 GiB"): None,
            IndexerResult("[Erai-raws] Wonder Egg Priority - 12 END [v0][1080p].mkv", "", 47, "1.2 GiB"): None,
            IndexerResult("[KasuTai] [ENG] Wonder Egg Priority - 11 [1080p]", "", 44, "672.4 MiB"): None,
            IndexerResult("[Nyanpasu] Wonder Egg Priority 1-12 Batch [1080p][HEVC]", "", 41, "4.7 GiB"): 0,
            IndexerResult("[badcvxy] Wonder Egg Priority - 11 (WEB-DL 1080p)", "", 39, "1.1 GiB"): None,
            IndexerResult("[Golumpa] WONDER EGG PRIORITY - 02 [English Dub] [FuniDub 1080p x264 AAC] [MKV] [67DDDC71]", "", 38, "1.2 GiB"): None
        },
        "rank_settings": {"titles": ["Wonder Egg Priority"], "pref_groups": ["HorribleSubs", "Erai-raws"],
                          "pref_quality": "1080p", "season": 1, "min_gib": 1, "min_seeders": 5, "seeders_importance": 1}
    },
    {
        "name": "Mononoke",
        "enable": True,
        "data": {
            IndexerResult("[Utsukushii-Raws+Anon subs] Mononoke (BD 1280x720 H264 FLAC 2.0) Ayakashi - Bakeneko (BD 960x720 H264 FLAC 2.0)", "", 22, "8.7 GiB"): 0,
            IndexerResult("[anon] Mononoke (BD 720p)", "", 19, "7.0 GiB"): 0,
            IndexerResult("Princess_Mononoke_(1997)_[1080p,BluRay,flac,x264]_-_THORA", "", 18, "17.4 GiB"): None,
            IndexerResult("[DragsterPS] Princess Mononoke [1080p] [Multi-Audio] [Multi-Subs]", "", 10, "19.5 GiB"): None,
            IndexerResult("[reddeimon] Mononoke 2007 [1080p Bluray Rip x264 FLAC]", "", 8, "12.8 GiB"): 0,
            IndexerResult("[HorribleSubs] Fukigen na Mononokean S2 - 09 [1080p].mkv", "", 6, "622.2 MiB"): None,
            IndexerResult("[Erai-raws] Mononoke-hime [1080p][Multiple Subtitle].mkv", "", 6, "6.5 GiB"): 1,  # title very similar
            # IndexerResult("[kamineko] Fukigen na Mononokean | The Morose Mononokean S1 (2016) [BD 1080p h264 FLAC]", "", 4, "9.1 GiB"): None,
            # IndexerResult("[HorribleSubs] Fukigen na Mononokean - 01 [1080p].mkv", "", 4, "541.1 MiB"): None,
            # IndexerResult("[Erai-raws] Fukigen na Mononokean Tsuzuki - 01 ~ 13 [1080p][Multiple Subtitle]", "", 4, "9.1 GiB"): None,
            # IndexerResult("[zza] Fukigen na Mononokean (S1+S2) [1080p.x265][multisubs:eng,fre,ger,por,spa][Vostfr]", "", 4, "4.1 GiB"): None,
            # IndexerResult("[Erai-raws] Fukigen na Mononokean - 01 ~ 13 [1080p][Multiple Subtitle]", "", 3, "8.2 GiB"): None,
            # IndexerResult("Princess Mononoke もののけ姫 (1997) (jp/en dub/en-jp subs)", "", 3, "2.8 GiB"): None,
            # IndexerResult("[JPSDR] Mononoke Hime [BDRip][1080p H264 Hi10P DTSHD-MA 5.1]", "", 2, "8.9 GiB"): None,
            # IndexerResult("Mononoke [Black-Sheep]", "", 2, "3.9 GiB"): None,
            # IndexerResult("[REVO]Mononoke Hime [1080p,FLAC]", "", 1, "21.3 GiB"): None,
            # IndexerResult("[TardSubs] Denki Groove - Mononoke Dance", "", 1, "71.7 MiB"): None,
            # IndexerResult("Princess.Mononoke.1080p.DualAudio.English.Japanese.6ch.hime.OST.Extras.BRrip.BDrip.[KoTuWa]", "", 1, "2.3 GiB"): None,
            # IndexerResult("Princess Mononoke (1997) [Dual Audio 1080p 10bit x265 DTS BD]", "", 1, "6.8 GiB"): None,
            # IndexerResult("[Yūrei] Mononoke Hime (Princess Mononoke) [BD 1080p x265 10bit Opus 5.1 Dual Audio]", "", 1, "14.0 GiB"): None,
            # IndexerResult("Mononoke 7 Black-Sheep", "", 0, "329.5 MiB"): None
        },
        "rank_settings": {"titles": ["Mononoke"], "pref_groups": ["HorribleSubs", "Erai-raws"],
                          "pref_quality": "1080p", "season": 1, "min_gib": 1, "min_seeders": 5, "seeders_importance": 0}
    },
    {
        "name": "Kaguya-sama",
        "enable": True,
        "data": {
            IndexerResult("[HorribleSubs] Kaguya-sama wa Kokurasetai S2 - 12 [1080p].mkv", "", 95, "1.3 GiB"): None,
            IndexerResult("[EMBER] Kaguya-sama: Love is War (2019-2020) (Season 1+2) [BDRip] [1080p Dual Audio HEVC 10 bits] (Kaguya-sama wa Kokurasetai: Tensai-tachi no Renai Zunousen)", "", 53, "13.4 GiB"): 0,
            IndexerResult("[GSK_kun] Kaguya-sama Love Is War [BDRip 1920x1080 HEVC FLAC]", "", 53, "18.7 GiB"): 0,
            IndexerResult("[HorribleSubs] Kaguya-sama wa Kokurasetai - 01 [1080p].mkv", "", 47, "877.5 MiB"): None,
            IndexerResult("[GJM] Kaguya-sama ~Love is War~ S2 - 08 [287F1F57].mkv", "", 40, "1.1 GiB"): None,
            IndexerResult("[Erai-raws] Kaguya-sama wa Kokurasetai - Tensai-tachi no Renai Zunousen - 01 ~ 12 [1080p][Multiple Subtitle]", "", 31, "9.3 GiB"): 1,
            IndexerResult("[HorribleSubs] Kaguya-sama wa Kokurasetai S2 (01-12) [1080p] (Unofficial Batch)", "", 27, "15.7 GiB"): None,
            IndexerResult("[NH] Kaguya-sama: Love is War - Season 1 (BD 1080p x265 10-bit AAC-FLAC) [Dual-Audio] | Kaguya-sama wa Kokurasetai: Tensai-tachi no Renai Zunousen", "", 22, "19.1 GiB"): 1,
            IndexerResult("[DB] Kaguya-sama wa Kokurasetai?: Tensai-tachi no Renai Zunousen | Kaguya-sama: Love is War Season 2 [Dual Audio 10bit BD1080p][HEVC-x265]", "", 15, "6.0 GiB"): None,
            IndexerResult("[HorribleSubs] Kaguya-sama wa Kokurasetai [1080p] (Unofficial Batch)", "", 15, "9.3 GiB"): 2,
            IndexerResult("[DB] Kaguya-sama wa Kokurasetai: Tensai-tachi no Renai Zunousen | Kaguya-sama: Love is War [Dual Audio 10bit BD1080p][HEVC-x265]", "", 14, "5.6 GiB"): 3,
            IndexerResult("[Erai-raws] Kaguya-sama wa Kokurasetai! Tensai-tachi no Renai Zunousen 2 - 04 [1080p].mkv", "", 14, "1.3 GiB"): None,
            IndexerResult("[GJM] Kaguya-sama ~Love is War~ - 08 [38E8B326].mkv", "", 13, "610.8 MiB"): None
        },
        "rank_settings": {"titles": ["Kaguya-sama wa Kokurasetai?: Tensai-tachi no Renai Zunousen", "Kaguya-sama: Love is War?"], "pref_groups": ["HorribleSubs", "Erai-raws"],
                          "pref_quality": "1080p", "season": 1, "min_gib": 1, "min_seeders": 5, "seeders_importance": 1}
    },
]
