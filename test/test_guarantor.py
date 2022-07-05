from forecaster.guarantor import verify_intermediate, verify_final, Status

schedule = {
    "fall": [
        {
            "course": {
                "code": "CSC225",
                "title": "Algorithms and Data Structures I"
            },
            "sections": [
                {
                    "professor": "",
                    "capacity": "0"
                }
            ]
        }
    ],
    "spring": [
        {
            "course": {
                "code": "CSC320",
                "title": "Foundations of Computer Science"
            },
            "sections": [
                {
                    "professor": "",
                    "capacity": "0"
                }
            ]
        }
    ],
    "summer": [
        {
            "course": {
                "code": "CSC360",
                "title": "Operating Systems"
            },
            "sections": [
                {
                    "professor": "",
                    "capacity": "0"
                }
            ]
        }
    ]
}


def test_intermediate_all_good():
    low_bound = 10
    high_bound = 100

    internal_series = {"CSC225-F": {"data": [1, 2, 3], "approach": 0, "capacity": 20},
                       "CSC320-SP": {"data": [1, 2, 3], "approach": 0, "capacity": 50},
                       "CSC360-SU": {"data": [1, 2, 3], "approach": 0, "capacity": 25}}

    status = verify_intermediate(internal_series, schedule, low_bound, high_bound)
    assert status == Status.GOOD


def test_intermediate_missing_class():
    low_bound = 10
    high_bound = 100

    internal_series = {"CSC225-F": {"data": [1, 2, 3], "approach": 0, "capacity": 20},
                       "CSC360-SU": {"data": [1, 2, 3], "approach": 0, "capacity": 25}}

    status = verify_intermediate(internal_series, schedule, low_bound, high_bound)
    assert status == Status.MISSING_CLASS


def test_intermediate_missing_assignment():
    low_bound = 10
    high_bound = 100

    internal_series = {"CSC225-F": {"data": [1, 2, 3], "approach": 0, "capacity": 20},
                       "CSC320-SP": {"data": [1, 2, 3], "approach": 0, "capacity": 50},
                       "CSC360-SU": {"data": [1, 2, 3], "approach": 0, "capacity": 0}}

    status = verify_intermediate(internal_series, schedule, low_bound, high_bound)
    assert status == Status.MISSING_ASSIGMENT


def test_intermediate_scale_down():
    low_bound = 10
    high_bound = 100

    internal_series = {"CSC225-F": {"data": [1, 2, 3], "approach": 0, "capacity": 26},
                       "CSC320-SP": {"data": [1, 2, 3], "approach": 0, "capacity": 50},
                       "CSC360-SU": {"data": [1, 2, 3], "approach": 0, "capacity": 25}}

    status = verify_intermediate(internal_series, schedule, low_bound, high_bound)
    assert status == Status.GOOD
    assert internal_series["CSC320-SP"]["capacity"] == 49


def test_intermediate_scale_up():
    low_bound = 15
    high_bound = 100

    internal_series = {"CSC225-F": {"data": [1, 2, 3], "approach": 0, "capacity": 5},
                       "CSC320-SP": {"data": [1, 2, 3], "approach": 0, "capacity": 4},
                       "CSC360-SU": {"data": [1, 2, 3], "approach": 0, "capacity": 5}}

    status = verify_intermediate(internal_series, schedule, low_bound, high_bound)
    assert status == Status.GOOD
    assert internal_series["CSC320-SP"]["capacity"] == 5


def test_verify_final_good():
    new_schedule = {
        "fall": [
            {
                "course": {
                    "code": "CSC225",
                    "title": "Algorithms and Data Structures I"
                },
                "sections": [
                    {
                        "professor": "",
                        "capacity": "25"
                    }
                ]
            }
        ],
        "spring": [
            {
                "course": {
                    "code": "CSC320",
                    "title": "Foundations of Computer Science"
                },
                "sections": [
                    {
                        "professor": "",
                        "capacity": "30"
                    }
                ]
            }
        ],
        "summer": [
            {
                "course": {
                    "code": "CSC360",
                    "title": "Operating Systems"
                },
                "sections": [
                    {
                        "professor": "",
                        "capacity": "50"
                    }
                ]
            }
        ]
    }
    status = verify_final(new_schedule, schedule)
    assert status == Status.GOOD


def test_verify_final_missing_class():
    new_schedule = {
        "fall": [
            {
                "course": {
                    "code": "CSC226",
                    "title": "Algorithms and Data Structures I"
                },
                "sections": [
                    {
                        "professor": "",
                        "capacity": "0"
                    }
                ]
            }
        ],
        "spring": [
            {
                "course": {
                    "code": "CSC320",
                    "title": "Foundations of Computer Science"
                },
                "sections": [
                    {
                        "professor": "",
                        "capacity": "0"
                    }
                ]
            }
        ],
        "summer": [
            {
                "course": {
                    "code": "CSC360",
                    "title": "Operating Systems"
                },
                "sections": [
                    {
                        "professor": "",
                        "capacity": "0"
                    }
                ]
            }
        ]
    }
    status = verify_final(new_schedule, schedule)
    assert status == Status.MISSING_CLASS


def test_verify_final_extra_class():
    new_schedule = {
        "fall": [
            {
                "course": {
                    "code": "CSC225",
                    "title": "Algorithms and Data Structures I"
                },
                "sections": [
                    {
                        "professor": "",
                        "capacity": "0"
                    }
                ]
            },
            {
                "course": {
                    "code": "CSC226",
                    "title": "Algorithms and Data Structures II"
                },
                "sections": [
                    {
                        "professor": "",
                        "capacity": "0"
                    }
                ]
            }
        ],
        "spring": [
            {
                "course": {
                    "code": "CSC320",
                    "title": "Foundations of Computer Science"
                },
                "sections": [
                    {
                        "professor": "",
                        "capacity": "0"
                    }
                ]
            }
        ],
        "summer": [
            {
                "course": {
                    "code": "CSC360",
                    "title": "Operating Systems"
                },
                "sections": [
                    {
                        "professor": "",
                        "capacity": "0"
                    }
                ]
            }
        ]
    }
    status = verify_final(new_schedule, schedule)
    assert status == Status.MISSING_ASSIGMENT
