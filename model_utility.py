import torch
from torch import nn
from transformers import AutoTokenizer, AutoModelWithLMHead
import torch.nn.functional as F


@torch.jit.script
def mish(input):
    return input * torch.tanh(F.softplus(input))
  
class Mish(nn.Module):
    def forward(self, input):
        return mish(input)


class EmoModel(nn.Module):
    def __init__(self, base_model, n_classes, base_model_output_size=768, dropout=0.05):
        super().__init__()
        self.base_model = base_model
        
        self.classifier = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(base_model_output_size, base_model_output_size),
            Mish(),
            nn.Dropout(dropout),
            nn.Linear(base_model_output_size, n_classes)
        )
        
        for layer in self.classifier:
            if isinstance(layer, nn.Linear):
                layer.weight.data.normal_(mean=0.0, std=0.02)
                if layer.bias is not None:
                    layer.bias.data.zero_()

    def forward(self, input_, *args):
        X, attention_mask = input_
        hidden_states = self.base_model(X, attention_mask=attention_mask)
        

        return self.classifier(hidden_states[0][:, 0,:])

def load_model():

    emotions = 6
    model = EmoModel(AutoModelWithLMHead.from_pretrained("distilroberta-model").base_model, emotions)
    model.load_state_dict(torch.load('roberta_trained', map_location='cpu'))

    return model

def load_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained('distilroberta-tokenizer')
    return tokenizer

def predict(model, tokenizer, inp):
    try:
        enc = tokenizer.encode_plus(inp)
        X = torch.tensor(enc["input_ids"]).unsqueeze(0)
        attn = torch.tensor(enc["attention_mask"]).unsqueeze(0)
    except Exception as e:
        return 6

    return torch.argmax( model( (X.cpu(), attn.cpu()) ) ).item()

if __name__ == "__main__":
    '''
    {
        "sadness": 0,
        "joy": 1,
        "love": 2,
        "anger": 3,
        "fear": 4,
        "surprise": 5
    }
    '''

    tokenizer = load_tokenizer()
    model = load_model()

    print(predict(model, tokenizer, 'hello i am happy'))
