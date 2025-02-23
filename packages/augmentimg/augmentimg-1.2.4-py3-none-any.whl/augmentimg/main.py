import sys
import os
import json
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QComboBox, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QGridLayout, QMessageBox, QSpinBox
import cv2
from albumentations import (
    Compose, RandomRotate90, Blur, RandomBrightnessContrast, 
    RandomGamma, Sharpen, HorizontalFlip, VerticalFlip, CLAHE, 
    HueSaturationValue, ShiftScaleRotate, BboxParams
)

def save_coco_json(coco_data, output_file_path):
    with open(output_file_path, 'w') as f:
        json.dump(coco_data, f, indent=4)

def load_coco_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def parse_coco_json(json_file):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {}, {}, {}

    if 'images' not in data or 'annotations' not in data or 'categories' not in data:
        print("JSON file is missing one or more required keys ('images', 'annotations', 'categories')")
        return {}, {}, {}

    annotations = {item['id']: [] for item in data['images']}
    for annotation in data['annotations']:
        image_id = annotation['image_id']
        annotations[image_id].append({
            'bbox': annotation['bbox'],  # COCO bbox [x_min, y_min, width, height]
            'category_id': annotation['category_id']
        })

    images = {item['id']: item['file_name'] for item in data['images']}
    classes = {category['id']: category['name'] for category in data['categories']}
    return annotations, images, classes

def augment_image_coco(image, image_id, annotations, classes, transform):
    bboxes = [ann['bbox'] for ann in annotations.get(image_id, [])]
    category_ids = [ann['category_id'] for ann in annotations.get(image_id, [])]

    transformed = transform(image=image, bboxes=bboxes, category_ids=category_ids)
    transformed_image = transformed['image']
    transformed_bboxes = transformed.get('bboxes', [])
    transformed_category_ids = transformed.get('category_ids', [])

    return transformed_image, transformed_bboxes, transformed_category_ids

def get_transform(selected_augmentations, annotation_format):
    bbox_format = 'albumentations'
    label_fields = []
    if annotation_format == "YOLO":
        bbox_format = 'yolo'
        label_fields = ['category_ids']
    elif annotation_format == "COCO":
        bbox_format = 'coco'
        label_fields = ['category_ids']

    transformations = []
    if selected_augmentations.get('rotate'):
        transformations.append(RandomRotate90(p=1.0))
    if selected_augmentations.get('flip_h'):
        transformations.append(HorizontalFlip(p=0.5))
    if selected_augmentations.get('flip_v'):
        transformations.append(VerticalFlip(p=0.5))
    if selected_augmentations.get('blur'):
        transformations.append(Blur(p=0.5))
    if selected_augmentations.get('saturation'):
        # Adjust saturation only using HueSaturationValue with no hue or brightness changes.
        transformations.append(HueSaturationValue(hue_shift_limit=0, sat_shift_limit=30, val_shift_limit=0, p=0.5))
    if selected_augmentations.get('contrast'):
        # Use RandomBrightnessContrast with brightness disabled for a contrast-only adjustment.
        transformations.append(RandomBrightnessContrast(brightness_limit=0.0, contrast_limit=0.3, p=0.5))
    if selected_augmentations.get('sharpness'):
        transformations.append(Sharpen(p=0.5))
    if selected_augmentations.get('gamma'):
        transformations.append(RandomGamma(p=0.5))
    if selected_augmentations.get('clahe'):
        transformations.append(CLAHE(p=0.5))
    if selected_augmentations.get('hsv'):
        transformations.append(HueSaturationValue(p=0.5))
    if selected_augmentations.get('ssr'):
        transformations.append(ShiftScaleRotate(p=0.5))
    if selected_augmentations.get('brightness'):
        transformations.append(RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0, p=0.5))

    if label_fields:
        return Compose(transformations, bbox_params=BboxParams(format=bbox_format, label_fields=label_fields))
    else:
        return Compose(transformations)

