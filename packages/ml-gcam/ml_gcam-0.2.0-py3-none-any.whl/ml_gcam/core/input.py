import os
import re
from pathlib import Path

import pandas as pd
from lxml import etree


def main(output_dir: Path, output_file: Path, config_dir: Path):
    """Parse scenario config -> inputs used."""
    # inputs = Path(GCAM_CORE_PATH) / "exp1_jr_file/inputs"
    config_dir = Path(config_dir)
    rows = []
    # get all the xml configs in the dir
    configs = [
        x
        for x in config_dir.iterdir()
        if x.name.endswith("xml") and x.stat().st_size != 0
    ]
    for f in configs:
        row = {}
        root = etree.parse(f)
        row["filename"] = f
        row["scenario_name"] = root.find('//Strings/Value[@name = "scenarioName"]').text
        values = root.findall("//ScenarioComponents/Value")
        for el in values:
            row[el.get("name")] = el.text
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(Path(output_dir) / output_file, index=False, sep="|")


def parse(batch_path: Path, filename, filedir):
    """Exploratory analysis of a single config file from the experiment."""
    doc = etree.parse(batch_path)
    root = doc.getroot()
    sets = root.xpath("./ComponentSet")

    runs = []
    for run in sets:
        category = run.get("name").lower().replace(" ", "_")
        subset = run.xpath("./FileSet")
        for s in subset:
            label = s.get("name")
            values = s.xpath("./Value")
            if values:
                for val in values:
                    metric = val.get("name")
                    filename = os.path.split(val.text)[1]
                    runs.append(
                        {
                            "category": category,
                            "label": label,
                            "metric": metric,
                            "filename": filename,
                        },
                    )
            else:
                runs.append(
                    {
                        "category": category,
                        "label": label,
                        "metric": None,
                        "filename": None,
                    },
                )
    df_runs = pd.DataFrame(runs)
    return df_runs


def defaults(config_file: Path):
    """Finds the common default values in the config file of a gcam run."""
    doc = etree.parse(config_file)
    root = doc.getroot()

    defaults = []
    for x in root.xpath("//ScenarioComponents/Value"):
        metric = x.get("name")
        filename = os.path.split(x.text)[1]
        defaults.append({"metric": metric, "filename": filename})
    return pd.DataFrame(defaults).sort_values("metric")


def check(filename, core, num_configs):
    """Validate gcam config file for input."""
    base = "/research/hutchinson/data/gcam/gcam_files"
    configs = Path("/research/hutchinson/data/gcam/gcam_files/configuration-sets")
    configs = [x for x in configs.iterdir() if "xml" in x.name]

    search = [
        Path(f"{base}/gcam-water-fix/exe"),
        Path(f"{core}/input/gcamdata/exe"),
        Path(f"{base}/exp1_jr_files/inputs"),
        Path(f"{core}/input/scenario_inputs"),
        Path(f"{base}/gcam-water-fix/input/scenario_inputs"),
        Path(f"{core}/input/gcamdata/xml"),
        Path(f"{base}/gcam-water-fix/input/gcamdata/xml"),
        Path(f"{base}/gcam-water-fix/input/gcamdata/xml/jr-water-fix-xmls"),
        Path(f"{base}/gcam-water-fix/input/gcamdata/xml/base_for_elec"),
    ]

    for conf in configs[:num_configs]:
        doc = etree.parse(conf)
        root = doc.getroot()
        inputs = [x.text for x in root.xpath("//Value") if "xml" in x.text]
        inputs = [f for f in inputs if re.search(f"{filename}", f)]
        for i in inputs:
            exists = False
            for s in search:
                name = os.path.split(i)[1]
                if (s / name).exists():
                    exists = True
                    print(f"found: {name} in {s.absolute()}", file=sys.stderr)
            if not exists:
                print(f"{i}", file=sys.stdout)
