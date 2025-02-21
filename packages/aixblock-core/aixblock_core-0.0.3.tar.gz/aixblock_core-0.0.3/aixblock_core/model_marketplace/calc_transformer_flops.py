# By Quentin Anthony and Beren Millidge


import argparse
import math

# Helper function to pretty-print message sizes
def convert_flops(params):
    if params == 0:
        return "0"
    size_name = ("", "KFLOPs", "MFLOPs", "GFLOPs", "TFLOPs", "PFLOPs", "EFLOPs", "ZFLOPs", "YFLOPs")
    i = int(math.floor(math.log(params, 1000)))
    p = math.pow(1000, i)
    s = round(params / p, 2)
    return "%s %s" % (s, size_name[i])

def convert_flops_float(params):
    if params == 0:
        return "0"
    size_name = ("", "KFLOPs", "MFLOPs", "GFLOPs", "TFLOPs", "PFLOPs", "EFLOPs", "ZFLOPs", "YFLOPs")
    i = int(math.floor(math.log(params, 1000)))
    p = math.pow(1000, i)
    s = round(params / 1e6, 2)
    return s

def config_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vocab-size", "-v",
                        type=int,
                        default=51200,
                        help='Size of the vocab')
    parser.add_argument("--hidden-size", "-hs",
                        type=int,
                        default=6144,
                        help='Dimension of the model\'s hidden size')
    parser.add_argument("--sequence-length", "-s",
                        type=int,
                        default=2048,
                        help='Sequence length used for training')
    parser.add_argument("--num-layers", "-l",
                        type=int,
                        default=44,
                        help='Number of transformer layers used in model')
    parser.add_argument("--kv-size-ratio", "-kv",
                        type=float,
                        default=1.0,
                        help='Ratio of kv heads to query heads used in model. 1.0 for MHA')
    parser.add_argument("--moe",
                    action="store_true",
                    help='Whether our model is MoE')
    parser.add_argument("--num-experts", "-e",
                    type=int,
                    default=128,
                    help='Number of experts for MoE')
    parser.add_argument("--expert-interval", "-ei",
                    type=int,
                    default=2,
                    help='Expert interval for MoE')
    parser.add_argument("--topk", "-t",
                        type=int,
                        default=1,
                        help='Top k routing for MoE')
    parser.add_argument("--swiglu",
                action="store_true",
                help='Use swiglu MLP. If set, ffn-hidden-size is defined as the inner dimension of each of the three MLP weights.')    
    parser.add_argument("--batch-size", "-b",
                        type=int,
                        default=1,
                        help='Global batch size in units of samples')
    parser.add_argument("--tokens",
                        type=int,
                        default=300e9,
                        help='Number of tokens you are training over')
    parser.add_argument("--no-checkpoint-activations", "-ca",
                        action='store_false',
                        help='Whether Megatron-style activation checkpointing is being used',
                        dest='checkpoint_activations')
    return parser

# calculates the flops of a model given its hparams
def calc_params(args):

    assert args.topk <= args.num_experts, "You cannot route to more experts than you have!"
    assert args.num_layers % args.expert_interval == 0, "Require for simplicity that we don't have hanging dense layers"

    # An A_(m x k) X B_(k x n) matrix multiplication requires 2m x k x n FLOPs (factor of 2 needed to account for multiplies and adds)

    # determine the flops factor. 
    # If no activation checkpointing/recomputation, 1 for fwd and 2 for bwd (because we need to calculate the grads with respect to both the input and weight tensors). 
    # If activation checkpointing/recomputation, add 1 more for the next full forward pass
    iter_factor = 3
    if args.checkpoint_activations:
        iter_factor += 1

    qkv_flops = int(iter_factor * 2 * (1 + 2 * args.kv_size_ratio) * args.num_layers * args.tokens * args.hidden_size * args.hidden_size)
    attention_matrix_flops = iter_factor * 2 * args.num_layers * args.tokens * args.sequence_length * args.hidden_size
    attention_over_values_flops = iter_factor * 2 * args.num_layers * args.tokens * args.sequence_length * args.hidden_size
    linear_projection_flops = iter_factor * 2 * args.num_layers * args.tokens * args.hidden_size * args.hidden_size
    ffn_flops = iter_factor * 16 * args.num_layers * args.tokens * args.hidden_size * args.hidden_size
    if args.swiglu:
        ffn_flops = 3/2 * ffn_flops
    # no activation checkpointing for embeddings
    embedding_flops = 6 * args.tokens * args.hidden_size * args.vocab_size

    if args.moe and args.topk > 1:
        ffn_flops += ffn_flops * args.topk / args.expert_interval

    if args.moe:
        gating_flops = 2 * args.num_experts * args.hidden_size / args.expert_interval

    total_flops = qkv_flops + attention_matrix_flops + attention_over_values_flops + linear_projection_flops + ffn_flops + embedding_flops

    if args.moe:
        total_flops += gating_flops

    print(f'Calculating number of FLOPs with training configuration: {vars(args)}\n')
    print(f'QKV FLOPs: {convert_flops(qkv_flops)}')
    print(f'Attention Matrix FLOPs: {convert_flops(attention_matrix_flops)}')
    print(f'Attention Over Values FLOPs: {convert_flops(attention_over_values_flops)}')
    print(f'Linear Projection FLOPs: {convert_flops(linear_projection_flops)}')
    print(f'FFN FLOPs: {convert_flops(ffn_flops)}')
    print(f'Embedding FLOPs: {convert_flops(embedding_flops)}')
    if args.moe:
        print(f'Gating FLOPs: {convert_flops(gating_flops)}')
    print(f'Total FLOPs for the Model: {convert_flops(total_flops)}')

    print('\nExample with Fairseq-MoE 15B: python calc_transformer_flops.py -l 12 -hs 768 --moe -e 512')
    print('Example with GPT-3 175B: python calc_transformer_flops.py -l 96 -hs 12288')
    
    return convert_flops_float(total_flops)
    # args = config_parser().parse_args()
    # calc_params(args)
