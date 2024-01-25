from torch.utils.data import Dataset, DataLoader
from PIL import Image

class CustomDataset(Dataset):
    def __init__(self, labels, paths, subset=False, transform=None):
        self.labels = labels
        self.paths = paths
        self.transform = transform
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        path = self.paths.iloc[idx]
        image = Image.open(path).convert('RGB')
        label = self.labels.iloc[idx]
        if self.transform:
            image = self.transform(image)
        return image, int(label)