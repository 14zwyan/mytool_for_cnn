# Detection part of BlitzNet ("BlitzNet: A Real-Time Deep Network for Scene Understanding" Nikita Dvornik et al. ICCV17)

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from torchvision.models.resnet import resnet50,Bottleneck
from collections import OrderedDict
from data import voc_res50
from layers import *
import os

def multibox(cfg,num_classes):
    loc_layers = []
    conf_layers = []
    in_channels=[512,1024,2048,2048,2048,2048]
    for k,v in enumerate(cfg['aspect_ratios']):
        n_anchors = len(v)*2 + 1
        loc_layers += [nn.Conv2d(in_channels[k],n_anchors*4,kernel_size=3,padding=1)]
        conf_layers += [ nn.Conv2d(in_channels[k],n_anchors*num_classes,kernel_size=3,padding=1)]
    return (loc_layers,conf_layers)


class SSD_Res50(nn.Module):

    def __init__(self, phase,size,base=None,head=None,num_classes=21):
        super(SSD_Res50, self).__init__()
        '''
        if image_size == 300:
            self.config300(x4)
        elif image_size == 512:
            self.config512(x4)
        '''
        self.phase=phase
        self.cfg = voc_res50
        self.priorbox = PriorBox(self.cfg)
        self.priors = Variable(self.priorbox.forward(),volatile=True)
        self.loc = nn.ModuleList( head[0] )
        self.conf = nn.ModuleList( head[1] )
        self.num_classes = num_classes
        self.base = resnet50(pretrained=True)
        self.extras = nn.Sequential(OrderedDict([
            ('layer5', nn.Sequential(Bottleneck(2048, 512, 2, shortcut()),
                                     Bottleneck(2048, 512, 1))),
            ('layer6', nn.Sequential(Bottleneck(2048, 512, 2, shortcut()),
                                     Bottleneck(2048, 512, 1))),
            ('layer7', nn.Sequential(Bottleneck(2048, 512, 2, shortcut()),
                                     Bottleneck(2048, 512, 1)))]))
        self.skip_layers = ['layer2', 'layer3', 'layer4', 'layer5', 'layer6', 'layer7']
        self.softmax = nn.Softmax(dim=-1)
        self.detect = Detect(num_classes,0,200,0.01,0.5)
        '''
            ('layer8', nn.Sequential(Bottleneck(2014, 512, 2, shortcut()),
                                     Bottleneck(2048, 512, 1)))]))


        self.Up = nn.Sequential(OrderedDict([
            ('rev_layer7', BottleneckSkip(2048, 2048, 512)),
            ('rev_layer6', BottleneckSkip(2048 if self.pred_layers[0] == 'rev_layer6' else 512, 2048, 512)),
            ('rev_layer5', BottleneckSkip(512,  2048, 512)),
            ('rev_layer4', BottleneckSkip(512,  2048, 512)),
            ('rev_layer3', BottleneckSkip(512,  1024, 512)),
            ('rev_layer2', BottleneckSkip(512,  512,  512)),
            ('rev_layer1', BottleneckSkip(512,  256,  512))]))
        '''
        '''
        n_boxes = len(self.config['aspect_ratios']) + 1
        self.Loc = nn.ModuleList([])
        self.Conf = nn.ModuleList([])
        for i in range(len(self.config['grids')):
            self.Loc.append(nn.Conv2d(512, n_boxes * 4, 3, padding=1))
            self.Conf.append(nn.Conv2d(512, n_boxes * (self.n_classes + 1), 3, padding=1))
        #self.Loc  = nn.Conv2d(512, n_boxes * 4, 3, padding=1)
        #self.Conf = nn.Conv2d(512, n_boxes * (self.n_classes+1), 3, padding=1)
        '''
    def forward(self, x):
        skips, xs = [], []
        loc= []
        conf = []
        for name, m in self.base._modules.items():
            x = m(x)
            if name in self.skip_layers:
                skips.append(x)
            if name == 'layer4':
                break




        for name, m in self.extras._modules.items():
            if name in self.skip_layers:
                x = m(x)
                skips.append(x)
        for (x,l,c) in zip(skips,self.loc,self.conf):
            loc.append( l(x).permute(0,2,3,1).contiguous() )
            conf.append( c(x).permute(0,2,3,1).contiguous() )

        loc = torch.cat([ o.view( o.size(0),-1 ) for o in loc ],1)
        conf = torch.cat( [o.view( o.size(0),-1) for o in conf],1 )
        if self.phase == 'test':
            output = self.detect(loc.view(loc.size(0),-1,4),
                                 self.softmax(conf.view(conf.size(0,-1,self.num_classes))),
                                 self.priors.type(type(x.data)))
        else:
            output = (
                loc.view(loc.size(0),-1,4),
                conf.view(conf.size(0),-1,self.num_classes),
                self.priors
            )
        return output
        '''

        ind = -2
        for name, m in self.Up._modules.items():
            if name in self.pred_layers:
                x = m(x, skips[ind])
                xs.append(x)
                ind -= 1

        xs = [F.avg_pool2d(xs[0], xs[0].size()[2:])] + xs
        return self._prediction(xs[::-1])
        '''




    def _prediction(self, xs):
        locs = []
        confs = []
        for i, x in enumerate(xs):
            loc = self.Loc[i](x) if isinstance(self.Loc, nn.ModuleList) else self.Loc(x)
            loc = loc.permute(0, 2, 3, 1).contiguous().view(loc.size(0), -1, 4)
            locs.append(loc)

            conf = self.Conf[i](x) if isinstance(self.Conf, nn.ModuleList) else self.Conf(x)
            conf = conf.permute(0, 2, 3, 1).contiguous().view(conf.size(0), -1, self.n_classes + 1)
            confs.append(conf)
        return torch.cat(locs, dim=1), torch.cat(confs, dim=1)


    '''
    def config300(x4=True):
        self.skip_layers = ['layer1', 'layer2', 'layer3', 'layer4', 'layer5', 'layer6', 'layer7']
        self.pred_layers = ['rev_layer6', 'rev_layer5', 'rev_layer4', 'rev_layer3', 'rev_layer2'] + ['rev_layer1']*x4
        self.config = {
            'name': 'BlitzNet300-resnet50-Det' + '-s4' if x4 else '-s8',
            'image_size': 300,
            'grids': [75]*x4 + [38, 19, 10, 5, 3, 1],
            'sizes': ,
            'aspect_ratios': (1/3.,  1/2.,  1,  2,  3),

            'batch_size': 32,
            'init_lr' = 1e-4,
            'stepvalues' = (35000, 50000),
            'max_iter' = 65000
        }

    def config512(x4=False):
        self.skip_layers = ['layer1', 'layer2', 'layer3', 'layer4', 'layer5', 'layer6', 'layer7', 'layer8']
        self.pred_layers = ['rev_layer7', 'rev_layer6', 'rev_layer5', 'rev_layer4', 'rev_layer3', 'rev_layer2'] + (
                           ['rev_layer1']*x4)
        self.config = {
            'name': 'BlitzNet512-resnet50-Det' + '-s4' if x4 else '-s8',
            'image_size': 512,
            'grids': [128]*x4 + [64, 32, 16, 8, 4, 2, 1],
            'sizes': ,
            'aspect_ratios': (1/3.,  1/2.,  1,  2,  3),

            'batch_size': 16,
            'init_lr' = 1e-4,
            'stepvalues' = (45000, 60000),
            'max_iter' = 75000
        }
    '''



