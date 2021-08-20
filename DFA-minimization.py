#!/usr/bin/env python
# coding: utf-8

# In[21]:


import copy


# In[22]:


url_file= 'input.txt'

# read data from file txt -> output: (data :string type)
def read_file(url_file):
    data = []
    with open(url_file, encoding='utf8') as f:
        for line in f:
            data.append(line.strip())
        f.close()
        return data
    return None

# file.txt: states : list
#           word   : list
#           start  : character
#           end    : list
#           transition: n row (one row [])

# formart data from (data :string type) -> output (states : list, sigma : list, s0: character, end_states: list, transition: list)
def format_data(url_file):
    
    data = read_file(url_file)

    states = list(data[0].split(","))
    sigma = list(data[1].split(","))
    s0 = data[2].split(",")
    end_states = list(data[3].split(","))
    transition = []
    for i in range(4, len(data)):
        a = tuple(data[i].split(","))
        transition.append(a)
    return states, sigma, s0, end_states, transition

# states, sigma,s0, end_states, transition = format_data('input.txt')
# formart input from (states, sigma,s0, end_states, transition) to input_otomat
# chuyển đổi từ otomat đơn định (5 thành phần) -> otomat theo định nghĩa bên dưới 
def format_input(url_file):
    states, sigma, s0, end_states, transition = format_data(url_file)
    
    end_states_number = []
    for i in end_states:
        end_states_number.append(states.index(i))
        
    states_number = []
    for i in range(0, len(states)):
        states_number.append(i)
        
    transition_cp = copy.deepcopy(transition)
    
    by_zero = [0 for i in range(0, len(states))]
    by_one = [0 for i in range(0, len(states))]

    for i in range(0, len(states)):
        for j in range(0, len(transition_cp)):
            if(transition_cp[j][0] == states[i]):
                temp = transition_cp[j][1]
                index_temp = states.index(temp)
                if(transition_cp[j][2] == '0'):
                    by_zero[i] = states_number[index_temp]
                else:
                    by_one[i] = states_number[index_temp]
    return states, states_number , end_states_number, by_zero, by_one

# states_word, states_number , end_states_number, by_zero, by_one = format_input('input.txt')
# print(states_number)
# print(end_states_number)
# print(by_zero)
# print(by_one)


# In[23]:


def read_Automaton(url_file):
    origin_states, states_number , end_states_number, by_zero, by_one = format_input(url_file)
    automaton = Automaton(states_number , end_states_number, by_zero, by_one)
    return automaton, origin_states


# In[24]:


class Automaton:
    def __init__(self, states=None, final_states=None, by_zero=None, by_one=None):
        self.states = states
        self.final_states = final_states
        self.by_zero = by_zero
        self.by_one = by_one

def print_otomat(automaton, origin_states):
    states = automaton.states
    final_states = automaton.final_states
    by_zero = automaton.by_zero
    by_one = automaton.by_one
    
    # print 
    states_out = []
    sigma_out = ['1','0']
    s0_out = ''
    end_states_out = []
    transition_out = []
    
    for i in states:
        states_out.append(origin_states[i])
    s0_out = states_out[0]
    
    for i in final_states:
        end_states_out.append(origin_states[i])
    
    for i in range(0, len(by_zero)):
        temp_transition_byzero = (origin_states[i],origin_states[by_zero[i]],0)
        temp_transition_byone = (origin_states[i],origin_states[by_one[i]],1)
        transition_out.append(temp_transition_byzero)
        transition_out.append(temp_transition_byone)
    print('')
    print(str('states:\t\t'),  end = ' ')
    print(states_out)
    print(str('sigma:\t\t'),  end = ' ')
    print(sigma_out)
    print(str('s0:\t\t'),  end = ' ')
    print(s0_out)
    print(str('end_states:\t'),  end = ' ')
    print(end_states_out)
    print(str('transition: '))
    for i in transition_out:
        print(str('\t\t'), i)

    print()

# Xây dựng lớp tương đương
def get_equivalence_classes(automaton):
    equivalence_classes = []
    
    # Đánh dấu state theo 0 đến đâu, và theo 1 đến đâu
    marked_states = []
    for state in automaton.states:
        if state in automaton.final_states:
            marked_states.append((1, (None, None)))  # (<class>, (<transition_by_zero_class>, <transition_by_one_class>))
        else:
            marked_states.append((0, (None, None)))

    old_classes_count = len(set(marked_states))

    while True:
        for state, state_marks in enumerate(marked_states):
            marked_states[state] =                 (state_marks[0],
                 (marked_states[automaton.by_zero[state]][0], marked_states[automaton.by_one[state]][0]))

        unique_marks = list(set(marked_states))
        for state, state_marks in enumerate(marked_states):
            marked_states[state] = (unique_marks.index(state_marks), (None, None))

        if len(unique_marks) == old_classes_count:
            for equivalence_class in range(len(unique_marks)):
                equivalence_classes.append([state for state, state_marks in enumerate(marked_states)
                                           if state_marks[0] == equivalence_class])
            break

        old_classes_count = len(unique_marks)

    return equivalence_classes

