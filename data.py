from jsonpath_ng import jsonpath, parse

DATA = {
    "Vayne": {
        "players": [
            {
                "name": "NEGATIVE MACRO",
                "country": "europe",
                "puuid": "n85Ra5AOp8MkuVbg55ZO0PBR4s4XI5En_pFRVfPI1VV9wzaPMk7VcrryKbFpFLtMk0PYWOtar6FCtQ",
            },
            {
                "name": "Sorest",
                "country": "europe",
                "puuid": "o571y5yiCauzTiPCSUQNgCsPe3bdcqEAEd2E2GVlBfWUyevnEey9UUJeMZox27942seIkzgA17mxfw",
            },
            {
                "name": "300 Ginz",
                "country": "europe",
                "puuid": "hatnrxhQQIxTmKIEtEdlqTKnh4pwgAeS101WwfKw6UAbhU2gFnHwXVKmuFsJ0CWRb358XKEhx6Srpw",
            },
            {
                "name": "TTV SaskioLoL",
                "country": "americas",
                "puuid": "RlYlAJauKkypiN1KO--S2Bo2kP3zJhP2P5OoKDkqJmvyEwpbTfwpkWSbxivJyhZ478JLfHrppjHaGQ",
            },
            {
                "name": "이길생각만하기",
                "country": "asia",
                "puuid": "NI_NjPdvwAaBuBmBrxkDlojAon5FCDzRd5OCsubF1OaC_b4Imhq4HOaXVMpaSRvPhZJ56N0vmz5rnQ",
            },
        ],
        "role": ["BOTTOM"],
        "columns": ['kills', 'deaths', 'csPerMinute', 'dmgPerMinute']
    },
    "Draven": {
        "players": [
            {
                "name": "TyChee",
                "country": "americas",
                "puuid": "bTjX6A-q928ZIgLGOzuQ__rEnzOZzjkgxt9XLFtM9ULdefjfwG95TWXI2LEkh-iDkk8_VXcFbJ3lKw",
            },
            {
                "name": "twitch tv NCXA",
                "country": "europe",
                "puuid": "4CmJC5nNFTXkAYtpQf2wCncpik9cOotn7VZT-dKDb3ZtEPEBADair7K1VNn8cXuesCEuaYY95BDr0A",
            },
            {
                "name": "Dealersz",
                "country": "europe",
                "puuid": "LU70bd6VUMdvFohboLfQ1ln-Ikqlxgghk5Ru79EfWyI4TGIqN_tQSKAjjj-T4VXKSuPpQ_AkwW4W1g",
            },
            {
                "name": "SWENZUUUUUUUUUUU",
                "country": "europe",
                "puuid": "eW8mLgDCWEbtspi13AYYdL1tl9Malwid_x1bwvggaS1LjlHwe94ay2sNJEjXBijQnwziw0wjPR7yYQ",
            },
            {
                "name": "J God1",
                "country": "asia",
                "puuid": "8girLdSJoA967zX-QfU1_2dZMJSyJxeJzScqBlhN8-WzIF9mKYoIXsUZbLIRv0FYy3wNWh7SzypwJQ",
            },
        ],
        "role": ["BOTTOM"],
        "columns": ['kills', 'deaths', 'csPerMinute', 'dmgPerMinute']
    },
    "Jax": {
        "players": [
            {
                "name": "RainCX",
                "country": "americas",
                "puuid": "941y6246rbs1PQWBnaxShczN5Gyq3rvJ2R392SajbWWJe8fBvvel6OkzZtoxMvq6a9G-s2mhNHWC6w",
            },
            {
                "name": "stefankø",
                "country": "europe",
                "puuid": "RuwiEEyrG64AABEUNPM6F-yaCqXKz-fKXEa2jXhWGC-6_VyMaD5LvSWAkMMCdphoDVkdTzZOpnq80A",
            },
            {
                "name": "Kât l ï Äm",
                "country": "europe",
                "puuid": "VcFMSEEOk8jTTXkt2MR68Jdk4WfeikyhWATeWGizX3S1zo5Pwr7t6_T7D87uHeVDi4lCwPG6OlZO_w",
            },
            {
                "name": "이현1",
                "country": "asia",
                "puuid": "K2V7QaGQH56sHnCE4b8xinexHB4feUIbPTRQEI9yo14GRc44Ir6WHfHygfBtsMaM5bM8ziqbAs6mxQ",
            },
            {
                "name": "양심팔아먹은사람",
                "country": "asia",
                "puuid": "WxeHIVEsMARArErs68MchbqPQ9bFpFzwNXGho5ExatV3Cxr4sjwHZP963zWWZN-4JZ_a5lmS8uMWyg",
            },
        ],
        "role": ["TOP", "MIDDLE"],
        "columns": ['kills', 'deaths', 'csPerMinute', 'dmgPerMinute']
    },
    "Gangplank": {
        "players": [
            {
                "name": "잼 비",
                "country": "asia",
                "puuid": "ggZg4HODrL6_2EAFHIqJZqL8ekvHoc9Q3B4lTLm292riUziudLz5Q7h9S2DSzysQ4QNkYWbdzFTQFw",
            },
            {
                "name": "칠대삼",
                "country": "asia",
                "puuid": "GQAAeU3szlog7IxqMzKIL4RAbUUAs0NIQ1MtfwrGQS3w_xj2AQMvg8Qx0O6Nuhg_L7plwq6fPakpqA",
            },
            {
                "name": "ChickenAndy",
                "country": "europe",
                "puuid": "D1TDp0hTaXuwmunOWQpAJ5V_KpjvJRQTl7P5gXPhX5BgDRb7jwU8raKjkBIlOCLNT3b85IgxLkE5LA",
            },
            {
                "name": "IMAFREAKBUILTDIF",
                "country": "america",
                "puuid": "KPFNO927r-noVy7qsoyzpki4zgc6Be5etdlsdm-0h230rbT0Gy-xaqyMs6YgNa9rsTN-R-acwKHfxQ",
            },
            {
                "name": "Tao yan pian zi",
                "country": "asia",
                "puuid": "W3UEOefNLbYD-yoG9KHDi955xhPX_wjmrXK6B7R4cbcDuGSDrcJL1PMAQ20RPs3l8GxEN36iZQIkWw",
            },
        ],
        "role": ["TOP"],
        "columns": ['kills', 'deaths', 'csPerMinute', 'dmgPerMinute']
    },
}
