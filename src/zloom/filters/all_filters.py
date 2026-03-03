from astropy.time import Time
true = True
false = False

all_filters = {

"test_filter": [
  {
    "$match": {
      "$and": [
        {
          "$or": [
            {
              "$and": [
                {
                  "properties.photstats.r.fading.rate": {
                    "$gt": 0.6
                  }
                },
                {
                  "properties.photstats.r.fading.red_chi2": {
                    "$lte": 2
                  }
                }
              ]
            },
            {
              "$and": [
                {
                  "properties.photstats.g.fading.rate": {
                    "$gt": 0.6
                  }
                },
                {
                  "properties.photstats.g.fading.red_chi2": {
                    "$lte": 2
                  }
                }
              ]
            },
            {
              "$and": [
                {
                  "properties.photstats.r.rising.rate": {
                    "$lte": -0.1
                  }
                },
                {
                  "properties.photstats.r.rising.red_chi2": {
                    "$lte": 2
                  }
                }
              ]
            },
            {
              "$and": [
                {
                  "properties.photstats.g.rising.rate": {
                    "$lte": -0.1
                  }
                },
                {
                  "properties.photstats.g.rising.red_chi2": {
                    "$lte": 2
                  }
                }
              ]
            }
          ]
        },
        {
          "properties.rock": {
            "$eq": false
          }
        },
        {
          "properties.photstats.g.rising.dt": {
            "$lte": 5
          }
        },
        {
          "properties.photstats.g.fading.rate": {
            "$lte": 5
          }
        },
        {
          "properties.photstats.r.rising.dt": {
            "$lte": 5
          }
        },
        {
          "properties.photstats.r.fading.rate": {
            "$lte": 5
          }
        }
      ]
    }
  },
  {
    "$project": {
      "objectId": 1,
      "candidate.jd": 1,
      "cross_matches.Gaia_DR3": 1
    }
  },
  {
    "$addFields": {
      "gaia_star": {
        "$anyElementTrue": {
          "$map": {
            "input": {
              "$ifNull": [
                "$cross_matches.Gaia_DR3",
                []
              ]
            },
            "in": {
              "$lte": [
                "$distance_arcsec",
                3
              ]
            }
          }
        }
      }
    }
  },
  {
    "$match": {
      "gaia_star": {
        "$eq": false
      }
    }
  },
  {
    "$project": {
      "objectId": 1,
      "candidate.jd": 1,
      "cross_matches.Gaia_DR3": 1,
      "gaia_star": 1
    }
  }
  ], 


"filter_with_jd": [
                    {
                        "$match": {
                        "$and": [
                            {
                            "$or": [
                                {
                                "$and": [
                                    {
                                    "properties.photstats.r.fading.rate": {
                                        "$gt": 4
                                    }
                                    },
                                    {
                                    "properties.photstats.r.fading.red_chi2": {
                                        "$lte": 2
                                    }
                                    }
                                ]
                                },
                                {
                                "$and": [
                                    {
                                    "properties.photstats.g.fading.rate": {
                                        "$gt": 4
                                    }
                                    },
                                    {
                                    "properties.photstats.g.fading.red_chi2": {
                                        "$lte": 2
                                    }
                                    }
                                ]
                                },
                                {
                                "$and": [
                                    {
                                    "properties.photstats.r.rising.rate": {
                                        "$lte": -4
                                    }
                                    },
                                    {
                                    "properties.photstats.r.rising.red_chi2": {
                                        "$lte": 2
                                    }
                                    }
                                ]
                                },
                                {
                                "$and": [
                                    {
                                    "properties.photstats.g.rising.rate": {
                                        "$lte": -4
                                    }
                                    },
                                    {
                                    "properties.photstats.g.rising.red_chi2": {
                                        "$lte": 2
                                    }
                                    }
                                ]
                                }
                            ]
                            },
                            {
                            "properties.rock": {
                                "$eq": false
                            }
                            },
                            {
                            "properties.star": {
                                "$eq": false
                            }
                            },
                            {
                            "properties.near_brightstar": {
                                "$eq": false
                            }
                            },
                            {
                            "candidate.isDipole": {
                                "$eq": false
                            }
                            },
                            {
                            "candidate.isdiffpos": {
                                "$eq": true
                            }
                            },
                            {
                            "candidate.reliability": {
                                "$gte": 0.8
                            }
                            },
                            {
                            "candidate.extendedness": {
                                "$lt": 1
                            }
                            }
                        ]
                        }
                    },
                    {
                        "$project": {
                        "objectId": 1,
                        "candidate.jd": 1,
                        "properties.photstats.r.fading.rate": 1,
                        "properties.photstats.r.fading.red_chi2": 1,
                        "properties.photstats.g.fading.rate": 1,
                        "properties.photstats.g.fading.red_chi2": 1,
                        "properties.photstats.r.rising.rate": 1,
                        "properties.photstats.r.rising.red_chi2": 1,
                        "properties.photstats.g.rising.rate": 1,
                        "properties.photstats.g.rising.red_chi2": 1,
                        "properties.rock": 1,
                        "properties.star": 1,
                        "properties.near_brightstar": 1,
                        "candidate.isDipole": 1,
                        "candidate.isdiffpos": 1,
                        "candidate.reliability": 1,
                        "candidate.extendedness": 1,
                        "cross_matches.milliquas_v8": 1,
                        "prv_candidates": 1
                        }
                    },
                    {
                        "$addFields": {
                        "IsQuasar": {
                            "$anyElementtrue": {
                            "$map": {
                                "input": {
                                "$ifNull": [
                                    "$cross_matches.milliquas_v8",
                                    []
                                ]
                                },
                                "in": {
                                "$eq": [
                                    "$Descrip",
                                    "Q"
                                ]
                                }
                            }
                            }
                        },
                        "first_jd_lsst": {
                            "$min": "$prv_candidates.jd"
                        }
                        }
                    },
                    {
                        "$addFields": {
                        "prevpasscount_total": {
                            "$filter": {
                            "input": "$prv_candidates",
                            "cond": {
                                "$and": [
                                {
                                    "$lt": [
                                    {
                                        "$subtract": [
                                        "$candidate.jd",
                                        "$$this.jd"
                                        ]
                                    },
                                    30
                                    ]
                                },
                                {
                                    "$gt": [
                                    {
                                        "$subtract": [
                                        "$candidate.jd",
                                        "$$this.jd"
                                        ]
                                    },
                                    0.75
                                    ]
                                },
                                {
                                    "$eq": [
                                    "$$this.isdiffpos",
                                    true
                                    ]
                                },
                                {
                                    "$gt": [
                                    "$$this.magpsf",
                                    0
                                    ]
                                },
                                {
                                    "$lt": [
                                    "$$this.magpsf",
                                    20.2
                                    ]
                                }
                                ]
                            }
                            }
                        }
                        }
                    },
                    {
                        "$addFields": {
                        "first_jd": {
                            "$min": "$prevpasscount_total.prv_candidates.jd"
                        }
                        }
                    },
                    {
                        "$match": {
                        "$and": [
                            {
                            "$expr": {
                                "$lt": [
                                {
                                    "$subtract": [
                                    "$cross_matches.AllWISE.w1mpro",
                                    "$cross_matches.AllWISE.w2mpro"
                                    ]
                                },
                                1
                                ]
                            }
                            },
                            {
                            "$and": [
                                {
                                "IsQuasar": {
                                    "$eq": false
                                }
                                },
                                {
                                "$expr": {
                                    "$lt": [
                                    {
                                        "$divide": [
                                        "$cross_matches.Gaia_DR3.pm",
                                        {
                                            "$sqrt": {
                                            "$add": [
                                                {
                                                "$pow": [
                                                    "$cross_matches.Gaia_DR3.pmra_error",
                                                    2
                                                ]
                                                },
                                                {
                                                "$pow": [
                                                    "$cross_matches.Gaia_DR3.pmdec_error",
                                                    2
                                                ]
                                                }
                                            ]
                                            }
                                        }
                                        ]
                                    },
                                    3
                                    ]
                                }
                                },
                                {
                                "first_jd_lsst": {
                                    "$eq": Time.now().jd - 3
                                }
                                },
                                {
                                "first_jd": {
                                    "$eq": Time.now().jd - 3
                                }
                                }
                            ]
                            }
                        ]
                        }
                    },
                    {
                        "$project": {
                        "objectId": 1,
                        "candidate.jd": 1,
                        "properties.photstats.r.fading.rate": 1,
                        "properties.photstats.r.fading.red_chi2": 1,
                        "properties.photstats.g.fading.rate": 1,
                        "properties.photstats.g.fading.red_chi2": 1,
                        "properties.photstats.r.rising.rate": 1,
                        "properties.photstats.r.rising.red_chi2": 1,
                        "properties.photstats.g.rising.rate": 1,
                        "properties.photstats.g.rising.red_chi2": 1,
                        "properties.rock": 1,
                        "properties.star": 1,
                        "properties.near_brightstar": 1,
                        "candidate.isDipole": 1,
                        "candidate.isdiffpos": 1,
                        "candidate.reliability": 1,
                        "candidate.extendedness": 1,
                        "cross_matches.milliquas_v8": 1,
                        "prv_candidates": 1,
                        "IsQuasar": 1,
                        "first_jd_lsst": 1,
                        "first_jd": 1,
                        "prevpasscount_total": 1
                        }
                    }
                    ]








}