def augment_image_and_annotation_yolo(image_path, annotation_path, save_dir, transform, count):
    image = cv2.imread(image_path)
    if image is None:
        raise Exception(f"Unable to read image: {image_path}")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with open(annotation_path, 'r') as file:
        annotations = [line.strip().split() for line in file.readlines()]
    bboxes = [(float(x[1]), float(x[2]), float(x[3]), float(x[4])) for x in annotations]
    class_labels = [int(x[0]) for x in annotations]

    transformed = transform(image=image, bboxes=bboxes, category_ids=class_labels)
    transformed_image = transformed['image']
    transformed_bboxes = transformed.get('bboxes', [])
    transformed_class_labels = transformed.get('category_ids', [])

    save_path = os.path.join(save_dir, f'aug_{count}_{os.path.basename(image_path)}')
    transformed_image = cv2.cvtColor(transformed_image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(save_path, transformed_image)

    annotation_save_path = os.path.join(save_dir, f'aug_{count}_{os.path.basename(annotation_path)}')
    with open(annotation_save_path, 'w') as file:
        for label, bbox in zip(transformed_class_labels, transformed_bboxes):
            file.write(f"{label} {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\n")

def augment_images_in_folder_yolo(folder_path, annotation_folder_path, total_desired_images, selected_augmentations):
    original_images = [img for img in os.listdir(folder_path) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))]
    print("Number of images found:", len(original_images))

    if len(original_images) == 0:
        raise Exception("No images found in the folder.")

    augmentations_needed = total_desired_images - len(original_images)
    if augmentations_needed <= 0:
        print("No additional images needed.")
        return

    save_dir = os.path.join(folder_path, 'augmented')
    os.makedirs(save_dir, exist_ok=True)

    transform = get_transform(selected_augmentations, "YOLO")

    count = 0
    for i in range(augmentations_needed):
        for image_name in original_images:
            if count >= augmentations_needed:
                break
            image_path = os.path.join(folder_path, image_name)
            annotation_path = os.path.join(annotation_folder_path, f"{os.path.splitext(image_name)[0]}.txt")

            if not os.path.exists(annotation_path):
                print(f"Annotation file does not exist for {image_path}")
                continue

            try:
                augment_image_and_annotation_yolo(image_path, annotation_path, save_dir, transform, count)
                count += 1
            except Exception as e:
                print(f"Unexpected error processing {image_name}: {str(e)}")
                continue

def augment_images_in_folder_coco(image_dir, json_path, total_desired_images, selected_augmentations):
    coco_data = load_coco_json(json_path)
    annotations, images, classes = parse_coco_json(json_path)
    save_dir = os.path.join(image_dir, 'augmented')
    os.makedirs(save_dir, exist_ok=True)

    augmented_images = []
    augmented_annotations = []

    transform = get_transform(selected_augmentations, "COCO")

    count = 0
    while count < total_desired_images:
        for image_id, file_name in images.items():
            if count >= total_desired_images:
                break
            image_path = os.path.join(image_dir, file_name)
            if not os.path.exists(image_path):
                print(f"Image {file_name} not found.")
                continue

            image = cv2.imread(image_path)
            if image is None:
                print(f"Failed to load image {file_name}. Skipping.")
                continue

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            try:
                transformed_image, transformed_bboxes, transformed_category_ids = augment_image_coco(
                    image, image_id, annotations, classes, transform
                )

                new_file_name = f"aug_{count}_{os.path.basename(file_name)}"
                new_image_path = os.path.join(save_dir, new_file_name)
                cv2.imwrite(new_image_path, cv2.cvtColor(transformed_image, cv2.COLOR_RGB2BGR))

                augmented_images.append({
                    "id": len(augmented_images),
                    "file_name": new_file_name,
                    "height": transformed_image.shape[0],
                    "width": transformed_image.shape[1]
                })

                for bbox, category_id in zip(transformed_bboxes, transformed_category_ids):
                    augmented_annotations.append({
                        "image_id": len(augmented_images) - 1,
                        "category_id": category_id,
                        "bbox": bbox,  # COCO format [x_min, y_min, width, height]
                        "area": bbox[2] * bbox[3],
                        "iscrowd": 0
                    })
                count += 1
            except Exception as e:
                print(f"Error processing image {file_name}: {e}")

    coco_data['images'].extend(augmented_images)
    coco_data['annotations'].extend(augmented_annotations)

    augmented_coco_json_path = os.path.join(save_dir, 'augmented_annotations.json')
    save_coco_json(coco_data, augmented_coco_json_path)

    print("Augmentation complete. Check the 'augmented' folder.")

