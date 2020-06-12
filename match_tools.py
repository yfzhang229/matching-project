#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 01:12:12 2020

@author: zhangyufeng
"""

import os

def num_edges(G):
    '''Compute the number of edges in G'''
    num = 0
    for v in G:
        num += len(G[v])
    return num / 2

def get_file_paths(directory='graphs'):
    file_paths = []
    for directory, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.mtx'):
                file_path = os.path.join(directory, file_name)
                file_paths.append(file_path)
    return file_paths

def from_mtx(mtx):
    '''Construct a graph from the mtx, the output G is a dictionary, 
    iter(G) is the set of vertices, iter(G[v]) is the neighborhood of v in G'''
    G = {}
    num_vertex = max(mtx.shape[0], mtx.shape[1])
    for v in range(num_vertex):
        G[v] = set([])
    
    num_edge = mtx.nnz
    for k in range(num_edge):
        if mtx.row[k] != mtx.col[k]:
            G[mtx.row[k]].add(mtx.col[k])
            G[mtx.col[k]].add(mtx.row[k])
    return G



class union_find:
    '''Union Find structure'''
    def __init__(self):
        self.parents = {}
        self.weights = {}
        
    def __getitem__(self, object):
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object
        
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]
            
        for v in path:
            self.parents[v] = root
        
        return root
    
    def select(self, base):
        root = self[base]
        for v in self.parents:
            if self[v] == root:
                self.parents[v] = base
                
    topless = -1
    def union(self, *objects, base=-1):
        if base == -1:
            roots = [self[x] for x in objects]
            root = max([(self.weights[r], r) for r in roots])[1]
            for r in roots:
                if r != root:
                    self.parents[r] = root
                    self.weights[root] += self.weights[r]
        else:
            roots = [self[x] for x in objects]
            root = base
            for r in roots:
                if r != root:
                    self.parents[r] = root
                    self.weights[root] += self.weights[r]
