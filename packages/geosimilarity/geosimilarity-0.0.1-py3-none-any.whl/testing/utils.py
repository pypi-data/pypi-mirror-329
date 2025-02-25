import torch
import torch.random
from typing_extensions import Self
import matplotlib.pyplot as plt


class LinearSpline():
    def __init__(self, num_control_pts: int) -> None:
        self.num_control_pts = num_control_pts

        # Generate initial set of control points on unit circle
        # Do not make the first and last point overlap, appropriately choose final angle to have
        # equal spacing between the generated points
        last_angle = 2 * torch.pi * (num_control_pts - 1)/(num_control_pts)
        theta = torch.linspace(0, last_angle, num_control_pts)
        self.CP = torch.stack((torch.cos(theta), torch.sin(theta)), dim = 1)
        self.CP.requires_grad_()
    

    def to(self, device: str) -> Self:
        self.CP = self.CP.to(device)
        return self
    

    def generate(self, num_pts: int) -> torch.Tensor:
        # Extend the control points by appending the first control point
        # This ensures that the segment from the last to the first point is included
        CP_ext = torch.cat([self.CP, self.CP[:1]], dim = 0)

        # There are num_control_pts segments now (one per edge of the closed shape)
        # Create a parameter t uniformly spaced in [0, num_control_pts)
        t = torch.linspace(0, self.num_control_pts, steps = num_pts + 1,
                           device = self.CP.device, dtype = self.CP.dtype)[:-1]
        
        # For each t, determine indices of the starting control point for each segment
        idx = torch.floor(t).long()
        # Compute the fractional part for interpolation in each segment
        alpha = (t - idx.to(self.CP.dtype)).unsqueeze(1)
        
        # Perform linear interpolation between CP_ext[idx] and CP_ext[idx+1]
        points = (1 - alpha) * CP_ext[idx] + alpha * CP_ext[idx + 1]
        return points
    

    def __call__(self, num_pts: int) -> torch.Tensor:
        return self.generate(num_pts)


def plot_curves(Xc: torch.Tensor, Xt: torch.Tensor):
    # Get torch tensor to cpu and disable gradient tracking to plot using matplotlib
    Xc = Xc.detach().cpu()
    Xt = Xt.detach().cpu()
    
    plt.fill(Xt[:, 0], Xt[:, 1], color = "#C9C9F5", alpha = 0.46, label = "Target Curve")
    plt.fill(Xc[:, 0], Xc[:, 1], color = "#F69E5E", alpha = 0.36, label = "Candidate Curve")

    plt.plot(Xt[:, 0], Xt[:, 1], color = "#000000", linewidth = 2)
    plt.plot(Xc[:, 0], Xc[:, 1], color = "#000000", linewidth = 2, linestyle = "--")

    plt.axis('equal')
    plt.show()


def automate_training(
    spline: LinearSpline,
    num_candidate_pts: int,
    Xt: torch.Tensor,
    loss_fn,
    epochs: int = 1000,
    print_cost_every: int = 200,
    learning_rate: float = 0.001,
) -> None:
    optimizer = torch.optim.Adam([spline.CP], lr = learning_rate)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, factor = 0.99)

    for epoch in range(epochs):
        Y_model = spline(num_candidate_pts)
        loss = loss_fn(Y_model, Xt)

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        scheduler.step(loss.item())

        if epoch == 0 or (epoch + 1) % print_cost_every == 0:
            num_digits = len(str(epochs))
            print(f'Epoch: [{epoch + 1:{num_digits}}/{epochs}]. Loss: {loss.item():11.6f}')
    return 0


if __name__ == '__main__':
    Xc = torch.rand(10, 2)
    Xt = torch.rand(10, 2)
    plot_curves(Xc, Xt)