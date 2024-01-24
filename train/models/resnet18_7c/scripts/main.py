import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import torch.backends.cudnn as cudnn
import torchvision
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split

from classes import CLASSES, class_labels_reassign
from CustomDataset import CustomDataset
from data_transforms import DATA_TRANSFORMS
from train_model import train_model

cudnn.benchmark = True
plt.ion()   # interactive mode

def split_dataset(metadata):
    X_train, X_test, y_train, y_test = train_test_split(metadata['path'], metadata['target'],
                                                    test_size=0.30, random_state=42)
    train_set = CustomDataset(y_train, X_train, transform = DATA_TRANSFORMS['train'])
    val_set = CustomDataset(y_test, X_test, transform = DATA_TRANSFORMS['val'])

    batch_size = 4
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=True, num_workers=0)
    dataloaders = {
      'train': train_loader,
      'val': val_loader
    }
    dataset_sizes = {
        'train': len(train_loader.dataset), 
        'val': len(val_loader.dataset)
    }
    return dataloaders, dataset_sizes

def plot_train_val_accuracy(num_epochs, train_accs, val_accs):
    epochs = range(0, num_epochs)
    plt.plot(epochs, train_accs, label='train')
    plt.plot(epochs, val_accs, label='val')
    plt.legend()
    plt.ylim(0, 1)
    plt.xlabel('Epoch #')
    plt.ylabel('Accuracy')
    plt.title(f'Train vs Val accuracy. Best: {max(val_accs)*100:.2f}%')
    plt.savefig('./output/train_val_accuracy.png')

if __name__ == "__main__":
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Device to be used: {device}")
  
    path_to_metadatacsv = os.path.realpath('D:\Karina\data/metadata-clean-aug.csv')
    metadata_full = pd.read_csv(path_to_metadatacsv)
    metadata_full['target'] = metadata_full['age'].map(class_labels_reassign)
    metadata = metadata_full
    print(f"Amount of crop images: {len(metadata)}")

    dataloaders, dataset_sizes = split_dataset(metadata)
    print(dataset_sizes)
    model_conv = torchvision.models.resnet18(weights='IMAGENET1K_V1')
    for param in model_conv.parameters():
        param.requires_grad = False # Parameters of newly constructed modules have requires_grad=True by default

    num_ftrs = model_conv.fc.in_features
    model_conv.fc = nn.Linear(num_ftrs, len(CLASSES))

    model_conv = model_conv.to(device)

    criterion = nn.CrossEntropyLoss()

    optimizer_conv = optim.SGD(model_conv.fc.parameters(), lr=0.001, momentum=0.9)

    # Decay LR by a factor of 0.1 every 5 epochs
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer_conv, step_size=5, gamma=0.1)
    num_epochs = 25
    model_conv, train_accs, val_accs = train_model(model_conv, criterion, optimizer_conv, exp_lr_scheduler, dataloaders,
                             device, dataset_sizes, num_epochs=num_epochs)
    output_dir = os.path.join('', 'output')
    isExist = os.path.exists(output_dir)
    if not isExist:
        os.makedirs(output_dir)
        print("Output dir is created!")
    torch.save(model_conv.state_dict(), './output/model.pt')
    plot_train_val_accuracy(num_epochs, train_accs, val_accs)

