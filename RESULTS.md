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
- **Epochs:** 10
- **Batch Size:** 8
- **Learning Rate:** 3e-5
- **Optimizer:** AdamW
- **Scheduler:** Linear with warmup (10% warmup steps)
- **Max Sequence Length:** 256 tokens
- **Device:** CPU

### Training Data
- **Train Set:** 600 examples
- **Dev Set:** 150 examples
- **Data Characteristics:** Noisy STT (Speech-to-Text) patterns including:
  - Homophones (e.g., "to" vs "too", "their" vs "there")
  - Missing punctuation
  - Inconsistent capitalization
  - Spacing errors
  - Common transcription mistakes

### Training Progress
```
Epoch 1  average loss: 2.6232
Epoch 2  average loss: 1.9436
Epoch 3  average loss: 1.6237
Epoch 4  average loss: 1.4032
Epoch 5  average loss: 1.2444
Epoch 6  average loss: 1.1283
Epoch 7  average loss: 1.0493
Epoch 8  average loss: 0.9844
Epoch 9  average loss: 0.9390
Epoch 10 average loss: 0.9274
```

## Performance Metrics

### Span F1 Scores (Per Entity Type)

| Entity Type  | Precision | Recall | F1 Score |
|--------------|-----------|--------|----------|
| PERSON_NAME  | 0.918     | 0.875  | **0.896** |
| DATE         | 0.509     | 0.628  | **0.562** |
| CREDIT_CARD  | 0.457     | 0.615  | **0.525** |
| EMAIL        | 0.347     | 0.486  | **0.405** |
| PHONE        | 0.323     | 0.429  | **0.368** |
| CITY         | 0.000     | 0.000  | **0.000** |
| LOCATION     | 0.000     | 0.000  | **0.000** |

### Overall Metrics
- **Macro-F1:** 0.394
- **PII-only Precision:** 0.521
- **PII-only Recall:** 0.631
- **PII-only F1:** 0.571

### Interpretation
- **Strong Performance:** PERSON_NAME detection (F1=0.896) shows excellent results
- **Good Performance:** DATE (F1=0.562) and CREDIT_CARD (F1=0.525) show solid detection
- **Moderate Performance:** EMAIL (F1=0.405) and PHONE (F1=0.368) need improvement
- **Poor Performance:** CITY and LOCATION (F1=0.000) require additional training data or model improvements

## Inference Latency

**Test Configuration:**
- Batch Size: 1 (single utterance)
- Runs: 50
- Device: CPU
- Input: Dev set examples

**Results:**
- **p50 Latency:** 7.11 ms
- **p95 Latency:** 12.15 ms

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

## Key Achievements

1. ✅ Successfully trained a lightweight NER model for PII detection
2. ✅ Achieved 57.1% F1 score on PII detection (0.571)
3. ✅ Maintained low latency: p95 = 12.15ms (well under 20ms requirement)
4. ✅ Excellent PERSON_NAME detection: 89.6% F1 score
5. ✅ Model handles noisy STT input with realistic transcription errors

## Future Improvements

### To Improve Performance:
1. **Data Augmentation:** Generate more training examples for CITY and LOCATION
2. **Model Size:** Test with `distilbert-base-uncased` (larger but still fast)
3. **Training Duration:** Increase to 15-20 epochs
4. **Learning Rate Schedule:** Experiment with cosine annealing
5. **Class Weights:** Apply class balancing for underrepresented entities
6. **Post-processing:** Add rule-based corrections for common patterns (emails, phones)
7. **Ensemble:** Combine predictions from multiple models

### To Optimize Latency:
1. **Model Quantization:** Apply INT8 quantization for faster inference
2. **ONNX Export:** Convert to ONNX format for optimized runtime
3. **Batch Processing:** For production, process multiple utterances together
4. **Model Distillation:** Further compress the model while maintaining accuracy

## Conclusion

The model demonstrates strong performance on PERSON_NAME detection and acceptable performance on most PII types, while maintaining excellent inference speed. The lightweight architecture (bert-tiny) provides a good balance between accuracy and latency, making it suitable for real-time applications.
