from pathlib import Path
from dcm_classifier.utility_functions import get_bvalue
import pydicom
path = "/tmp/1353_MRI_BRAIN_BRAIN_STEM_W_W_O_CONTRAST_6731038345184526/402/DICOM"
for file in Path(path).iterdir():
    print(file)
    dataset = pydicom.dcmread(file)
    print(get_bvalue(dataset))
    assert get_bvalue(dataset) == 0

