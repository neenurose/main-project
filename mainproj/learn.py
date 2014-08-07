import sys
import re
import glob
import math
import itertools
from nltk.corpus import wordnet as wn
import pickle

class learn():
    def __init__(self, reserved_words=[], word_thresh=.001):
        self.word_thresh = float(word_thresh)
        self.label_hash = {'motorbike':'motorcycle', 'television':'tv', 'pottedplant':'plant'}
        self.hypernym_hash = {}
        self.obj_probs = {}
        self.plural_hash = {}
        self.mod_hash = {}
        self.det_hash = {}
        self.att_hash = {}
        self.preps = {}
        self.prep_hash = {'verb-prep':{}, 'prep-noun':{}, 'noun-prep':{}}
        self.read_as_pickle()

    def read_as_pickle(self):
        print "loading models..."
        #print "1"
        #self.visual_thresh_hash = pickle.load(open("C:/meenuneenu/project/libsvm-3.17/python/pickled_files/visual_thresh_hash.pk", "rb"))
        print "1"
        self.hypernym_hash = pickle.load(open("C:/meenuneenu/project/libsvm-3.17/python/pickled_files/hypernym_hash.pk", "rb"))
        print "2"
        self.obj_probs = pickle.load(open("C:/meenuneenu/project/libsvm-3.17/python/pickled_files/obj_probs.pk", "rb"))
        #print "4"
        #self.mod_ngram_hash = pickle.load(open("C:/meenuneenu/project/libsvm-3.17/python/pickled_files/mod_ngram_hash.pk", "rb"))
        print "3"
        self.plural_hash = pickle.load(open("C:/meenuneenu/project/libsvm-3.17/python/pickled_files/plural_hash.pk", "rb"))
        print "4"
        self.mod_hash = pickle.load(open("C:/meenuneenu/project/libsvm-3.17/python/pickled_files/mod_hash.pk", "rb"))
        print "5"
        self.det_hash = pickle.load(open("C:/meenuneenu/project/libsvm-3.17/python/pickled_files/det_hash.pk", "rb"))
        print "6"
        self.att_hash = pickle.load(open("C:/meenuneenu/project/libsvm-3.17/python/pickled_files/att_hash.pk", "rb"))
        print "7"
        self.preps = pickle.load(open("C:/meenuneenu/project/libsvm-3.17/python/pickled_files/preps.pk", "rb"))
        """
        print "10"
        self.verb_hash = pickle.load(open("C:/meenuneenu/project/libsvm-3.17/python/pickled_files/verb_hash.pk", "rb"))
        """
        print "8"
        self.prep_hash = pickle.load(open("C:/meenuneenu/project/libsvm-3.17/python/pickled_files/prep_hash.pk", "rb"))
        """
        print "12"
        self.verb_trans_hash = pickle.load(open("C:/meenuneenu/project/libsvm-3.17/python/pickled_files/verb_trans_hash.pk", "rb"))
        print "13"
        self.noun_freq_hash = pickle.load(open("C:/meenuneenu/project/libsvm-3.17/python/pickled_files/noun_freq_hash.pk", "rb"))
        print "14"
        #self.noun_noun_hash = pickle.load(open("pickled_files/noun_noun_hash.pk", "rb"))
        print "15"
        self.ins_hash = pickle.load(open("C:/meenuneenu/project/libsvm-3.17/python/pickled_files/ins_hash.pk", "rb"))
        """
        print "Done!"

    def get_hyp_probs(self, obj_set):
        self.num_objs = len(obj_set)
        found = False
        for obj in obj_set:
            if obj in self.obj_probs:
                continue
            obj_syn = wn.synset(obj + ".n.01")
            found = False
            for hypernym_path in obj_syn.hypernym_paths():
                if found:
                    break
                hypernym_path = list(hypernym_path)
                hypernym_path.reverse()
                for hypernym in hypernym_path:
                    if found:
                        break
                    # Return p(pos|num_objs) for all possible pos.
                    # e.g., {1:0.4, 2:.3, 3:.3}
                    self.obj_probs[obj] = self.hypernym_hash[self.num_objs][str(hypernym)]
                    found = True
                    break
        """
        if not self.read_pickle:
            pickle.dump(self.obj_probs, open("pickled_files/obj_probs.pk", "wb"))
        """

    def order_set(self, obj_list):
        final_set = []
        # For each position...
        tuple_list = []
        for i in range(1, self.num_objs + 1):
            # Grab the probability of each object in this position.
            for obj in self.obj_probs:
                try:
                    obj_prob = self.obj_probs[obj][i]
                except KeyError:
                    obj_prob = .000000000001
                tuple_thing = (obj_prob, obj, i)
                tuple_list += [tuple_thing]
        tuple_list.sort()
        tuple_list.reverse()
        order_hash = {}
        for tuple_thing in tuple_list:
            obj = tuple_thing[1]
            pos = tuple_thing[2]
            if pos not in order_hash:
                while obj in obj_list:
                    try:
                        order_hash[pos][obj] += 1
                    except KeyError:
                        try:
                            order_hash[pos][obj] = 1
                        except KeyError:
                            order_hash[pos] = {obj:1}
                    obj_index = obj_list.index(obj)
                    obj_list.pop(obj_index)
        for pos in sorted(order_hash):
            obj = order_hash[pos].keys()
            obj = obj[0]
            for i in range(order_hash[pos][obj]):
                final_set += [obj]
        # Chosen object is the most probable one.
        return final_set


    def cluster_objs(self, obj_list):
        """ Nominal ordering from hypernyms. """
        self.get_hyp_probs(obj_list)
        final_set = self.order_set(obj_list)
        return final_set

    def get_determiners(self, obj, tag="NN"):
        try:
            return self.det_hash[(obj, tag)]
        except KeyError:
            return self.det_hash[(obj, "NN")]

    def get_mods(self, obj):
        try:
            return self.mod_hash[obj]
        except KeyError:
            return {}

    def get_att(self, mod):
        for att in self.att_hash:
            if mod in self.att_hash[att]:
                # If this happens more than 
                # once?
                return att
        return None

    def get_preps(self, prep, order):
        return self.preps[prep][order]

    def get_PPs(self, i, j=None, c_preps=None):
        prep_hash = {}
 
        if j == None:
            if c_preps == None:
                return self.prep_hash['prep-noun'][i]
            else:

                try:
                    for o_prep in self.prep_hash['prep-noun'][i]:
                        for c_prep in c_preps:
                            if c_prep == o_prep[1]:
                                prep_hash[o_prep] = self.prep_hash['prep-noun'][i][o_prep][1]
                            else: 
                                pass
                except KeyError:

                    for c_prep in c_preps:
                        prep_hash[c_prep] = self.word_thresh
                return prep_hash
      
        try:
            for node in self.prep_hash['prep-noun'][j]:
                if node in self.prep_hash['noun-prep'][i]:
                    i_prob = self.prep_hash['noun-prep'][i][node][1]
                    j_prob = self.prep_hash['prep-noun'][j][node][1]
                    ij_prob = round(math.sqrt(i_prob * j_prob), 4)
                    """
                    print "i_prob noun-prep"
                    print i_prob
                    print "j_prob prep-noun"
                    print j_prob
                    print "ij_prob"
                    print ij_prob
                    """

                    if c_preps != None:

                        if node[1] in c_preps or (node[1] == "against" and "in" in c_preps):
                            prep_hash[node] = ij_prob #j_prob
                        else:
                            pass
                    else:
                        prep_hash[node] = ij_prob
        except KeyError:
            pass
        return prep_hash


