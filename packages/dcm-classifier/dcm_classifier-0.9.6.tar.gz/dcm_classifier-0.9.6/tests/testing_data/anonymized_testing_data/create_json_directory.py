import json
from pathlib import Path
from dcm_classifier.dicom_config import required_DICOM_fields, optional_DICOM_fields, inference_features
import pydicom

dicom_directory = Path("/home/cavriley/programs/dcm-classifier/tests/testing_data/anonymized_testing_data/anonymized_data/1/DICOM")
adjacent_data_directory = Path("/home/cavriley/programs/dcm-classifier/tests/testing_data/anonymized_testing_data/adjacent_json_data")

# create adjacent directory
if not adjacent_data_directory.exists():
    adjacent_data_directory.mkdir(exist_ok=True, parents=True)

all_tags = required_DICOM_fields #+ optional_DICOM_fields + inference_features
for filename in dicom_directory.rglob("*.dcm"):
    print(filename)
    file_json_data = pydicom.dcmread(filename, stop_before_pixels=True).to_json_dict()
    # json_string = json.dumps(file_json_data, indent=4)
    print(file_json_data)
    # save off to file in adjacent_data_directory
    with open(adjacent_data_directory / f"{filename.stem}.json", "w") as outfile:
        json.dump(file_json_data, outfile, indent=4)
    # break

