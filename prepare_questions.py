'''
Script para cambiar el formato del json de miniGQA al utilizado por la red
MAC.
'''

# Librerías a utilizar.
import json
import argparse

def prepare_questions(args):
    print('Loading data...')
    with open(args.input_questions_dir, 'r') as f:
        data  = json.load(f)
    filter_img = open(args.img_filter,'r').read().split('\n')
    print('Processing data...')
    imgs_idxs = set()
    questions = []
    filtered_questions = []
    for index, question in data.items():
        img_idx = question["imageId"]#data['image_index'][index]
        if img_idx in filter_img:
            print(f"question {index} was filtered. Image {img_idx} not "\
                  f"available")
            filtered_questions.append(index)
        else:
            imgs_idxs.add(img_idx)
            q = {
            'question': question["question"],
            'answer': question["answer"],
            #'program': data['program'][index], # Revisar
            'index': int(index),
            'image_index': img_idx,
            'group': question["groups"],
            'type': question["types"]
            #'question_family_index': data['question_family_index'][index] # Revisar
            }
            questions.append(q)
    print(f"Number of filtered questions: {len(filtered_questions)}")
    print(f"New number of questions: {len(questions)}")
    #questions.sort(key=lambda x: x['index'])
    imgs_idxs = sorted(imgs_idxs)
    mapper = {x: i for i, x in enumerate(imgs_idxs)}
    for q in questions:
        q['image_index'] = mapper[q['image_index']]
    
    print('Saving data...')
    with open(args.output_questions_dir, 'w') as f:
        f.write(json.dumps(questions))
    with open(args.filtered_questions_log, 'w+') as f:
        f.write('\n'.join(filtered_questions))
    
    print('Done!')
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_questions_dir', required=True)
    parser.add_argument('--output_questions_dir', required=True)
    parser.add_argument('--img_filter', required=True)
    parser.add_argument('--filtered_questions_log', required=True)

    args = parser.parse_args()
    prepare_questions(args)