def augment_images_only(folder_path, total_desired_images, selected_augmentations):
    original_images = [img for img in os.listdir(folder_path) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))]
    print("Number of images found:", len(original_images))

    if len(original_images) == 0:
        raise Exception("No images found in the folder.")

    augmentations_needed = total_desired_images - len(original_images)
    if augmentations_needed <= 0:
        print("No additional images needed.")
        return

    save_dir = os.path.join(folder_path, 'augmented')
    os.makedirs(save_dir, exist_ok=True)

    transform = get_transform(selected_augmentations, "")

    count = 0
    for i in range(augmentations_needed):
        for image_name in original_images:
            if count >= augmentations_needed:
                break
            image_path = os.path.join(folder_path, image_name)
            try:
                image = cv2.imread(image_path)
                if image is None:
                    print(f"Failed to load image {image_name}. Skipping.")
                    continue
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                transformed = transform(image=image)
                transformed_image = transformed['image']

                new_file_name = f"aug_{count}_{os.path.basename(image_name)}"
                new_image_path = os.path.join(save_dir, new_file_name)
                cv2.imwrite(new_image_path, cv2.cvtColor(transformed_image, cv2.COLOR_RGB2BGR))
                count += 1
            except Exception as e:
                print(f"Unexpected error processing {image_name}: {str(e)}")
                continue

class ImageAugmentationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selectedFolder = ''
        self.annotationFolder = ''
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Augmentation Tool')
        self.setGeometry(100, 100, 800, 600)
        mainLayout = QVBoxLayout()

        # Layout for selecting image directory
        directoryLayout = QHBoxLayout()
        self.btnSelectFolder = QPushButton('Select Image Folder', self)
        self.btnSelectFolder.clicked.connect(self.openFolderDialog)
        mainLayout.addWidget(self.btnSelectFolder)

        # Checkbox for annotations
        self.cbAnnotations = QCheckBox('Check this if you have annotations', self)
        self.cbAnnotations.stateChanged.connect(self.annotationCheckboxChanged)
        mainLayout.addWidget(self.cbAnnotations)

        # Dropdown for annotation format
        self.annotationFormatDropdown = QComboBox(self)
        self.annotationFormatDropdown.addItem("YOLO (.txt)")
        self.annotationFormatDropdown.addItem("COCO (.json)")
        self.annotationFormatDropdown.setEnabled(False)
        mainLayout.addWidget(self.annotationFormatDropdown)

        # Layout for selecting annotation directory or file
        annotationLayout = QHBoxLayout()
        self.btnSelectAnnotationFolder = QPushButton('Select Annotations', self)
        self.btnSelectAnnotationFolder.clicked.connect(self.openAnnotationFolderDialog)
        self.btnSelectAnnotationFolder.setEnabled(False)
        annotationLayout.addWidget(self.btnSelectAnnotationFolder)
        mainLayout.addLayout(annotationLayout)

        # Grid layout for augmentation checkboxes
        gridLayout = QGridLayout()
        self.setupCheckBoxes(gridLayout)
        mainLayout.addLayout(gridLayout)

        # Spin box for total desired images
        spinBoxLayout = QHBoxLayout()
        self.labelDesiredImages = QLabel('Total Desired Images:', self)
        self.spinBoxDesiredImages = QSpinBox(self)
        self.spinBoxDesiredImages.setRange(1, 1000)
        self.spinBoxDesiredImages.setValue(10)
        spinBoxLayout.addWidget(self.labelDesiredImages)
        spinBoxLayout.addWidget(self.spinBoxDesiredImages)
        mainLayout.addLayout(spinBoxLayout)

        # Augment Images button
        self.btnAugmentImages = QPushButton('Augment', self)
        self.btnAugmentImages.clicked.connect(self.augmentImages)
        mainLayout.addWidget(self.btnAugmentImages)

        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

    def setupCheckBoxes(self, gridLayout):
        self.cbRotate = QCheckBox('Rotate 90', self)
        self.cbFlipH = QCheckBox('Flip Horizontally', self)
        self.cbFlipV = QCheckBox('Flip Vertically', self)
        self.cbBlur = QCheckBox('Blur', self)
        self.cbSaturation = QCheckBox('Saturation', self)
        self.cbContrast = QCheckBox('Contrast', self)
        self.cbSharpness = QCheckBox('Sharpness', self)
        self.cbGamma = QCheckBox('Gamma', self)
        self.cbCLAHE = QCheckBox('CLAHE', self)
        self.cbHSV = QCheckBox('HSV', self)
        self.cbSSR = QCheckBox('Shift, Scale, Rotate', self)
        self.cbBrightness = QCheckBox('Brightness', self)

        gridLayout.addWidget(self.cbRotate, 0, 0)
        gridLayout.addWidget(self.cbFlipH, 0, 1)
        gridLayout.addWidget(self.cbFlipV, 0, 2)
        gridLayout.addWidget(self.cbBlur, 1, 0)
        gridLayout.addWidget(self.cbSaturation, 1, 1)
        gridLayout.addWidget(self.cbContrast, 1, 2)
        gridLayout.addWidget(self.cbSharpness, 1, 3)
        gridLayout.addWidget(self.cbGamma, 2, 0)
        gridLayout.addWidget(self.cbCLAHE, 2, 1)
        gridLayout.addWidget(self.cbHSV, 2, 2)
        gridLayout.addWidget(self.cbSSR, 2, 3)
        gridLayout.addWidget(self.cbBrightness, 0, 3)

    def annotationCheckboxChanged(self):
        if self.cbAnnotations.isChecked():
            self.annotationFormatDropdown.setEnabled(True)
            self.btnSelectAnnotationFolder.setEnabled(True)
        else:
            self.annotationFormatDropdown.setEnabled(False)
            self.btnSelectAnnotationFolder.setEnabled(False)

    def openFolderDialog(self):
        self.selectedFolder = QFileDialog.getExistingDirectory(self, "Select Image Directory")
        if not self.selectedFolder:
            QMessageBox.warning(self, "Selection Error", "No directory selected")

    def openAnnotationFolderDialog(self):
        annotation_format = self.annotationFormatDropdown.currentText()
        if annotation_format == "COCO (.json)":
            self.annotationFolder, _ = QFileDialog.getOpenFileName(self, "Select COCO Annotation File", "", "JSON Files (*.json)")
            if not self.annotationFolder:
                QMessageBox.warning(self, "Selection Error", "No file selected")
        else:
            self.annotationFolder = QFileDialog.getExistingDirectory(self, "Select Annotation Directory")
            if not self.annotationFolder:
                QMessageBox.warning(self, "Selection Error", "No directory selected")

    def augmentImages(self):
        if not self.selectedFolder:
            QMessageBox.critical(self, "Error", "Please select an image folder.")
            return

        selected_augmentations = {
            'rotate': self.cbRotate.isChecked(),
            'flip_h': self.cbFlipH.isChecked(),
            'flip_v': self.cbFlipV.isChecked(),
            'blur': self.cbBlur.isChecked(),
            'saturation': self.cbSaturation.isChecked(),
            'contrast': self.cbContrast.isChecked(),
            'sharpness': self.cbSharpness.isChecked(),
            'gamma': self.cbGamma.isChecked(),
            'clahe': self.cbCLAHE.isChecked(),
            'hsv': self.cbHSV.isChecked(),
            'ssr': self.cbSSR.isChecked(),
            'brightness': self.cbBrightness.isChecked()
        }
        total_desired_images = self.spinBoxDesiredImages.value()

        try:
            if self.cbAnnotations.isChecked():
                if not self.annotationFolder:
                    QMessageBox.critical(self, "Error", "Please select an annotation folder or file.")
                    return

                annotation_format = self.annotationFormatDropdown.currentText()
                if annotation_format == "COCO (.json)":
                    augment_images_in_folder_coco(self.selectedFolder, self.annotationFolder, total_desired_images, selected_augmentations)
                else:
                    augment_images_in_folder_yolo(self.selectedFolder, self.annotationFolder, total_desired_images, selected_augmentations)
            else:
                augment_images_only(self.selectedFolder, total_desired_images, selected_augmentations)

            QMessageBox.information(self, "Success", "Images have been augmented. Check the 'augmented' folder.")
        except Exception as e:
            QMessageBox.critical(self, "Error during augmentation", f"{str(e)}")
            print(f"Error during augmentation: {str(e)}")

def main():
    app = QApplication(sys.argv)
    ex = ImageAugmentationApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
