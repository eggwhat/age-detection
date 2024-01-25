import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import torch.backends.cudnn as cudnn
import torchvision
from torchvision.models import ResNet50_Weights
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

# python -u main.py > train.log
if __name__ == "__main__":
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Device to be used: {device}")
  
    path_to_metadatacsv = os.path.realpath('D:\Karina\data/metadata-clean-aug.csv')
    df = pd.read_csv(path_to_metadatacsv)
    df['target'] = df['age'].map(class_labels_reassign)
    print(f"0: {len(df[df['target'] == 0])}")
    print(f"1: {len(df[df['target'] == 1])}")
    print(f"2: {len(df[df['target'] == 2])}")
    print(f"3: {len(df[df['target'] == 3])}")
    print(f"4: {len(df[df['target'] == 4])}")
    print(f"5: {len(df[df['target'] == 5])}")
    print(f"6: {len(df[df['target'] == 6])}")
    df0 = df[df['target'] == 0]
    df1 = df[df['target'] == 1]
    df2 = df[df['target'] == 2]
    df3 = df[df['target'] == 3].head(30000)
    df4 = df[df['target'] == 4].head(30000)
    df5 = df[df['target'] == 5].head(30000)
    df6 = df[df['target'] == 6].head(30000)
    metadata = pd.concat([df0, df1, df2, df3, df4, df5, df6])
    print(f"Amount of crop images: {len(metadata)}")

    dataloaders, dataset_sizes = split_dataset(metadata)
    print(dataset_sizes)
    model_conv = torchvision.models.resnet50(weights=ResNet50_Weights.DEFAULT)
    for param in model_conv.parameters():
        param.requires_grad = False # Parameters of newly constructed modules have requires_grad=True by default

    num_ftrs = model_conv.fc.in_features
    # model_conv.fc = nn.Linear(num_ftrs, len(CLASSES))
    model_conv.fc = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(num_ftrs, len(CLASSES))
    )

    model_conv = model_conv.to(device)

    criterion = nn.CrossEntropyLoss()

    optimizer_conv = optim.SGD(model_conv.fc.parameters(), lr=0.01, momentum=0.9)

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

