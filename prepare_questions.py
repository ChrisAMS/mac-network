import json
import argparse


def prepare_questions(args):
    print('Loading data...')
    with open(args.input_questions_dir, 'r') as f:
        # questions keys: answer, question, program, index, image_index (transformed starting from zero)
        data  = json.load(f)

    print('Processing data...')
    imgs_idxs = set()
    questions = []
    for index, question in data['question'].items():
        img_idx = data['image_index'][index]
        imgs_idxs.add(img_idx)
        q = {
        'question': question,
        'answer': data['answer'][index],
        'program': data['program'][index],
        'index': int(index),
        'image_index': img_idx,
        'question_family_index': data['question_family_index'][index]
        }
        questions.append(q)
    questions.sort(key=lambda x: x['index'])
    imgs_idxs = sorted(imgs_idxs)
    mapper = {x: i for i, x in enumerate(imgs_idxs)}
    for q in questions:
        q['image_index'] = mapper[q['image_index']]
    
    print('Saving data...')
    with open(args.output_questions_dir, 'w') as f:
        f.write(json.dumps(questions))
    
    print('Done!')
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_questions_dir', required=True)
    parser.add_argument('--output_questions_dir', required=True)

    args = parser.parse_args()
    prepare_questions(args)
