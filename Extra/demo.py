import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms
from torch.utils.data import DataLoader, Dataset
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from PIL import Image
from torch.optim.lr_scheduler import ReduceLROnPlateau
import numpy as np


import pretrainedmodels

## Define custom data structure
class CustomInputs(Dataset):
    def __init__(self, imgPath, annotations, transform=None): ## Initializing Class
        self.imgPath = imgPath
        self.annotations = annotations
        self.transform = transform

    def __len__(self):  ## Function to return string length
        return len(self.imgPath)

    def __getitem__(self, idx):  ## Function to return element at an index
        image = Image.open(self.imgPath[idx]).convert('RGB')
        notation = self.annotations[idx]
        if self.transform:
            image = self.transform(image)
        return image, notation

transform_train = transforms.Compose([ ## Adjust image augmentation and normalization for the model for training
    transforms.RandomResizedCrop(299),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

transform_val_test = transforms.Compose([ ## Adjust image augmentation and normalization for the model for testing
    transforms.Resize(299),
    transforms.CenterCrop(299),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Create datasets and load data for Training, Validation and Testing
training_set = CustomInputs(train_X, train_Y, transform=transform_train)  ## training set
validation_set = CustomInputs(val_X, val_Y, transform=transform_val_test)  ## validation set
testing_set = CustomInputs(test_X, test_Y, transform=transform_val_test)  ## testing set
training_data = DataLoader(training_set, batch_size=32, shuffle=True)  ## load training data for the model
validation_data = DataLoader(validation_set, batch_size=32, shuffle=False)  ## load validation data for the model
testing_data = DataLoader(testing_set, batch_size=32, shuffle=False)  ## load testing data for the model

# Load Xceptoin Model
xception_model = pretrainedxception_models.__dict__['xception'](pretrained='imagenet')
count_features = xception_model.last_linear.in_features
xception_model.last_linear = nn.Linear(count_features, 31)

# Fine Tuning Unfreezing layers
for param in xception_model.parameters():
    param.requires_grad = True

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
xception_model = xception_model.to(device)

cross_entropy = nn.CrossEntropyLoss()
adam_optimizer = optim.Adam(xception_model.parameters(), lr=0.0001, weight_decay=1e-4)

# Learning rate schedule_optimizer
schedule_optimizer = ReduceLROnPlateau(adam_optimizer, mode='min', factor=0.1, patience=3, verbose=True)

# Training function
def train_xception_model(xception_model, training_data, validation_data, cross_entropy, adam_optimizer, schedule_optimizer, epoch_count=20):
    baseline_accuracy = 0.0
    early_stopping_patience = 5
    check_early_stopping = 0

    for epoch in range(epoch_count):
        xception_model.train()
        active_difference = 0.0
        for images, annotations in training_data:
            images = images.to(device)
            annotations = annotations.to(device)

            adam_optimizer.zero_grad()
            derived_image = xception_model(images)
            loss = cross_entropy(derived_image, annotations)
            loss.backward()

            # Gradient clipping
            nn.utils.clip_grad_norm_(xception_model.parameters(), max_norm=2.0)

            adam_optimizer.step()
            active_difference += loss.item() * images.size(0)

        epoch_difference = active_difference / len(training_data.dataset)
        check_validation_set, _, _, _ = evaluate_xception_model(xception_model, validation_data)

        schedule_optimizer.step(epoch_difference)

        if check_validation_set > baseline_accuracy:
            baseline_accuracy = check_validation_set
            torch.save(xception_model.state_dict(), 'best_xception.pth')
            check_early_stopping = 0
        else:
            check_early_stopping += 1

        print(f'Epoch [{epoch+1}/{epoch_count}], Loss: {epoch_difference:.4f}, Val Accuracy: {check_validation_set:.4f}')

        if check_early_stopping >= early_stopping_patience:
            print("Early stopping triggered")
            break

# Evaluation function
def evaluate_xception_model(xception_model, data_loader):
    xception_model.eval()
    predictions = []
    all_annotations = []
    with torch.no_grad():
        for images, annotations in data_loader:
            images = images.to(device)
            annotations = annotations.to(device)
            derived_image = xception_model(images)
            _, preds = torch.max(derived_image, 1)
            predictions.extend(preds.cpu().numpy())
            all_annotations.extend(annotations.cpu().numpy())

    accuracy = accuracy_score(all_annotations, predictions)
    precision = precision_score(all_annotations, predictions, average='weighted', zero_division=0)
    recall = recall_score(all_annotations, predictions, average='weighted', zero_division=0)
    f1 = f1_score(all_annotations, predictions, average='weighted', zero_division=0)
    return accuracy, precision, recall, f1

# Train the xception_model
train_xception_model(xception_model, training_data, validation_data, cross_entropy, adam_optimizer, schedule_optimizer, epoch_count=20)

# Load the best xception_model and evaluate on test data
xception_model.load_state_dict(torch.load('best_xception.pth'))

## Testing and Metrics
test_accuracy, test_precision, test_recall, test_f1 = evaluate_xception_model(xception_model, test_loader)
print(f'Test Accuracy: {test_accuracy:.4f}, Precision: {test_precision:.4f}, Recall: {test_recall:.4f}, F1 Score: {test_f1:.4f}')