# Tối thiểu hoá automaton
def minimize_automaton(automaton, equivalence_classes):
    minimal_automaton = copy.deepcopy(automaton)
    
    # Các lớp tương đương 
    for equivalence_class in equivalence_classes:
        for state in equivalence_class:
            if minimal_automaton.by_zero[state] in equivalence_class:
                minimal_automaton.by_zero[state] = state
            else:
                minimal_automaton.by_zero[state] =                     min(equivalence_classes[[equivalence_classes.index(equivalence_class)
                                             for equivalence_class in equivalence_classes
                                             if minimal_automaton.by_zero[state] in equivalence_class][0]])
            if minimal_automaton.by_one[state] in equivalence_class:
                minimal_automaton.by_one[state] = state
            else:
                minimal_automaton.by_one[state] =                     min(equivalence_classes[[equivalence_classes.index(equivalence_class)
                                             for equivalence_class in equivalence_classes
                                             if minimal_automaton.by_one[state] in equivalence_class][0]])
    # Các lớp tương đương 
    for equivalence_class in equivalence_classes:
        for state in equivalence_class[1:]:
            minimal_automaton.by_zero[state] = -1
            minimal_automaton.by_one[state] = -1
            if state in minimal_automaton.final_states:
                minimal_automaton.final_states.remove(state)
            minimal_automaton.states[minimal_automaton.states.index(state)] = -1

    not_deleted = lambda x: x != -1
    minimal_automaton.states = list(filter(not_deleted, minimal_automaton.states))
    minimal_automaton.by_zero = list(filter(not_deleted, minimal_automaton.by_zero))
    minimal_automaton.by_one = list(filter(not_deleted, minimal_automaton.by_one))

    for i, state in enumerate(minimal_automaton.states):
        if i < len(minimal_automaton.final_states):
            minimal_automaton.final_states[i] = minimal_automaton.states.index(minimal_automaton.final_states[i])
        minimal_automaton.by_zero[i] = minimal_automaton.states.index(minimal_automaton.by_zero[i])
        minimal_automaton.by_one[i] = minimal_automaton.states.index(minimal_automaton.by_one[i])
    minimal_automaton.states = list(range(len(minimal_automaton.states)))

    return minimal_automaton


# In[25]:


if __name__ == '__main__':
    url_filetxt = 'input.txt'
    
    # initial_automaton
    initial_automaton, origin_states = read_Automaton(url_filetxt)
    print("initial_automaton: ")
    print_otomat(initial_automaton,origin_states)
    equivalence_classes = get_equivalence_classes(initial_automaton)
    
    # minimal_automaton
    minimal_automaton = minimize_automaton(initial_automaton, equivalence_classes)
    print('minimal_automaton:')
    print_otomat(minimal_automaton,origin_states)


# In[26]:


# use lib pythomata 
# Nhược điểm là output đưa ra chưa được format về giống state ban đầu
# kiểu dữ liệu là set => dễ bị sáo chỗ khi in ra màn hình
# install lib
# pip install pythomata
from pythomata import SimpleDFA

states = {"A", "B", "C", "D", "E", "F", "G", "H"}
alphabet = {"1", "0"}
initial_state = "A"
accepting_states = {"C"}

transition_function = {
    "A": { 
        "0": "B",
        "1": "F",
    },
    "B": {
        "0": "G",
        "1": "C",
    },
    "C": {
        "0": "A",
        "1": "C",
    },
    "D": {
        "0": "C",
        "1": "G",
    },
    "E": {
        "0": "H",
        "1": "F",
    },
    "F": {
        "0": "C",
        "1": "G",
    },
    "G": {
        "0": "G",
        "1": "E",
    },
    "H": {
        "0": "G",
        "1": "C",
    }
}
        
# create otomat
dfa = SimpleDFA(states, alphabet, initial_state, accepting_states, transition_function)

minimize_automaton = dfa.minimize()

def print_automaton_(automaton_in):
    print(str('states:\t\t\t'),  end = ' ')
    print(automaton_in.states)
    print(str('alphabet:\t\t'),  end = ' ')
    print(list(automaton_in.alphabet))
    print(str('initial_state:\t\t'),  end = ' ')
    print(automaton_in.initial_state)
    print(str('accepting_states:\t'),  end = ' ')
    print(automaton_in.accepting_states)
    print(str('get_transitions:\t'),  end = ' ')
    print(automaton_in.get_transitions())
    print()
    
print('automaton: ')
print_automaton_(dfa)  
print('minimize_automaton: ')
print_automaton_(minimize_automaton)

