# -*- coding: utf-8 -*-
"""Question6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1U7FoQo_Qw0vVybwConRI8fDEOumtHGmk
"""

# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BeCs3VYE7aFjX3LJ8J6qvxlekCpN-amA
"""

# -*- coding: utf-8 -*-
"""NN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aLx2W7RV_ErI4PZR3_NBJFbiud0WjBMD
"""

import torch
import torchvision
import torchvision.transforms as transforms
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
'''
# http://pytorch.org/
from os.path import exists
from wheel.pep425tags import get_abbr_impl, get_impl_ver, get_abi_tag
platform = '{}{}-{}'.format(get_abbr_impl(), get_impl_ver(), get_abi_tag())
cuda_output = !ldconfig -p|grep cudart.so|sed -e 's/.*\.\([0-9]*\)\.\([0-9]*\)$/cu\1\2/'
accelerator = cuda_output[0] if exists('/dev/nvidia0') else 'cpu'

!pip install -q http://download.pytorch.org/whl/{accelerator}/torch-0.4.1-{platform}-linux_x86_64.whl torchvision
import torch
'''
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=4,
                                          shuffle=True, num_workers=8)

testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                       download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=4,
                                         shuffle=False, num_workers=8)

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
					 
							   
						   

# 2 convolutional layers along with maxpooling layers before the fully
#connected layers
class NetFCQ1Q4(nn.Module):
    def __init__(self):
        super(NetFCQ1Q4, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def draw(yTitle,y):
    plt.yticks(rotation = 90)
    plt.ylabel = yTitle
    plt.xlabel = 'Epochs'
    plt.plot(range(1,len(y)+1),y)
    plt.show()
#Function to calculate the accuracy of the predicted model when run on Training Data as well as TestData.
#An optimizer is used and the loss function used is Cross Entropy . We are using a Learning Rate of 0.001 and varying Batch Size

def AccuracyCheck(trainloader, testloader, net, criterion, optimizer, batch_size, classes):
				  
				   
		 
    device = torch.device("cpu" if torch.cuda.is_available() else "cpu")
    print(device)
    net.to(device)
    loss_lst = []
    accuracy_tst_lst = []
    accuracy_train_lst = []
    size_data = 12000
    for epoch in range(50):  # Setting the epochs to 50 as suggested in the question
        
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            inputs, labels = data
            inputs = inputs.to(device)
            labels = labels.to(device)


            optimizer.zero_grad()

									 
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

						  
            running_loss += loss.item()
            if i % 2000 == 1999:    
                print('[%d, %5d] loss: %.3f' %
                      (epoch + 1, i + 1, running_loss / 2000))
                if(size_data == i+1):
                    loss_lst.append(running_loss / 2000)
                running_loss = 0.0
		  

        correct = 0
        total = 0
        with torch.no_grad():
            for data in trainloader:
                images, labels = data
                images = images.to(device)
                labels = labels.to(device)
                outputs = net(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
#Accuracy on TrainData Calculated and Printed
        print('Accuracy on the train images: %d %%' % (100 * correct / total))
        
        accuracy_train_lst.append(100 * correct / total)
    
        correct = 0
        total = 0
        with torch.no_grad():
            for data in testloader:
                images, labels = data
                images = images.to(device)
                labels = labels.to(device)
                outputs = net(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
#Accuracy on TestData Calculated and Printed
        print('Accuracy on the test images: %d %%' % (100 * correct / total))
        accuracy_tst_lst.append(100 * correct / total)

    print('Finished Training')

    dataiter = iter(testloader)
    images, labels = dataiter.next()
    images = images.to(device)
    labels = labels.to(device)
    
    print('GroundTruth: ', ' '.join('%5s' % classes[labels[j]] for j in range(batch_size)))

    outputs = net(images)
    _, predicted = torch.max(outputs, 1)

    print('Predicted: ', ' '.join('%5s' % classes[predicted[j]]
                                  for j in range(batch_size)))
    correct = 0
    total = 0
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            images = images.to(device)
            labels = labels.to(device)
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print('Accuracy of the network on the 10000 test images: %d %%' % (
        100 * correct / total))

    class_correct = list(0. for i in range(10))
    class_total = list(0. for i in range(10))
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            images = images.to(device)
            labels = labels.to(device)
            outputs = net(images)
            _, predicted = torch.max(outputs, 1)
            c = (predicted == labels).squeeze()
            for i in range(batch_size):
                label = labels[i]
                class_correct[label] += c[i].item()
                class_total[label] += 1


    for i in range(10):
        print('Accuracy of %5s : %2d %%' % (
            classes[i], 100 * class_correct[i] / class_total[i]))

    return loss_lst,accuracy_train_lst,accuracy_tst_lst

def main():
#Varying learning Rates to check the effect of it on accuracy on the training and test data
  learning_rate = [0.1,0.01,0.0001,10]
  for i in learning_rate:

    net = NetFCQ1Q4()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=i, momentum=0.9)
    loss, Accuracy_trainset, Accuracy_testset = AccuracyCheck(trainloader,testloader,net, criterion, optimizer, 4, classes)
    print(loss)
    print(Accuracy_trainset)
    print(Accuracy_testset)
    draw('Loss',loss)
    draw('Train Accuracy',Accuracy_trainset)
    draw('Test Accuracy',Accuracy_testset)


if __name__ == "__main__": 
    main()

