# -*- coding:utf-8 -*-
# @File  : main.py
# @Author: Zhou
# @Date  : 2023/11/29
import pandas as pd
import torch
from torchvision import datasets
import torchvision.transforms as transforms
import time

from pimpy.memmat_tensor import DPETensor
from NN_layers import  ResNetMem,ResNet,ResNet18_cifar,ResNet18_cifar_mem
from tqdm import tqdm

def train(model, nn_type='fc', n_epochs=50, train_loader=None, test_loader=None, device=None,  mem_en=False):
    # 定义损失函数和优化器
    lossfunc = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(params=model.parameters(), lr=0.1,momentum=0.9,weight_decay=5e-4,nesterov=True)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, factor=0.2, patience=3, threshold=0.001, mode='max')
    best_acc = 0.0  # 初始化最高准确率
    best_model_state = None  # 用于保存最高准确率时的模型状态
    # 开始训练
    for epoch in tqdm(range(n_epochs)):
        counter = 0
        train_loss = 0.0
        inference_time_sum = backward_time_sum = 0.0
        for data, target in train_loader:
            start = time.time()
            data, target = data.to(device), target.to(device)
            if nn_type == 'fc':
                data = data.view(data.size(0), -1)
            optimizer.zero_grad()  # 清空上一步的残余更新参数值
            output = model(data)  # 得到预测值
            loss = lossfunc(output, target)  # 计算两者的误差
            inference_time = time.time() - start
            loss.backward()  # 误差反向传播, 计算参数更新值
            optimizer.step()  # 将参数更新值施加到 net 的 parameters 上
            if  mem_en:
                model.update_weight()
            train_loss += loss.item() * data.size(0)
            backward_time = time.time() - start - inference_time
            inference_time_sum += inference_time
            backward_time_sum += backward_time
            counter += 1
        
        train_loss = train_loss / len(train_loader.dataset)
        print('Epoch:  {}  \tTraining Loss: {:.6f}'.format(epoch + 1, train_loss))
        acc = test(model, nn_type, test_loader, device)
        scheduler.step(acc)
        current_lr = optimizer.param_groups[0]['lr']
        print(f"Epoch: {epoch + 1}, Current Learning Rate: {current_lr:.6f}")
        #save model,add accuracy as model name like "resnet18_cifar10_7612.pth"
        if acc > best_acc:
            best_acc = acc
            best_model_state = model.state_dict()
            print(f"New best accuracy: {best_acc:.4f}")

    # 在训练结束后保存最高准确率对应的模型
    if best_model_state is not None:
        accuracy_str = f"{int(best_acc * 100):02d}"
        model_filename = f"./model_trained/resnet18_cifar100/resnet18_cifar100_{accuracy_str}.pth"
        torch.save(best_model_state, model_filename)
        print(f"Best model saved as {model_filename} with accuracy {best_acc:.4f}")

    print(f"Training complete. Best accuracy: {best_acc:.4f}")

# 在数据集上测试神经网络
def test(model, nn_type='fc', test_loader=None, device=None):
    model.eval()
    correct = 0
    total = 0
    count = 0
    progress_bar = tqdm(test_loader, desc="Testing")
    for images, labels in progress_bar:
        images, labels = images.to(device), labels.to(device)
        if nn_type == 'fc':
            images = images.view(images.size(0), -1)
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        count += labels.size(0)
        
        # 计算当前准确率并更新进度条描述
        current_accuracy = 100.0 * correct / total
        progress_bar.set_description(f"Testing (Current Accuracy: {current_accuracy:.2f}%)")
        
    final_accuracy =  correct / total
    return final_accuracy

def main():
    # 定义全局变量
    torch.manual_seed(42)
    transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5071, 0.4867, 0.4408], std=[0.2675, 0.2565, 0.2761])
])
    # 定义训练集个测试集，如果找不到数据，就下载
    train_data = datasets.CIFAR100(root='D:/dataset/cifar100', train=True, download=True, transform=transform)
    test_data = datasets.CIFAR100(root='D:/dataset/cifar100', train=False, download=True, transform=transform)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    tb_mode = 1
    if tb_mode == 0:
        n_epochs = 50  # epoch 的数目
        batch_size = 32
        train_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size, num_workers=0)
        test_loader = torch.utils.data.DataLoader(test_data, batch_size=batch_size, num_workers=0)
        engine = DPETensor(var=0.0,quant_array_gran=(128,128),quant_input_gran=(1,128),paral_array_size=(64,64),paral_input_size=(1,64))
        in_slice_method = (1, 3)
        weight_slice_method =  (1, 3)
        model = ResNet18_cifar_mem(engine, in_slice_method, weight_slice_method, device,bw_e=None,num_classes=100)
        model.to(device)
        train(model, 'cnn', n_epochs, train_loader, test_loader, device, mem_en=True)
    elif tb_mode == 1:
        batch_size = 32  # 决定每次读取多少图片
        test_loader = torch.utils.data.DataLoader(test_data, batch_size=batch_size, num_workers=0)
        engine = DPETensor(var=0.0,rdac=2**4,g_level=2**4,radc=2**16,quant_array_gran=(128,1),quant_input_gran=(1,128),paral_array_size=(64,1),paral_input_size=(1,64))
        in_slice_method = (1, 3, 4)
        weight_slice_method =  (1, 3, 4)
        model = ResNet18_cifar_mem(engine, in_slice_method, weight_slice_method, device,num_classes=100,bw_e=None , input_en=True)
        model.to(device)
        model.load_state_dict(torch.load('./resnet18-cifar100_7926.bin'))
        model.update_weight() 
        acc=test(model, 'cnn', test_loader, device)
        print('Accuracy of the network on the test images: %.2f %%' % ( acc))


if __name__ == '__main__':
    # 定义全局变量
    main()