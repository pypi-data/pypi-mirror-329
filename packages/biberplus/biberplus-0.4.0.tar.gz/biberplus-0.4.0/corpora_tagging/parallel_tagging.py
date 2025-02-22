import os
import jsonlines

from glob import glob
from multiprocessing import Pool
from biberplus.reducer import encode_text
from biberplus.tagger.tagger_utils import load_tokenizer


def tag_partitions(config, input_directory, output_directory, num_workers, default_niceness=20):
    process_args = build_process_args(config, input_directory, output_directory)

    def set_niceness():
        os.nice(default_niceness)

    with Pool(num_workers, initializer=set_niceness) as pool:
        pool.starmap(tag_partition, process_args)


def tag_partition(config, input_file, output_file):
    print(f"Tagging file {input_file}\n")
    tokenizer = load_tokenizer(use_gpu=False)
    tagged_objects = []

    with jsonlines.open(input_file) as reader:
        for obj in reader:
            tagged_object = tag_object(obj, config, tokenizer)
            tagged_objects.append(tagged_object)

            if len(tagged_objects) % 5000 == 0:
                append_chunk(output_file, tagged_objects)
                # with Pool(1) as pool:
                #     pool.apply(append_chunk, [(output_file, tagged_objects)])
                tagged_objects = []

    if tagged_objects:
        append_chunk(output_file, tagged_objects)


def build_process_args(config, input_directory, output_directory):
    partition_files = glob(f"{input_directory}*.jsonl")
    process_args = []

    for fp in partition_files:
        fname = fp.rsplit('/', 1)[-1].replace('.jsonl', '') + '-tagged.jsonl'
        out = f"{output_directory}{fname}"
        process_args.append((config, fp, out))

    return process_args


def tag_object(obj, config, tokenizer):
    try:
        num_tokens = len(tokenizer(obj['fullText']))
        obj['num_tokens'] = num_tokens
        if num_tokens >= 10:
            obj['encodings'] = encode_text(text=obj['fullText'], config=config)
    except Exception:
        pass

    return obj


def append_chunk(output_file, tagged_objects):
    with jsonlines.open(output_file, mode='a') as writer:
        writer.write_all(tagged_objects)
