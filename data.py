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
        "role": "BOTTOM",
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
        "role": "BOTTOM",
        "columns": ['kills', 'deaths', 'csPerMinute', 'dmgPerMinute']
    },
}
