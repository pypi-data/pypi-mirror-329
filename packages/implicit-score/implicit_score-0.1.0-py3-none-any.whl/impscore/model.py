import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

import logging
import torch
import torch.nn as nn
from sentence_transformers import (
    SentenceTransformer,
)
import torch.nn.init as init
import torch.nn.functional as F
import os
import json
import argparse
from huggingface_hub import hf_hub_download

REPO_ID = "audreyeleven/ImpScore"  # e.g. "john123/my-impscore-model"
STATE_DICT_FILENAME = "model_state_dict_v_0_1_0.pth"
ARGS_FILENAME = "model_args_v_0_1_0.json"

class ImpModel(nn.Module):
    def __init__(self, train_args, device):
        super(ImpModel, self).__init__()

        # set the device
        self.device = device

        # load the pre-trained sent-transformer model
        self.encoder_name = "all-mpnet-base-v2"
        self.encoder = SentenceTransformer(self.encoder_name, device=self.device)

        for param in self.encoder.parameters():
            param.requires_grad = False

        self.encoder = self.encoder.to(self.device)

        self.feat_dim = int(train_args.feat_dim)
        self.transform_direct = train_args.space_direct  # 'p2s', 's2p', or 'another'
        self.imp_metric = train_args.imp_metric  # 'euc' or 'cos'
        self.prag_metric = train_args.prag_metric  # 'euc' or 'cos'

        assert self.transform_direct in ['p2s', 's2p', 'another'], "Invalid transformation direction in initialization"
        assert self.imp_metric in ['euc', 'cos'], "Invalid metric for implicit loss in initialization"
        assert self.prag_metric in ['euc', 'cos'], "Invalid metric for pragmatic loss in initialization"

        self.weight_p = nn.Linear(768, self.feat_dim, bias=False)
        self.weight_s = nn.Linear(768, self.feat_dim, bias=False)

        if self.transform_direct in ['p2s', 's2p']:
            self.weight_t = nn.Linear(self.feat_dim, self.feat_dim, bias=False)
        else:
            self.weight_t_p = nn.Linear(self.feat_dim, self.feat_dim, bias=False)
            self.weight_t_s = nn.Linear(self.feat_dim, self.feat_dim, bias=False)

        self.initialize_weights()

        self.margin1 = float(train_args.margin1)
        self.margin2 = float(train_args.margin2)
        self.alpha = float(train_args.alpha)

    def initialize_weights(self):
        if self.transform_direct in ['p2s', 's2p']:
            for m in [self.weight_p, self.weight_s, self.weight_t]:
                if isinstance(m, nn.Linear):
                    init.xavier_uniform_(m.weight)
                    if m.bias is not None:
                        init.constant_(m.bias, 0)
        else:
            for m in [self.weight_p, self.weight_s, self.weight_t_p, self.weight_t_s]:
                if isinstance(m, nn.Linear):
                    init.xavier_uniform_(m.weight)
                    if m.bias is not None:
                        init.constant_(m.bias, 0)

    def infer_single(self, sentence):
        '''
        Infer the implicit score of a sentence
        :param sentence: str, input sentence
        :return:
            imp_score: implicit score of the sentence,
            prag_emb: tensor, pragmatic embedding of the sentence,
            sem_emb: tensor, semantic embedding of the sentence
        '''
        sent_emb = self.encoder.encode(sentence, show_progress_bar=False)
        sent_emb = torch.tensor(sent_emb, dtype=torch.float32).to(self.device)

        prag_emb = self.weight_p(sent_emb)
        sem_emb = self.weight_s(sent_emb)

        if self.transform_direct == 'p2s':
            map_emb = self.weight_t(prag_emb)
            if self.imp_metric == 'euc':
                imp_score = torch.norm(sem_emb - map_emb, dim=-1)
            else:
                imp_score = 1.0 - F.cosine_similarity(sem_emb, map_emb, dim=-1)
        elif self.transform_direct == 's2p':
            map_emb = self.weight_t(sem_emb)
            if self.imp_metric == 'euc':
                imp_score = torch.norm(prag_emb - map_emb, dim=-1)
            else:
                imp_score = 1.0 - F.cosine_similarity(prag_emb, map_emb, dim=-1)
        else:
            map_prag_emb = self.weight_t_p(prag_emb)
            map_sem_emb = self.weight_t_s(sem_emb)
            if self.imp_metric == 'euc':
                imp_score = torch.norm(map_prag_emb - map_sem_emb, dim=-1)
            else:
                imp_score = 1.0 - F.cosine_similarity(map_prag_emb, map_sem_emb, dim=-1)

        return imp_score, prag_emb, sem_emb

    def infer_pairs(self, sentence1, sentence2):
        # generate text embeddings for statement1 and statement2
        sent_bert_emb1 = self.encoder.encode(sentence1, show_progress_bar=False)
        sent_bert_emb2 = self.encoder.encode(sentence2, show_progress_bar=False)

        sent_bert_emb1 = torch.tensor(sent_bert_emb1, dtype=torch.float32).to(self.device)
        sent_bert_emb2 = torch.tensor(sent_bert_emb2, dtype=torch.float32).to(self.device)

        assert sent_bert_emb1.shape[1] == self.weight_p.in_features, "Mismatch in embedding size"
        assert sent_bert_emb2.shape[1] == self.weight_s.in_features, "Mismatch in embedding size"

        # project text embeddings to pragmatic space
        prag_emb1 = self.weight_p(sent_bert_emb1)
        prag_emb2 = self.weight_p(sent_bert_emb2)

        # project text embeddings to semantic space
        sem_emb1 = self.weight_s(sent_bert_emb1)
        sem_emb2 = self.weight_s(sent_bert_emb2)

        # transform embeddings to another space
        if self.transform_direct == 'p2s':
            map_emb1 = self.weight_t(prag_emb1)
            map_emb2 = self.weight_t(prag_emb2)
            if self.imp_metric == 'euc':
                imp_score1 = torch.norm(sem_emb1 - map_emb1, dim=1)
                imp_score2 = torch.norm(sem_emb2 - map_emb2, dim=1)
            else:  # higher implicit score means smaller distance
                imp_score1 = 1.0 - F.cosine_similarity(sem_emb1, map_emb1, dim=1)
                imp_score2 = 1.0 - F.cosine_similarity(sem_emb2, map_emb2, dim=1)
        elif self.transform_direct == 's2p':
            map_emb1 = self.weight_t(sem_emb1)
            map_emb2 = self.weight_t(sem_emb2)
            if self.imp_metric == 'euc':
                imp_score1 = torch.norm(prag_emb1 - map_emb1, dim=1)
                imp_score2 = torch.norm(prag_emb2 - map_emb2, dim=1)
            else:
                imp_score1 = 1.0 - F.cosine_similarity(prag_emb1, map_emb1, dim=1)
                imp_score2 = 1.0 - F.cosine_similarity(prag_emb2, map_emb2, dim=1)
        else:
            map_prag_emb1 = self.weight_t_p(prag_emb1)
            map_prag_emb2 = self.weight_t_p(prag_emb2)
            map_sem_emb1 = self.weight_t_s(sem_emb1)
            map_sem_emb2 = self.weight_t_s(sem_emb2)
            if self.imp_metric == 'euc':
                imp_score1 = torch.norm(map_prag_emb1 - map_sem_emb1, dim=1)
                imp_score2 = torch.norm(map_prag_emb2 - map_sem_emb2, dim=1)
            else:
                imp_score1 = 1.0 - F.cosine_similarity(map_prag_emb1, map_sem_emb1, dim=1)
                imp_score2 = 1.0 - F.cosine_similarity(map_prag_emb2, map_sem_emb2, dim=1)

        # calculate cosine similarity between pragmatic embeddings
        if self.prag_metric == 'cos':
            # the range of pragmatic distance is [0, 2]
            prag_distance = 1.0 - F.cosine_similarity(prag_emb1, prag_emb2, dim=1)
        else:
            prag_distance = torch.norm(prag_emb1 - prag_emb2, dim=1)

        return imp_score1, imp_score2, prag_distance

    def forward(self, pos_pair, neg_pair):
        """
        Forward pass of the model
        :param pos_pair: a batch of positive pairs, shape=(batch_size, 2)
        :param neg_pair: a batch of negative pairs, shape=(batch_size, 2)
        :return: final_loss: total loss
        """
        assert pos_pair.shape[0] == neg_pair.shape[0], "Batch size mismatch between pos_pair and neg_pair"

        pos1, pos2 = pos_pair[:, 0], pos_pair[:, 1]
        neg1, neg2 = neg_pair[:, 0], neg_pair[:, 1]

        imp_score_pos1, imp_score_pos2, prag_dis_pos = self.infer_pairs(pos1, pos2)
        imp_score_neg1, imp_score_neg2, prag_dis_neg = self.infer_pairs(neg1, neg2)

        # calculate losses using pairwise ranking loss
        loss_imp_pos = torch.mean(torch.clamp(self.margin1 - (imp_score_pos1 - imp_score_pos2), min=0))
        loss_imp_neg = torch.mean(torch.clamp(self.margin1 - (imp_score_neg1 - imp_score_neg2), min=0))

        loss_prag = torch.mean(torch.clamp(self.margin2 - (prag_dis_neg - prag_dis_pos), min=0))

        final_loss = (loss_imp_pos + loss_imp_neg) + self.alpha * loss_prag

        return final_loss

    def compare_two_sentences(self, sentence1, sentence2):
        sent_emb1 = self.encoder.encode(sentence1, show_progress_bar=False)
        sent_emb2 = self.encoder.encode(sentence2, show_progress_bar=False)

        # convert embeddings to tensor
        sent_emb1 = torch.tensor(sent_emb1, dtype=torch.float32).to(self.device)
        sent_emb2 = torch.tensor(sent_emb2, dtype=torch.float32).to(self.device)

        assert sent_emb1.shape[1] == self.weight_p.in_features, "Mismatch in embedding size"

        prag_emb1 = self.weight_p(sent_emb1)
        prag_emb2 = self.weight_p(sent_emb2)

        sem_emb1 = self.weight_s(sent_emb1)
        sem_emb2 = self.weight_s(sent_emb2)

        # transform embeddings to another space
        if self.transform_direct == 'p2s':
            map_emb1 = self.weight_t(prag_emb1)
            map_emb2 = self.weight_t(prag_emb2)
            if self.imp_metric == 'euc':
                imp_score1 = torch.norm(sem_emb1 - map_emb1, dim=1)
                imp_score2 = torch.norm(sem_emb2 - map_emb2, dim=1)
            else:  # higher implicit score means smaller distance
                imp_score1 = 1.0 - F.cosine_similarity(sem_emb1, map_emb1, dim=1)
                imp_score2 = 1.0 - F.cosine_similarity(sem_emb2, map_emb2, dim=1)
        elif self.transform_direct == 's2p':
            map_emb1 = self.weight_t(sem_emb1)
            map_emb2 = self.weight_t(sem_emb2)
            if self.imp_metric == 'euc':
                imp_score1 = torch.norm(prag_emb1 - map_emb1, dim=1)
                imp_score2 = torch.norm(prag_emb2 - map_emb2, dim=1)
            else:
                imp_score1 = 1.0 - F.cosine_similarity(prag_emb1, map_emb1, dim=1)
                imp_score2 = 1.0 - F.cosine_similarity(prag_emb2, map_emb2, dim=1)
        else:
            map_prag_emb1 = self.weight_t_p(prag_emb1)
            map_prag_emb2 = self.weight_t_p(prag_emb2)
            map_sem_emb1 = self.weight_t_s(sem_emb1)
            map_sem_emb2 = self.weight_t_s(sem_emb2)
            if self.imp_metric == 'euc':
                imp_score1 = torch.norm(map_prag_emb1 - map_sem_emb1, dim=1)
                imp_score2 = torch.norm(map_prag_emb2 - map_sem_emb2, dim=1)
            else:
                imp_score1 = 1.0 - F.cosine_similarity(map_prag_emb1, map_sem_emb1, dim=1)
                imp_score2 = 1.0 - F.cosine_similarity(map_prag_emb2, map_sem_emb2, dim=1)

        if self.prag_metric == 'cos':
            prag_distance = 1.0 - F.cosine_similarity(prag_emb1, prag_emb2, dim=1)
        else:
            prag_distance = torch.norm(prag_emb1 - prag_emb2, dim=1)

        imp_loss = torch.mean(torch.clamp(self.margin1 - (imp_score1 - imp_score2), min=0))

        return imp_loss, imp_score1, imp_score2, prag_distance

    def print_model_size(self):
        logging.info("Model parameters and their sizes:")
        for name, module in self.named_children():
            total_size = 0
            for param in module.parameters():
                total_size += param.numel()
            # convert bytes to MB
            total_size = total_size / (1024 ** 2)
            logging.info(f"(self.{name}) total size = {total_size:.2f}MB")


def load_model(load_device="cuda"):
    """Lazy-load the model weights from disk if not already loaded."""

    args_path = hf_hub_download(repo_id=REPO_ID, filename=ARGS_FILENAME)
    state_dict_path = hf_hub_download(repo_id=REPO_ID, filename=STATE_DICT_FILENAME)
    state_dict = torch.load(state_dict_path, map_location=load_device)

    # Load model args
    with open(args_path, "r") as f:
        config = json.load(f)

    config.pop('device', None)

    # convert dictionary back to Namespace
    args = argparse.Namespace(**config)

    # Initialize your model using those args
    model = ImpModel(args, load_device)
    model.load_state_dict(state_dict)
    model.to(load_device)
    model.eval()

    return model
