import sys
from pathlib import Path

try:
    from dcm_classifier.study_processing import ProcessOneDicomStudyToVolumesMappingBase
    from dcm_classifier.image_type_inference import ImageTypeClassifierBase
except Exception as e:
    print(f"Missing module import {e}")
    print(
        f"Try setting export PYTHONPATH={Path(__file__).parent.parent.as_posix()}/src"
    )
    sys.exit(255)


inference_model_path = "/home/cavriley/programs/dcm-classifier/src/dcm_classifier/models/ova_rf_classifier.onnx"


inferer = ImageTypeClassifierBase(classification_model_filename=inference_model_path)

json_series_directory = "/home/cavriley/programs/dcm-classifier/tests/testing_data/anonymized_testing_data/adjacent_json_data"
# json_file_list = list(Path(json_series_directory).rglob("*.json"))
study = ProcessOneDicomStudyToVolumesMappingBase(
    study_directory=json_series_directory, inferer=inferer, use_json=True
)
study.run_inference()
print(study.get_study_dictionary())
for series_number, series in study.series_dictionary.items():
    assert series.get_series_number() == 1
    print(series.get_modality_probabilities())
