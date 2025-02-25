import time

import pyoctopus


class InstantRace:
    id = pyoctopus.json("$.id", converter=pyoctopus.int_converter())
    league = pyoctopus.json("$.league.i", converter=pyoctopus.int_converter())
    league_name = pyoctopus.json("$.league.n")
    host = pyoctopus.json("$.host.i", converter=pyoctopus.int_converter())
    host_name = pyoctopus.json("$.host.n")
    guest = pyoctopus.json("$.guest.i", converter=pyoctopus.int_converter())
    guest_name = pyoctopus.json("$.guest.n")

    init_handicap = pyoctopus.json("$.sd.f.hrf", converter=pyoctopus.float_converter())
    init_goal_line = pyoctopus.json("$.sd.f.hdx", converter=pyoctopus.float_converter())

    status = pyoctopus.json("$.status")
    host_goal = pyoctopus.json("$.rd.hg", converter=pyoctopus.int_converter())
    guest_goal = pyoctopus.json("$.rd.gg", converter=pyoctopus.int_converter())
    host_corner = pyoctopus.json("$.rd.hg", converter=pyoctopus.int_converter())
    guest_corner = pyoctopus.json("$.rd.gg", converter=pyoctopus.int_converter())

    handicap = pyoctopus.json("$.f_ld.hrf", converter=pyoctopus.float_converter())
    handicap_host_odds = pyoctopus.json("$.f_ld.hrfsp", converter=pyoctopus.float_converter())
    handicap_guest_odds = pyoctopus.json("$.f_ld.grfsp", converter=pyoctopus.float_converter())
    goal_line = pyoctopus.json("$.f_ld.hdx", converter=pyoctopus.float_converter())
    goal_line_up_odds = pyoctopus.json("$.f_ld.hdxsp", converter=pyoctopus.float_converter())
    goal_line_down_odds = pyoctopus.json("$.f_ld.gdxsp", converter=pyoctopus.float_converter())

    host_attacks = pyoctopus.json("$.plus.ha", converter=pyoctopus.int_converter())
    guest_attacks = pyoctopus.json("$.plus.ga", converter=pyoctopus.int_converter())
    host_danger_attacks = pyoctopus.json("$.plus.hd", converter=pyoctopus.int_converter())
    guest_danger_attacks = pyoctopus.json("$.plus.gd", converter=pyoctopus.int_converter())
    host_shot_on = pyoctopus.json("$.plus.hso", converter=pyoctopus.int_converter())
    guest_shot_on = pyoctopus.json("$.plus.gso", converter=pyoctopus.int_converter())
    host_shot_off = pyoctopus.json("$.plus.hsf", converter=pyoctopus.int_converter())
    guest_shot_off = pyoctopus.json("$.plus.gsf", converter=pyoctopus.int_converter())


class InstantRaceResponse:
    races = pyoctopus.embedded(pyoctopus.json("$.rs[*]", multi=True), InstantRace)


