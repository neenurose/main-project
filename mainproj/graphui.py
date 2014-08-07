#Thanks to Mitchell et al. (2012).  "Midge: Generating Image Descriptions From Computer Vision Detections." Proceedings of EACL 2012.

from Tkinter import *
from ttk import Frame, Button, Label, Style
from tkFileDialog import askopenfilename
import sys
import re
import itertools
import yaml
import pickle
from math import log
from learn import learn
from newhognew import *
#from classify import *
import svminput
import svmfile
from deletefiles import *
final_sentence={}



def buttonPushed():
    data = None
    word_thresh=0.01
    objects = []
    verb_forms = {}
    spec_post = False
    with_preps = True
    print "success"
    newhognew(file1)
    svminput.svminputfn()
    svmfile.svmfilefn()
    #classi()
    #print file1
    #txt.insert(END, file1)
    data = yaml.load(file('C:/meenuneenu/project/libsvm-3.17/python/detail.txt', 'r'))
    pickle.dump(data, open("C:/meenuneenu/project/libsvm-3.17/python/pickled_files/data.pk", "wb"))
    learn_obj = learn(objects, word_thresh)
    gen_obj = Generator(learn_obj, data, spec_post, with_preps)
    final_sentence=gen_obj.run()
    
    for post_id in sorted(final_sentence):
        print "***", post_id
        for s_num in final_sentence[post_id]:
            for sentence in final_sentence[post_id][s_num]:
                #print sentence + '.'+ '\n'
                txt.insert(END, sentence)
                txt.insert(END, '.\n')

    deletefiles()


def quit_handler():
    print "program is quitting!"
    sys.exit(0)

def open_file_handler():
    global file1
    file1= askopenfilename()
    print file1
    captn = Label( top, text=file1, foreground="red")
    #captn.pack(side=TOP)
    captn.grid(row=3)
    #file2=str(file1)
    return file1



