def experiment_name_to_label(name) -> str:
    """Convert key to titlecase."""
    m = {
        "dawn_exp1_jr": "binary",
        "wwu_exp1_jr": "wwu_binary",
        "interp_hypercube": "hypercube",
        "interp_random": "random",
        "interp_sobol": "sobol",
        "interp_dgsm": "dgsm",
        "mixed": "mixed",
        "super": "super",
        "core": "core",
    }
    return m[name]


def experiment_label_to_name(label) -> str:
    """Convert titlecase to key."""
    m = {
        "binary": "dawn_exp1_jr",
        "wwu_binary": "wwu_exp1_jr",
        "hypercube": "interp_hypercube",
        "random": "interp_random",
        "sobol": "interp_sobol",
        "dgsm": "interp_dgsm",
        "mixed": "mixed",
        "super": "super",
        "core": "core",
    }
    return m[label]


def experiment_name_to_paper_label(name) -> str:
    """Convert key to titlecase."""
    m = {
        "dawn_exp1_jr": "binary",
        "wwu_exp1_jr": "binary",
        "interp_hypercube": "interpolated",
        "interp_random": "interpolar",
        "interp_sobol": "interpolated",
        "interp_dgsm": "interpolated",
        "mixed": "mixed",
        "super": "super",
        "core": "core",
    }
    return m[name]
