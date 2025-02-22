import pydicom
from pathlib import Path

# from image_type_inference import ImageTypeClassifierBase
# from study_processing import ProcessOneDicomStudyToVolumesMappingBase

#
# inference_model_path = "/home/cavriley/programs/dcm-classifier/src/dcm_classifier/models/ova_rf_classifier.onnx"
#
#
# inferer = ImageTypeClassifierBase(classification_model_filename=inference_model_path)
#
# json_series_directory = "/home/cavriley/programs/dcm-classifier/tests/testing_data/anonymized_testing_data/adjacent_json_data"
#
# study = ProcessOneDicomStudyToVolumesMappingBase(
#     study_directory=json_series_directory, inferer=inferer
# )
# study.run_inference()
#
# for series_number, series in study.series_dictionary.items():
#     assert series.get_series_number() == 1

# mosaic_image_path = "/localscratch/Users/cavriley/ascb_additional_data/3912_MRI_BRAIN_W_WO_CONTRAST__2822362831731038/5/DICOM/1.3.12.2.1107.5.1.4.50383210595611579337085544700478893786-5-13-xy7y8k.dcm"
# dummy_image = "/home/cavriley/programs/dcm-classifier/tests/testing_data/anonymized_testing_data/all_fields_data/all_fields_file.dcm"
# mosaic_ds = pydicom.dcmread(mosaic_image_path)
# dummy_ds = pydicom.dcmread(dummy_image)
# mosaic_image_type = mosaic_ds.ImageType
#
# print(mosaic_image_type)
# dummy_ds.ImageType = mosaic_image_type
# print(dummy_ds.ImageType)
#
# print(dummy_ds)
#
# # save image
# pydicom.dcmwrite("../../tests/testing_data/anonymized_testing_data/mosaic_data/mosaic_image.dcm", dummy_ds)

all_fields_path: Path = Path("/home/cavriley/programs/dcm-classifier/tests/testing_data/anonymized_testing_data/all_fields_data/all_fields_file.dcm")
updated_all_fields_path: Path = Path("/home/cavriley/programs/dcm-classifier/tests/testing_data/anonymized_testing_data/all_fields_data/updated_all_fields_file.dcm")

ds = pydicom.dcmread(all_fields_path)
ds.SeriesDescription = "EmptyValue"

pydicom.dcmwrite(updated_all_fields_path, ds)

