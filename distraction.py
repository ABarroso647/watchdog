import torch
from torch import nn
from torchvision import transforms
from PIL import Image
import numpy as np

'''
labels = ['Safe driving',
          'Texting - right',
          'Talking on the phone - right',
          'Texting - left',
          'Talking on the phone - left',
          'Operating the radio',
          'Drinking',
          'Reaching behind',
          'Hair and makeup',
          'Talking to passenger']
'''

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.layer2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.layer3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.drop = nn.Dropout()
        self.fc1 = nn.Linear(32 * 52 * 52, 1024)
        self.fc2 = nn.Linear(1024, 256)
        self.fc3 = nn.Linear(256, 10)

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        return x


def image_loader(loader, image):
    #image = Image.open(image)
    image = loader(image).float()
    image = image.clone().detach().requires_grad_(True)
    image = image.unsqueeze(0)
    return image


def distraction_label(img):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = Net()
    model.load_state_dict(torch.load('model.pth', map_location=torch.device(device)))
    model.eval()

    p = transforms.Compose([transforms.Resize(size=(224, 224)),
                            transforms.ToTensor(),
                            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
                            ])
    img = image_loader(p, img)
    output = model(img)
    prediction = np.argmax(output.detach().numpy())
    return prediction
