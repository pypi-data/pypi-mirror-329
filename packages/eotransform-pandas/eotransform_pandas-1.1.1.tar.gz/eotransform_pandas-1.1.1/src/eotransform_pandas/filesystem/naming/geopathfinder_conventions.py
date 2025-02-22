from typing import Dict

from geopathfinder.naming_conventions.yeoda_naming import YeodaFilename


def yeoda_naming_convention(file_name: str) -> Dict:
    try:
        yeoda_file = YeodaFilename.from_filename(file_name, convert=True)
        return {k: yeoda_file[k] for k in yeoda_file.fields_def if yeoda_file[k]}
    except ValueError:
        return {}
