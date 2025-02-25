# Private objects (not accessible on import)
_d00 = {
    "source": {
        "authors": [
            "Nani Yuningsih", "Sardjito Sardjito", "Yunita Citra Dewi"
        ],
        "title": "Determination of Earth's Gravitational Acceleration and Moment of Inertia of Rigid Body Using Physical Pendulum Experiments",
        "journal": "IOP Conference Series: Materials Science and Engineering",
        "volume": "830",
        "number": "2",
        "pages": "022001",
        "month": "May",
        "year": 2020,
        "url": "https://doi.org/10.1088/1757-899X/830/2/022001"
    },
    "data": {
        "distance": {
            "values": [0.350, 0.325, 0.300, 0.275, 0.250, 0.200, 0.188, 0.175, 0.150, 0.125, 0.100, 0.075, 0.050],
            "unit": "m"
        },
        "period": {
            "values": [1.360, 1.381, 1.350, 1.333, 1.330, 1.320, 1.332, 1.342, 1.362, 1.415, 1.523, 1.725, 1.990],
            "unit": "s"
        },
        "angle": {
            "value": 10,
            "unit": "degree"
        },
        "mass": {
            "value": 0.465,
            "unit": "kg"
        },
        "length": {
            "value": 0.75,
            "unit": "m"
        }
    },
    "others": {
        "camcorder": {
            "type": "Panasonic HDC-SD9",
            "fps": 25,
            "observation": {
                "duration": 50,
                "unit": "oscillation"
            }
        }
    }
}

_d01 = {
    "source": {
        "authors": [
            "Mustafa Coramik", "Buket İnanç"
        ],
        "title": "A physical pendulum experiment with Lego, Phyphox and Tracker",
        "journal": "Physics Education",
        "volume": "58",
        "number": "5",
        "pages": "055014",
        "month": "July",
        "year": 2023,
        "url": "http://dx.doi.org/10.1088/1361-6552/ace57d"
    },
    "data": {
        "total_length": {
            "values": [48.00, 52.80, 57.60, 62.40, 67.20],
            "unit": "cm"
        },
        "angle": {
            "values": [13.8, 15.5, 12.8, 9.4, 9.5],
            "unit": "degree"
        },
        "number_of_brick": {
            "values": [50, 55, 60, 65, 70],
            "unit": ""
        },
        "repetion": {
            "values": [5, 5, 5, 5, 5],
            "unit": ""
        },
        "period_tracker": {
            "values": [1.139, 1.199, 1.249, 1.300, 1.349],
            "unit": "s"
        },
        "period_phyphox": {
            "values": [1.140, 1.199, 1.258, 1.300, 1.340],
            "unit": "s"
        }
    },
    "others": {
        "smartphone": {
            "fps": 60
        }
    }
}

_d02 = {
    "source": {
        "authors": [
            "Sardjito", "Nani Yuningsih"
        ],
        "title": "The Period of Physical Pendulum Motion with Large Angular Displacement",
        "journal": "Advances in Engineering Research",
        "volume": "198",
        "number": "",
        "pages": "197-201",
        "month": "December",
        "year": 2020,
        "url": "https://doi.org/10.2991/aer.k.201221.034"
    },
    "data": {
        "swinging_angle": {
            "values": [5, 10, 15, 20, 25, 30, 35, 40, 45],
            "unit": "degree"
        },
        "period": {
            "values": [1.148, 1.149, 1.150, 1.152, 1.153, 1.160, 1.166, 1.175, 1.179],
            "unit": "degree"
        }
    }
}

_d03 = {
    "source": {
        "authors": [
            "T. H. Richardson", "S. A. Brittle"
        ],
        "title": "Physical pendulum experiments to enhance the understanding of moments of inertia and simple harmonic motion",
        "journal": "Physics Education",
        "volume": "47",
        "number": "5",
        "pages": "537-544",
        "month": "September",
        "year": 2012,
        "url": "http://dx.doi.org/10.1088/0031-9120/47/5/537"
    },
    "data": {
        "pendulum": {
            "shapes": ["tennis ball", "hoop", "disc", "beam"],
            "unit": ""
        },
        "total_time": {
            "values": [52.88, 52.63, 45.78, 43.20],
            "unit": "s",
            "number_of_cycles": 30
        }
    }
}

_d04 = {
   "source": {
        "authors": [
            "Mária Kladivová", "L'ubomír Mucha"
        ],
        "title": "Physical pendulum—a simple experiment can give comprehensive information about a rigid body",
        "journal": "European Journal of Physics",
        "volume": "35",
        "number": "2",
        "pages": "025018",
        "month": "March",
        "year": 2014,
        "url": "http://doi.org/10.1088/0143-0807/35/2/0255018"
    },
    "data": {
        "pivot_position": {
            "values": [0.01, 0.08, 0.10, 0.12, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.20, 0.21, 0.23, 0.25, 0.46, 0.48, 0.50, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.59],
            "unit": "m"
        },
        "period": {
            "values": [1.338, 1.265, 1.248, 1.235, 1.223, 1.218, 1.220, 1.214, 1.216, 1.215, 1.224, 1.226, 1.272, 1.309, 1.324, 1.257, 1.234, 1.236, 1.221, 1.221, 1.215, 1.218, 1.219, 1.224, 1.231],
            "unit": "s"
        }
    }
}

# Expose only 'data' publicly
data = [_d00, _d01, _d02, _d03, _d04]

# Limit module exports
__all__ = ["data"]
