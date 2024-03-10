import pygame
import math

##################
# pygame setup
##################
pygame.init()
screen = pygame.display.set_mode((1280, 780))
clock = pygame.time.Clock()
running = True
dt = 0

# Fonts
my_font = pygame.font.SysFont('Comic Sans MS', 14)
font_color = (0, 0, 0)

soft_blue = pygame.Color(173, 216, 230)  # R: 173, G: 216, B: 230
##################

##################
# Matplotlib setup
# Within pygame, see article here:
# https://stackoverflow.com/questions/48093361/using-matplotlib-in-pygame
##################
import matplotlib
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
##################

##################
# economy setup
##################
scenario_name = "Lewis Baseline"

Y1 = 1 # Output in sector 1 (traditional)
Y2 = 1 # Output in sector 2 (modern)
L1 = 1 # employment in sector 1
L2 = 1 # employment in sector 2
w1 = 1 # subsistence real wage sector 1 (baseline)
w2 = 1 # real wage sector 2
K = 10  # capital stock (only in sector 2)
P2 = 1 # profits in sector 2

# Set fixed parameter values
alpha = 0.7  # labour elasticity of output, sector 1
rho = 1      # wage premium
L = 20       # total labour supply (exogenous)
gamma = 0.2  # labour supply coefficient, sector 2
lambda_val = 10  # employment at which MPL in sector 1 becomes zero
beta = 0.7   # labour elasticity of output, sector 2

# Set baseline parameter values
# w1 = np.ones((S, T))  # subsistence real wage sector 1 (baseline)
# # Set parameter values for different scenarios
# w1[1, s:T] = 0.9     # scenario 2: fall in subsistence wage

# Initialise such that there is surplus labour (L1 > lambda)
L1 = 0.9 * L
L2 = L - L1

##################

##################
# Show graph of the economy
# https://macrosimulation.org/a_neoclassical_synthesis_model_is_lm_as_ad#directed-graph
##################

def iterate_economy(L1, lambda_val, alpha, gamma, L2, w1, rho, beta, K, P2, w2, L):
    # Model equations
    # Output sector1 and wages sector 2
    Y1 = lambda_val ** alpha
    w2 = w1 + rho
    if L1 < lambda_val:
        Y1 = L1 ** alpha
        w2 = gamma * L2

    # Output sector 2
    Y2 = (L2 ** beta) * (K ** (1 - beta))

    # Capital accumulation sector 2
    K = K + P2

    # Profits sector 2
    P2 = Y2 - w2 * L2

    # Employment sector 2
    L2 = (beta * Y2) / w2

    # Employment sector 1
    L1 = L - L2

    return Y1, w2, Y2, K, P2, L2, L1


# Enable this to automatically iterate
AUTO_ITERATIOM = True
if (AUTO_ITERATIOM):
    # Set an automatic iteration event every 500 miliseconds 
    pygame.time.set_timer(pygame.USEREVENT, 500)

# Maximum number of iterations to display in each graph
MAX_PLOT_LENGTH = 100

# Count number of iterations for this simulation
iteration_count = 0
is_iter = False

# Used for plotting the simulation over time
Y1_time = []
Y2_time = []
L1_time = []
L2_time = []
P2_time = []

# Append initial value
Y1_time.append(Y1)
Y2_time.append(Y2)
L1_time.append(L1)
L2_time.append(L2)
P2_time.append(P2)

# graph images to render
Y1_surf = None
Y2_surf = None
L1_surf = None
L2_surf = None
P2_surf = None

