import torch
import torch.nn as nn
import torchvision
from torchvision import transforms

class Resnet18_7C:
  def __init__(self):
    model_path = 'assets/models/resnet18_7classes.pt'
    self.classes = {
        0: '0 - 2',
        1: '3 - 9',
        2: '10 - 20',
        3: '21 - 27',
        4: '28 - 45',
        5: '46 - 65',
        6: '> 65'
    }
    self.data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }
    self.loaded_model = torchvision.models.resnet18(weights='IMAGENET1K_V1')
    num_ftrs = self.loaded_model.fc.in_features
    self.loaded_model.fc = nn.Linear(num_ftrs, len(self.classes))
    self.loaded_model.load_state_dict(torch.load(model_path, map_location='cpu'))
    self.loaded_model.eval()

  def predict(self, img):
    preds = None
  
    # img = Image.open(img_path).convert('RGB') # make sure img is an RGB image
    img = self.data_transforms['val'](img)
    img = img.unsqueeze(0)
    img = img.to("cpu")
  
    with torch.no_grad():
        outputs = self.loaded_model(img)
        _, preds = torch.max(outputs, 1)
    return self.classes[preds[0].item()]