class Generator():
    def __init__(self, learn_obj, data={}, spec_post=False, with_preps=True):
        self.data = data
        self.mod_detections = {}
        self.action_detections = {}
        self.prep_detections = {}
        self.learn_obj = learn_obj
        self.label_id_hash = {}
        self.spec_post = spec_post
        self.with_preps = with_preps
        self.colors={"red","white","black","brown","blue","green","yellow"}
        self.get_detections()

    def get_detections(self, data={}):
        label = ""
        if data == {}:
            data = self.data
        for a in data:
            last_label = label
            try:
                label = self.learn_obj.label_hash[a['label']]
            except KeyError:
                label = a['label']
            except:
                txt.insert(END, 'No sentence')
                deletefiles()
            id_n = str(a['id'])
            post_id = a['post_id']
            # Generating for just a single image.
            if self.spec_post and post_id != self.spec_post:
                continue
            try:
                self.label_id_hash[post_id][id_n] = label
            except KeyError:
                self.label_id_hash[post_id] = {id_n:label}
            try:
                if a['preps'] == {}:
                    self.prep_detections[post_id] = {}
                for id_set in a['preps']:
                    ids = id_set.split(",")
                    id1 = ids[0].strip("'")
                    id2 = ids[1].strip("'")
                    try:
                        self.prep_detections[post_id][(id1, id2)] = a['preps'][id_set]
                    except KeyError:
                        self.prep_detections[post_id] = {(id1, id2): a['preps'][id_set]}
            except KeyError:
                pass
            try:
                self.mod_detections[post_id][id_n] = {}
            except KeyError:
                self.mod_detections[post_id] = {id_n:{}}
            try:
                for mod in a['attrs']:
                    self.mod_detections[post_id][id_n][mod] = a['attrs'][mod]
            except KeyError:
                self.mod_detections[post_id][id_n] = {}


    def check_plurals(self, objs):
        is_plural = {}
        obj_hash_in = {}
        obj_hash_out = {}
        for obj in objs:
            obj_hash_in[obj] = obj_hash_in.setdefault(obj, 0) + 1
        for obj in obj_hash_in:
            if obj_hash_in[obj] > 1:
                obj_hash_out[obj] = self.learn_obj.plural_hash[obj]
                is_plural[self.learn_obj.plural_hash[obj]] = {}
            else:
                obj_hash_out[obj] = obj
        return (obj_hash_out, is_plural)

    def maximize_det_prob(self, dets_with_scores):
        adj_det_list = []
        noadj_det_list = []
        for det_tuple in dets_with_scores:
            det = det_tuple[0]
            if det == "+":
                continue
            adj = det_tuple[2]
            prob = dets_with_scores[det_tuple][1]
            if adj:
                adj_det_list += [(prob, det_tuple, dets_with_scores[det_tuple])]
            else:
                noadj_det_list += [(prob, det_tuple, dets_with_scores[det_tuple])]
        adj_det_list.sort()
        noadj_det_list.sort()
        adj_det_list.reverse()
        noadj_det_list.reverse()
        det_hash = {}
        if adj_det_list != []:
            det_hash[adj_det_list[0][1]] = adj_det_list[0][2]
        if noadj_det_list != []:
            det_hash[noadj_det_list[0][1]] = noadj_det_list[0][2]
        return det_hash

    def get_NP(self, post_id, id_n, obj, is_plural, det_hash, mod_hash):
        att_hash = {}
        NPs = {}
        mods = {}
        if obj not in is_plural:
            o_tag = "NN"
            
            for mod in self.mod_detections[post_id][id_n]:
                
                mod_tag = "JJ"
                att = self.learn_obj.get_att(mod)
                v_score = float(self.mod_detections[post_id][id_n][mod])
                
                if att == None:
                    att_hash[mod] = (mod, v_score, mod_tag)
                elif att in att_hash:
                    c_score = att_hash[att][1]
                   
                    if v_score > c_score:
                        att_hash[att] = (mod, v_score, mod_tag)
                else:
                    att_hash[att] = (mod, v_score, mod_tag)
        else:
            o_tag = "NNS"
        for att in att_hash:
            mod = att_hash[att][0]
            for mod_tuple in mod_hash:
                language_mod = mod_tuple[0]
                prob = mod_hash[mod_tuple][1]
                if mod == language_mod:
                    mods[mod] = prob
                    break
        mod_len = len(mods)
        mod_orders = {}
        while mod_len > 0:
            mod_combinations = itertools.combinations(mods, mod_len)
            mod_len -= 1
            for mod_combination in mod_combinations:
                if mod_len == 0:
                    ordered_mods = mod_combination
                else:
                    ordered_mods = self.learn_obj.order_mods(mod_combination, obj)
                new_ordered_mods = []
                for mod in ordered_mods:
                    mod_node = (mod_tag, mod)
                    mod_prob = mods[mod]
                    mod_node_w_prob = (mod_tag, mod, mod_prob)
                    new_ordered_mods += [mod_node_w_prob]
                mod_orders[tuple(new_ordered_mods)] = {}
        for det_tuple in det_hash:
            det = det_tuple[0]
            det_prob = det_hash[det_tuple][1]
            jj_present = det_tuple[2]
            if det == "+":
                continue
            obj_node = (o_tag, obj)
            obj_node_w_prob = (o_tag, obj, 1.0)
            if not jj_present:
                NP = (self.__get_det__(det, obj_node, det_prob), obj_node_w_prob)
                NPs[NP] = {}
            if (jj_present or det == "-") and mods != []:
                for mod_order in mod_orders:
                    if mod_order == ():
                        continue
                    NP = tuple([self.__get_det__(det, mod_order[0], det_prob)] + list(mod_order) + [obj_node_w_prob]) 
                    NPs[NP] = {}
        return NPs

    def __get_det__(self, det, word_tag, prob):

        word = word_tag[1]
        if det == "an":
            if word[0] not in "aeiou":
                det = "a"
        elif det == "a":
            if word[0] in "aeiou":
                det = "an"
        return ("DT", det, prob)

    def generate_sentences(self, NPs, obj2_relations={}):
        sentence_hash = {}
        if obj2_relations == {}:
            sys.stderr.write("Nothing defined other than an NP.\n")
        else:
            for id_list in obj2_relations:
                sentence_hash[id_list] = {}
                if len(id_list) == 1:
                    id_n = id_list[0]
                    for NP1 in NPs[id_n]:
                        final_string = self.print_sentence_single(NP1)
                        sentence_hash[id_list][final_string] = {}
                else:
                    mentioned_objs = {}
                    id3 = ""
                    try:
                        [id1, id2, id3] = id_list[:3]
                    except ValueError:
                        [id1, id2] = id_list[:2]
                    for NP1 in NPs[id1]:
                        for NP2 in NPs[id2]:
                            if id3 != "":
                                for NP3 in NPs[id3]:
                                    for RELS2 in obj2_relations[id_list][(id1, id2)]:
                                        for RELS3 in obj2_relations[id_list][(id1, id3)]:
                                            final_string = self.print_sentence(NP1, RELS2, NP2, RELS3, NP3)
                                            sentence_hash[id_list][final_string] = {}
                            else:
                                for RELS in obj2_relations[id_list][(id1, id2)]:
                                    final_string = self.print_sentence(NP1, RELS, NP2)
                                    sentence_hash[id_list][final_string] = {}
        return sentence_hash

    def print_sentence(self, NP1, RELS, NP2, RELS2="", NP3=""):
        final_str = self.nonterm_surface("NP", NP1)
        final_str = self.nonterm_surface_rels(RELS, final_str)
        final_str += self.nonterm_surface("NP", NP2)
        #final_str += (")" * (final_str.count("(") - final_str.count(")")))
        if NP3 == "":
            pass
        else:
            if RELS2[0] == RELS[0] and RELS2[1][1] == RELS[1][1]:
                RELS2 = ('CONJP', ('CC', 'and', RELS2[1][-1]))
            final_str = self.nonterm_surface_rels(RELS2, final_str)
            final_str += self.nonterm_surface("NP", NP3)
            #final_str += (")" * (final_str.count("(") - final_str.count(")")))
        return final_str

    def print_sentence_single(self, NP, VP=None):
        final_str = self.nonterm_surface("NP", NP)
        if VP:
            final_str = self.nonterm_surface_rels(VP, final_str)
        #final_str += (")" * (final_str.count("(") - final_str.count(")")))
        return final_str

    def nonterm_surface(self, tag, nodes):
        nodes = self.prenom_or_postnom(nodes)
        #s = " (" + tag
        s=""
        for node in nodes:
            s += " " + self.surface_node(node)
        #s += ")"
        return s

    def prenom_or_postnom(self, nodes):
        head_in = False
        new_nodes = []
        if nodes[-1][1] == "person":
            for node in nodes[:-1]:
                if node[0] == "JJ":
                    if node[1] in self.colors:
                        new_nodes += [nodes[-1], ("PP", ("IN", "in", 1.0), ("ADJP", node))]
                        head_in = True
                    else:
                        new_nodes += [tuple(node)]
                else:
                    new_nodes += [tuple(node)]
            if not head_in:
                new_nodes += [tuple(nodes[-1])]
        else:
            new_nodes = nodes
        return tuple(new_nodes)

    def surface_node(self, node):
        #surface_str = "(" + node[0]
        surface_str=""
        x = 1
        while x < len(node):
            sub_node = node[x]
            if isinstance(sub_node, tuple):
                surface_str += " " + self.surface_node(sub_node)
            else:
                surface_str += " " + node[x]
                x += 1
            x += 1
        #surface_str += ")" 
        return surface_str

    def nonterm_surface_rels(self, RELS, cur_str):
        last_rel_tuple = None
        for rel_tuple in RELS:
            if rel_tuple == "PP":
                cur_str = cur_str
                continue
            elif rel_tuple == "CONJP":
                cur_str = cur_str
                last_rel_tuple = None
                continue
            cur_str += " " + self.surface_node(rel_tuple)
        return cur_str

    def run(self):
        if self.prep_detections == {}:
            sys.stderr.write("Have not read in spatial relations from bounding boxes; generating prepositions from language model alone.\n")
            self.with_preps = False
        final_sentence = {}
        # For each image..
        for post_id in self.label_id_hash:
            final_sentence[post_id] = {}
            # Get the detected objects.
            objs = self.label_id_hash[post_id].values()
            obj_list = []
            is_plural = {}
            # Simplest case:  Only 1 object detected.
            if len(objs) == 1:
                # Figure out just the determiner/action for that guy.
                obj_list = objs
                id_list = self.label_id_hash[post_id].keys()
            else:
                (obj_plural_hash, is_plural) = self.check_plurals(objs)
                obj_list = self.learn_obj.cluster_objs(obj_plural_hash.keys())
                id_list = []
                for obj in obj_list:
                    for id_x in self.label_id_hash[post_id]:
                        if self.label_id_hash[post_id][id_x] == obj and id_x not in id_list:
                            id_list += [id_x]
                            break
                #print id_list
                tmp_obj_list = []
                for obj in obj_list:
                    tmp_obj_list += [obj_plural_hash[obj]]
                obj_list = tmp_obj_list

            NPs = {}
            # Stores the possible modifiers for each object
            obj_mod_hash = {}
            # Stores the possible determiners for each object
            obj_det_hash = {}
            VPs = {}
            PPs = {}
            CONJPs = {}
            if self.with_preps:
                given_preps = self.prep_detections[post_id]
            obj_id_cnt = 0
            while obj_id_cnt < len(id_list):
                id_n = id_list[obj_id_cnt]
                obj = obj_list[obj_id_cnt]
                obj_id_cnt += 1
                if obj not in obj_det_hash:
                    if obj in is_plural:
                        obj_det_hash[obj] = self.learn_obj.get_determiners(obj, "NNS")
                    else:
                        obj_det_hash[obj] = self.learn_obj.get_determiners(obj)
                    obj_det_hash[obj] = self.maximize_det_prob(obj_det_hash[obj])
                #Find out modifiers
                if obj not in obj_mod_hash:
                    if obj in is_plural:
                        obj_mod_hash[obj] = {}
                    else:
                        obj_mod_hash[obj] = self.learn_obj.get_mods(obj)
                NPs[id_n] = self.get_NP(post_id, id_n, obj, is_plural, obj_det_hash[obj], obj_mod_hash[obj])
            sentences = {}
            n = 0
            mentioned = {}
            x = 0
            last_y = 0
            V_PPs = {}
            while x < len(id_list):
                i = id_list[x]
                obj_i = obj_list[x]
                x += 1
                y = x
                if i in mentioned:
                    continue
                mentioned[i] = {}
                while y < len(id_list):
                    j = id_list[y]
                    obj_j = obj_list[y]
                    # Should never happen, but just in case code gets changed...
                    if j in mentioned:
                        continue
                    y += 1
                    mentioned[j] = {}
                    c_preps = None
                    if self.with_preps:
                        try:
                            g_prep = given_preps[(i, j)]
                            c_preps = self.learn_obj.get_preps(g_prep, 'ab')
                        except KeyError:
                            g_prep = given_preps[(j, i)]
                            c_preps = self.learn_obj.get_preps(g_prep, 'ba')
                    PPs[(i, j)] = self.learn_obj.get_PPs(obj_i, obj_j, c_preps)
                    if PPs[(i, j)] == {}:
                        CONJPs[(i, j)] = {("CC", "and"): 1.0} #if no prepositions bw two objects then 'and' is used.
            """   
            print "NPs"
            print NPs
            print "PPs"
            print PPs
            """
            #sentence generarion starting


            last_items = id_list[last_y:]
            if last_items != []:
                sentences[n] = (id_list[last_y:])
            #print sentences

            s_count = 0
            obj_relations = {}
            for sentence in sentences:
                id_list = sentences[sentence]
                s = tuple(id_list)
                obj_relations[s] = {}
                s_count += 1
                i = 0
                try:
                    id_tuples = [(id_list[0], id_list[1])]
                    try:
                        id_tuples += [(id_list[0], id_list[2])]
                    except IndexError:
                        pass
                except IndexError:
                    id_tuples = [(id_list[0],)]
                #print "id tuple is", id_tuples
                for id_tuple in id_tuples:
                    id1 = id_tuple[0]
                    try:
                        id2 = id_tuple[1]
                    except IndexError:
                        pass
                    chose_prep = False
                    obj_relations[s][id_tuple] = {}
                    
                    if len(id_tuple) > 1:

                        if PPs[id_tuple] == {}:
                            for conj_node in CONJPs[id_tuple]:
                                prob = CONJPs[id_tuple][conj_node]
                                tag_conj_prob = (conj_node[0], conj_node[1], prob)
                                #print tag_conj_prob
                                obj_relations[s][id_tuple][("CONJP", tag_conj_prob)] = {}
                        else:
                            for prep_node in PPs[id_tuple]:
                                prob = PPs[id_tuple][prep_node]
                                tag_prep_prob = (prep_node[0], prep_node[1], prob)
                                obj_relations[s][id_tuple][("PP", tag_prep_prob)] = prob

                # Generate sentences.
                final_sentence[post_id] = self.generate_sentences(NPs, obj_relations)
        return final_sentence
        

