import markovify
import random


#user may provide their own text libraries from which markov text will be generated

#imported_text_1 = open(**input text file**).read()  #block of code opens and stores text file
#text_model_1 = markovify.Text(**imported_text_1**)
#text_model_1 = text_model_1.compile()

#text models = [put as many rext models ]

#list_of_text_models = [**input text models**]

def generate_markov_reply(list_of_text_models, number_of_sentences):
    """(none)-> string
function randomly selects a text model and a number of sentences.
Function then generates list of markov generated strings. Then
function joins sentences and returns complete string.

"""
    random_text_model = random.choice([text_model,text_model_2]) 
    
    reply =[]
    
    for i in range(number_of_sentences): 
        
        generated_sentence = random_text_model.make_sentence(tries=100)
        if reply != None: #100 tries to generate unique a comment as possible
            reply.append(generated_sentence)                                
        #sometimes markov returns none if a comment is deemed not unique enough                                                                
    
    return " ".join(reply)

