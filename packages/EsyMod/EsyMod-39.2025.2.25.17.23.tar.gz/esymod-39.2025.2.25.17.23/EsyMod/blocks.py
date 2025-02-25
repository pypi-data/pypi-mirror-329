import torch
from torch import nn
from . import Model, manipulators

class ResConv(Model):
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int = 3, stride: int = 1,
                 stimuli=nn.Hardswish):
        """
        conv block with res connection
        :param in_channels:
        :param out_channels:
        :param kernel_size:
        :param stride:
        """

        super().__init__()
        if isinstance(kernel_size, int):
            padding = kernel_size // 2
        else:
            padding = [k // 2 for k in kernel_size]
        self.res_conv = nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=1, stride=stride ** 2)
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, stride=stride,
                      padding=padding),
            stimuli()
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels=out_channels, out_channels=out_channels, kernel_size=kernel_size, stride=stride,
                      padding=padding),
            stimuli()
        )

    def get_output(self, x: torch.Tensor) -> torch.Tensor:
        direct = self.conv2(self.conv1(x))
        res = self.res_conv(x)
        return res + direct


class ResTConv(Model):
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int = 3, stride: int = 1,
                 stimuli=nn.Hardswish):
        """
        conv block with res connection
        :param in_channels:
        :param out_channels:
        :param kernel_size:
        :param stride:
        """

        super().__init__()
        self.res_conv = nn.ConvTranspose2d(in_channels=in_channels, out_channels=out_channels, kernel_size=1,
                                           stride=stride ** 2)
        self.conv1 = nn.Sequential(
            nn.ConvTranspose2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size,
                               stride=stride,
                               padding=kernel_size // 2),
            stimuli()
        )
        self.conv2 = nn.Sequential(
            nn.ConvTranspose2d(in_channels=out_channels, out_channels=out_channels, kernel_size=kernel_size,
                               stride=stride,
                               padding=kernel_size // 2),
            stimuli()
        )

    def get_output(self, x: torch.Tensor) -> torch.Tensor:
        direct = self.conv2(self.conv1(x))
        res = self.res_conv(x)
        return res + direct


class MultiplyLayer(manipulators.Multiply):
    def __init__(self, input_dim, output_dim, bias=True):
        route1 = nn.Linear(input_dim, output_dim, bias=bias)
        route2 = nn.Linear(input_dim, output_dim, bias=bias)
        super().__init__(route1, route2)

class FullConnectedLayer(torch.nn.Sequential):
    def __init__(self, input_dim, output_dim, bias=True, stimuli=nn.Hardswish()):
        super().__init__(
            nn.Linear(input_dim, output_dim, bias=bias),
            stimuli
        )
        
class VAE(Model):
    def __init__(self, encoder, decoder):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        
    def get_output(self, x):
        mu, log_var = self.encoder(x).chunk(2, dim=1)
        z = mu + torch.randn_like(mu) * torch.exp(log_var / 2)
        self.mu = mu
        self.log_var = log_var
        self.din = x
        return self.decoder(z)