class BottleneckSkip(nn.Module):
    def __init__(self, in_channels1, in_channels2, out_channels, stride=1,
                    mode='bilinear'):
        super().__init__()
        self.mode = mode

        if stride != 1 or in_channels1 != out_channels:
            self.shortcut = shortcut(in_channels1, out_channels, stride)
        else:
            self.shortcut = nn.Sequential()

        self.residual = nn.Sequential(
            nn.Conv2d(in_channels1 + in_channels2, out_channels // 4, 1, bias=False),
            nn.BatchNorm2d(out_channels // 4),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels // 4, out_channels // 4, 3, padding=1, stride=stride, bias=False),
            nn.BatchNorm2d(out_channels // 4),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels // 4, out_channels, 1, bias=False),
            nn.BatchNorm2d(out_channels))

    def forward(self, x, skip):
        x = F.upsample(x, size=skip.size()[2:], mode=self.mode)
        shortcut = self.shortcut(x)
        residual = self.residual(torch.cat([x, skip], dim=1))

        return F.relu(shortcut + residual, inplace=True)



def shortcut(in_channels=2048, out_channels=2048, stride=2):
    #if in_channels == out_channels:    # in BlitzNet's tensorflow implementation
    #    return nn.MaxPool2d(1, stride=stride)
    return nn.Sequential(
        nn.Conv2d(in_channels, out_channels, 1, stride=stride, bias=False),
        nn.BatchNorm2d(out_channels))


def build_ssd(phase,size=300,num_classes=21):
    if phase != 'test' and phase!='train':
        print('ERROR Phase:' + phase + 'not recognized')

    cfg = voc_res50
    head = multibox(cfg,num_classes)

    return SSD_Res50(phase,size,head=head)
