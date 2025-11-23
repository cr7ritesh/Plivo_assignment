# PII NER Model Results

## Model Architecture

**Base Model:** `prajjwal1/bert-tiny`
- **Type:** BERT (Bidirectional Encoder Representations from Transformers)
- **Size:** Tiny variant - optimized for speed and low latency
- **Parameters:** ~4.4M parameters
- **Hidden Size:** 128
- **Layers:** 2 transformer layers
- **Attention Heads:** 2
- **Vocabulary Size:** 30,522

**Task:** Token Classification for Named Entity Recognition (NER)
- **Output Classes:** 7 entity types (PERSON_NAME, EMAIL, PHONE, CREDIT_CARD, DATE, CITY, LOCATION)
- **Classification Head:** Linear layer on top of BERT outputs

## Training Configuration

### Hyperparameters

- **Epochs:** 22
- **Batch Size:** 8
- **Learning Rate:** 3e-5
- **Optimizer:** AdamW
- **Scheduler:** Linear with warmup (10% warmup steps)
- **Max Sequence Length:** 256 tokens
- **Device:** CPU

### Training Data
- **Train Set:** 1000 examples
- **Dev Set:** 200 examples
- **Data Characteristics:** Noisy STT (Speech-to-Text) patterns including:
  - Homophones (e.g., "to" vs "too", "their" vs "there")
  - Missing punctuation
  - Inconsistent capitalization
  - Spacing errors
  - Common transcription mistakes
  - Enhanced templates for CITY and LOCATION entities

### Label Distribution (Training Set)
- CITY: 325 examples
- LOCATION: 295 examples
- PERSON_NAME: 280 examples
- EMAIL: 130 examples
- PHONE: 159 examples
- DATE: 141 examples
- CREDIT_CARD: 97 examples

### Training Progress

```text
Epoch 1  average loss: 2.6490
Epoch 2  average loss: 2.0380
Epoch 3  average loss: 1.6093
Epoch 4  average loss: 1.3176
Epoch 5  average loss: 1.0926
Epoch 6  average loss: 0.9342
Epoch 7  average loss: 0.8137
Epoch 8  average loss: 0.7262
Epoch 9  average loss: 0.6502
Epoch 10 average loss: 0.5958
Epoch 11 average loss: 0.5458
Epoch 12 average loss: 0.5208
Epoch 13 average loss: 0.4893
Epoch 14 average loss: 0.4667
Epoch 15 average loss: 0.4442
Epoch 16 average loss: 0.4295
Epoch 17 average loss: 0.4187
Epoch 18 average loss: 0.4094
Epoch 19 average loss: 0.3975
Epoch 20 average loss: 0.3937
Epoch 21 average loss: 0.3896
Epoch 22 average loss: 0.3777
```

## Performance Metrics

### Span F1 Scores (Per Entity Type)

| Entity Type  | Precision | Recall | F1 Score |
|--------------|-----------|--------|----------|
| PERSON_NAME  | 0.951     | 0.951  | **0.951** |
| DATE         | 0.907     | 0.929  | **0.918** |
| LOCATION     | 0.836     | 0.823  | **0.829** |
| CREDIT_CARD  | 0.700     | 0.700  | **0.700** |
| CITY         | 0.725     | 0.673  | **0.698** |
| EMAIL        | 0.548     | 0.567  | **0.557** |
| PHONE        | 0.438     | 0.452  | **0.444** |

### Overall Metrics

- **Macro-F1:** 0.728
- **PII-only Precision:** 0.763
- **PII-only Recall:** 0.776
- **PII-only F1:** 0.769
- **Non-PII Precision:** 0.795
- **Non-PII Recall:** 0.761
- **Non-PII F1:** 0.777

## Inference Latency

**Test Configuration:**

- Batch Size: 1 (single utterance)
- Runs: 50
- Device: CPU
- Input: Dev set examples

**Results:**

- **p50 Latency:** 7.82 ms
- **p95 Latency:** 14.16 ms

**Status:** ✅ **Meets requirement** (p95 < 20ms)

## Model Files

All model artifacts are saved in the `out/` directory:

- `config.json` - Model configuration
- `pytorch_model.bin` - Trained model weights
- `tokenizer_config.json` - Tokenizer configuration
- `vocab.txt` - Vocabulary file
- `special_tokens_map.json` - Special tokens mapping

## Predictions

Predictions are saved in: `out/dev_pred.json`

- Format: JSON dictionary mapping utterance IDs to lists of detected entities
- Each entity includes: start position, end position, label, and PII flag
