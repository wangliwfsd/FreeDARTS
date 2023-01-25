##################################################
# Copyright (c) Xuanyi Dong [GitHub D-X-Y], 2019 #
##############################################################################
import torch, random
import torch.nn as nn
from copy import deepcopy
from ..cell_operations import ResNetBasicblock
from .search_cells     import SearchCell
from .genotypes        import Structure


class TinyNetworkRANDOM(nn.Module):

  def __init__(self, C, N, max_nodes, num_classes, search_space):
    super(TinyNetworkRANDOM, self).__init__()
    self._C        = C
    self._layerN   = N
    self.max_nodes = max_nodes
    self.stem = nn.Sequential(
                    nn.Conv2d(3, C, kernel_size=3, padding=1, bias=False),
                    nn.BatchNorm2d(C))
  
    layer_channels   = [C    ] * N + [C*2 ] + [C*2  ] * N + [C*4 ] + [C*4  ] * N    
    layer_reductions = [False] * N + [True] + [False] * N + [True] + [False] * N

    C_prev, num_edge, edge2index = C, None, None
    self.cells = nn.ModuleList()
    for index, (C_curr, reduction) in enumerate(zip(layer_channels, layer_reductions)):
      if reduction:
        cell = ResNetBasicblock(C_prev, C_curr, 2)
      else:
        cell = SearchCell(C_prev, C_curr, 1, max_nodes, search_space)
        if num_edge is None: num_edge, edge2index = cell.num_edges, cell.edge2index
        else: assert num_edge == cell.num_edges and edge2index == cell.edge2index, 'invalid {:} vs. {:}.'.format(num_edge, cell.num_edges)
      self.cells.append( cell )
      C_prev = cell.out_dim
    self.op_names   = deepcopy( search_space )
    self._Layer     = len(self.cells)
    self.edge2index = edge2index
    self.lastact    = nn.Sequential(nn.BatchNorm2d(C_prev), nn.ReLU(inplace=True))
    self.global_pooling = nn.AdaptiveAvgPool2d(1)
    self.classifier = nn.Linear(C_prev, num_classes)
    self.arch_cache = None
    
  def get_message(self):
    string = self.extra_repr()
    for i, cell in enumerate(self.cells):
      string += '\n {:02d}/{:02d} :: {:}'.format(i, len(self.cells), cell.extra_repr())
    return string

  def extra_repr(self):
    return ('{name}(C={_C}, Max-Nodes={max_nodes}, N={_layerN}, L={_Layer})'.format(name=self.__class__.__name__, **self.__dict__))

  def random_genotype(self, set_cache):
    genotypes = []
    operations=[]
    for i in range(1, self.max_nodes):
      xlist = []
      for j in range(i):
        node_str = '{:}<-{:}'.format(i, j)
        op_name  = random.choice( self.op_names )
        xlist.append((op_name, j))
        operations.append(op_name)
      genotypes.append( tuple(xlist) )
    arch = Structure( genotypes )
    if set_cache: self.arch_cache = arch
    return arch,genotypes,operations

  def set_genotype(self, arch):
    self.arch_cache = arch
    return arch

  def arch_compensate(self, operations_pre,operations):
    genotypes_com = []
    operations_com=[]
    for i in range(1, self.max_nodes):
        xlist = []
        indx=[0,1,3]
        m=indx[i-1]
        for j in range(i):
            node_str = '{:}<-{:}'.format(i, j)
            if operations_pre[j+m]==operations[j+m]:
                op_name  = random.choice( self.op_names )
                while op_name==operations_pre[j+m]:
                    op_name  = random.choice( self.op_names )
            else:
                op_name  = operations[j+m]
            xlist.append((op_name, j))
            operations_com.append(op_name)
            genotypes_com.append( tuple(xlist) )
    arch_com = Structure(genotypes_com )
    return arch_com,operations_com,genotypes_com


  def arch_diver(self, operations_pre):
    genotypes_com = []
    operations_com=[]
    for i in range(1, self.max_nodes):
        xlist = []
        indx=[0,1,3]
        m=indx[i-1]
        for j in range(i):
            node_str = '{:}<-{:}'.format(i, j)
            op_name  = random.choice( self.op_names )
            while op_name==operations_pre[j+m]:
                op_name  = random.choice( self.op_names )

            xlist.append((op_name, j))
            operations_com.append(op_name)
            genotypes_com.append( tuple(xlist) )
    arch_com = Structure(genotypes_com )
    return arch_com,operations_com,genotypes_com

  def arch_diver2(self, operations_pre,operations_pre_pre):
    genotypes_com = []
    operations_com=[]
    for i in range(1, self.max_nodes):
        xlist = []
        indx=[0,1,3]
        m=indx[i-1]
        for j in range(i):
            node_str = '{:}<-{:}'.format(i, j)
            op_name  = random.choice( self.op_names )
            while op_name==operations_pre[j+m] or op_name==operations_pre_pre[j+m]:
                op_name  = random.choice( self.op_names )

            xlist.append((op_name, j))
            operations_com.append(op_name)
            genotypes_com.append( tuple(xlist) )
    arch_com = Structure(genotypes_com )
    return arch_com,operations_com,genotypes_com



  def arch_diver3(self, operations_pre,operations_pre_pre,operations_pre_pre_pre):
    genotypes_com = []
    operations_com=[]
    for i in range(1, self.max_nodes):
        xlist = []
        indx=[0,1,3]
        m=indx[i-1]
        for j in range(i):
            node_str = '{:}<-{:}'.format(i, j)
            op_name  = random.choice( self.op_names )
            while op_name==operations_pre[j+m] or op_name==operations_pre_pre[j+m] or op_name==operations_pre_pre_pre[j+m]:
                op_name  = random.choice( self.op_names )

            xlist.append((op_name, j))
            operations_com.append(op_name)
            genotypes_com.append( tuple(xlist) )
    arch_com = Structure(genotypes_com )
    return arch_com,operations_com,genotypes_com


  def arch_diver4(self, operations_pre,operations_pre_pre,operations_pre_pre_pre,operations_pre_pre_pre_pre):
    genotypes_com = []
    operations_com=[]
    for i in range(1, self.max_nodes):
        xlist = []
        indx=[0,1,3]
        m=indx[i-1]
        for j in range(i):
            node_str = '{:}<-{:}'.format(i, j)
            op_name  = random.choice( self.op_names )
            while op_name==operations_pre[j+m] or op_name==operations_pre_pre[j+m] or op_name==operations_pre_pre_pre[j+m] or op_name==operations_pre_pre_pre_pre[j+m]:
                op_name  = random.choice( self.op_names )

            xlist.append((op_name, j))
            operations_com.append(op_name)
            genotypes_com.append( tuple(xlist) )
    arch_com = Structure(genotypes_com )
    return arch_com,operations_com,genotypes_com






  def forward(self, inputs):

    feature = self.stem(inputs)
    for i, cell in enumerate(self.cells):
      if isinstance(cell, SearchCell):
        feature = cell.forward_dynamic(feature, self.arch_cache)
      else: feature = cell(feature)

    out = self.lastact(feature)
    out = self.global_pooling( out )
    out = out.view(out.size(0), -1)
    logits = self.classifier(out)
    return out, logits
