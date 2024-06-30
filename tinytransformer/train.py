import os
from typing import Callable
import torch
import torch.nn as nn
from torch.nn import functional as F

# type hint examplte with function tuple as return type
# def init_tokenzier(text: str) -> tuple[Callable[[str], list[int]], Callable[[list[int]], str]]:


def main():

    # READ DATA

    curr_dir = os.getcwd()
    shakespeare_file_path = os.path.join('datasets', 'text', 'tinyshakespeare')
    shakespeare_file_name = 'tinyshakespeare.txt'
    shakespeare_full_path = os.path.join(
        curr_dir, shakespeare_file_path, shakespeare_file_name)

    print('full dataset path is:', shakespeare_full_path)

    with open(shakespeare_full_path, 'r', encoding='utf-8') as f:
        text = f.read()

    print('dataset character length:', len(text))
    print('first 1000 characters:\n\n', text[:1000])

    # TOKENIZER

    # hint: GPT uses tiktoken which is a BPE (byte pair encoding): pip install tiktoken (or use a tokenizer from hugging face)
    chars = sorted(list(set(text)))
    vocab_size = len(chars)
    print(''.join(chars))
    print(vocab_size)

    stoi = {ch: i for i, ch in enumerate(chars)}
    itos = {i: ch for i, ch in enumerate(chars)}

    def encode(s): return [stoi[c] for c in s]  # string to list of integers

    def decode(l): return ''.join([itos[i]
                                   for i in l])  # list of integers to string

    example = "hi there!"
    encoded_example = encode(example)
    print(f'encode example of "hi there!": {encoded_example}')

    decoded_example = decode(encoded_example)
    print(f'decode example of encoded "hi there!": {decoded_example}')

    # INIT DATA

    data = torch.tensor(encode(text), dtype=torch.long)
    print('data characteristics:', data.shape, data.dtype)
    print(data[:10])

    split = int(0.9*len(data))
    train_data = data[:split]
    val_data = data[split:]

    block_size = 8
    x = train_data[:block_size]
    y = train_data[1:block_size+1]
    for t in range(block_size):
        context = x[:t+1]
        target = y[t]
        print(f'when input is {context} the target: {target}')

    torch.manual_seed(1248)

    batch_size = 4
    block_size = 8

    def get_batch(split):
        # generate a batch of data of inputs x and targets y
        data = train_data if split == 'train' else val_data
        ix = torch.randint(len(data) - block_size, (batch_size,))
        x = torch.stack([data[i:i+block_size] for i in ix])
        y = torch.stack([data[i+1:i+block_size+1] for i in ix])
        return x, y

    xb, yb = get_batch('train')
    print('inputs:')
    print(xb.shape)
    print(xb)
    print('targets:')
    print(yb.shape)
    print(yb)

    print('----')

    for b in range(batch_size):  # b for batch dimension
        for t in range(block_size):  # t for time dimension
            context = xb[b, :t+1]
            target = yb[b, t]
            print(f'when input is {context} the target: {target}')

    m = BigramLanguageModel(vocab_size)
    logits, loss = m(xb, yb)
    print('logits:', logits.shape)
    print(logits)

    print('loss:', loss)


class BigramLanguageModel(nn.Module):

    def __init__(self, vocab_size):
        super().__init__()
        # each key directly reads off the logits for the next token from a lookup table
        self.token_embedding_table = nn.Embedding(vocab_size, vocab_size)

    def forward(self, idx, targets):

        # idx and targets are both (Batch, Time) tensor of integers
        # logits are (Batch, Time, Channel), channel is vocab_size
        logits = self.token_embedding_table(idx)

        B, T, C = logits.shape
        logits = logits.view(B*T, C)
        targets = targets.view(B*T)
        loss = F.cross_entropy(logits, targets)

        return logits, loss


if __name__ == '__main__':
    main()