if __name__ == '__main__':
    text = """
    {
        "rs": [
            {
            "id": "1406336",
            "league": {
                "i": "2463",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "澳威U20",
                "fn": "澳大利亚新南威尔士联赛 20岁以下",
                "ls": "A",
                "sbn": "澳大利亚新南威尔士联赛 20岁以下",
                "stn": "澳大利亚新南威尔士联赛 20岁以下",
                "spy": "aoxinnanu20",
                "ci": "7",
                "cn": "澳大利亚",
                "cs": "A"
            },
            "host": {
                "i": "27168",
                "n": "FC圣乔治 20岁以下",
                "sbn": "FC圣乔治 20岁以下",
                "stn": "FC圣乔治 20岁以下"
            },
            "guest": {
                "i": "32012",
                "n": "Mt Druitt Town Rangers 20岁以下",
                "sbn": "Mt Druitt Town Rangers 20岁以下",
                "stn": "Mt Druitt Town Rangers 20岁以下"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 21,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "0.0",
                "hdx": "3.5",
                "hcb": "10"
                },
                "h": {
                "hrf": "0.0",
                "hdx": "1.5",
                "hcb": "4.5"
                }
            },
            "events": [
                {
                "t": "h",
                "c": "上半场后得分 - 1-0"
                },
                {
                "t": "gc",
                "c": "41' - 第6角球 - Mt Druitt Town Rangers 20岁以下"
                },
                {
                "t": "gc",
                "c": "39' - 第5角球 - Mt Druitt Town Rangers 20岁以下"
                },
                {
                "t": "gyc",
                "c": "24' ~ 第1张黄牌 ~  ~(Mt Druitt Town Rangers 20岁以下)"
                },
                {
                "t": "hg",
                "c": "23' - 第1个进球 -   (FC圣乔治 20岁以下) -"
                },
                {
                "t": "d",
                "c": "23' - 首先达到3个角球 - FC圣乔治 20岁以下"
                },
                {
                "t": "hc",
                "c": "23' - 第4角球 - FC圣乔治 20岁以下"
                },
                {
                "t": "hc",
                "c": "23' - 第3角球 - FC圣乔治 20岁以下"
                },
                {
                "t": "hc",
                "c": "14' - 第2角球 - FC圣乔治 20岁以下"
                },
                {
                "t": "gc",
                "c": "6' - 第1角球 - Mt Druitt Town Rangers 20岁以下"
                },
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                {
                    "status": "6",
                    "t": "gc",
                    "content": "6' - 第1角球 - Mt Druitt Town Rangers 20岁以下"
                },
                {
                    "status": "14",
                    "t": "hc",
                    "content": "14' - 第2角球 - FC圣乔治 20岁以下"
                },
                {
                    "status": "23",
                    "t": "hc",
                    "content": "23' - 第3角球 - FC圣乔治 20岁以下"
                },
                {
                    "status": "23",
                    "t": "hc",
                    "content": "23' - 第4角球 - FC圣乔治 20岁以下"
                },
                {
                    "status": "23",
                    "t": "hg",
                    "content": "23' - 第1个进球 -   (FC圣乔治 20岁以下) -"
                },
                {
                    "status": "39",
                    "t": "gc",
                    "content": "39' - 第5角球 - Mt Druitt Town Rangers 20岁以下"
                },
                {
                    "status": "41",
                    "t": "gc",
                    "content": "41' - 第6角球 - Mt Druitt Town Rangers 20岁以下"
                }
                ],
                "ml": "90",
                "status": 48
            },
            "ht": "0",
            "ss": "S",
            "ss_ta": "0",
            "rd": {
                "hg": "1",
                "gg": "0",
                "hc": "3",
                "gc": "3",
                "hy": "0",
                "gy": "1",
                "hr": "0",
                "gr": "0"
            },
            "plus": {
                "ha": "50",
                "ga": "47",
                "hd": "38",
                "gd": "17",
                "hso": "5",
                "gso": "1",
                "hsf": "6",
                "gsf": "2",
                "hqq": "52",
                "gqq": "48"
            },
            "rh": {
                "hg": "1",
                "gg": "0",
                "hc": "3",
                "gc": "3"
            },
            "status": "48",
            "h_ld": {
                "hrf": "0.0",
                "hrfsp": "1.475",
                "grfsp": "2.600",
                "rft": "-2",
                "rf": [
                {
                    "hrf": "0.0",
                    "hrfsp": "1.475",
                    "grfsp": "2.600",
                    "rft": "-2",
                    "ps": "2511"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.500",
                    "grfsp": "2.500",
                    "rft": "-2",
                    "ps": "2447"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.525",
                    "grfsp": "2.425",
                    "rft": "-2",
                    "ps": "2434"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.600",
                    "grfsp": "2.300",
                    "rft": "-1",
                    "ps": "2420"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.725",
                    "grfsp": "2.075",
                    "rft": "1",
                    "ps": "2416"
                }
                ],
                "hdx": "1.5",
                "hdxsp": "6.000",
                "gdxsp": "1.125",
                "dxt": "2",
                "dx": [
                {
                    "hdx": "1.5",
                    "hdxsp": "6.000",
                    "gdxsp": "1.125",
                    "dxt": "2",
                    "ps": "2529"
                },
                {
                    "hdx": "1.5",
                    "hdxsp": "5.900",
                    "gdxsp": "1.130",
                    "dxt": "2",
                    "ps": "2516"
                },
                {
                    "hdx": "1.5",
                    "hdxsp": "5.750",
                    "gdxsp": "1.140",
                    "dxt": "2",
                    "ps": "2494"
                },
                {
                    "hdx": "1.5",
                    "hdxsp": "5.500",
                    "gdxsp": "1.150",
                    "dxt": "2",
                    "ps": "2479"
                },
                {
                    "hdx": "1.5",
                    "hdxsp": "5.250",
                    "gdxsp": "1.160",
                    "dxt": "2",
                    "ps": "2463"
                }
                ],
                "hcb": "6.5",
                "hcbsp": "2.600",
                "gcbsp": "1.475",
                "cbt": "2",
                "cb": [
                {
                    "hcb": "6.5",
                    "hcbsp": "2.600",
                    "gcbsp": "1.475",
                    "cbt": "2",
                    "ps": "2529"
                },
                {
                    "hcb": "6.5",
                    "hcbsp": "2.500",
                    "gcbsp": "1.500",
                    "cbt": "2",
                    "ps": "2516"
                },
                {
                    "hcb": "6.5",
                    "hcbsp": "2.425",
                    "gcbsp": "1.525",
                    "cbt": "2",
                    "ps": "2503"
                },
                {
                    "hcb": "6.5",
                    "hcbsp": "2.375",
                    "gcbsp": "1.550",
                    "cbt": "2",
                    "ps": "2494"
                },
                {
                    "hcb": "6.5",
                    "hcbsp": "2.350",
                    "gcbsp": "1.575",
                    "cbt": "2",
                    "ps": "2488"
                }
                ]
            },
            "f_ld": {
                "hrf": "-0.25",
                "hrfsp": "1.775",
                "grfsp": "2.025",
                "rft": "0",
                "rf": [
                {
                    "hrf": "-0.25",
                    "hrfsp": "1.775",
                    "grfsp": "2.025",
                    "rft": "0",
                    "ps": "2833"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.975",
                    "grfsp": "1.725",
                    "rft": "0",
                    "ps": "2757"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "1.725",
                    "grfsp": "1.975",
                    "rft": "0",
                    "ps": "2587"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.950",
                    "grfsp": "1.750",
                    "rft": "0",
                    "ps": "2540"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "1.775",
                    "grfsp": "2.025",
                    "rft": "-2",
                    "ps": "2529"
                }
                ],
                "hdx": "2.75",
                "hdxsp": "1.925",
                "gdxsp": "1.875",
                "dxt": "2",
                "dx": [
                {
                    "hdx": "2.75",
                    "hdxsp": "1.925",
                    "gdxsp": "1.875",
                    "dxt": "2",
                    "ps": "2875"
                },
                {
                    "hdx": "2.75",
                    "hdxsp": "1.900",
                    "gdxsp": "1.900",
                    "dxt": "2",
                    "ps": "2833"
                },
                {
                    "hdx": "2.75",
                    "hdxsp": "1.850",
                    "gdxsp": "1.950",
                    "dxt": "2",
                    "ps": "2777"
                },
                {
                    "hdx": "2.75",
                    "hdxsp": "1.825",
                    "gdxsp": "1.975",
                    "dxt": "2",
                    "ps": "2746"
                },
                {
                    "hdx": "2.75",
                    "hdxsp": "1.800",
                    "gdxsp": "2.000",
                    "dxt": "1",
                    "ps": "2700"
                }
                ],
                "hcb": "10.5",
                "hcbsp": "1.950",
                "gcbsp": "1.850",
                "cbt": "2",
                "cb": [
                {
                    "hcb": "10.5",
                    "hcbsp": "1.950",
                    "gcbsp": "1.850",
                    "cbt": "2",
                    "ps": "2869"
                },
                {
                    "hcb": "10.5",
                    "hcbsp": "1.925",
                    "gcbsp": "1.875",
                    "cbt": "2",
                    "ps": "2859"
                },
                {
                    "hcb": "10.5",
                    "hcbsp": "1.900",
                    "gcbsp": "1.900",
                    "cbt": "2",
                    "ps": "2843"
                },
                {
                    "hcb": "10.5",
                    "hcbsp": "1.875",
                    "gcbsp": "1.925",
                    "cbt": "2",
                    "ps": "2833"
                },
                {
                    "hcb": "10.5",
                    "hcbsp": "1.850",
                    "gcbsp": "1.950",
                    "cbt": "2",
                    "ps": "2810"
                }
                ]
            },
            "hot": 9
            },
            {
            "id": "1406335",
            "league": {
                "i": "2463",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "澳威U20",
                "fn": "澳大利亚新南威尔士联赛 20岁以下",
                "ls": "A",
                "sbn": "澳大利亚新南威尔士联赛 20岁以下",
                "stn": "澳大利亚新南威尔士联赛 20岁以下",
                "spy": "aoxinnanu20",
                "ci": "7",
                "cn": "澳大利亚",
                "cs": "A"
            },
            "host": {
                "i": "14541",
                "n": "曼立联 20岁以下",
                "sbn": "曼立联队U20",
                "stn": "曼立联 20岁以下"
            },
            "guest": {
                "i": "14962",
                "n": "悉尼联盟 20岁以下",
                "sbn": "悉尼联盟U20",
                "stn": "悉尼联盟 20岁以下"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 27,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "-0.75",
                "hdx": "3.25",
                "hcb": null
                },
                "h": {
                "hrf": "-0.25",
                "hdx": "1.25",
                "hcb": null
                }
            },
            "events": [
                {
                "t": "h",
                "c": "上半场后得分 - 2-0"
                },
                {
                "t": "hc",
                "c": "31' - 第1角球 - 曼立联 20岁以下"
                },
                {
                "t": "hg",
                "c": "16' - 第2个进球 -   (曼立联 20岁以下) -"
                },
                {
                "t": "hg",
                "c": "11' - 第1个进球 -   (曼立联 20岁以下) -"
                },
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                {
                    "status": "11",
                    "t": "hg",
                    "content": "11' - 第1个进球 -   (曼立联 20岁以下) -"
                },
                {
                    "status": "16",
                    "t": "hg",
                    "content": "16' - 第2个进球 -   (曼立联 20岁以下) -"
                },
                {
                    "status": "31",
                    "t": "hc",
                    "content": "31' - 第1角球 - 曼立联 20岁以下"
                }
                ],
                "ml": "90",
                "status": 48
            },
            "ht": "0",
            "ss": "S",
            "ss_ta": "0",
            "rd": {
                "hg": "2",
                "gg": "0",
                "hc": "1",
                "gc": "0",
                "hy": "0",
                "gy": "0",
                "hr": "0",
                "gr": "0"
            },
            "plus": {
                "ha": "32",
                "ga": "34",
                "hd": "15",
                "gd": "12",
                "hso": "8",
                "gso": "0",
                "hsf": "0",
                "gsf": "0",
                "hqq": "0",
                "gqq": "0"
            },
            "rh": {
                "hg": "2",
                "gg": "0",
                "hc": "1",
                "gc": "0"
            },
            "status": "48",
            "h_ld": {
                "hrf": "0.0",
                "hrfsp": "1.525",
                "grfsp": "2.425",
                "rft": "0",
                "rf": [
                {
                    "hrf": "0.0",
                    "hrfsp": "1.525",
                    "grfsp": "2.425",
                    "rft": "0",
                    "ps": "1938"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "2.400",
                    "grfsp": "1.500",
                    "rft": "-1",
                    "ps": "1903"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "2.425",
                    "grfsp": "1.525",
                    "rft": "2",
                    "ps": "1852"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "2.375",
                    "grfsp": "1.550",
                    "rft": "2",
                    "ps": "1829"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "2.350",
                    "grfsp": "1.575",
                    "rft": "1",
                    "ps": "1809"
                }
                ],
                "hdx": "2.5",
                "hdxsp": "4.650",
                "gdxsp": "1.180",
                "dxt": "2",
                "dx": [
                {
                    "hdx": "2.5",
                    "hdxsp": "4.650",
                    "gdxsp": "1.180",
                    "dxt": "2",
                    "ps": "2463"
                },
                {
                    "hdx": "2.5",
                    "hdxsp": "4.500",
                    "gdxsp": "1.190",
                    "dxt": "2",
                    "ps": "2454"
                },
                {
                    "hdx": "2.5",
                    "hdxsp": "4.400",
                    "gdxsp": "1.200",
                    "dxt": "2",
                    "ps": "2441"
                },
                {
                    "hdx": "2.5",
                    "hdxsp": "4.250",
                    "gdxsp": "1.210",
                    "dxt": "2",
                    "ps": "2428"
                },
                {
                    "hdx": "2.5",
                    "hdxsp": "4.150",
                    "gdxsp": "1.220",
                    "dxt": "2",
                    "ps": "2416"
                }
                ]
            },
            "f_ld": {
                "hrf": "-0.5",
                "hrfsp": "1.975",
                "grfsp": "1.825",
                "rft": "2",
                "rf": [
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.975",
                    "grfsp": "1.825",
                    "rft": "2",
                    "ps": "2787"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.950",
                    "grfsp": "1.850",
                    "rft": "2",
                    "ps": "2679"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.925",
                    "grfsp": "1.875",
                    "rft": "2",
                    "ps": "2639"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.900",
                    "grfsp": "1.900",
                    "rft": "2",
                    "ps": "2497"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.875",
                    "grfsp": "1.925",
                    "rft": "2",
                    "ps": "2428"
                }
                ],
                "hdx": "3.75",
                "hdxsp": "1.800",
                "gdxsp": "2.000",
                "dxt": "2",
                "dx": [
                {
                    "hdx": "3.75",
                    "hdxsp": "1.800",
                    "gdxsp": "2.000",
                    "dxt": "2",
                    "ps": "2887"
                },
                {
                    "hdx": "3.75",
                    "hdxsp": "1.775",
                    "gdxsp": "2.025",
                    "dxt": "0",
                    "ps": "2850"
                },
                {
                    "hdx": "4.0",
                    "hdxsp": "1.975",
                    "gdxsp": "1.725",
                    "dxt": "0",
                    "ps": "2827"
                },
                {
                    "hdx": "3.75",
                    "hdxsp": "1.725",
                    "gdxsp": "1.975",
                    "dxt": "0",
                    "ps": "2810"
                },
                {
                    "hdx": "4.0",
                    "hdxsp": "2.025",
                    "gdxsp": "1.775",
                    "dxt": "2",
                    "ps": "2787"
                }
                ]
            },
            "hot": 1
            },
            {
            "id": "1406723",
            "league": {
                "i": "3542",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "埃塞高等联",
                "fn": "埃塞俄比亚Higher联赛",
                "ls": "A",
                "sbn": "埃塞俄比亚高等联赛",
                "stn": "埃塞俄比亚高等联赛",
                "spy": "ehl",
                "ci": "43",
                "cn": "埃塞俄比亚",
                "cs": "A"
            },
            "host": {
                "i": "55503",
                "n": "Sululta Ketema",
                "sbn": "Sululta Ketema",
                "stn": "Sululta Ketema"
            },
            "guest": {
                "i": "51981",
                "n": "沙舍默内凯内马FC",
                "sbn": "沙舍默内凯内马FC",
                "stn": "沙舍默内凯内马FC"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 3,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "-0.25",
                "hdx": "2.25",
                "hcb": null
                },
                "h": {
                "hrf": "0.0",
                "hdx": "0.75",
                "hcb": null
                }
            },
            "events": [
                {
                "t": "h",
                "c": "上半场后得分 - 0-0"
                },
                {
                "t": "it",
                "c": "上半场补时: 2 分钟"
                },
                {
                "t": "hc",
                "c": "38' - 第2角球 - Sululta Ketema"
                },
                {
                "t": "hc",
                "c": "3' - 第1角球 - Sululta Ketema"
                },
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                {
                    "status": "3",
                    "t": "hc",
                    "content": "3' - 第1角球 - Sululta Ketema"
                },
                {
                    "status": "38",
                    "t": "hc",
                    "content": "38' - 第2角球 - Sululta Ketema"
                }
                ],
                "ml": "90",
                "status": "45"
            },
            "ht": "0",
            "ss": "M",
            "ss_ta": "0",
            "rd": {
                "hg": "0",
                "gg": "0",
                "hc": "2",
                "gc": "0",
                "hy": "0",
                "gy": "0",
                "hr": "0",
                "gr": "0"
            },
            "plus": {
                "ha": "47",
                "ga": "54",
                "hd": "34",
                "gd": "32",
                "hso": "1",
                "gso": "1",
                "hsf": "2",
                "gsf": "3",
                "hqq": "0",
                "gqq": "0"
            },
            "rh": {
                "hg": "0",
                "gg": "0",
                "hc": "2",
                "gc": "0"
            },
            "status": "半",
            "h_ld": {
                "hrf": "0.0",
                "hrfsp": "1.975",
                "grfsp": "1.825",
                "rft": "-2",
                "rf": [
                {
                    "hrf": "0.0",
                    "hrfsp": "1.975",
                    "grfsp": "1.825",
                    "rft": "-2",
                    "ps": "2599"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "2.000",
                    "grfsp": "1.800",
                    "rft": "-1",
                    "ps": "2594"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "2.025",
                    "grfsp": "1.775",
                    "rft": "1",
                    "ps": "2521"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "2.000",
                    "grfsp": "1.800",
                    "rft": "-2",
                    "ps": "2505"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "2.025",
                    "grfsp": "1.775",
                    "rft": "-1",
                    "ps": "2340"
                }
                ],
                "hdx": "0.5",
                "hdxsp": "6.600",
                "gdxsp": "1.110",
                "dxt": "-2",
                "dx": [
                {
                    "hdx": "0.5",
                    "hdxsp": "6.600",
                    "gdxsp": "1.110",
                    "dxt": "-2",
                    "ps": "2599"
                },
                {
                    "hdx": "0.5",
                    "hdxsp": "7.800",
                    "gdxsp": "1.090",
                    "dxt": "-1",
                    "ps": "2594"
                },
                {
                    "hdx": "0.5",
                    "hdxsp": "10.00",
                    "gdxsp": "1.060",
                    "dxt": "2",
                    "ps": "2582"
                },
                {
                    "hdx": "0.5",
                    "hdxsp": "9.500",
                    "gdxsp": "1.065",
                    "dxt": "2",
                    "ps": "2564"
                },
                {
                    "hdx": "0.5",
                    "hdxsp": "9.000",
                    "gdxsp": "1.070",
                    "dxt": "2",
                    "ps": "2553"
                }
                ]
            },
            "f_ld": {
                "hrf": "0.0",
                "hrfsp": "1.725",
                "grfsp": "2.075",
                "rft": "1",
                "rf": [
                {
                    "hrf": "0.0",
                    "hrfsp": "1.725",
                    "grfsp": "2.075",
                    "rft": "1",
                    "ps": "2793"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.700",
                    "grfsp": "2.100",
                    "rft": "-2",
                    "ps": "2683"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.725",
                    "grfsp": "2.075",
                    "rft": "-2",
                    "ps": "2427"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.750",
                    "grfsp": "2.050",
                    "rft": "-1",
                    "ps": "2377"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.775",
                    "grfsp": "2.025",
                    "rft": "1",
                    "ps": "2249"
                }
                ],
                "hdx": "1.0",
                "hdxsp": "1.750",
                "gdxsp": "2.050",
                "dxt": "1",
                "dx": [
                {
                    "hdx": "1.0",
                    "hdxsp": "1.750",
                    "gdxsp": "2.050",
                    "dxt": "1",
                    "ps": "2700"
                },
                {
                    "hdx": "1.0",
                    "hdxsp": "1.725",
                    "gdxsp": "2.075",
                    "dxt": "-1",
                    "ps": "2793"
                },
                {
                    "hdx": "1.0",
                    "hdxsp": "1.750",
                    "gdxsp": "2.050",
                    "dxt": "2",
                    "ps": "2742"
                },
                {
                    "hdx": "1.0",
                    "hdxsp": "1.725",
                    "gdxsp": "2.075",
                    "dxt": "2",
                    "ps": "2722"
                },
                {
                    "hdx": "1.0",
                    "hdxsp": "1.700",
                    "gdxsp": "2.100",
                    "dxt": "0",
                    "ps": "2700"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1406746",
            "league": {
                "i": "2927",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "澳新北后",
                "fn": "澳大利亚新南威尔士北部后备队联赛",
                "ls": "A",
                "sbn": "澳大利亚新南威尔士北部后备队联赛",
                "stn": "澳大利亚新南威尔士北部后备队联赛",
                "spy": "aoxinhou",
                "ci": "7",
                "cn": "澳大利亚",
                "cs": "A"
            },
            "host": {
                "i": "40683",
                "n": "亚登斯顿玫瑰花蕾 后备队",
                "sbn": "亚登斯顿玫瑰花蕾 后备队",
                "stn": "亚登斯顿玫瑰花蕾 后备队"
            },
            "guest": {
                "i": "40667",
                "n": "瓦伦蒂勒凤凰 后备队",
                "sbn": "瓦伦蒂勒凤凰 后备队",
                "stn": "瓦伦蒂勒凤凰 后备队"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 5,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "-0.25",
                "hdx": "3.5",
                "hcb": null
                },
                "h": {
                "hrf": "0.0",
                "hdx": "1.5",
                "hcb": null
                }
            },
            "events": [
                {
                "t": "gg",
                "c": "30' - 第2个进球 -   (瓦伦蒂勒凤凰 后备队) -"
                },
                {
                "t": "hyc",
                "c": "28' ~ 第1张黄牌 ~  ~(亚登斯顿玫瑰花蕾 后备队)"
                },
                {
                "t": "hc",
                "c": "25' - 第1角球 - 亚登斯顿玫瑰花蕾 后备队"
                },
                {
                "t": "hg",
                "c": "22' - 第1个进球 -   (亚登斯顿玫瑰花蕾 后备队) -"
                },
                {
                "t": "hgc",
                "c": "2' - 第1个进球 -   (亚登斯顿玫瑰花蕾 后备队) -"
                },
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                {
                    "status": "2",
                    "t": "hgc",
                    "content": "2' - 第1个进球 -   (亚登斯顿玫瑰花蕾 后备队) -"
                },
                {
                    "status": "22",
                    "t": "hg",
                    "content": "22' - 第1个进球 -   (亚登斯顿玫瑰花蕾 后备队) -"
                },
                {
                    "status": "25",
                    "t": "hc",
                    "content": "25' - 第1角球 - 亚登斯顿玫瑰花蕾 后备队"
                },
                {
                    "status": "30",
                    "t": "gg",
                    "content": "30' - 第2个进球 -   (瓦伦蒂勒凤凰 后备队) -"
                }
                ],
                "ml": "90",
                "status": 30
            },
            "ht": "0",
            "ss": "F",
            "ss_ta": "0",
            "rd": {
                "hg": "1",
                "gg": "1",
                "hc": "1",
                "gc": "0",
                "hy": "1",
                "gy": "0",
                "hr": "0",
                "gr": "0"
            },
            "plus": {
                "ha": "22",
                "ga": "18",
                "hd": "12",
                "gd": "9",
                "hso": "4",
                "gso": "1",
                "hsf": "3",
                "gsf": "1",
                "hqq": "0",
                "gqq": "0"
            },
            "status": "30",
            "h_ld": {
                "hrf": "0.0",
                "hrfsp": "1.575",
                "grfsp": "2.350",
                "rft": "100",
                "rf": [
                {
                    "hrf": "0.0",
                    "hrfsp": "1.575",
                    "grfsp": "2.350",
                    "rft": "100",
                    "ps": "1787"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.525",
                    "grfsp": "2.425",
                    "rft": "0",
                    "ps": "1729"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "2.425",
                    "grfsp": "1.525",
                    "rft": "0",
                    "ps": "1693"
                },
                {
                    "hrf": null,
                    "hrfsp": null,
                    "grfsp": null,
                    "rft": "100",
                    "ps": "1654"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.575",
                    "grfsp": "2.350",
                    "rft": "0",
                    "ps": "1647"
                }
                ],
                "hdx": "2.5",
                "hdxsp": "2.150",
                "gdxsp": "1.675",
                "dxt": "2",
                "dx": [
                {
                    "hdx": "2.5",
                    "hdxsp": "2.150",
                    "gdxsp": "1.675",
                    "dxt": "2",
                    "ps": "1828"
                },
                {
                    "hdx": "2.5",
                    "hdxsp": "2.100",
                    "gdxsp": "1.700",
                    "dxt": "2",
                    "ps": "1800"
                },
                {
                    "hdx": "2.5",
                    "hdxsp": "2.075",
                    "gdxsp": "1.725",
                    "dxt": "0",
                    "ps": "1787"
                },
                {
                    "hdx": "1.5",
                    "hdxsp": "2.075",
                    "gdxsp": "1.725",
                    "dxt": "2",
                    "ps": "1775"
                },
                {
                    "hdx": "1.5",
                    "hdxsp": "2.050",
                    "gdxsp": "1.750",
                    "dxt": "2",
                    "ps": "1755"
                }
                ]
            },
            "f_ld": {
                "hrf": "-0.5",
                "hrfsp": "1.975",
                "grfsp": "1.825",
                "rft": "2",
                "rf": [
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.975",
                    "grfsp": "1.825",
                    "rft": "2",
                    "ps": "1822"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.950",
                    "grfsp": "1.850",
                    "rft": "100",
                    "ps": "1787"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.900",
                    "grfsp": "1.900",
                    "rft": "0",
                    "ps": "1693"
                },
                {
                    "hrf": null,
                    "hrfsp": null,
                    "grfsp": null,
                    "rft": "100",
                    "ps": "1654"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.900",
                    "grfsp": "1.900",
                    "rft": "2",
                    "ps": "1647"
                }
                ],
                "hdx": "4.5",
                "hdxsp": "1.875",
                "gdxsp": "1.925",
                "dxt": "2",
                "dx": [
                {
                    "hdx": "4.5",
                    "hdxsp": "1.875",
                    "gdxsp": "1.925",
                    "dxt": "2",
                    "ps": "1828"
                },
                {
                    "hdx": "4.5",
                    "hdxsp": "1.850",
                    "gdxsp": "1.950",
                    "dxt": "2",
                    "ps": "1800"
                },
                {
                    "hdx": "4.5",
                    "hdxsp": "1.825",
                    "gdxsp": "1.975",
                    "dxt": "0",
                    "ps": "1787"
                },
                {
                    "hdx": "3.5",
                    "hdxsp": "1.925",
                    "gdxsp": "1.875",
                    "dxt": "2",
                    "ps": "1771"
                },
                {
                    "hdx": "3.5",
                    "hdxsp": "1.900",
                    "gdxsp": "1.900",
                    "dxt": "2",
                    "ps": "1729"
                }
                ]
            },
            "hot": 1
            },
            {
            "id": "1406368",
            "league": {
                "i": "3529",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "澳维超1U23",
                "fn": "澳大利亚维多利亚超级联赛1 23岁以下",
                "ls": "A",
                "sbn": "澳大利亚维多利亚超级联赛1 23岁以下",
                "stn": "澳大利亚维多利亚超级联赛1 23岁以下",
                "spy": "avpl1u23",
                "ci": "7",
                "cn": "澳大利亚",
                "cs": "A"
            },
            "host": {
                "i": "52920",
                "n": "宾特利绿军 23岁以下",
                "sbn": "宾特利绿军 23岁以下",
                "stn": "宾特利绿军 23岁以下"
            },
            "guest": {
                "i": "52918",
                "n": "东方雄狮 23岁以下",
                "sbn": "东方雄狮 23岁以下",
                "stn": "东方雄狮 23岁以下"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 2,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "-0.75",
                "hdx": "4.0",
                "hcb": null
                },
                "h": {
                "hrf": "-0.25",
                "hdx": "1.5",
                "hcb": null
                }
            },
            "events": [
                {
                "t": "hyc",
                "c": "15' ~ 第2张黄牌 ~  ~(宾特利绿军 23岁以下)"
                },
                {
                "t": "gc",
                "c": "12' - 第1角球 - 东方雄狮 23岁以下"
                },
                {
                "t": "gyc",
                "c": "10' ~ 第1张黄牌 ~  ~(东方雄狮 23岁以下)"
                },
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                {
                    "status": "12",
                    "t": "gc",
                    "content": "12' - 第1角球 - 东方雄狮 23岁以下"
                }
                ],
                "ml": "90",
                "status": 17
            },
            "ht": "0",
            "ss": "F",
            "ss_ta": "0",
            "rd": {
                "hg": "0",
                "gg": "0",
                "hc": "0",
                "gc": "1",
                "hy": "1",
                "gy": "1",
                "hr": "0",
                "gr": "0"
            },
            "plus": {
                "ha": "9",
                "ga": "11",
                "hd": "14",
                "gd": "5",
                "hso": "0",
                "gso": "0",
                "hsf": "0",
                "gsf": "0",
                "hqq": "50",
                "gqq": "50"
            },
            "status": "17",
            "h_ld": {
                "hrf": "-0.25",
                "hrfsp": "2.000",
                "grfsp": "1.800",
                "rft": "1",
                "rf": [
                {
                    "hrf": "-0.25",
                    "hrfsp": "2.000",
                    "grfsp": "1.800",
                    "rft": "1",
                    "ps": "1032"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "1.975",
                    "grfsp": "1.825",
                    "rft": "-1",
                    "ps": "960"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "2.000",
                    "grfsp": "1.800",
                    "rft": "2",
                    "ps": "920"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "1.975",
                    "grfsp": "1.825",
                    "rft": "2",
                    "ps": "861"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "1.950",
                    "grfsp": "1.850",
                    "rft": "1",
                    "ps": "753"
                }
                ],
                "hdx": "1.0",
                "hdxsp": "1.775",
                "gdxsp": "2.025",
                "dxt": "-1",
                "dx": [
                {
                    "hdx": "1.0",
                    "hdxsp": "1.775",
                    "gdxsp": "2.025",
                    "dxt": "-1",
                    "ps": "1032"
                },
                {
                    "hdx": "1.0",
                    "hdxsp": "1.800",
                    "gdxsp": "2.000",
                    "dxt": "2",
                    "ps": "1013"
                },
                {
                    "hdx": "1.0",
                    "hdxsp": "1.775",
                    "gdxsp": "2.025",
                    "dxt": "2",
                    "ps": "977"
                },
                {
                    "hdx": "1.0",
                    "hdxsp": "1.750",
                    "gdxsp": "2.050",
                    "dxt": "2",
                    "ps": "960"
                },
                {
                    "hdx": "1.0",
                    "hdxsp": "1.725",
                    "gdxsp": "2.075",
                    "dxt": "0",
                    "ps": "939"
                }
                ]
            },
            "f_ld": {
                "hrf": "-0.75",
                "hrfsp": "1.875",
                "grfsp": "1.925",
                "rft": "1",
                "rf": [
                {
                    "hrf": "-0.75",
                    "hrfsp": "1.875",
                    "grfsp": "1.925",
                    "rft": "1",
                    "ps": "1026"
                },
                {
                    "hrf": "-0.75",
                    "hrfsp": "1.850",
                    "grfsp": "1.950",
                    "rft": "-2",
                    "ps": "960"
                },
                {
                    "hrf": "-0.75",
                    "hrfsp": "1.875",
                    "grfsp": "1.925",
                    "rft": "-1",
                    "ps": "939"
                },
                {
                    "hrf": "-0.75",
                    "hrfsp": "1.900",
                    "grfsp": "1.900",
                    "rft": "2",
                    "ps": "847"
                },
                {
                    "hrf": "-0.75",
                    "hrfsp": "1.875",
                    "grfsp": "1.925",
                    "rft": "2",
                    "ps": "800"
                }
                ],
                "hdx": "3.5",
                "hdxsp": "1.975",
                "gdxsp": "1.825",
                "dxt": "0",
                "dx": [
                {
                    "hdx": "3.5",
                    "hdxsp": "1.975",
                    "gdxsp": "1.825",
                    "dxt": "0",
                    "ps": "1032"
                },
                {
                    "hdx": "3.25",
                    "hdxsp": "1.825",
                    "gdxsp": "1.975",
                    "dxt": "0",
                    "ps": "1026"
                },
                {
                    "hdx": "3.5",
                    "hdxsp": "1.975",
                    "gdxsp": "1.825",
                    "dxt": "1",
                    "ps": "994"
                },
                {
                    "hdx": "3.5",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "-1",
                    "ps": "972"
                },
                {
                    "hdx": "3.5",
                    "hdxsp": "1.975",
                    "gdxsp": "1.825",
                    "dxt": "2",
                    "ps": "960"
                }
                ]
            },
            "hot": 95
            },
            {
            "id": "1406367",
            "league": {
                "i": "3530",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "澳维U23",
                "fn": "澳大利亚NPL维多利亚 23岁以下",
                "ls": "A",
                "sbn": "澳大利亚NPL维多利亚 23岁以下",
                "stn": "澳大利亚NPL维多利亚 23岁以下",
                "spy": "anplvu23",
                "ci": "7",
                "cn": "澳大利亚",
                "cs": "A"
            },
            "host": {
                "i": "52922",
                "n": "普雷斯顿狮子 23岁以下",
                "sbn": "普雷斯顿狮子 23岁以下",
                "stn": "普雷斯顿狮子 23岁以下"
            },
            "guest": {
                "i": "52929",
                "n": "阿尔托纳魔术 23岁以下",
                "sbn": "阿尔托纳魔术 23岁以下",
                "stn": "阿尔托纳魔术 23岁以下"
            },
            "heh": "0",
            "lvc": 0,
            "rcn": 2,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "-0.75",
                "hdx": "3.25",
                "hcb": null
                },
                "h": {
                "hrf": "-0.25",
                "hdx": "1.25",
                "hcb": null
                }
            },
            "events": [
                {
                "t": "gc",
                "c": "16' - 第1角球 - 阿尔托纳魔术 23岁以下"
                },
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                {
                    "status": "16",
                    "t": "gc",
                    "content": "16' - 第1角球 - 阿尔托纳魔术 23岁以下"
                }
                ],
                "ml": "90",
                "status": 16
            },
            "ht": "0",
            "ss": "F",
            "ss_ta": "0",
            "rd": {
                "hg": "0",
                "gg": "0",
                "hc": "0",
                "gc": "1",
                "hy": "0",
                "gy": "0",
                "hr": "0",
                "gr": "0"
            },
            "plus": {
                "ha": "6",
                "ga": "5",
                "hd": "3",
                "gd": "10",
                "hso": "0",
                "gso": "0",
                "hsf": "0",
                "gsf": "0",
                "hqq": "0",
                "gqq": "0"
            },
            "status": "16",
            "h_ld": {
                "hrf": "-0.25",
                "hrfsp": "2.100",
                "grfsp": "1.700",
                "rft": "1",
                "rf": [
                {
                    "hrf": "-0.25",
                    "hrfsp": "2.100",
                    "grfsp": "1.700",
                    "rft": "1",
                    "ps": "976"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "2.050",
                    "grfsp": "1.750",
                    "rft": "-1",
                    "ps": "965"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "2.075",
                    "grfsp": "1.725",
                    "rft": "2",
                    "ps": "927"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "2.050",
                    "grfsp": "1.750",
                    "rft": "2",
                    "ps": "901"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "2.025",
                    "grfsp": "1.775",
                    "rft": "2",
                    "ps": "806"
                }
                ],
                "hdx": "0.75",
                "hdxsp": "1.700",
                "gdxsp": "2.100",
                "dxt": "0",
                "dx": [
                {
                    "hdx": "0.75",
                    "hdxsp": "1.700",
                    "gdxsp": "2.100",
                    "dxt": "0",
                    "ps": "976"
                },
                {
                    "hdx": "1.0",
                    "hdxsp": "2.100",
                    "gdxsp": "1.700",
                    "dxt": "2",
                    "ps": "965"
                },
                {
                    "hdx": "1.0",
                    "hdxsp": "2.050",
                    "gdxsp": "1.750",
                    "dxt": "2",
                    "ps": "947"
                },
                {
                    "hdx": "1.0",
                    "hdxsp": "2.025",
                    "gdxsp": "1.775",
                    "dxt": "1",
                    "ps": "927"
                },
                {
                    "hdx": "1.0",
                    "hdxsp": "2.000",
                    "gdxsp": "1.800",
                    "dxt": "-1",
                    "ps": "901"
                }
                ]
            },
            "f_ld": {
                "hrf": "-0.5",
                "hrfsp": "1.825",
                "grfsp": "1.975",
                "rft": "-1",
                "rf": [
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.825",
                    "grfsp": "1.975",
                    "rft": "-1",
                    "ps": "965"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.850",
                    "grfsp": "1.950",
                    "rft": "2",
                    "ps": "901"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.825",
                    "grfsp": "1.975",
                    "rft": "0",
                    "ps": "806"
                },
                {
                    "hrf": "-0.75",
                    "hrfsp": "1.975",
                    "grfsp": "1.825",
                    "rft": "-1",
                    "ps": "679"
                },
                {
                    "hrf": "-0.75",
                    "hrfsp": "2.000",
                    "grfsp": "1.800",
                    "rft": "2",
                    "ps": "660"
                }
                ],
                "hdx": "2.75",
                "hdxsp": "1.900",
                "gdxsp": "1.900",
                "dxt": "2",
                "dx": [
                {
                    "hdx": "2.75",
                    "hdxsp": "1.900",
                    "gdxsp": "1.900",
                    "dxt": "2",
                    "ps": "982"
                },
                {
                    "hdx": "2.75",
                    "hdxsp": "1.875",
                    "gdxsp": "1.925",
                    "dxt": "2",
                    "ps": "976"
                },
                {
                    "hdx": "2.75",
                    "hdxsp": "1.850",
                    "gdxsp": "1.950",
                    "dxt": "2",
                    "ps": "965"
                },
                {
                    "hdx": "2.75",
                    "hdxsp": "1.825",
                    "gdxsp": "1.975",
                    "dxt": "1",
                    "ps": "947"
                },
                {
                    "hdx": "2.75",
                    "hdxsp": "1.800",
                    "gdxsp": "2.000",
                    "dxt": "-2",
                    "ps": "873"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1406881",
            "league": {
                "i": "3529",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "澳维超1U23",
                "fn": "澳大利亚维多利亚超级联赛1 23岁以下",
                "ls": "A",
                "sbn": "澳大利亚维多利亚超级联赛1 23岁以下",
                "stn": "澳大利亚维多利亚超级联赛1 23岁以下",
                "spy": "avpl1u23",
                "ci": "7",
                "cn": "澳大利亚",
                "cs": "A"
            },
            "host": {
                "i": "56209",
                "n": "北鹰阳光 23岁以下",
                "sbn": "北鹰阳光 23岁以下",
                "stn": "北鹰阳光 23岁以下"
            },
            "guest": {
                "i": "52928",
                "n": "莫兰德城 23岁以下",
                "sbn": "莫兰德城 23岁以下",
                "stn": "莫兰德城 23岁以下"
            },
            "heh": "0",
            "lvc": 0,
            "rcn": 1,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "-0.25",
                "hdx": "4.0",
                "hcb": null
                },
                "h": {
                "hrf": "0.0",
                "hdx": "1.5",
                "hcb": null
                }
            },
            "events": [
                {
                "t": "gg",
                "c": "16' - 第1个进球 -   (莫兰德城 23岁以下) -"
                },
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                {
                    "status": "16",
                    "t": "gg",
                    "content": "16' - 第1个进球 -   (莫兰德城 23岁以下) -"
                }
                ],
                "ml": "90",
                "status": 15
            },
            "ht": "0",
            "ss": "F",
            "ss_ta": "0",
            "rd": {
                "hg": "0",
                "gg": "1",
                "hc": "0",
                "gc": "0",
                "hy": "0",
                "gy": "0",
                "hr": "0",
                "gr": "0"
            },
            "plus": {
                "ha": "8",
                "ga": "14",
                "hd": "4",
                "gd": "7",
                "hso": "2",
                "gso": "1",
                "hsf": "1",
                "gsf": "2",
                "hqq": "0",
                "gqq": "0"
            },
            "status": "15",
            "h_ld": {
                "hrf": "+0.25",
                "hrfsp": "1.700",
                "grfsp": "2.100",
                "rft": "100",
                "rf": [
                {
                    "hrf": "+0.25",
                    "hrfsp": "1.700",
                    "grfsp": "2.100",
                    "rft": "100",
                    "ps": "925"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "2.150",
                    "grfsp": "1.675",
                    "rft": "2",
                    "ps": "858"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "2.100",
                    "grfsp": "1.700",
                    "rft": "0",
                    "ps": "820"
                },
                {
                    "hrf": "+0.25",
                    "hrfsp": "1.725",
                    "grfsp": "2.075",
                    "rft": "-2",
                    "ps": "550"
                },
                {
                    "hrf": "+0.25",
                    "hrfsp": "1.750",
                    "grfsp": "2.050",
                    "rft": "-2",
                    "ps": "477"
                }
                ],
                "hdx": "2.25",
                "hdxsp": "2.000",
                "gdxsp": "1.800",
                "dxt": "2",
                "dx": [
                {
                    "hdx": "2.25",
                    "hdxsp": "2.000",
                    "gdxsp": "1.800",
                    "dxt": "2",
                    "ps": "939"
                },
                {
                    "hdx": "2.25",
                    "hdxsp": "1.975",
                    "gdxsp": "1.825",
                    "dxt": "0",
                    "ps": "925"
                },
                {
                    "hdx": "1.25",
                    "hdxsp": "1.975",
                    "gdxsp": "1.825",
                    "dxt": "-1",
                    "ps": "912"
                },
                {
                    "hdx": "1.25",
                    "hdxsp": "2.000",
                    "gdxsp": "1.800",
                    "dxt": "2",
                    "ps": "897"
                },
                {
                    "hdx": "1.25",
                    "hdxsp": "1.975",
                    "gdxsp": "1.825",
                    "dxt": "2",
                    "ps": "869"
                }
                ]
            },
            "f_ld": {
                "hrf": "+0.25",
                "hrfsp": "2.000",
                "grfsp": "1.800",
                "rft": "100",
                "rf": [
                {
                    "hrf": "+0.25",
                    "hrfsp": "2.000",
                    "grfsp": "1.800",
                    "rft": "100",
                    "ps": "925"
                },
                {
                    "hrf": "+0.25",
                    "hrfsp": "1.925",
                    "grfsp": "1.875",
                    "rft": "0",
                    "ps": "820"
                },
                {
                    "hrf": "+0.5",
                    "hrfsp": "1.850",
                    "grfsp": "1.950",
                    "rft": "1",
                    "ps": "801"
                },
                {
                    "hrf": "+0.5",
                    "hrfsp": "1.825",
                    "grfsp": "1.975",
                    "rft": "-2",
                    "ps": "486"
                },
                {
                    "hrf": "+0.5",
                    "hrfsp": "1.850",
                    "grfsp": "1.950",
                    "rft": "-1",
                    "ps": "421"
                }
                ],
                "hdx": "4.75",
                "hdxsp": "2.000",
                "gdxsp": "1.800",
                "dxt": "2",
                "dx": [
                {
                    "hdx": "4.75",
                    "hdxsp": "2.000",
                    "gdxsp": "1.800",
                    "dxt": "2",
                    "ps": "948"
                },
                {
                    "hdx": "4.75",
                    "hdxsp": "1.975",
                    "gdxsp": "1.825",
                    "dxt": "0",
                    "ps": "925"
                },
                {
                    "hdx": "3.5",
                    "hdxsp": "1.825",
                    "gdxsp": "1.975",
                    "dxt": "2",
                    "ps": "897"
                },
                {
                    "hdx": "3.5",
                    "hdxsp": "1.800",
                    "gdxsp": "2.000",
                    "dxt": "0",
                    "ps": "869"
                },
                {
                    "hdx": "3.75",
                    "hdxsp": "2.000",
                    "gdxsp": "1.800",
                    "dxt": "2",
                    "ps": "858"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1406363",
            "league": {
                "i": "3530",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "澳维U23",
                "fn": "澳大利亚NPL维多利亚 23岁以下",
                "ls": "A",
                "sbn": "澳大利亚NPL维多利亚 23岁以下",
                "stn": "澳大利亚NPL维多利亚 23岁以下",
                "spy": "anplvu23",
                "ci": "7",
                "cn": "澳大利亚",
                "cs": "A"
            },
            "host": {
                "i": "52933",
                "n": "墨尔本港 23岁以下",
                "sbn": "墨尔本港 23岁以下",
                "stn": "墨尔本港 23岁以下"
            },
            "guest": {
                "i": "52923",
                "n": "欧克莱卡诺 23岁以下",
                "sbn": "欧克莱卡诺 23岁以下",
                "stn": "欧克莱卡诺 23岁以下"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 2,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "+0.25",
                "hdx": "3.75",
                "hcb": null
                },
                "h": {
                "hrf": "0.0",
                "hdx": "1.5",
                "hcb": null
                }
            },
            "events": [
                {
                "t": "hrc",
                "c": "6' ~ 第1红牌 ~  ~(墨尔本港 23岁以下)"
                },
                {
                "t": "gc",
                "c": "2' - 第1角球 - 欧克莱卡诺 23岁以下"
                },
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                {
                    "status": "2",
                    "t": "gc",
                    "content": "2' - 第1角球 - 欧克莱卡诺 23岁以下"
                },
                {
                    "status": "6",
                    "t": "hrc",
                    "content": "6' ~ 第1红牌 ~  ~(墨尔本港 23岁以下)"
                }
                ],
                "ml": "90",
                "status": 11
            },
            "ht": "0",
            "ss": "F",
            "ss_ta": "0",
            "rd": {
                "hg": "0",
                "gg": "0",
                "hc": "0",
                "gc": "1",
                "hy": "0",
                "gy": "0",
                "hr": "1",
                "gr": "0"
            },
            "plus": {
                "ha": "7",
                "ga": "14",
                "hd": "2",
                "gd": "10",
                "hso": "0",
                "gso": "0",
                "hsf": "1",
                "gsf": "1",
                "hqq": "0",
                "gqq": "0"
            },
            "status": "11",
            "h_ld": {
                "hrf": "+0.5",
                "hrfsp": "1.950",
                "grfsp": "1.850",
                "rft": "2",
                "rf": [
                {
                    "hrf": "+0.5",
                    "hrfsp": "1.950",
                    "grfsp": "1.850",
                    "rft": "2",
                    "ps": "678"
                },
                {
                    "hrf": "+0.5",
                    "hrfsp": "1.925",
                    "grfsp": "1.875",
                    "rft": "1",
                    "ps": "669"
                },
                {
                    "hrf": "+0.5",
                    "hrfsp": "1.900",
                    "grfsp": "1.900",
                    "rft": "-2",
                    "ps": "626"
                },
                {
                    "hrf": "+0.5",
                    "hrfsp": "1.925",
                    "grfsp": "1.875",
                    "rft": "-1",
                    "ps": "608"
                },
                {
                    "hrf": "+0.5",
                    "hrfsp": "1.950",
                    "grfsp": "1.850",
                    "rft": "1",
                    "ps": "597"
                }
                ],
                "hdx": "1.25",
                "hdxsp": "1.800",
                "gdxsp": "2.000",
                "dxt": "-2",
                "dx": [
                {
                    "hdx": "1.25",
                    "hdxsp": "1.800",
                    "gdxsp": "2.000",
                    "dxt": "-2",
                    "ps": "678"
                },
                {
                    "hdx": "1.25",
                    "hdxsp": "1.850",
                    "gdxsp": "1.950",
                    "dxt": "-1",
                    "ps": "666"
                },
                {
                    "hdx": "1.25",
                    "hdxsp": "1.900",
                    "gdxsp": "1.900",
                    "dxt": "2",
                    "ps": "640"
                },
                {
                    "hdx": "1.25",
                    "hdxsp": "1.875",
                    "gdxsp": "1.925",
                    "dxt": "2",
                    "ps": "616"
                },
                {
                    "hdx": "1.25",
                    "hdxsp": "1.850",
                    "gdxsp": "1.950",
                    "dxt": "2",
                    "ps": "608"
                }
                ]
            },
            "f_ld": {
                "hrf": "+1.5",
                "hrfsp": "1.975",
                "grfsp": "1.825",
                "rft": "1",
                "rf": [
                {
                    "hrf": "+1.5",
                    "hrfsp": "1.975",
                    "grfsp": "1.825",
                    "rft": "1",
                    "ps": "678"
                },
                {
                    "hrf": "+1.5",
                    "hrfsp": "1.900",
                    "grfsp": "1.900",
                    "rft": "-1",
                    "ps": "669"
                },
                {
                    "hrf": "+1.5",
                    "hrfsp": "1.950",
                    "grfsp": "1.850",
                    "rft": "2",
                    "ps": "616"
                },
                {
                    "hrf": "+1.5",
                    "hrfsp": "1.925",
                    "grfsp": "1.875",
                    "rft": "1",
                    "ps": "608"
                },
                {
                    "hrf": "+1.5",
                    "hrfsp": "1.900",
                    "grfsp": "1.900",
                    "rft": "-1",
                    "ps": "572"
                }
                ],
                "hdx": "3.75",
                "hdxsp": "1.950",
                "gdxsp": "1.850",
                "dxt": "0",
                "dx": [
                {
                    "hdx": "3.75",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "0",
                    "ps": "678"
                },
                {
                    "hdx": "3.5",
                    "hdxsp": "1.875",
                    "gdxsp": "1.925",
                    "dxt": "2",
                    "ps": "669"
                },
                {
                    "hdx": "3.5",
                    "hdxsp": "1.850",
                    "gdxsp": "1.950",
                    "dxt": "2",
                    "ps": "640"
                },
                {
                    "hdx": "3.5",
                    "hdxsp": "1.825",
                    "gdxsp": "1.975",
                    "dxt": "0",
                    "ps": "608"
                },
                {
                    "hdx": "3.75",
                    "hdxsp": "2.000",
                    "gdxsp": "1.800",
                    "dxt": "2",
                    "ps": "572"
                }
                ]
            },
            "hot": 3
            },
            {
            "id": "1406724",
            "league": {
                "i": "2241",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "印尼L2",
                "fn": "印尼Liga 2",
                "ls": "Y",
                "sbn": "印尼Liga 2",
                "stn": "印尼Liga 2",
                "spy": "yinni2",
                "ci": "65",
                "cn": "印度尼西亚",
                "cs": "Y"
            },
            "host": {
                "i": "30729",
                "n": "帕庄内格洛Bojonegoro",
                "sbn": "帕庄内格洛Bojonegoro",
                "stn": "帕庄内格洛Bojonegoro"
            },
            "guest": {
                "i": "1280",
                "n": "格勒斯克联",
                "sbn": "格勒斯克联",
                "stn": "格勒斯克联"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "-0.25",
                "hdx": "2.25",
                "hcb": null
                },
                "h": {
                "hrf": "0.0",
                "hdx": "1.0",
                "hcb": null
                }
            },
            "rtime": "2025/02/21 16:00",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "ht": "0",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "-0.25",
                "hrfsp": "1.975",
                "grfsp": "1.825",
                "rft": "-1",
                "rf": [
                {
                    "hrf": "-0.25",
                    "hrfsp": "1.975",
                    "grfsp": "1.825",
                    "rft": "-1",
                    "ps": "0"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "2.050",
                    "grfsp": "1.750",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.800",
                    "grfsp": "2.000",
                    "rft": "-1",
                    "ps": "0"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.950",
                    "grfsp": "1.850",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "1.775",
                    "grfsp": "2.025",
                    "rft": "0",
                    "ps": "0"
                }
                ],
                "hdx": "2.25",
                "hdxsp": "1.925",
                "gdxsp": "1.875",
                "dxt": "1",
                "dx": [
                {
                    "hdx": "2.25",
                    "hdxsp": "1.925",
                    "gdxsp": "1.875",
                    "dxt": "1",
                    "ps": "0"
                },
                {
                    "hdx": "2.25",
                    "hdxsp": "1.875",
                    "gdxsp": "1.925",
                    "dxt": "-1",
                    "ps": "0"
                },
                {
                    "hdx": "2.25",
                    "hdxsp": "1.975",
                    "gdxsp": "1.825",
                    "dxt": "1",
                    "ps": "0"
                },
                {
                    "hdx": "2.25",
                    "hdxsp": "1.850",
                    "gdxsp": "1.950",
                    "dxt": "-1",
                    "ps": "0"
                },
                {
                    "hdx": "2.25",
                    "hdxsp": "2.000",
                    "gdxsp": "1.800",
                    "dxt": "0",
                    "ps": "0"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1405854",
            "league": {
                "i": "723",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "澳威超",
                "fn": "澳大利亚新南威尔士超级联赛",
                "ls": "A",
                "sbn": "澳大利亚新南威尔士超级联赛",
                "stn": "澳大利亚新南威尔士超级联赛",
                "spy": "aoxinnanchao",
                "ci": "7",
                "cn": "澳大利亚",
                "cs": "A"
            },
            "host": {
                "i": "42445",
                "n": "西悉尼流浪者NPL",
                "sbn": "西悉尼流浪者NPL",
                "stn": "西悉尼流浪者NPL",
                "p": "7"
            },
            "guest": {
                "i": "7673",
                "n": "萨瑟兰鲨鱼",
                "sbn": "萨瑟兰鲨鱼",
                "stn": "萨瑟兰鲨鱼",
                "p": "4"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "+0.25",
                "hdx": "3.25",
                "hcb": "9.5"
                },
                "h": {
                "hrf": "0.0",
                "hdx": "1.25",
                "hcb": "4.5"
                }
            },
            "rtime": "2025/02/21 16:00",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "ht": "0",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "+0.25",
                "hrfsp": "1.950",
                "grfsp": "1.850",
                "rft": "0",
                "rf": [
                {
                    "hrf": "+0.25",
                    "hrfsp": "1.950",
                    "grfsp": "1.850",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "+0.5",
                    "hrfsp": "1.800",
                    "grfsp": "2.000",
                    "rft": "-1",
                    "ps": "0"
                },
                {
                    "hrf": "+0.5",
                    "hrfsp": "1.825",
                    "grfsp": "1.975",
                    "rft": "2",
                    "ps": "0"
                },
                {
                    "hrf": "+0.5",
                    "hrfsp": "1.800",
                    "grfsp": "2.000",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "+0.25",
                    "hrfsp": "2.000",
                    "grfsp": "1.800",
                    "rft": "1",
                    "ps": "0"
                }
                ],
                "hdx": "3.25",
                "hdxsp": "2.000",
                "gdxsp": "1.800",
                "dxt": "2",
                "dx": [
                {
                    "hdx": "3.25",
                    "hdxsp": "2.000",
                    "gdxsp": "1.800",
                    "dxt": "2",
                    "ps": "0"
                },
                {
                    "hdx": "3.25",
                    "hdxsp": "1.975",
                    "gdxsp": "1.825",
                    "dxt": "1",
                    "ps": "0"
                },
                {
                    "hdx": "3.25",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "-1",
                    "ps": "0"
                },
                {
                    "hdx": "3.25",
                    "hdxsp": "1.975",
                    "gdxsp": "1.825",
                    "dxt": "2",
                    "ps": "0"
                },
                {
                    "hdx": "3.25",
                    "hdxsp": "1.850",
                    "gdxsp": "1.950",
                    "dxt": "2",
                    "ps": "0"
                }
                ],
                "hcb": "9.5",
                "hcbsp": "1.825",
                "gcbsp": "1.975",
                "cbt": "100",
                "cb": [
                {
                    "hcb": "9.5",
                    "hcbsp": "1.825",
                    "gcbsp": "1.975",
                    "cbt": "100",
                    "ps": "0"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1407087",
            "league": {
                "i": "2283",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "菲足联",
                "fn": "菲律宾足球联赛",
                "ls": "F",
                "sbn": "菲律宾足球联赛",
                "stn": "菲律宾足球联赛",
                "spy": "pfl",
                "ci": "19",
                "cn": "菲律宾",
                "cs": "F"
            },
            "host": {
                "i": "9332",
                "n": "洛约拉FC",
                "sbn": "洛约拉足球俱乐部",
                "stn": "洛约拉足球俱乐部"
            },
            "guest": {
                "i": "11973",
                "n": "Mendiola FC",
                "sbn": "曼迪奥拉",
                "stn": "曼迪奥拉"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "-3.25",
                "hdx": "4.75",
                "hcb": null
                },
                "h": {
                "hrf": "-1.25",
                "hdx": "2.0",
                "hcb": null
                }
            },
            "rtime": "2025/02/21 16:00",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "ht": "0",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "-4.25",
                "hrfsp": "1.850",
                "grfsp": "1.950",
                "rft": "0",
                "rf": [
                {
                    "hrf": "-4.25",
                    "hrfsp": "1.850",
                    "grfsp": "1.950",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "-3.25",
                    "hrfsp": "1.900",
                    "grfsp": "1.900",
                    "rft": "100",
                    "ps": "0"
                }
                ],
                "hdx": "5.0",
                "hdxsp": "1.925",
                "gdxsp": "1.875",
                "dxt": "0",
                "dx": [
                {
                    "hdx": "5.0",
                    "hdxsp": "1.925",
                    "gdxsp": "1.875",
                    "dxt": "0",
                    "ps": "0"
                },
                {
                    "hdx": "4.75",
                    "hdxsp": "1.900",
                    "gdxsp": "1.900",
                    "dxt": "0",
                    "ps": "0"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1406942",
            "league": {
                "i": "2574",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "越锦女U19",
                "fn": "越南锦标赛 19岁以下 女子",
                "ls": "Y",
                "sbn": "越南锦标赛 19岁以下 女子",
                "stn": "越南锦标赛 19岁以下 女子",
                "spy": "yunanjinu19nv",
                "ci": "78",
                "cn": "越南",
                "cs": "Y"
            },
            "host": {
                "i": "26990",
                "n": "丰富府里 19岁以下 女子",
                "sbn": "丰富府里女足U19",
                "stn": "丰富府里女足U19"
            },
            "guest": {
                "i": "47103",
                "n": "越南太原 19 岁以下 女子",
                "sbn": "Thai Nguyen 19 岁以下",
                "stn": "Thai Nguyen 19 岁以下"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "-0.75",
                "hdx": "2.5",
                "hcb": null
                },
                "h": {
                "hrf": "-0.25",
                "hdx": "1.0",
                "hcb": null
                }
            },
            "rtime": "2025/02/21 16:00",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "ht": "0",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "-0.75",
                "hrfsp": "1.925",
                "grfsp": "1.875",
                "rft": "-1",
                "rf": [
                {
                    "hrf": "-0.75",
                    "hrfsp": "1.925",
                    "grfsp": "1.875",
                    "rft": "-1",
                    "ps": "0"
                },
                {
                    "hrf": "-0.75",
                    "hrfsp": "2.000",
                    "grfsp": "1.800",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "-1.0",
                    "hrfsp": "1.950",
                    "grfsp": "1.850",
                    "rft": "100",
                    "ps": "0"
                }
                ],
                "hdx": "2.5",
                "hdxsp": "1.950",
                "gdxsp": "1.850",
                "dxt": "2",
                "dx": [
                {
                    "hdx": "2.5",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "2",
                    "ps": "0"
                },
                {
                    "hdx": "2.5",
                    "hdxsp": "1.800",
                    "gdxsp": "2.000",
                    "dxt": "0",
                    "ps": "0"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1406943",
            "league": {
                "i": "2574",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "越锦女U19",
                "fn": "越南锦标赛 19岁以下 女子",
                "ls": "Y",
                "sbn": "越南锦标赛 19岁以下 女子",
                "stn": "越南锦标赛 19岁以下 女子",
                "spy": "yunanjinu19nv",
                "ci": "78",
                "cn": "越南",
                "cs": "Y"
            },
            "host": {
                "i": "32429",
                "n": "Than KSVN 女子 19岁以下",
                "sbn": "陶翰KSN女足U19",
                "stn": "陶翰KSN女足U19"
            },
            "guest": {
                "i": "54975",
                "n": "永福 19岁以下 女子",
                "sbn": "永福 19岁以下 女子",
                "stn": "永福 19岁以下 女子"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "+0.5",
                "hdx": "3.25",
                "hcb": null
                },
                "h": {
                "hrf": "0.0",
                "hdx": "1.5",
                "hcb": null
                }
            },
            "rtime": "2025/02/21 16:00",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "ht": "0",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "+0.5",
                "hrfsp": "1.900",
                "grfsp": "1.900",
                "rft": "0",
                "rf": [
                {
                    "hrf": "+0.5",
                    "hrfsp": "1.900",
                    "grfsp": "1.900",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.950",
                    "grfsp": "1.850",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "+0.25",
                    "hrfsp": "1.775",
                    "grfsp": "2.025",
                    "rft": "-1",
                    "ps": "0"
                },
                {
                    "hrf": "+0.25",
                    "hrfsp": "1.950",
                    "grfsp": "1.850",
                    "rft": "1",
                    "ps": "0"
                },
                {
                    "hrf": "+0.25",
                    "hrfsp": "0.000",
                    "grfsp": "0.000",
                    "rft": "-1",
                    "ps": "0"
                }
                ],
                "hdx": "3.25",
                "hdxsp": "1.800",
                "gdxsp": "2.000",
                "dxt": "0",
                "dx": [
                {
                    "hdx": "3.25",
                    "hdxsp": "1.800",
                    "gdxsp": "2.000",
                    "dxt": "0",
                    "ps": "0"
                },
                {
                    "hdx": "3.5",
                    "hdxsp": "1.825",
                    "gdxsp": "1.975",
                    "dxt": "-1",
                    "ps": "0"
                },
                {
                    "hdx": "3.5",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "0",
                    "ps": "0"
                },
                {
                    "hdx": "3.25",
                    "hdxsp": "1.850",
                    "gdxsp": "1.950",
                    "dxt": "0",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "0",
                    "gdxsp": "0",
                    "dxt": "-2",
                    "ps": "0"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1406711",
            "league": {
                "i": "1102",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "印I联2D",
                "fn": "印度I联赛2nd Division",
                "ls": "Y",
                "sbn": "印度I联赛2nd Division",
                "stn": "印度I联赛2nd Division",
                "spy": "ill2d",
                "ci": "17",
                "cn": "印度",
                "cs": "Y"
            },
            "host": {
                "i": "39588",
                "n": "KLASA",
                "sbn": "克拉萨",
                "stn": "克拉萨",
                "p": "8"
            },
            "guest": {
                "i": "22864",
                "n": "尼罗卡FC",
                "sbn": "尼罗卡",
                "stn": "尼罗卡",
                "p": "7"
            },
            "heh": "0",
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "+0.75",
                "hdx": "3.0",
                "hcb": null
                },
                "h": {
                "hrf": "+0.25",
                "hdx": "1.25",
                "hcb": null
                }
            },
            "rtime": "2025/02/21 16:30",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "ht": "0",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "+0.75",
                "hrfsp": "1.900",
                "grfsp": "1.900",
                "rft": "100",
                "rf": [
                {
                    "hrf": "+0.75",
                    "hrfsp": "1.900",
                    "grfsp": "1.900",
                    "rft": "100",
                    "ps": "0"
                }
                ],
                "hdx": "3.0",
                "hdxsp": "1.900",
                "gdxsp": "1.900",
                "dxt": "0",
                "dx": [
                {
                    "hdx": "3.0",
                    "hdxsp": "1.900",
                    "gdxsp": "1.900",
                    "dxt": "0",
                    "ps": "0"
                },
                {
                    "hdx": "2.5",
                    "hdxsp": "1.900",
                    "gdxsp": "1.900",
                    "dxt": "0",
                    "ps": "0"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1406091",
            "league": {
                "i": "196",
                "zc": "1",
                "jc": "0",
                "bd": "0",
                "n": "印尼超",
                "fn": "印度尼西亚甲级联赛",
                "ls": "Y",
                "sbn": "印度尼西亚超级联赛",
                "stn": "印度尼西亚超级联赛",
                "spy": "yinnichao",
                "ci": "65",
                "cn": "印度尼西亚",
                "cs": "Y"
            },
            "host": {
                "i": "26664",
                "n": "巴克伦佛",
                "sbn": "PSBS巴克伦佛",
                "stn": "巴克伦佛",
                "p": "12"
            },
            "guest": {
                "i": "1651",
                "n": "佩斯凯迪瑞",
                "sbn": "佩斯克",
                "stn": "佩斯凯迪瑞",
                "p": "11"
            },
            "heh": "1",
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "-0.25",
                "hdx": "2.5",
                "hcb": "9"
                },
                "h": {
                "hrf": "-0.25",
                "hdx": "1.0",
                "hcb": "4.5"
                }
            },
            "rtime": "2025/02/21 16:30",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "ht": "0",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "-0.25",
                "hrfsp": "1.800",
                "grfsp": "2.000",
                "rft": "2",
                "rf": [
                {
                    "hrf": "-0.25",
                    "hrfsp": "1.800",
                    "grfsp": "2.000",
                    "rft": "2",
                    "ps": "0"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "1.775",
                    "grfsp": "2.025",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.975",
                    "grfsp": "1.825",
                    "rft": "-1",
                    "ps": "0"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "2.000",
                    "grfsp": "1.800",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "1.775",
                    "grfsp": "2.025",
                    "rft": "0",
                    "ps": "0"
                }
                ],
                "hdx": "2.5",
                "hdxsp": "1.950",
                "gdxsp": "1.850",
                "dxt": "1",
                "dx": [
                {
                    "hdx": "2.5",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "1",
                    "ps": "0"
                },
                {
                    "hdx": "2.5",
                    "hdxsp": "1.925",
                    "gdxsp": "1.875",
                    "dxt": "-1",
                    "ps": "0"
                },
                {
                    "hdx": "2.5",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "1",
                    "ps": "0"
                },
                {
                    "hdx": "2.5",
                    "hdxsp": "1.925",
                    "gdxsp": "1.875",
                    "dxt": "-1",
                    "ps": "0"
                },
                {
                    "hdx": "2.5",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "1",
                    "ps": "0"
                }
                ],
                "hcb": "9",
                "hcbsp": "1.850",
                "gcbsp": "1.950",
                "cbt": "0",
                "cb": [
                {
                    "hcb": "9",
                    "hcbsp": "1.850",
                    "gcbsp": "1.950",
                    "cbt": "0",
                    "ps": "0"
                },
                {
                    "hcb": "8.5",
                    "hcbsp": "1.850",
                    "gcbsp": "1.950",
                    "cbt": "100",
                    "ps": "0"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1405417",
            "league": {
                "i": "196",
                "zc": "1",
                "jc": "0",
                "bd": "0",
                "n": "印尼超",
                "fn": "印度尼西亚甲级联赛",
                "ls": "Y",
                "sbn": "印度尼西亚超级联赛",
                "stn": "印度尼西亚超级联赛",
                "spy": "yinnichao",
                "ci": "65",
                "cn": "印度尼西亚",
                "cs": "Y"
            },
            "host": {
                "i": "4117",
                "n": "佩斯斯索罗",
                "sbn": "伯希索罗",
                "stn": "佩斯斯索罗",
                "p": "18"
            },
            "guest": {
                "i": "1652",
                "n": "塞曼巴东",
                "sbn": "塞曼巴东",
                "stn": "塞曼巴东",
                "p": "15"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "-0.25",
                "hdx": "2.5",
                "hcb": "9.5"
                },
                "h": {
                "hrf": "-0.25",
                "hdx": "1.0",
                "hcb": "4.5"
                }
            },
            "rtime": "2025/02/21 16:30",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "ht": "0",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "-0.25",
                "hrfsp": "1.825",
                "grfsp": "1.975",
                "rft": "0",
                "rf": [
                {
                    "hrf": "-0.25",
                    "hrfsp": "1.825",
                    "grfsp": "1.975",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "2.000",
                    "grfsp": "1.800",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "1.825",
                    "grfsp": "1.975",
                    "rft": "-1",
                    "ps": "0"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "1.850",
                    "grfsp": "1.950",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.825",
                    "grfsp": "1.975",
                    "rft": "0",
                    "ps": "0"
                }
                ],
                "hdx": "2.5",
                "hdxsp": "1.950",
                "gdxsp": "1.850",
                "dxt": "1",
                "dx": [
                {
                    "hdx": "2.5",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "1",
                    "ps": "0"
                },
                {
                    "hdx": "2.5",
                    "hdxsp": "1.925",
                    "gdxsp": "1.875",
                    "dxt": "-1",
                    "ps": "0"
                },
                {
                    "hdx": "2.5",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "1",
                    "ps": "0"
                },
                {
                    "hdx": "2.5",
                    "hdxsp": "1.925",
                    "gdxsp": "1.875",
                    "dxt": "-1",
                    "ps": "0"
                },
                {
                    "hdx": "2.5",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "1",
                    "ps": "0"
                }
                ],
                "hcb": "9.5",
                "hcbsp": "1.850",
                "gcbsp": "1.950",
                "cbt": "0",
                "cb": [
                {
                    "hcb": "9.5",
                    "hcbsp": "1.850",
                    "gcbsp": "1.950",
                    "cbt": "0",
                    "ps": "0"
                },
                {
                    "hcb": "10",
                    "hcbsp": "1.925",
                    "gcbsp": "1.875",
                    "cbt": "100",
                    "ps": "0"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1406720",
            "league": {
                "i": "3542",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "埃塞高等联",
                "fn": "埃塞俄比亚Higher联赛",
                "ls": "A",
                "sbn": "埃塞俄比亚高等联赛",
                "stn": "埃塞俄比亚高等联赛",
                "spy": "ehl",
                "ci": "43",
                "cn": "埃塞俄比亚",
                "cs": "A"
            },
            "host": {
                "i": "53152",
                "n": "哈拉巴城",
                "sbn": "哈拉巴城",
                "stn": "哈拉巴城"
            },
            "guest": {
                "i": "53197",
                "n": "Dessie凯特玛",
                "sbn": "Dessie凯特玛",
                "stn": "Dessie凯特玛"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "-0.25",
                "hdx": "2.0",
                "hcb": null
                },
                "h": {
                "hrf": "0.0",
                "hdx": "0.75",
                "hcb": null
                }
            },
            "rtime": "2025/02/21 16:30",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "ht": "0",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "-0.25",
                "hrfsp": "2.000",
                "grfsp": "1.800",
                "rft": "100",
                "rf": [
                {
                    "hrf": "-0.25",
                    "hrfsp": "2.000",
                    "grfsp": "1.800",
                    "rft": "100",
                    "ps": "0"
                }
                ],
                "hdx": "2.0",
                "hdxsp": "1.900",
                "gdxsp": "1.900",
                "dxt": "0",
                "dx": [
                {
                    "hdx": "2.0",
                    "hdxsp": "1.900",
                    "gdxsp": "1.900",
                    "dxt": "0",
                    "ps": "0"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1405857",
            "league": {
                "i": "723",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "澳威超",
                "fn": "澳大利亚新南威尔士超级联赛",
                "ls": "A",
                "sbn": "澳大利亚新南威尔士超级联赛",
                "stn": "澳大利亚新南威尔士超级联赛",
                "spy": "aoxinnanchao",
                "ci": "7",
                "cn": "澳大利亚",
                "cs": "A"
            },
            "host": {
                "i": "6941",
                "n": "曼立联",
                "sbn": "猛男联队",
                "stn": "曼立联",
                "p": "8"
            },
            "guest": {
                "i": "7473",
                "n": "悉尼联58",
                "sbn": "悉尼联盟",
                "stn": "悉尼联58",
                "p": "11"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "0.0",
                "hdx": "2.75",
                "hcb": "10.5"
                },
                "h": {
                "hrf": "0.0",
                "hdx": "1.0",
                "hcb": "5"
                }
            },
            "rtime": "2025/02/21 16:30",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "ht": "0",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "0.0",
                "hrfsp": "1.775",
                "grfsp": "2.025",
                "rft": "0",
                "rf": [
                {
                    "hrf": "0.0",
                    "hrfsp": "1.775",
                    "grfsp": "2.025",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "1.975",
                    "grfsp": "1.825",
                    "rft": "2",
                    "ps": "0"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "1.950",
                    "grfsp": "1.850",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "2.000",
                    "grfsp": "1.800",
                    "rft": "2",
                    "ps": "0"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.975",
                    "grfsp": "1.825",
                    "rft": "2",
                    "ps": "0"
                }
                ],
                "hdx": "2.75",
                "hdxsp": "1.900",
                "gdxsp": "1.900",
                "dxt": "1",
                "dx": [
                {
                    "hdx": "2.75",
                    "hdxsp": "1.900",
                    "gdxsp": "1.900",
                    "dxt": "1",
                    "ps": "0"
                },
                {
                    "hdx": "2.75",
                    "hdxsp": "1.800",
                    "gdxsp": "2.000",
                    "dxt": "-2",
                    "ps": "0"
                },
                {
                    "hdx": "2.75",
                    "hdxsp": "1.900",
                    "gdxsp": "1.900",
                    "dxt": "-2",
                    "ps": "0"
                },
                {
                    "hdx": "2.75",
                    "hdxsp": "1.925",
                    "gdxsp": "1.875",
                    "dxt": "-1",
                    "ps": "0"
                },
                {
                    "hdx": "2.75",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "2",
                    "ps": "0"
                }
                ],
                "hcb": "10.5",
                "hcbsp": "1.925",
                "gcbsp": "1.875",
                "cbt": "100",
                "cb": [
                {
                    "hcb": "10.5",
                    "hcbsp": "1.925",
                    "gcbsp": "1.875",
                    "cbt": "100",
                    "ps": "0"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1405860",
            "league": {
                "i": "723",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "澳威超",
                "fn": "澳大利亚新南威尔士超级联赛",
                "ls": "A",
                "sbn": "澳大利亚新南威尔士超级联赛",
                "stn": "澳大利亚新南威尔士超级联赛",
                "spy": "aoxinnanchao",
                "ci": "7",
                "cn": "澳大利亚",
                "cs": "A"
            },
            "host": {
                "i": "14908",
                "n": "圣乔治圣徒",
                "sbn": "FC圣乔治",
                "stn": "St George Saints",
                "p": "15"
            },
            "guest": {
                "i": "15388",
                "n": "芒特德瑞特城流浪者",
                "sbn": "米特卓瑞特",
                "stn": "米特 德瑞特 Town Rangers",
                "p": "12"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "-0.25",
                "hdx": "3.0",
                "hcb": "9"
                },
                "h": {
                "hrf": "-0.25",
                "hdx": "1.25",
                "hcb": "4"
                }
            },
            "rtime": "2025/02/21 16:30",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "ht": "0",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "-0.25",
                "hrfsp": "1.800",
                "grfsp": "2.000",
                "rft": "0",
                "rf": [
                {
                    "hrf": "-0.25",
                    "hrfsp": "1.800",
                    "grfsp": "2.000",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.975",
                    "grfsp": "1.825",
                    "rft": "2",
                    "ps": "0"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.900",
                    "grfsp": "1.900",
                    "rft": "2",
                    "ps": "0"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.850",
                    "grfsp": "1.950",
                    "rft": "2",
                    "ps": "0"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.800",
                    "grfsp": "2.000",
                    "rft": "0",
                    "ps": "0"
                }
                ],
                "hdx": "3.0",
                "hdxsp": "2.000",
                "gdxsp": "1.800",
                "dxt": "2",
                "dx": [
                {
                    "hdx": "3.0",
                    "hdxsp": "2.000",
                    "gdxsp": "1.800",
                    "dxt": "2",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.975",
                    "gdxsp": "1.825",
                    "dxt": "1",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.925",
                    "gdxsp": "1.875",
                    "dxt": "-2",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "-1",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "2.000",
                    "gdxsp": "1.800",
                    "dxt": "2",
                    "ps": "0"
                }
                ],
                "hcb": "9",
                "hcbsp": "1.950",
                "gcbsp": "1.850",
                "cbt": "100",
                "cb": [
                {
                    "hcb": "9",
                    "hcbsp": "1.950",
                    "gcbsp": "1.850",
                    "cbt": "100",
                    "ps": "0"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1406352",
            "league": {
                "i": "1237",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "澳新联2",
                "fn": "澳大利亚新南威尔士联赛2",
                "ls": "A",
                "sbn": "澳大利亚新南威尔士联赛2",
                "stn": "澳大利亚新南威尔士联赛2",
                "spy": "answl2",
                "ci": "7",
                "cn": "澳大利亚",
                "cs": "A"
            },
            "host": {
                "i": "41237",
                "n": "Central Coast United FC",
                "sbn": "中岸水手联",
                "stn": "中岸水手联"
            },
            "guest": {
                "i": "12636",
                "n": "费拉瑟",
                "sbn": "费拉瑟",
                "stn": "费拉瑟"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "-0.75",
                "hdx": "4.0",
                "hcb": null
                },
                "h": {
                "hrf": "-0.25",
                "hdx": "1.5",
                "hcb": null
                }
            },
            "rtime": "2025/02/21 16:30",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "ht": "0",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "-0.75",
                "hrfsp": "1.825",
                "grfsp": "1.975",
                "rft": "-1",
                "rf": [
                {
                    "hrf": "-0.75",
                    "hrfsp": "1.825",
                    "grfsp": "1.975",
                    "rft": "-1",
                    "ps": "0"
                },
                {
                    "hrf": "-0.75",
                    "hrfsp": "1.900",
                    "grfsp": "1.900",
                    "rft": "2",
                    "ps": "0"
                },
                {
                    "hrf": "-0.75",
                    "hrfsp": "1.850",
                    "grfsp": "1.950",
                    "rft": "100",
                    "ps": "0"
                }
                ],
                "hdx": "4.0",
                "hdxsp": "1.950",
                "gdxsp": "1.850",
                "dxt": "-1",
                "dx": [
                {
                    "hdx": "4.0",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "-1",
                    "ps": "0"
                },
                {
                    "hdx": "4.0",
                    "hdxsp": "2.000",
                    "gdxsp": "1.800",
                    "dxt": "2",
                    "ps": "0"
                },
                {
                    "hdx": "4.0",
                    "hdxsp": "1.975",
                    "gdxsp": "1.825",
                    "dxt": "0",
                    "ps": "0"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1406701",
            "league": {
                "i": "3322",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "澳昆超U23",
                "fn": "澳大利亚昆士兰超级联赛 23岁以下",
                "ls": "A",
                "sbn": "澳大利亚昆士兰州超级联赛 23岁以下",
                "stn": "澳大利亚昆士兰州超级联赛 23岁以下",
                "spy": "aokunchao2u23",
                "ci": "7",
                "cn": "澳大利亚",
                "cs": "A"
            },
            "host": {
                "i": "42893",
                "n": "荷兰公园老鹰 23岁以下",
                "sbn": "荷兰公园老鹰 23岁以下",
                "stn": "荷兰公园老鹰 23岁以下"
            },
            "guest": {
                "i": "42790",
                "n": "瑞德兰茨联 23岁以下",
                "sbn": "瑞德兰茨联 23岁以下",
                "stn": "瑞德兰茨联 23岁以下"
            },
            "heh": "0",
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "-0.5",
                "hdx": "4.25",
                "hcb": null
                },
                "h": {
                "hrf": "-0.25",
                "hdx": "1.75",
                "hcb": null
                }
            },
            "rtime": "2025/02/21 16:30",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "ht": "0",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "-0.5",
                "hrfsp": "1.875",
                "grfsp": "1.925",
                "rft": "100",
                "rf": [
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.875",
                    "grfsp": "1.925",
                    "rft": "100",
                    "ps": "0"
                }
                ],
                "hdx": "4.25",
                "hdxsp": "1.900",
                "gdxsp": "1.900",
                "dxt": "0",
                "dx": [
                {
                    "hdx": "4.25",
                    "hdxsp": "1.900",
                    "gdxsp": "1.900",
                    "dxt": "0",
                    "ps": "0"
                },
                {
                    "hdx": "4.0",
                    "hdxsp": "1.900",
                    "gdxsp": "1.900",
                    "dxt": "0",
                    "ps": "0"
                },
                {
                    "hdx": "3.75",
                    "hdxsp": "1.900",
                    "gdxsp": "1.900",
                    "dxt": "0",
                    "ps": "0"
                },
                {
                    "hdx": "3.5",
                    "hdxsp": "1.850",
                    "gdxsp": "1.950",
                    "dxt": "0",
                    "ps": "0"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1405870",
            "league": {
                "i": "3527",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "澳维NPL",
                "fn": "澳大利亚NPL维多利亚",
                "ls": "A",
                "sbn": "澳大利亚NPL维多利亚",
                "stn": "澳大利亚NPL维多利亚",
                "spy": "anplv",
                "ci": "7",
                "cn": "澳大利亚",
                "cs": "A"
            },
            "host": {
                "i": "7667",
                "n": "绿色溪谷",
                "sbn": "卡瓦利尔斯",
                "stn": "卡瓦利尔斯",
                "p": "11"
            },
            "guest": {
                "i": "7680",
                "n": "休城",
                "sbn": "休城",
                "stn": "休城",
                "p": "5"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "0.0",
                "hdx": "3.0",
                "hcb": "10.5"
                },
                "h": {
                "hrf": "0.0",
                "hdx": "1.25",
                "hcb": "5"
                }
            },
            "rtime": "2025/02/21 16:30",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "ht": "0",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "0.0",
                "hrfsp": "1.775",
                "grfsp": "2.025",
                "rft": "0",
                "rf": [
                {
                    "hrf": "0.0",
                    "hrfsp": "1.775",
                    "grfsp": "2.025",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "2.000",
                    "grfsp": "1.800",
                    "rft": "2",
                    "ps": "0"
                },
                {
                    "hrf": "-0.25",
                    "hrfsp": "1.800",
                    "grfsp": "2.000",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "2.000",
                    "grfsp": "1.800",
                    "rft": "1",
                    "ps": "0"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "1.975",
                    "grfsp": "1.825",
                    "rft": "-1",
                    "ps": "0"
                }
                ],
                "hdx": "3.0",
                "hdxsp": "1.975",
                "gdxsp": "1.825",
                "dxt": "2",
                "dx": [
                {
                    "hdx": "3.0",
                    "hdxsp": "1.975",
                    "gdxsp": "1.825",
                    "dxt": "2",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "2",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.925",
                    "gdxsp": "1.875",
                    "dxt": "2",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.900",
                    "gdxsp": "1.900",
                    "dxt": "2",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.875",
                    "gdxsp": "1.925",
                    "dxt": "0",
                    "ps": "0"
                }
                ],
                "hcb": "10.5",
                "hcbsp": "1.950",
                "gcbsp": "1.850",
                "cbt": "100",
                "cb": [
                {
                    "hcb": "10.5",
                    "hcbsp": "1.950",
                    "gcbsp": "1.850",
                    "cbt": "100",
                    "ps": "0"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1405869",
            "league": {
                "i": "3527",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "澳维NPL",
                "fn": "澳大利亚NPL维多利亚",
                "ls": "A",
                "sbn": "澳大利亚NPL维多利亚",
                "stn": "澳大利亚NPL维多利亚",
                "spy": "anplv",
                "ci": "7",
                "cn": "澳大利亚",
                "cs": "A"
            },
            "host": {
                "i": "6938",
                "n": "墨尔本骑士",
                "sbn": "墨尔本骑士",
                "stn": "墨尔本骑士",
                "p": "8"
            },
            "guest": {
                "i": "4336",
                "n": "阿文德尔联",
                "sbn": "艾文多尔山庄",
                "stn": "阿文德尔联",
                "p": "1"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "+1.0",
                "hdx": "3.25",
                "hcb": "10.5"
                },
                "h": {
                "hrf": "+0.5",
                "hdx": "1.25",
                "hcb": "5"
                }
            },
            "rtime": "2025/02/21 16:30",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "ht": "0",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "+1.0",
                "hrfsp": "1.825",
                "grfsp": "1.975",
                "rft": "0",
                "rf": [
                {
                    "hrf": "+1.0",
                    "hrfsp": "1.825",
                    "grfsp": "1.975",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "+1.25",
                    "hrfsp": "1.775",
                    "grfsp": "2.025",
                    "rft": "-1",
                    "ps": "0"
                },
                {
                    "hrf": "+1.25",
                    "hrfsp": "1.800",
                    "grfsp": "2.000",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "+1.0",
                    "hrfsp": "1.875",
                    "grfsp": "1.925",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "+0.75",
                    "hrfsp": "2.025",
                    "grfsp": "1.775",
                    "rft": "0",
                    "ps": "0"
                }
                ],
                "hdx": "3.25",
                "hdxsp": "1.975",
                "gdxsp": "1.825",
                "dxt": "2",
                "dx": [
                {
                    "hdx": "3.25",
                    "hdxsp": "1.975",
                    "gdxsp": "1.825",
                    "dxt": "2",
                    "ps": "0"
                },
                {
                    "hdx": "3.25",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "1",
                    "ps": "0"
                },
                {
                    "hdx": "3.25",
                    "hdxsp": "1.900",
                    "gdxsp": "1.900",
                    "dxt": "-1",
                    "ps": "0"
                },
                {
                    "hdx": "3.25",
                    "hdxsp": "2.000",
                    "gdxsp": "1.800",
                    "dxt": "0",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.775",
                    "gdxsp": "2.025",
                    "dxt": "0",
                    "ps": "0"
                }
                ],
                "hcb": "10.5",
                "hcbsp": "1.950",
                "gcbsp": "1.850",
                "cbt": "100",
                "cb": [
                {
                    "hcb": "10.5",
                    "hcbsp": "1.950",
                    "gcbsp": "1.850",
                    "cbt": "100",
                    "ps": "0"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1406380",
            "league": {
                "i": "1614",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "澳维超2",
                "fn": "澳大利亚维多利亚超级联赛2",
                "ls": "A",
                "sbn": "澳大利亚维多利亚超级联赛2",
                "stn": "澳大利亚维多利亚超级联赛2",
                "spy": "avpl2",
                "ci": "7",
                "cn": "澳大利亚",
                "cs": "A"
            },
            "host": {
                "i": "12883",
                "n": "博克斯山联",
                "sbn": "波克海尔",
                "stn": "博克斯山联"
            },
            "guest": {
                "i": "13333",
                "n": "南得瓦丁",
                "sbn": "鲁纳沃丁城",
                "stn": "南得瓦丁"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "0.0",
                "hdx": "3.0",
                "hcb": null
                },
                "h": {
                "hrf": "0.0",
                "hdx": "1.25",
                "hcb": null
                }
            },
            "rtime": "2025/02/21 16:30",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "ht": "0",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "0.0",
                "hrfsp": "1.975",
                "grfsp": "1.825",
                "rft": "2",
                "rf": [
                {
                    "hrf": "0.0",
                    "hrfsp": "1.975",
                    "grfsp": "1.825",
                    "rft": "2",
                    "ps": "0"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.950",
                    "grfsp": "1.850",
                    "rft": "2",
                    "ps": "0"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.900",
                    "grfsp": "1.900",
                    "rft": "1",
                    "ps": "0"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.875",
                    "grfsp": "1.925",
                    "rft": "-1",
                    "ps": "0"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.925",
                    "grfsp": "1.875",
                    "rft": "2",
                    "ps": "0"
                }
                ],
                "hdx": "3.0",
                "hdxsp": "1.850",
                "gdxsp": "1.950",
                "dxt": "2",
                "dx": [
                {
                    "hdx": "3.0",
                    "hdxsp": "1.850",
                    "gdxsp": "1.950",
                    "dxt": "2",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.825",
                    "gdxsp": "1.975",
                    "dxt": "1",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.800",
                    "gdxsp": "2.000",
                    "dxt": "-1",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.850",
                    "gdxsp": "1.950",
                    "dxt": "2",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.825",
                    "gdxsp": "1.975",
                    "dxt": "2",
                    "ps": "0"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1402103",
            "league": {
                "i": "3",
                "zc": "1",
                "jc": "1",
                "bd": "1",
                "n": "澳超",
                "fn": "澳大利亚A联赛",
                "ls": "A",
                "sbn": "澳大利亚超级联赛",
                "stn": "澳大利亚A级联赛",
                "spy": "aochao",
                "ci": "7",
                "cn": "澳大利亚",
                "cs": "A"
            },
            "host": {
                "i": "349",
                "n": "纽卡斯尔喷射机",
                "sbn": "纽卡斯尔喷气机",
                "stn": "纽卡斯尔喷射机",
                "p": "11"
            },
            "guest": {
                "i": "350",
                "n": "布里斯班狮吼",
                "sbn": "布里斯班狮吼",
                "stn": "布里斯班狮吼",
                "p": "13"
            },
            "heh": "1",
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "-0.5",
                "hdx": "3.0",
                "hcb": "11"
                },
                "h": {
                "hrf": "-0.25",
                "hdx": "1.25",
                "hcb": "5.5"
                }
            },
            "rtime": "2025/02/21 16:35",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "tc": {
                "bd_c": "52",
                "bd_r": "25023"
            },
            "ht": "1",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "-0.5",
                "hrfsp": "2.050",
                "grfsp": "1.850",
                "rft": "-1",
                "rf": [
                {
                    "hrf": "-0.5",
                    "hrfsp": "2.050",
                    "grfsp": "1.850",
                    "rft": "-1",
                    "ps": "0"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "2.060",
                    "grfsp": "1.840",
                    "rft": "2",
                    "ps": "0"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "2.050",
                    "grfsp": "1.850",
                    "rft": "2",
                    "ps": "0"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "2.020",
                    "grfsp": "1.880",
                    "rft": "2",
                    "ps": "0"
                },
                {
                    "hrf": "-0.5",
                    "hrfsp": "2.010",
                    "grfsp": "1.890",
                    "rft": "1",
                    "ps": "0"
                }
                ],
                "hdx": "3.0",
                "hdxsp": "1.850",
                "gdxsp": "2.000",
                "dxt": "1",
                "dx": [
                {
                    "hdx": "3.0",
                    "hdxsp": "1.850",
                    "gdxsp": "2.000",
                    "dxt": "1",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.825",
                    "gdxsp": "2.025",
                    "dxt": "-2",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.850",
                    "gdxsp": "2.000",
                    "dxt": "-1",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.875",
                    "gdxsp": "1.975",
                    "dxt": "1",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.850",
                    "gdxsp": "2.000",
                    "dxt": "-2",
                    "ps": "0"
                }
                ],
                "hcb": "11",
                "hcbsp": "1.875",
                "gcbsp": "1.925",
                "cbt": "-1",
                "cb": [
                {
                    "hcb": "11",
                    "hcbsp": "1.875",
                    "gcbsp": "1.925",
                    "cbt": "-1",
                    "ps": "0"
                },
                {
                    "hcb": "11",
                    "hcbsp": "1.925",
                    "gcbsp": "1.875",
                    "cbt": "100",
                    "ps": "0"
                }
                ]
            },
            "sty": 1,
            "hot": 7
            },
            {
            "id": "1406780",
            "league": {
                "i": "842",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "以乙南",
                "fn": "以色列丙级联赛 南部",
                "ls": "Y",
                "sbn": "以色列乙级联赛 南方",
                "stn": "以色列乙级联赛 南方",
                "spy": "yibingnan",
                "ci": "97",
                "cn": "以色列",
                "cs": "Y"
            },
            "host": {
                "i": "8697",
                "n": "Beita佩塔提克瓦",
                "sbn": "贝塔尔佩塔提克瓦",
                "stn": "贝塔尔佩塔提克瓦"
            },
            "guest": {
                "i": "8683",
                "n": "夏普尔Mahane Yehuda",
                "sbn": "马哈尼耶侯达",
                "stn": "夏普尔Mahane Yehuda"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "+1.25",
                "hdx": "2.75",
                "hcb": null
                },
                "h": {
                "hrf": "+0.5",
                "hdx": "1.0",
                "hcb": null
                }
            },
            "rtime": "2025/02/21 16:45",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "ht": "0",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "+1.25",
                "hrfsp": "2.000",
                "grfsp": "1.800",
                "rft": "0",
                "rf": [
                {
                    "hrf": "+1.25",
                    "hrfsp": "2.000",
                    "grfsp": "1.800",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "+1.5",
                    "hrfsp": "1.800",
                    "grfsp": "2.000",
                    "rft": "-2",
                    "ps": "0"
                },
                {
                    "hrf": "+1.5",
                    "hrfsp": "1.850",
                    "grfsp": "1.950",
                    "rft": "-1",
                    "ps": "0"
                },
                {
                    "hrf": "+1.5",
                    "hrfsp": "1.900",
                    "grfsp": "1.900",
                    "rft": "0",
                    "ps": "0"
                },
                {
                    "hrf": "+1.25",
                    "hrfsp": "1.975",
                    "grfsp": "1.825",
                    "rft": "100",
                    "ps": "0"
                }
                ],
                "hdx": "2.75",
                "hdxsp": "1.850",
                "gdxsp": "1.950",
                "dxt": "0",
                "dx": [
                {
                    "hdx": "2.75",
                    "hdxsp": "1.850",
                    "gdxsp": "1.950",
                    "dxt": "0",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "2",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.875",
                    "gdxsp": "1.925",
                    "dxt": "2",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.800",
                    "gdxsp": "2.000",
                    "dxt": "0",
                    "ps": "0"
                },
                {
                    "hdx": "3.25",
                    "hdxsp": "2.000",
                    "gdxsp": "1.800",
                    "dxt": "0",
                    "ps": "0"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1405876",
            "league": {
                "i": "3423",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "澳南超",
                "fn": "澳大利亚南澳大利亚州超级联赛",
                "ls": "A",
                "sbn": "澳大利亚 - 南澳大利亚州超级联赛",
                "stn": "澳大利亚 - 南澳大利亚州超级联赛",
                "spy": "asapl",
                "ci": "7",
                "cn": "澳大利亚",
                "cs": "A"
            },
            "host": {
                "i": "12200",
                "n": "坎贝尔镇市",
                "sbn": "坎贝尔市体育馆",
                "stn": "坎贝尔镇市"
            },
            "guest": {
                "i": "8732",
                "n": "地铁之星",
                "sbn": "地铁之星",
                "stn": "地铁之星"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "0.0",
                "hdx": "2.75",
                "hcb": "10.5"
                },
                "h": {
                "hrf": "0.0",
                "hdx": "1.25",
                "hcb": "5"
                }
            },
            "rtime": "2025/02/21 17:00",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "ht": "0",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "0.0",
                "hrfsp": "1.900",
                "grfsp": "1.900",
                "rft": "-2",
                "rf": [
                {
                    "hrf": "0.0",
                    "hrfsp": "1.900",
                    "grfsp": "1.900",
                    "rft": "-2",
                    "ps": "0"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.925",
                    "grfsp": "1.875",
                    "rft": "-1",
                    "ps": "0"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.950",
                    "grfsp": "1.850",
                    "rft": "2",
                    "ps": "0"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.900",
                    "grfsp": "1.900",
                    "rft": "2",
                    "ps": "0"
                },
                {
                    "hrf": "0.0",
                    "hrfsp": "1.850",
                    "grfsp": "1.950",
                    "rft": "1",
                    "ps": "0"
                }
                ],
                "hdx": "2.75",
                "hdxsp": "1.800",
                "gdxsp": "2.000",
                "dxt": "0",
                "dx": [
                {
                    "hdx": "2.75",
                    "hdxsp": "1.800",
                    "gdxsp": "2.000",
                    "dxt": "0",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "2.000",
                    "gdxsp": "1.800",
                    "dxt": "2",
                    "ps": "0"
                },
                {
                    "hdx": "3.0",
                    "hdxsp": "1.900",
                    "gdxsp": "1.900",
                    "dxt": "0",
                    "ps": "0"
                },
                {
                    "hdx": "3.25",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "2",
                    "ps": "0"
                },
                {
                    "hdx": "3.25",
                    "hdxsp": "1.900",
                    "gdxsp": "1.900",
                    "dxt": "0",
                    "ps": "0"
                }
                ],
                "hcb": "10.5",
                "hcbsp": "1.950",
                "gcbsp": "1.850",
                "cbt": "100",
                "cb": [
                {
                    "hcb": "10.5",
                    "hcbsp": "1.950",
                    "gcbsp": "1.850",
                    "cbt": "100",
                    "ps": "0"
                }
                ]
            },
            "hot": 0
            },
            {
            "id": "1405866",
            "league": {
                "i": "1129",
                "zc": "0",
                "jc": "0",
                "bd": "0",
                "n": "澳威北超",
                "fn": "澳大利亚新南威尔士北部超级联赛",
                "ls": "A",
                "sbn": "澳大利亚新南威尔士北部超级联赛",
                "stn": "澳大利亚新南威尔士北部超级联赛",
                "spy": "aoxinanchao",
                "ci": "7",
                "cn": "澳大利亚",
                "cs": "A"
            },
            "host": {
                "i": "25996",
                "n": "亚登斯顿玫瑰花蕾",
                "sbn": "亚登斯顿玫瑰花蕾",
                "stn": "亚登斯顿玫瑰花蕾",
                "p": "12"
            },
            "guest": {
                "i": "20442",
                "n": "Valentine凤凰",
                "sbn": "瓦伦蒂勒",
                "stn": "Valentine凤凰",
                "p": "6"
            },
            "heh": 1,
            "lvc": 0,
            "rcn": 0,
            "zhanyi": "0",
            "sd": {
                "f": {
                "hrf": "+1.75",
                "hdx": "4.0",
                "hcb": "10.5"
                },
                "h": {
                "hrf": "+0.75",
                "hdx": "1.5",
                "hcb": "5"
                }
            },
            "rtime": "2025/02/21 17:00",
            "events": [
                {
                "t": "cd",
                "c": "场地：良好"
                },
                {
                "t": "tq",
                "c": "天气：良好"
                }
            ],
            "events_graph": {
                "events": [
                
                ],
                "ml": 0,
                "status": 0
            },
            "ht": "0",
            "ss": "",
            "status": "未",
            "f_ld": {
                "hrf": "+1.75",
                "hrfsp": "1.900",
                "grfsp": "1.900",
                "rft": "1",
                "rf": [
                {
                    "hrf": "+1.75",
                    "hrfsp": "1.900",
                    "grfsp": "1.900",
                    "rft": "1",
                    "ps": "0"
                },
                {
                    "hrf": "+1.75",
                    "hrfsp": "1.825",
                    "grfsp": "1.975",
                    "rft": "-2",
                    "ps": "0"
                },
                {
                    "hrf": "+1.75",
                    "hrfsp": "1.900",
                    "grfsp": "1.900",
                    "rft": "-2",
                    "ps": "0"
                },
                {
                    "hrf": "+1.75",
                    "hrfsp": "1.925",
                    "grfsp": "1.875",
                    "rft": "-1",
                    "ps": "0"
                },
                {
                    "hrf": "+1.75",
                    "hrfsp": "1.950",
                    "grfsp": "1.850",
                    "rft": "2",
                    "ps": "0"
                }
                ],
                "hdx": "4.0",
                "hdxsp": "2.000",
                "gdxsp": "1.800",
                "dxt": "0",
                "dx": [
                {
                    "hdx": "4.0",
                    "hdxsp": "2.000",
                    "gdxsp": "1.800",
                    "dxt": "0",
                    "ps": "0"
                },
                {
                    "hdx": "3.75",
                    "hdxsp": "1.975",
                    "gdxsp": "1.825",
                    "dxt": "2",
                    "ps": "0"
                },
                {
                    "hdx": "3.75",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "1",
                    "ps": "0"
                },
                {
                    "hdx": "3.75",
                    "hdxsp": "1.925",
                    "gdxsp": "1.875",
                    "dxt": "-1",
                    "ps": "0"
                },
                {
                    "hdx": "3.75",
                    "hdxsp": "1.950",
                    "gdxsp": "1.850",
                    "dxt": "2",
                    "ps": "0"
                }
                ],
                "hcb": "10.5",
                "hcbsp": "1.950",
                "gcbsp": "1.850",
                "cbt": "100",
                "cb": [
                {
                    "hcb": "10.5",
                    "hcbsp": "1.950",
                    "gcbsp": "1.850",
                    "cbt": "100",
                    "ps": "0"
                }
                ]
            },
            "hot": 0
            }
        ],
        "mt": "1740152107"
    }
    """
    start = time.time()
    r = pyoctopus.select(text, None, InstantRaceResponse)
    print(f"\n{time.time() - start}")
    print(len(r[0].races))
