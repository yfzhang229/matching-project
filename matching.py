#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 01:20:04 2020

@author: zhangyufeng
"""

from match_tools import union_find, from_mtx
from scipy.io import mmread


global EVEN, ODD, NULL
EVEN = 0
ODD = 1
NULL = -1

def greedy_matching(G):
    '''Get a greedy matching'''
    M = {}
    for v in G:
        if v not in M:
            for u in G[v]:
                if u not in G[v]:
                    M[u] = v
                    M[v] = u
                    break
    return M

def card_matching(mate):
    count = 0
    for v in mate:
        if mate[v] != NULL:
            count += 1
        
    return count / 2

def is_matching(G, mate):
    for v in mate:
        if mate[v] != NULL:
            w = mate[v]
            if mate[w] != v:
                return False
            elif w not in G[v]:
                return False
    return True

def find_max_matching(G):
    
    M = greedy_matching(G)
    
    
    mate = {}
    for v in G:
        if v in M:
            mate[v] = M[v]
        else:
            mate[v] = NULL
            
    card = card_matching(mate)
                
            
    def alternating_forest():
        
        label = {}
        pred = {}
        pnode = union_find()  
        bridge = {}
        
        
        def alternating_tree(v):
            
            Q = [v]
            label[v] = EVEN
            
            def examine(v, w):
                
                def extend_tree(v, w):
                    
                    label[w] = ODD
                    pred[w] = v
                    label[mate[w]] = EVEN
                    pred[mate[w]] = w
                    Q.append(mate[w])
                
                def shrink_blossom(v, w):
                    
                    def find_base(v, w):
                    
                        path1 = {}
                        path2 = {}
                        head1 = v
                        head2 = w
                        def step(path, head):
                            head = pnode[head]
                            if pred[head] == -1:
                                return head
                            parent = pnode[pred[head]]
                            path[head] = parent
                            path[parent] = pnode[pred[parent]]
                            return path[parent]
                            
                            
                        while 1:
                            head1 = step(path1, head1)
                            head2 = step(path2, head2)
                            if head1 == head2:
                                return head1
                            elif head1 in path2:
                                return head1
                            elif head2 in path1:
                                return head2
                            
                    def find_shrink_path(b, v, w):
                        path = [pnode[v]]
                        bri = (v, w)
                        while path[-1] != b:
                            u = pred[path[-1]]
                            path.append(u)
                            bridge[u] = bri
                            Q.append(u)
                            path.append(pnode[pred[u]])
                        return path
                            
                    
                    b = pnode[find_base(v, w)]
                    path1 = find_shrink_path(b, v, w)
                    path2 = find_shrink_path(b, w, v)
                    pnode.union(*path1, base=b)
                    pnode.union(*path2, base=b)
                    
                def augmenting_path(v, w):
                    
                    topless = object()
                    def find_path(s, t=topless):
                        path = []
                        while 1:
                            while label[s] == ODD:
                                v, w = bridge[s]
                                vs = find_path(v, s)
                                vs.reverse()
                                path += vs
                                s = w
                            path.append(s)
                            if mate[s] == NULL:
                                return path
                            u = mate[s]
                            path.append(u)
                            if u == t:
                                return path
                            s = pred[u]
                        
                    return [w] + find_path(v)
                        
                    
                
                
                vb = pnode[v]
                wb = pnode[w]
                
                if vb != wb:
                    if label[wb] == NULL:
                        if mate[w] == NULL:
                           
                            P = augmenting_path(v, w)  
                           
                            k = 0
                            while k < len(P):
                                u = P[k]
                                v = P[k + 1]
                                mate[u] = v
                                mate[v] = u
                                k += 2
                                
                            
                            return True
                            
                        else:
                            
                            extend_tree(v, w)
                            
                            return False
                            
                    elif label[wb] == EVEN:
                        
                        shrink_blossom(v, w)
                       
                        return False
                
                        
                        
                        
            
            current = 0
            while current < len(Q):
                
                v = Q[current]
                current += 1
                for w in G[v]:
                    if examine(v, w):
                        return True
            return False
        
        
        
        for v in G:
            label[v] = NULL
            pred[v] = NULL
            pnode[v]
            
        for v in G:
            if mate[v] == NULL:
                if alternating_tree(v):
                    return True
        
        return False
    
    while alternating_forest():
        card = card_matching(mate)
        #if card % 200 == 0:
            #print(f'card of mate is {card_matching(mate)}')
        pass
    
    return mate



# test

if __name__ == "__main__":
    
    mtx = mmread('graphs/poli.mtx')
#    mtx = mmread('graphs/poli.mtx')
    G = from_mtx(mtx)
    mate = find_max_matching(G)
    print(f'The size of maximum cardinality matching is {card_matching(mate)}')
                