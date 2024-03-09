import pygame
import numpy as np

##################
# pygame setup
##################
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# Fonts
my_font = pygame.font.SysFont('Comic Sans MS', 30)
##################


##################
# Matplotlib setup
# Within pygame, see article here:
# 
##################
import matplotlib
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
##################


##################
# economy setup
##################
### Simulate Samuelson 1939
max_iter = 100
# Set the number of parameterisations that will be considered
S = 2

# Set the period in which a shock or shift in 'an' will occur
s = 15

# Set fixed parameter values
c1 = 0.8
beta = 0.6

# Construct (S x max_iter) matrices in which values for different periods will be stored; initialize at 1
C = np.ones((S, max_iter))
I = np.ones((S, max_iter))
G0 = np.ones((S, max_iter))*5 

# Calculate output
Y = C + G0 + I

# Set parameter values for different scenarios
G0[1, s:max_iter] = 6  # scenario: permanent increase in government spending from I0=5 to I0=6 from period s=15 onwards


##################

def iterate_economy(C, I , c1, G0, beta, i, t):
        '''
        i: Simulation index
        A: Productivity shifter
        a: Capital elasticity of output
        K: Exogenous capital stock
        N: Labour supply
        I: Investment
        leisure: Household preference for leisure
        discount_rate: ??????????????
        money_pref: Household preference for money ????????????
        G0: Government expenditures
        Yf: Expected future income
        Gf: Future government spending
        r: Real interest rate ?
        '''
        C[i, t] = c1 * (C[i, t - 1] + I[i, t - 1] + G0[i, t - 1])
        I[i, t] = beta * (c1 * (C[i, t - 1] + I[i, t - 1] + G0[i, t - 1]) - 
                          C[i, t - 1])

        return C, I

for sim_no in range(S):

    # User is closing pygame
    if not running:
        break

    # Count number of iterations for this simulation
    iteration_count = 1
    is_iter = False
    in_sim = True

    while in_sim and running and iteration_count < max_iter:

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Space bar pressed!")
                    is_iter = True
                if event.key == pygame.K_e:
                    print("e pressed!")
                    in_sim = False
            
            # Player has triggered an iteration
            if is_iter:
                # Run economy updates
                C, I = iterate_economy(C, I , c1, G0, beta, sim_no, iteration_count)
                # Calculate output
                Y = C + G0 + I

                iteration_count += 1
                # Wait for next iteration from player
                is_iter = False

            # fill the screen with a color to wipe away anything from last frame
            screen.fill("purple")

            #########################
            # Update economic visuals
            #########################

            # Add simple text
            iterate_text_surface = my_font.render('Press the space bar to iterate the economy', True, (255, 255, 255))
            Y_text_surface = my_font.render('Y: ' + str(Y[:, iteration_count - 1]), True, (255, 255, 255))
            iter_text_surface = my_font.render('Iteration number: ' + str(iteration_count), True, (255, 255, 255))

            # Render text on the page at the specified positions
            screen.blit(iterate_text_surface, (50, 10)) 
            screen.blit(Y_text_surface, (50, 150)) 
            screen.blit(iter_text_surface, (50, 600)) 

            # Plot output
            # plt.plot(range(1, iteration_count), Y[0, 0:iteration_count - 1], color='black', linewidth=2, linestyle='-')
            # plt.xlabel("Time")
            # plt.ylabel("Y")
            # plt_title = "Scenario " + str(sim_no) + ": Output"
            # plt.title(plt_title, fontsize=10)
            # fig = plt.figure(plt_title)
            # fig.set_size_inches(5, 4)

            # canvas = agg.FigureCanvasAgg(fig)
            # canvas.draw()
            # renderer = canvas.get_renderer()
            # raw_data = renderer.tostring_rgb()

            # size = canvas.get_width_height()

            # surf = pygame.image.fromstring(raw_data, size, "RGB")
            # screen.blit(surf, (800,0))

            # Plot consumption and investment
            fig, ax1 = plt.subplots()
            plt.xlabel("Time")
            plt.ylabel("C")
            plt_title = "Figure 4: Consumption and Investment" + str(sim_no)
            plt.title(plt_title, fontsize=10)

            ax1.plot(range(1, iteration_count), C[0, 0:iteration_count - 1], color='black', linewidth=2, linestyle='-', 
                    label='C')
            ax1.set_xlabel("Time")
            ax1.set_ylabel("C", color='black')
            ax1.tick_params(axis='y', labelcolor='black')
            ax2 = ax1.twinx()
            ax2.plot(range(1, iteration_count), I[0, 0:iteration_count - 1], color='black', linewidth=2, linestyle='--',
                    label='I')
            ax2.set_ylabel("I", color='black')
            ax2.tick_params(axis='y', labelcolor='black')
            lines, labels = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax2.legend(lines + lines2, labels + labels2, loc='right')
            canvas = agg.FigureCanvasAgg(fig)
            canvas.draw()
            renderer = canvas.get_renderer()
            raw_data = renderer.tostring_rgb()

            size = canvas.get_width_height()

            surf = pygame.image.fromstring(raw_data, size, "RGB")
            screen.blit(surf, (600,200))
            ##########################

            # flip() the display to put your work on screen
            pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

pygame.quit()