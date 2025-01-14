import torch.nn as nn
import torch.nn.functional as F


class LSTM(nn.Module):
    def __init__(self,
                 in_channels,
                 hidden,
                 out_channels,
                 n_layers=2,
                 embed_size=8):
        super(LSTM, self).__init__()
        self.in_channels = in_channels
        self.hidden = hidden
        self.embed_size = embed_size
        self.out_channels = out_channels
        self.n_layers = n_layers

        self.encoder = nn.Embedding(in_channels, embed_size)

        self.rnn =\
            nn.LSTM(
                input_size=embed_size,
                hidden_size=hidden,
                num_layers=n_layers,
                batch_first=True
            )

        self.decoder = nn.Linear(hidden, out_channels)

    def forward(self, input_):
        encoded = self.encoder(input_)
        output, _ = self.rnn(encoded)
        output = self.decoder(output)
        output = output.permute(0, 2, 1)  # change dimension to (B, C, T)
        final_word = output[:, :, -1]
        return final_word