if __name__ == "__main__":
    data = None
    word_thresh=0.01
    objects = []
    verb_forms = {}
    spec_post = False
    with_preps = True
    top = Tk()
    top.geometry("500x500+500+500")

    top.title("Description Generator")
    top.style = Style()
    top.style.theme_use("default")
    #top.pack(fill=BOTH, expand=1)

    top.columnconfigure(1, weight=1)
    top.columnconfigure(3, pad=7)
    top.rowconfigure(3, weight=1)
    top.rowconfigure(5, pad=7)

    lbl = Label(top, text="Description Generator")
    lbl.grid(sticky=W, pady=10, padx=10)

    captn = Label( top, text="Select an image file", foreground="red")
    #captn.pack(side=TOP)
    captn.grid(row=3)

    open_file = Button(top, command=open_file_handler, text="Open File")
    #open_file.pack()
    open_file.grid(row=3, column=3,padx=100)

    mybutton=Button(top,text="Generate",command=buttonPushed)
    #mybutton.pack()
    mybutton.grid(row=4, column=3)

    txt = Text(master=top)
    #txt.pack(side=TOP)
    #txt.insert(END,"generating...")
    txt.grid(row=7, column=0, columnspan=5, rowspan=4,padx=5, sticky=E+W+S+N)

    quit_button = Button(top, command=quit_handler, text="Close")
    #quit_button.pack()
    quit_button.grid(row=12, column=3, padx=100)

    top.mainloop()
    """
    for arg in sys.argv[1:]:
        split_arg = arg.split("=")
        if split_arg[0] == "--data-file":
            data = yaml.load(file(split_arg[1], 'r'))
            pickle.dump(data, open("C:/Python27/Lib/site-packages/Midge-master/pickled_files/data.pk", "wb"))
            learn_obj = learn(objects, word_thresh)
            gen_obj = Generator(learn_obj, data, spec_post, with_preps)
            final_sentence=gen_obj.run()

            for post_id in sorted(final_sentence):
                print "***", post_id
                for s_num in final_sentence[post_id]:
                    for sentence in final_sentence[post_id][s_num]:
                        print sentence + '.'+ '\n'
    """