# Current profit share
PS = P2 / (Y1 + Y2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            is_iter = True
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Space bar pressed!")
                is_iter = True
            if event.key == pygame.K_w:
                print("w pressed!")
                w1 += 0.1
            if event.key == pygame.K_s:
                print("s pressed!")
                w1 -= 0.1
    
    # Player has triggered an iteration
    if is_iter:
         # Run economy updates
        Y1, w2, Y2, K, P2, L2, L1 = iterate_economy(L1, lambda_val, alpha, gamma, L2, w1, rho, beta, K, P2, w2, L)
        
        # Calculate profit share of sector 2
        PS = P2 / (Y1 + Y2)

        Y1_time.append(Y1)
        Y2_time.append(Y2)
        L1_time.append(L1)
        L2_time.append(L2)
        P2_time.append(P2)
        iteration_count += 1

        ###########################
        plot_min = max(0, iteration_count - MAX_PLOT_LENGTH)
        plot_max = iteration_count

        # Rerender the graph images
        # # Plot output 1
        plt.plot(Y1_time, color='black', linewidth=2, linestyle='-')
        plt.xlabel("Time")
        plt.ylabel("Y1")
        plt_title = scenario_name + ": Output Y1"
        plt.title(plt_title, fontsize=15)
        plt.xlim((plot_min, plot_max))
        fig = plt.figure(plt_title)
        fig.set_figwidth(5)
        fig.set_figheight(4)

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()

        size = canvas.get_width_height()
        Y1_surf = pygame.image.fromstring(raw_data, size, "RGB")
        Y1_surf = pygame.transform.scale(Y1_surf, (400, 360))
        # Clear the plot
        plt.clf()

        # Plot output 2
        plt.plot(Y2_time, color='black', linewidth=2, linestyle='-')
        plt.xlabel("Time")
        plt.ylabel("Y2")
        plt_title = scenario_name + ": Output Y2"
        plt.title(plt_title, fontsize=15)
        plt.xlim((plot_min, plot_max))
        fig = plt.figure(plt_title)
        fig.set_figwidth(5)
        fig.set_figheight(4)

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()

        size = canvas.get_width_height()
        Y2_surf = pygame.image.fromstring(raw_data, (size), "RGB")
        Y2_surf = pygame.transform.scale(Y2_surf, (400, 360))
        # Clear the plot
        plt.clf()

        # Plot labor 1
        plt.plot(L1_time, color='black', linewidth=2, linestyle='-')
        plt.xlabel("Time")
        plt.ylabel("Labor 1")
        plt_title = scenario_name + ": Labor 1"
        plt.title(plt_title, fontsize=15)
        plt.xlim((plot_min, plot_max))
        fig = plt.figure(plt_title)
        fig.set_figwidth(5)
        fig.set_figheight(4)

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()

        size = canvas.get_width_height()

        L1_surf = pygame.image.fromstring(raw_data, size, "RGB")
        L1_surf = pygame.transform.scale(L1_surf, (400, 360))
        # Clear the plot
        plt.clf()

        # Plot labor 2
        plt.plot(L2_time, color='black', linewidth=2, linestyle='-')
        plt.xlabel("Time")
        plt.ylabel("Labor 2")
        plt_title = scenario_name + ": Labor 2"
        plt.title(plt_title, fontsize=15)
        plt.xlim((plot_min, plot_max))
        fig = plt.figure(plt_title)
        fig.set_figwidth(5)
        fig.set_figheight(4)

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()

        size = canvas.get_width_height()

        L2_surf = pygame.image.fromstring(raw_data, size, "RGB")
        L2_surf = pygame.transform.scale(L2_surf, (400, 360))
        # Clear the plot
        plt.clf()

        # Plot employment level
        plt.plot(P2_time, color='black', linewidth=2, linestyle='-')
        plt.xlabel("Time")
        plt.ylabel("Profits 2")
        plt_title = scenario_name + ": Profits 2"
        plt.title(plt_title, fontsize=15)
        plt.xlim((plot_min, plot_max))
        fig = plt.figure(plt_title)
        fig.set_figwidth(5)
        fig.set_figheight(4)

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()

        size = canvas.get_width_height()

        P2_surf = pygame.image.fromstring(raw_data, size, "RGB")
        P2_surf = pygame.transform.scale(P2_surf, (400, 360))
        # Clear the plot
        plt.clf()
        ##########################
        
        # Wait for next iteration from player
        is_iter = False
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill(soft_blue)

    #########################
    # Update economic visuals
    #########################
    # Add simple text
    iterate_text_surface = my_font.render('Press the space bar to iterate the economy', True, font_color)
    sim_text_surface = my_font.render(scenario_name, True, font_color)
    PS_text_surface = my_font.render('Sector 2 profit share: ' + str(PS), True, font_color)
    w1_text_surface = my_font.render('subsistence real wage: ' + str(w1), True, font_color)
    w2_text_surface = my_font.render('luxury real wage: ' + str(w2), True, font_color)
    iter_text_surface = my_font.render('Iteration number: ' + str(iteration_count), True, font_color)

    # Render text on the page at the specified positions
    screen.blit(iterate_text_surface, (20, 10)) 
    screen.blit(sim_text_surface, (20, 50)) 
    screen.blit(PS_text_surface, (20, 80))
    screen.blit(w1_text_surface, (20, 110))
    screen.blit(w2_text_surface, (20, 140))
    screen.blit(iter_text_surface, (20, 400)) 

    if (iteration_count > 0):
        #add the graph images to the screen
        screen.blit(Y1_surf, (400,0))
        screen.blit(Y2_surf, (800,0))
        screen.blit(L1_surf, (400,360))
        screen.blit(L2_surf, (800,360))
        screen.blit(P2_surf, (0,420))
    ##########################

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 30
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(30) / 1000

pygame.quit()